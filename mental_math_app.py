import streamlit as st
import random
import time
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 定数・設定
# ==========================================
RANKING_FILE = "ranking.csv"
MAX_LIMIT = 10**13
TOTAL_QUESTIONS = 10

# ==========================================
# デザイン設定 (CSS)
# ==========================================
def apply_custom_design():
    custom_css = """
    <style>
        .stApp {
            background-color: #0F172A;
            color: #F8FAFC;
        }
        h1, h2, h3 {
            color: #38BDF8;
            font-family: "Roboto", "Helvetica Neue", sans-serif;
            font-weight: 700;
            letter-spacing: 0.05em;
        }
        /* プライマリーボタン */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #2563EB 0%, #1E3A8A 100%);
            color: white;
            border-radius: 4px;
            border: none;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
            font-weight: bold;
            letter-spacing: 0.05em;
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
        }
        /* セカンダリーボタン（透明） */
        div.stButton > button:nth-child(2) {
            background-color: transparent;
            color: #38BDF8;
            border: 1px solid #38BDF8;
            border-radius: 4px;
        }
        div.stButton > button:nth-child(2):hover {
            background-color: rgba(56, 189, 248, 0.1);
        }
        [data-testid="stMetricValue"] {
            color: #FACC15;
            font-family: 'Consolas', 'Monaco', monospace;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(250, 204, 21, 0.3);
        }
        [data-testid="stMetricLabel"] {
            color: #94A3B8;
        }
        .css-card {
            background-color: #1E293B;
            border-left: 4px solid #FACC15;
            padding: 20px;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }
        .stAlert {
            background-color: #1E293B;
            border: 1px solid #334155;
            color: #E2E8F0;
        }
        hr {
            border-color: #334155;
        }
        /* 履歴テーブル用のスタイル */
        .history-row {
            background-color: #1E293B;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 3px solid #38BDF8;
            font-size: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        /* タブのスタイル調整 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #1E293B;
            border-radius: 4px 4px 0 0;
            color: #94A3B8;
        }
        .stTabs [aria-selected="true"] {
            background-color: #38BDF8 !important;
            color: #0F172A !important;
            font-weight: bold;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# ランキング機能
# ==========================================
def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return pd.DataFrame(columns=["timestamp", "nickname", "mode", "score", "duration"])
    return pd.read_csv(RANKING_FILE)

def save_ranking(nickname, mode, score, duration):
    df = load_ranking()
    new_data = pd.DataFrame({
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "nickname": [nickname],
        "mode": [mode],
        "score": [score],
        "duration": [duration]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(RANKING_FILE, index=False)

def display_ranking(filter_mode=None):
    df = load_ranking()
    if df.empty:
        st.info("まだランキングデータがありません。")
        return

    # モードでフィルタリング
    if filter_mode:
        df = df[df["mode"] == filter_mode]
        if df.empty:
            st.info(f"ランキングデータはまだありません。")
            return

    # ソート（スコア降順、タイム昇順）
    df = df.sort_values(by=["score", "duration"], ascending=[False, True]).reset_index(drop=True)
    
    # 表示用に整形
    display_df = df[["nickname", "score", "duration", "timestamp"]].copy()
    display_df["rank"] = display_df.index + 1
    display_df["duration"] = display_df["duration"].apply(lambda x: f"{int(x//60)}分{int(x%60)}秒")
    display_df.columns = ["ニックネーム", "スコア/正解数", "タイム", "日付", "順位"]
    display_df = display_df[["順位", "ニックネーム", "スコア/正解数", "タイム", "日付"]] # 列順変更

    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ==========================================
# 共通関数: 数値フォーマット・生成
# ==========================================
def format_japanese_answer(num):
    """結果表示用: 漢数字（例: 1億2000万）"""
    try:
        int_num = int(num)
    except:
        return str(num)
    if int_num == 0: return "0"
    units = [(10**12, "兆"), (10**8, "億"), (10**4, "万"), (1, "")]
    result = []
    remaining = abs(int_num)
    for unit_val, unit_name in units:
        if remaining >= unit_val:
            val = remaining // unit_val
            remaining %= unit_val
            result.append(f"{val:,}{unit_name}")
    return "".join(result) if result else "0"

def format_number_with_unit_label(value):
    """問題文表示用: 単位付き（例: 1.5万）"""
    if value >= 10**8:
        if value % 10**8 == 0: return f"{value // 10**8:,}億"
        else: return f"{value / 10**8:.1f}億".replace(".0", "")
    elif value >= 10**4:
        if value % 10**4 == 0: return f"{value // 10**4:,}万"
        else: return f"{value / 10**4:.1f}万".replace(".0", "")
    else:
        return f"{value:,}"

def get_random_val(min_val, max_val, simple=False):
    val = random.randint(min_val, max_val)
    if simple:
        digits = len(str(val))
        if digits > 1:
            bases = [10, 20, 30, 40, 50, 60, 70, 80, 90, 15, 25, 12, 18]
            base = random.choice(bases)
            min_digits = len(str(min_val))
            target_digits = random.randint(min_digits, len(str(max_val)))
            power = max(0, target_digits - 2)
            val = base * (10**power)
            if val < min_val: val = min_val
            if val > max_val: val = max_val
            if val < 100: val = (val // 10) * 10
    return int(val)

# ==========================================
# シナリオデータ定義
# ==========================================
SCENARIOS = [
    # パターン1: A * B
    { "pattern": 1, "template": "単価 <b>{label1}円</b> の商品が <b>{label2}個</b> 売れました。<br>売上推定値は？", "range1": (100, 50000), "range2": (100, 100000), "unit1":"円", "unit2":"個" },
    { "pattern": 1, "template": "1人あたり <b>{label1}円</b> のコストがかかる研修に <b>{label2}人</b> が参加します。<br>総費用推定値は？", "range1": (5000, 200000), "range2": (10, 5000), "unit1":"円", "unit2":"人" },
    { "pattern": 1, "template": "月商 <b>{label1}円</b> の店舗を <b>{label2}店舗</b> 運営しています。<br>全店の月商合計は？", "range1": (1000000, 50000000), "range2": (3, 1000), "unit1":"円", "unit2":"店舗" },
    { "pattern": 1, "template": "契約単価 <b>{label1}円</b> のサブスク会員が <b>{label2}人</b> います。<br>毎月の売上は？", "range1": (500, 10000), "range2": (1000, 1000000), "unit1":"円", "unit2":"人" },
    # パターン2: A * r
    { "pattern": 2, "template": "売上高 <b>{label1}円</b> に対して、営業利益率は <b>{pct}%</b> です。<br>営業利益は？", "range1": (100000000, 1000000000000), "pct_range": (1, 30), "unit1":"円" },
    { "pattern": 2, "template": "市場規模 <b>{label1}円</b> の業界で、シェア <b>{pct}%</b> を獲得しました。<br>自社の売上は？", "range1": (1000000000, 1000000000000), "pct_range": (1, 60), "unit1":"円" },
    { "pattern": 2, "template": "予算 <b>{label1}円</b> のうち、すでに <b>{pct}%</b> を消化しました。<br>消化した金額は？", "range1": (1000000, 1000000000), "pct_range": (5, 95), "unit1":"円" },
    { "pattern": 2, "template": "投資額 <b>{label1}円</b> に対して、リターン（利回り）が <b>{pct}%</b> ありました。<br>利益額は？", "range1": (1000000, 10000000000), "pct_range": (3, 20), "unit1":"円" },
    # パターン3: A * B * r
    { "pattern": 3, "template": "単価 <b>{label1}円</b> の商品を <b>{label2}個</b> 販売し、利益率は <b>{pct}%</b> でした。<br>利益額は？", "range1": (100, 20000), "range2": (100, 50000), "pct_range": (5, 40), "unit1":"円", "unit2":"個" },
    { "pattern": 3, "template": "客単価 <b>{label1}円</b> で <b>{label2}人</b> が来店し、原価率は <b>{pct}%</b> です。<br>原価の総額は？", "range1": (500, 10000), "range2": (100, 50000), "pct_range": (20, 80), "unit1":"円", "unit2":"人" },
    { "pattern": 3, "template": "案件単価 <b>{label1}円</b> の案件が <b>{label2}件</b> あり、成約率は <b>{pct}%</b> でした。<br>成約による売上合計は？", "range1": (100000, 5000000), "range2": (10, 500), "pct_range": (5, 60), "unit1":"円", "unit2":"件" },
    # パターン4: A * B(年)
    { "pattern": 4, "template": "子会社株式の減損テスト。将来CF <b>{label1}円</b> が <b>{label2}</b> 続くと仮定します。<br>割引前のCF総額は？", "range1": (10000000, 5000000000), "range2": (3, 15), "suffix2": "年", "unit1":"円", "unit2":"年間" },
    { "pattern": 4, "template": "投資案件の評価。年間 <b>{label1}円</b> のリターンが <b>{label2}</b> 継続する見込みです。<br>期間累計のリターンは？", "range1": (1000000, 1000000000), "range2": (3, 20), "suffix2": "年", "unit1":"円", "unit2":"年間" },
    { "pattern": 4, "template": "新規事業のPL計画。年間固定費 <b>{label1}円</b> が <b>{label2}</b> かかる見通しです。<br>固定費の総額は？", "range1": (5000000, 500000000), "range2": (2, 5), "suffix2": "年", "unit1":"円", "unit2":"年間" }
]

def generate_question_data(is_advanced=False, force_pattern=None, simple_amounts=None, simple_pct=None):
    if simple_amounts is None: simple_amounts = not is_advanced
    if simple_pct is None: simple_pct = not is_advanced

    if force_pattern:
        candidates = [s for s in SCENARIOS if s['pattern'] == force_pattern]
    else:
        candidates = SCENARIOS
        
    scenario = random.choice(candidates)
    pattern = scenario['pattern']
    
    val1 = get_random_val(scenario['range1'][0], scenario['range1'][1], simple=simple_amounts)
    val2 = 1
    pct = 0
    
    if 'range2' in scenario:
        val2 = get_random_val(scenario['range2'][0], scenario['range2'][1], simple=simple_amounts)
        
    if 'pct_range' in scenario:
        min_p, max_p = scenario['pct_range']
        excluded_pct = [10, 50]
        if simple_pct:
            candidates_pct = list(range(min_p, max_p+1, 5))
            candidates_pct = [p for p in candidates_pct if p not in excluded_pct and p != 0]
            if not candidates_pct: pct = 5
            else: pct = random.choice(candidates_pct)
        else:
            while True:
                pct = random.randint(min_p, max_p)
                if pct not in excluded_pct: break
    
    if simple_amounts:
        label1 = format_number_with_unit_label(val1)
    else:
        label1 = f"{val1:,}"
    
    label2 = ""
    suffix2 = scenario.get('suffix2', '')
    
    if pattern in [1, 3]:
        if simple_amounts:
            label2 = format_number_with_unit_label(val2)
        else:
            label2 = f"{val2:,}"
    elif pattern == 4:
        label2 = f"{val2}{suffix2}"
        
    correct_val = 0
    if pattern == 1: correct_val = val1 * val2
    elif pattern == 2: correct_val = val1 * (pct / 100.0)
    elif pattern == 3: correct_val = val1 * val2 * (pct / 100.0)
    elif pattern == 4: correct_val = val1 * val2

    q_text = scenario['template'].format(label1=label1, label2=label2, pct=pct)
    
    unit1 = scenario.get('unit1', '')
    unit2 = scenario.get('unit2', '')
    if pattern == 4: unit2 = suffix2
    
    return {
        "q_text": q_text,
        "correct": correct_val,
        "pattern": pattern,
        "raw_val1": val1, "raw_val2": val2, "raw_pct": pct,
        "unit1": unit1, "unit2": unit2,
        "is_advanced": is_advanced
    }

# ==========================================
# タイマー表示 (JavaScript)
# ==========================================
def show_timer():
    timer_html = """
    <div style="font-size:20px; color:#FACC15; font-weight:bold; margin-bottom:10px; font-family:monospace;">
        ⏱️ Time: <span id="time_display">0.0</span>s
    </div>
    <script>
        let start = Date.now();
        let timer = setInterval(function() {
            let delta = Date.now() - start;
            let el = document.getElementById("time_display");
            if(el) {
                el.innerHTML = (delta / 1000).toFixed(1);
            }
        }, 100);
    </script>
    """
    st.components.v1.html(timer_html, height=50)

# ==========================================
# スコア計算
# ==========================================
def calculate_score(user_val, correct_val):
    if correct_val == 0: return 0, 0.0, False
    diff_pct = abs((user_val - correct_val) / correct_val * 100)
    is_perfect = (user_val == correct_val)
    points = 0
    if diff_pct <= 2: points = 10
    elif diff_pct <= 4: points = 9
    elif diff_pct <= 6: points = 8
    elif diff_pct <= 8: points = 7
    elif diff_pct <= 10: points = 6
    elif diff_pct <= 12: points = 5
    elif diff_pct <= 14: points = 4
    elif diff_pct <= 16: points = 3
    elif diff_pct <= 18: points = 2
    elif diff_pct <= 20: points = 1
    else: points = 0
    return points, diff_pct, is_perfect

# ==========================================
# ゲーム進行管理
# ==========================================
def init_game_state():
    st.session_state.current_q_idx = 1
    st.session_state.score = 0
    st.session_state.exact_matches = 0
    st.session_state.total_duration = 0.0
    st.session_state.current_start_time = time.time()
    st.session_state.game_finished = False
    st.session_state.quiz_data = None
    st.session_state.quiz_answered = False
    st.session_state.history = []
    st.session_state.ranked_in = False

def next_question():
    if st.session_state.current_q_idx >= TOTAL_QUESTIONS:
        st.session_state.game_finished = True
    else:
        st.session_state.current_q_idx += 1
        st.session_state.quiz_data = None
        st.session_state.quiz_answered = False
        st.session_state.current_start_time = time.time()

# ==========================================
# 結果画面共通処理
# ==========================================
def show_result_screen(mode_name):
    mins = int(st.session_state.total_duration // 60)
    secs = int(st.session_state.total_duration % 60)
    
    st.markdown(f"""
    <div class="css-card" style="text-align: center;">
        <h3 style="color: #38BDF8;">MISSION COMPLETE</h3>
        <p style="font-size: 20px; color: #E2E8F0;">TOTAL SCORE</p>
        <p style="color: #FACC15; font-weight: bold; font-size: 48px; margin: 0;">{st.session_state.score}<span style="font-size: 24px;"> / 100</span></p>
        {'<p style="font-size: 16px; color: #38BDF8; margin-top: 10px;">🏆 ピタリ賞: ' + str(st.session_state.exact_matches) + ' 回</p>' if 'チャレンジ' in mode_name else ''}
        <hr style="border-color: #334155;">
        <p style="font-size: 18px; color: #F8FAFC;">⏱️ 合計タイム: <b>{mins}分 {secs}秒</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- ランキング登録フォーム ---
    if not st.session_state.ranked_in:
        with st.container():
            st.markdown("### 🏆 ランキングに登録")
            c1, c2 = st.columns([3, 1])
            nickname = c1.text_input("ニックネームを入力", placeholder="名無しさん")
            if c2.button("登録する", type="primary"):
                if not nickname: nickname = "名無しさん"
                save_ranking(nickname, mode_name, st.session_state.score, st.session_state.total_duration)
                st.session_state.ranked_in = True
                st.rerun()
    else:
        st.success("ランキングに登録しました！")
        st.markdown(f"### 📊 {mode_name} のランキング")
        display_ranking(filter_mode=mode_name)

    # --- 履歴詳細 ---
    st.markdown("---")
    st.write("### 📝 結果詳細")
    for h in st.session_state.history:
        label = h['result_label']
        color = '#FACC15' if ('⭕' in label or '点' in label and int(label.replace('点',''))>=8) else '#EF4444'
        st.markdown(f"""
        <div class="history-row">
            <span style="color:{color}; font-weight:bold; margin-right:10px; min-width:50px;">
                {label}
            </span>
            <span style="color:#E2E8F0; margin-right:15px; flex-grow:1;">
                {h['formula_kanji']}
            </span>
            <span style="color:#38BDF8; font-family:monospace;">
                {h['time']:.1f}s
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    if c1.button("もう一度挑戦", type="primary"):
        init_game_state()
        st.rerun()
    if c2.button("トップに戻る"):
        st.session_state.page = "home"
        st.rerun()

# ==========================================
# モード1：チャレンジモード (入力式)
# ==========================================
def mode_training(advanced=False):
    mode_name = "チャレンジ(上級)" if advanced else "チャレンジ(基礎)"
    st.markdown(f"## 💪 {mode_name}")
    
    if st.session_state.game_finished:
        show_result_screen(mode_name)
        return

    progress = st.session_state.current_q_idx / TOTAL_QUESTIONS
    st.progress(progress)
    st.caption(f"Q.{st.session_state.current_q_idx} / {TOTAL_QUESTIONS} | Score: {st.session_state.score}")
    
    if st.button("トップに戻る（中断）"):
        st.session_state.page = "home"
        st.rerun()

    if st.session_state.quiz_data is None:
        force_p = None
        if advanced:
            if st.session_state.current_q_idx > 6: force_p = 3
        else:
            while True:
                temp_q = generate_question_data(is_advanced=False)
                if temp_q['pattern'] != 3:
                    st.session_state.quiz_data = temp_q
                    break
        
        if st.session_state.quiz_data is None:
             st.session_state.quiz_data = generate_question_data(is_advanced=advanced, force_pattern=force_p)

    q = st.session_state.quiz_data

    st.markdown(f"""
    <div class="css-card">
        <h3 style="margin-top:0; color: #38BDF8;">Question</h3>
        <p style="font-size: 18px; line-height: 1.6; color: #F1F5F9;">{q['q_text']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.quiz_answered:
        show_timer()
    
    user_ans = st.number_input(
        "概算解答を入力 (円)", 
        value=0, 
        step=1, 
        format="%d",
        key=f"train_ans_{st.session_state.current_q_idx}"
    )
    
    if user_ans > 0:
        st.markdown(f"<p style='color:#FACC15; font-weight:bold;'>入力プレビュー: {user_ans:,} 円</p>", unsafe_allow_html=True)
    
    if not st.session_state.quiz_answered:
        if st.button("答え合わせ"):
            elapsed = time.time() - st.session_state.current_start_time
            st.session_state.total_duration += elapsed
            st.session_state.current_q_time = elapsed
            st.session_state.quiz_answered = True
            st.rerun()
    else:
        correct_val = q['correct']
        pattern_used = q['pattern']
        v1 = q['raw_val1']
        v2 = q['raw_val2']
        pct = q['raw_pct']
        u1 = q['unit1']
        u2 = q['unit2']
        
        # 解説用（アラビア数字）
        calc_str_arabic = ""
        if pattern_used == 1: calc_str_arabic = f"{v1:,} × {v2:,} = {correct_val:,.0f}"
        elif pattern_used == 2: calc_str_arabic = f"{v1:,} × {pct}% = {correct_val:,.0f}"
        elif pattern_used == 3: calc_str_arabic = f"{v1:,} × {v2:,} × {pct}% = {correct_val:,.0f}"
        elif pattern_used == 4: calc_str_arabic = f"{v1:,} × {v2} = {correct_val:,.0f}"

        # 履歴用（漢数字+単位）
        f_v1 = format_japanese_answer(v1) + u1
        f_ans = format_japanese_answer(correct_val) + "円"
        calc_str_kanji = ""
        if pattern_used == 1: 
            f_v2 = format_japanese_answer(v2) + u2
            calc_str_kanji = f"{f_v1} × {f_v2} ＝ {f_ans}"
        elif pattern_used == 2: 
            calc_str_kanji = f"{f_v1} × {pct}% ＝ {f_ans}"
        elif pattern_used == 3: 
            f_v2 = format_japanese_answer(v2) + u2
            calc_str_kanji = f"{f_v1} × {f_v2} × {pct}% ＝ {f_ans}"
        elif pattern_used == 4: 
            f_v2 = f"{v2}{u2}"
            calc_str_kanji = f"{f_v1} × {f_v2} ＝ {f_ans}"

        points, diff_pct, is_perfect = calculate_score(user_ans, correct_val)
        
        if len(st.session_state.history) < st.session_state.current_q_idx:
            st.session_state.history.append({
                "result_label": f"{points}点",
                "points": points,
                "formula_kanji": calc_str_kanji,
                "time": st.session_state.current_q_time
            })

        st.markdown(f"あなたの回答: **{user_ans:,}**")
        st.info(f"🧮 計算イメージ: {calc_str_arabic}")
        st.markdown(f"**正解:** <span style='font-size: 20px; color: #FACC15;'>{format_japanese_answer(correct_val)}</span> <span style='font-size: 14px; color: #888;'>({correct_val:,})</span>", unsafe_allow_html=True)
        
        if is_perfect:
            st.markdown(f"<div style='background-color:rgba(250, 204, 21, 0.2); padding:10px; border-radius:5px; text-align:center; color:#FACC15; font-weight:bold; margin-bottom:10px;'>🏆 ピタリ賞！ 獲得ポイント: {points}点</div>", unsafe_allow_html=True)
        elif points >= 8:
            st.success(f"⭕ 素晴らしい！ 獲得ポイント: {points}点 (ズレ: {diff_pct:.2f}%)")
        elif points >= 1:
            st.warning(f"🔺 まずまず！ 獲得ポイント: {points}点 (ズレ: {diff_pct:.2f}%)")
        else:
            st.error(f"❌ 残念... 獲得ポイント: {points}点 (ズレ: {diff_pct:.2f}%)")

        if st.button("次の問題へ", type="primary"):
            st.session_state.score += points
            if is_perfect: st.session_state.exact_matches += 1
            next_question()
            st.rerun()

# ==========================================
# モード2：お気軽モード (4択式)
# ==========================================
def mode_quiz(advanced=False):
    mode_name = "お気軽(上級)" if advanced else "お気軽(基礎)"
    st.markdown(f"## 🧩 {mode_name}")
    
    if st.session_state.game_finished:
        show_result_screen(mode_name)
        return

    progress = st.session_state.current_q_idx / TOTAL_QUESTIONS
    st.progress(progress)
    st.caption(f"Q.{st.session_state.current_q_idx} / {TOTAL_QUESTIONS} | Score: {st.session_state.score}")

    if st.button("トップに戻る（中断）"):
        st.session_state.page = "home"
        st.rerun()

    if st.session_state.quiz_data is None:
        force_p = None
        if advanced:
            if st.session_state.current_q_idx > 6: force_p = 3
        else:
            while True:
                temp_q = generate_question_data(is_advanced=False)
                if temp_q['pattern'] != 3:
                    st.session_state.quiz_data = temp_q
                    break
        
        if st.session_state.quiz_data is None:
             if not advanced:
                 st.session_state.quiz_data = generate_question_data(is_advanced=False, force_pattern=force_p, simple_amounts=False, simple_pct=True)
             else:
                 st.session_state.quiz_data = generate_question_data(is_advanced=True, force_pattern=force_p)
        
        q = st.session_state.quiz_data
        correct = q['correct']
        options = [correct]
        
        if advanced:
            multipliers = [0.85, 0.90, 0.95, 1.05, 1.10, 1.15]
            selected_mults = random.sample(multipliers, 3)
            for m in selected_mults:
                options.append(correct * m)
        else:
            if q['pattern'] == 2:
                options.extend([correct * 0.8, correct * 1.2, correct * 1.5])
            else:
                options.append(correct * 10)
                options.append(correct / 10)
                options.append(random.choice([correct * 100, correct / 100, correct * 2]))

        random.shuffle(options)
        q['options'] = options

    q = st.session_state.quiz_data
    
    st.markdown(f"""
    <div class="css-card">
        <h3 style="margin-top:0; color: #38BDF8;">Question</h3>
        <p style="font-size: 18px; line-height: 1.6; color: #F1F5F9;">{q['q_text']}</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.quiz_answered:
        show_timer()

    if not st.session_state.quiz_answered:
        col1, col2 = st.columns(2)
        for i, opt in enumerate(q['options']):
            btn_label = format_japanese_answer(opt)
            target_col = col1 if i % 2 == 0 else col2
            
            if target_col.button(f"{btn_label}", key=f"q_{st.session_state.current_q_idx}_opt_{i}", use_container_width=True):
                elapsed = time.time() - st.session_state.current_start_time
                st.session_state.total_duration += elapsed
                st.session_state.current_q_time = elapsed
                
                st.session_state.quiz_answered = True
                st.session_state.user_choice = opt
                st.rerun()
    else:
        user_val = st.session_state.user_choice
        correct_val = q['correct']
        v1 = q['raw_val1']
        v2 = q['raw_val2']
        pct = q['raw_pct']
        pat = q['pattern']
        u1 = q['unit1']
        u2 = q['unit2']
        
        # 解説用（アラビア数字）
        calc_str_arabic = ""
        if pat == 1: calc_str_arabic = f"{v1:,} × {v2:,} = {correct_val:,.0f}"
        elif pat == 2: calc_str_arabic = f"{v1:,} × {pct}% = {correct_val:,.0f}"
        elif pat == 3: calc_str_arabic = f"{v1:,} × {v2:,} × {pct}% = {correct_val:,.0f}"
        elif pat == 4: calc_str_arabic = f"{v1:,} × {v2} = {correct_val:,.0f}"

        # 履歴用（漢数字+単位）
        f_v1 = format_japanese_answer(v1) + u1
        f_ans = format_japanese_answer(correct_val) + "円"
        calc_str_kanji = ""
        if pat == 1: 
            f_v2 = format_japanese_answer(v2) + u2
            calc_str_kanji = f"{f_v1} × {f_v2} ＝ {f_ans}"
        elif pat == 2: 
            calc_str_kanji = f"{f_v1} × {pct}% ＝ {f_ans}"
        elif pat == 3: 
            f_v2 = format_japanese_answer(v2) + u2
            calc_str_kanji = f"{f_v1} × {f_v2} × {pct}% ＝ {f_ans}"
        elif pat == 4: 
            f_v2 = f"{v2}{u2}"
            calc_str_kanji = f"{f_v1} × {f_v2} ＝ {f_ans}"

        ratio = user_val / correct_val if correct_val != 0 else 0
        is_correct = (0.99 <= ratio <= 1.01)
        
        if len(st.session_state.history) < st.session_state.current_q_idx:
            st.session_state.history.append({
                "result_label": "⭕" if is_correct else "❌",
                "points": 1 if is_correct else 0,
                "formula_kanji": calc_str_kanji,
                "time": st.session_state.current_q_time
            })
        
        if is_correct: 
            st.success("🎉 正解！")
        else:
            st.error(f"❌ 不正解... 正解は 「{format_japanese_answer(correct_val)}」")
        
        st.info(f"🧮 計算イメージ: {calc_str_arabic}")

        if st.button("次の問題へ", type="primary"):
            if is_correct: st.session_state.score += 1
            next_question()
            st.rerun()

# ==========================================
# メイン
# ==========================================
def main():
    st.set_page_config(page_title="ビジネス暗算道場", page_icon="💼")
    apply_custom_design()
    
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'current_q_idx' not in st.session_state:
        init_game_state()

    if st.session_state.page == "home":
        st.markdown("<h1 style='text-align: center; color: #38BDF8; font-size: 3.5rem; text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);'>💼 ビジネス暗算道場</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94A3B8;'>Advance your mental math skills with professional tools.</p>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("🧩 お気軽モード（4択式）")
            if st.button("基礎編", key="quiz_basic_btn", use_container_width=True):
                init_game_state()
                st.session_state.page = "quiz"
                st.rerun()
            if st.button("上級編", key="quiz_adv_btn", use_container_width=True):
                init_game_state()
                st.session_state.page = "quiz_advanced"
                st.rerun()
            st.caption("4択で瞬時に判断する実戦モード。")

        with col2:
            st.info("📊 チャレンジモード（入力式）")
            if st.button("基礎編", key="train_basic_btn", use_container_width=True):
                init_game_state()
                st.session_state.page = "training"
                st.rerun()
            if st.button("上級編", key="train_adv_btn", use_container_width=True):
                init_game_state()
                st.session_state.page = "training_advanced"
                st.rerun()
            st.caption("誤差2%以内で満点。基礎は丸い数字、上級は実戦的。")

        # ランキング表示エリア (タブ分け)
        st.write("")
        st.markdown("---")
        st.subheader("🏆 最新ランキング")
        
        tab1, tab2, tab3, tab4 = st.tabs(["お気軽(基礎)", "お気軽(上級)", "チャレンジ(基礎)", "チャレンジ(上級)"])
        
        with tab1:
            st.caption("お気軽モード（基礎編）")
            display_ranking("お気軽(基礎)")
        with tab2:
            st.caption("お気軽モード（上級編）")
            display_ranking("お気軽(上級)")
        with tab3:
            st.caption("チャレンジモード（基礎編）")
            display_ranking("チャレンジ(基礎)")
        with tab4:
            st.caption("チャレンジモード（上級編）")
            display_ranking("チャレンジ(上級)")

        st.write("")
        st.markdown("---")
        st.subheader("📚 おすすめの学習資料")
        bk1, bk2 = st.columns(2)
        with bk1:
            st.markdown("Example: **外資系コンサルのフェルミ推定** ([Link](https://amazon.co.jp))")
        with bk2:
            st.markdown("Example: **決算書の読み方** ([Link](https://amazon.co.jp))")

    elif st.session_state.page == "training":
        mode_training(advanced=False)
    elif st.session_state.page == "training_advanced":
        mode_training(advanced=True)
    elif st.session_state.page == "quiz":
        mode_quiz(advanced=False)
    elif st.session_state.page == "quiz_advanced":
        mode_quiz(advanced=True)

if __name__ == "__main__":
    main()
