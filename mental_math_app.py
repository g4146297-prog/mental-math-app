import streamlit as st
import random

# ==========================================
# デザイン設定 (CSS) - 案A改: スマート＆モダン
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
        .stProgress > div > div > div > div {
            background-color: #38BDF8;
            box-shadow: 0 0 8px #38BDF8;
        }
        hr {
            border-color: #334155;
        }
        .stCaption {
            color: #94A3B8;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 定数設定
# ==========================================
MAX_LIMIT = 10**13  # 上限: 10兆
MIN_LIMIT = 100
TOTAL_QUESTIONS = 10

# ==========================================
# 共通関数: 数値フォーマット・生成
# ==========================================
def format_japanese_answer(num):
    """数値を '1兆2000億' のような形式に変換"""
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
    """
    数値を読みやすい単位付き文字列に変換して返す (例: 15000 -> 1.5万, 100 -> 100)
    問題文の表示用。
    """
    if value >= 10**8:
        # 億単位
        if value % 10**8 == 0:
            return f"{value // 10**8:,}億"
        else:
            return f"{value / 10**8:.1f}億".replace(".0", "")
    elif value >= 10**4:
        # 万単位
        if value % 10**4 == 0:
            return f"{value // 10**4:,}万"
        else:
            return f"{value / 10**4:.1f}万".replace(".0", "")
    else:
        return f"{value:,}"

def get_random_val(min_val, max_val, simple=False):
    """
    指定範囲内でランダムな整数を生成する。
    simple=True の場合、有効数字1桁程度のキリの良い数字にする。
    """
    val = random.randint(min_val, max_val)
    
    if simple:
        # 桁数に合わせて丸める
        digits = len(str(val))
        if digits > 1:
            # 上位1桁〜2桁を残して0にするなどの調整
            # ここではシンプルに「上位1桁 + ゼロ」または「上位2桁(50, 25など) + ゼロ」にする
            
            # 候補となる「キリの良い係数」
            bases = [10, 20, 30, 40, 50, 60, 70, 80, 90, 15, 25, 12, 18]
            base = random.choice(bases)
            
            # 桁合わせ
            # min_valの桁数を考慮
            min_digits = len(str(min_val))
            target_digits = random.randint(min_digits, len(str(max_val)))
            
            # 10^(target_digits - 2) などを掛ける
            power = max(0, target_digits - 2)
            val = base * (10**power)
            
            # 範囲外なら補正
            if val < min_val: val = min_val
            if val > max_val: val = max_val
            
            # さらに100以下なら丸めすぎない
            if val < 100:
                val = (val // 10) * 10
            
    return int(val)

# ==========================================
# シナリオデータ定義
# ==========================================
# 各シナリオに「現実的な数値範囲」を設定
SCENARIOS = [
    # --- パターン1: A * B (単価 * 個数 / コスト * 人数 / etc) ---
    {
        "pattern": 1,
        "template": "単価 <b>{label1}円</b> の商品が <b>{label2}個</b> 売れました。<br>売上推定値は？",
        "range1": (100, 50000),      # 単価: 100円 ~ 5万円
        "range2": (100, 100000)      # 個数: 100個 ~ 10万個
    },
    {
        "pattern": 1,
        "template": "1人あたり <b>{label1}円</b> のコストがかかる研修に <b>{label2}人</b> が参加します。<br>総費用推定値は？",
        "range1": (5000, 200000),    # コスト: 5,000円 ~ 20万円
        "range2": (10, 5000)         # 人数: 10人 ~ 5,000人
    },
    {
        "pattern": 1,
        "template": "月商 <b>{label1}円</b> の店舗を <b>{label2}店舗</b> 運営しています。<br>全店の月商合計は？",
        "range1": (1000000, 50000000), # 月商: 100万円 ~ 5,000万円
        "range2": (3, 1000)          # 店舗数: 3店舗 ~ 1,000店舗
    },
    {
        "pattern": 1,
        "template": "契約単価 <b>{label1}円</b> のサブスク会員が <b>{label2}人</b> います。<br>毎月の売上は？",
        "range1": (500, 10000),      # 単価: 500円 ~ 1万円
        "range2": (1000, 1000000)    # 会員数: 1,000人 ~ 100万人
    },

    # --- パターン2: A * r (金額 * %) ---
    {
        "pattern": 2,
        "template": "売上高 <b>{label1}円</b> に対して、営業利益率は <b>{pct}%</b> です。<br>営業利益は？",
        "range1": (100000000, 1000000000000), # 売上: 1億円 ~ 1兆円
        "pct_range": (1, 30)        # 利益率: 1% ~ 30%
    },
    {
        "pattern": 2,
        "template": "市場規模 <b>{label1}円</b> の業界で、シェア <b>{pct}%</b> を獲得しました。<br>自社の売上は？",
        "range1": (1000000000, 1000000000000), # 市場: 10億円 ~ 1兆円
        "pct_range": (1, 50)        # シェア: 1% ~ 50%
    },
    {
        "pattern": 2,
        "template": "予算 <b>{label1}円</b> のうち、すでに <b>{pct}%</b> を消化しました。<br>消化した金額は？",
        "range1": (1000000, 1000000000), # 予算: 100万円 ~ 10億円
        "pct_range": (5, 95)        # 消化率
    },
    {
        "pattern": 2,
        "template": "投資額 <b>{label1}円</b> に対して、リターン（利回り）が <b>{pct}%</b> ありました。<br>利益額は？",
        "range1": (1000000, 10000000000), # 投資: 100万円 ~ 100億円
        "pct_range": (3, 20)        # 利回り: 3% ~ 20%
    },

    # --- パターン3: A * B * r (単価 * 個数 * %) ---
    {
        "pattern": 3,
        "template": "単価 <b>{label1}円</b> の商品を <b>{label2}個</b> 販売し、利益率は <b>{pct}%</b> でした。<br>利益額は？",
        "range1": (100, 20000),      # 単価
        "range2": (100, 50000),      # 個数
        "pct_range": (5, 40)         # 利益率
    },
    {
        "pattern": 3,
        "template": "客単価 <b>{label1}円</b> で <b>{label2}人</b> が来店し、原価率は <b>{pct}%</b> です。<br>原価の総額は？",
        "range1": (500, 10000),      # 客単価
        "range2": (100, 50000),      # 来店数
        "pct_range": (20, 80)        # 原価率
    },
    {
        "pattern": 3,
        "template": "案件単価 <b>{label1}円</b> の案件が <b>{label2}件</b> あり、成約率は <b>{pct}%</b> でした。<br>成約による売上合計は？",
        "range1": (100000, 5000000), # 案件単価
        "range2": (10, 500),         # 件数
        "pct_range": (5, 50)         # 成約率
    },

    # --- パターン4: A * B (金額 * 年数) ---
    {
        "pattern": 4,
        "template": "子会社株式の減損テスト。将来CF <b>{label1}円</b> が <b>{label2}</b> 続くと仮定します。<br>割引前のCF総額は？",
        "range1": (10000000, 5000000000), # CF: 1000万円 ~ 50億円
        "range2": (3, 15),           # 年数: 3年 ~ 15年
        "suffix2": "年"
    },
    {
        "pattern": 4,
        "template": "投資案件の評価。年間 <b>{label1}円</b> のリターンが <b>{label2}</b> 継続する見込みです。<br>期間累計のリターンは？",
        "range1": (1000000, 1000000000),  # リターン
        "range2": (3, 20),           # 年数
        "suffix2": "年"
    },
    {
        "pattern": 4,
        "template": "新規事業のPL計画。年間固定費 <b>{label1}円</b> が <b>{label2}</b> かかる見通しです。<br>固定費の総額は？",
        "range1": (5000000, 500000000),   # 固定費
        "range2": (2, 5),            # 年数
        "suffix2": "年"
    }
]

def generate_question_data(is_advanced=False, force_pattern=None):
    """
    シナリオリストから適切な問題を選び、数値を生成して返す
    """
    # パターンによるフィルタリング（指定があれば）
    if force_pattern:
        candidates = [s for s in SCENARIOS if s['pattern'] == force_pattern]
    else:
        # 上級か基礎かで出現パターンを調整してもよいが、ここでは全候補から
        candidates = SCENARIOS
        
    scenario = random.choice(candidates)
    pattern = scenario['pattern']
    
    # --- 数値生成 (基礎編ならsimple=True) ---
    simple_mode = not is_advanced
    
    val1 = get_random_val(scenario['range1'][0], scenario['range1'][1], simple=simple_mode)
    
    val2 = 1
    pct = 0
    
    # 2つ目の値 (パターン1, 3, 4で使用)
    if 'range2' in scenario:
        val2 = get_random_val(scenario['range2'][0], scenario['range2'][1], simple=simple_mode)
        
    # %の値 (パターン2, 3で使用)
    if 'pct_range' in scenario:
        min_p, max_p = scenario['pct_range']
        if simple_mode:
            # 5%刻み (5, 10, 15...)
            pct = random.choice(list(range(min_p, max_p+1, 5)))
            if pct == 0: pct = 5
        else:
            # 1%刻み
            pct = random.randint(min_p, max_p)
    
    # ラベル生成 (単位付き)
    label1 = format_number_with_unit_label(val1)
    
    label2 = ""
    if pattern in [1, 3]:
        label2 = format_number_with_unit_label(val2)
    elif pattern == 4:
        label2 = f"{val2}{scenario.get('suffix2', '')}"
        
    # 正解計算
    correct_val = 0
    if pattern == 1: # A * B
        correct_val = val1 * val2
    elif pattern == 2: # A * r
        correct_val = val1 * (pct / 100.0)
    elif pattern == 3: # A * B * r
        correct_val = val1 * val2 * (pct / 100.0)
    elif pattern == 4: # A * B(年)
        correct_val = val1 * val2

    # 問題文フォーマット
    q_text = scenario['template'].format(label1=label1, label2=label2, pct=pct)
    
    return {
        "q_text": q_text,
        "correct": correct_val,
        "pattern": pattern,
        "raw_val1": val1, "raw_val2": val2, "raw_pct": pct,
        "is_advanced": is_advanced
    }

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
    st.session_state.game_finished = False
    st.session_state.quiz_data = None
    st.session_state.quiz_answered = False

def next_question():
    if st.session_state.current_q_idx >= TOTAL_QUESTIONS:
        st.session_state.game_finished = True
    else:
        st.session_state.current_q_idx += 1
        st.session_state.quiz_data = None
        st.session_state.quiz_answered = False

# ==========================================
# モード1：トレーニング (入力式)
# ==========================================
def mode_training(advanced=False):
    title = "💪 入力式テスト（上級編）" if advanced else "💪 入力式テスト（基礎編）"
    st.markdown(f"## {title}")
    
    if st.session_state.game_finished:
        st.markdown(f"""
        <div class="css-card" style="text-align: center;">
            <h3 style="color: #38BDF8;">MISSION COMPLETE</h3>
            <p style="font-size: 20px; color: #E2E8F0;">TOTAL SCORE</p>
            <p style="color: #FACC15; font-weight: bold; font-size: 48px; margin: 0;">{st.session_state.score}<span style="font-size: 24px;"> / 100</span></p>
            <p style="font-size: 16px; color: #38BDF8; margin-top: 10px;">🏆 ピタリ賞: {st.session_state.exact_matches} 回</p>
        </div>
        """, unsafe_allow_html=True)
        
        rate = st.session_state.score
        if rate >= 90:
            st.success("🏆 評価: S (神レベル) - 完璧な感覚です！")
        elif rate >= 70:
            st.info("🥇 評価: A (上級者) - 素晴らしい精度です。")
        elif rate >= 40:
            st.warning("🥈 評価: B (普通) - まずまずです。")
        else:
            st.error("🥉 評価: C (修行中) - 桁感覚を鍛えましょう。")
            
        c1, c2 = st.columns(2)
        if c1.button("もう一度挑戦", type="primary"):
            init_game_state()
            st.rerun()
        if c2.button("トップに戻る"):
            st.session_state.page = "home"
            st.rerun()
        return

    progress = st.session_state.current_q_idx / TOTAL_QUESTIONS
    st.progress(progress)
    st.caption(f"Q.{st.session_state.current_q_idx} / {TOTAL_QUESTIONS} | Score: {st.session_state.score}")
    
    if st.button("トップに戻る（中断）"):
        st.session_state.page = "home"
        st.rerun()

    # --- 問題生成 ---
    if st.session_state.quiz_data is None:
        # パターン制御
        force_p = None
        if advanced:
            # 上級: 後半(7-10問目)は3要素計算(パターン3)
            if st.session_state.current_q_idx > 6:
                force_p = 3
        else:
            # 基礎: 3要素計算(パターン3)は出さない。パターン1,2,4から
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
    
    st.write("")
    
    # 入力フィールド
    user_ans = st.number_input(
        "概算解答を入力 (円)", 
        value=0, 
        step=1, 
        format="%d",
        key=f"train_ans_{st.session_state.current_q_idx}"
    )
    
    if not st.session_state.quiz_answered:
        if st.button("答え合わせ"):
            st.session_state.quiz_answered = True
            st.rerun()
    else:
        correct_val = q['correct']
        pattern_used = q['pattern']
        v1 = q['raw_val1']
        v2 = q['raw_val2']
        pct = q['raw_pct']
        
        calc_str = ""
        # 表示用の計算式構築
        lbl1 = format_number_with_unit_label(v1)
        if pattern_used == 1: 
            lbl2 = format_number_with_unit_label(v2)
            calc_str = f"{lbl1} × {lbl2} = {format_japanese_answer(correct_val)}"
        elif pattern_used == 2: 
            calc_str = f"{lbl1} × {pct}% = {format_japanese_answer(correct_val)}"
        elif pattern_used == 3: 
            lbl2 = format_number_with_unit_label(v2)
            calc_str = f"{lbl1} × {lbl2} × {pct}% = {format_japanese_answer(correct_val)}"
        elif pattern_used == 4: 
            calc_str = f"{lbl1} × {v2}年 = {format_japanese_answer(correct_val)}"

        points, diff_pct, is_perfect = calculate_score(user_ans, correct_val)
        
        st.markdown(f"あなたの回答: **{user_ans:,}**")

        st.info(f"🧮 計算イメージ: {calc_str}")
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
            if is_perfect:
                st.session_state.exact_matches += 1
            next_question()
            st.rerun()

# ==========================================
# モード2：クイズ (4択式)
# ==========================================
def mode_quiz(advanced=False):
    title = "🧩 4択クイズ（上級編）" if advanced else "🧩 4択クイズ（基礎編）"
    st.markdown(f"## {title}")
    
    if st.session_state.game_finished:
        st.markdown(f"""
        <div class="css-card" style="text-align: center;">
            <h3 style="color: #38BDF8;">MISSION COMPLETE</h3>
            <p style="font-size: 24px; color: #E2E8F0;">SCORE: <span style="color: #FACC15; font-weight: bold; font-size: 32px;">{st.session_state.score}</span> / {TOTAL_QUESTIONS}</p>
        </div>
        """, unsafe_allow_html=True)

        rate = st.session_state.score
        if rate >= 9:
            st.success("🏆 評価: CEO級 - 経営判断も任せられます！")
        elif rate >= 7:
            st.info("🥇 評価: 部長級 - 安定した数字力です。")
        elif rate >= 4:
            st.warning("🥈 評価: 課長級 - 基礎はできています。")
        else:
            st.error("🥉 評価: 新人級 - まずは単位を覚えましょう。")
        
        c1, c2 = st.columns(2)
        if c1.button("もう一度挑戦", type="primary"):
            init_game_state()
            st.rerun()
        if c2.button("トップに戻る"):
            st.session_state.page = "home"
            st.rerun()
        return

    progress = st.session_state.current_q_idx / TOTAL_QUESTIONS
    st.progress(progress)
    st.caption(f"Q.{st.session_state.current_q_idx} / {TOTAL_QUESTIONS} | Score: {st.session_state.score}")

    if st.button("トップに戻る（中断）"):
        st.session_state.page = "home"
        st.rerun()

    # --- 問題生成 ---
    if st.session_state.quiz_data is None:
        # パターン制御
        force_p = None
        if advanced:
            # 上級: 後半(7-10問目)は3要素計算
            if st.session_state.current_q_idx > 6:
                force_p = 3
        else:
            # 基礎: 3要素計算は除外
            while True:
                temp_q = generate_question_data(is_advanced=False)
                if temp_q['pattern'] != 3:
                    st.session_state.quiz_data = temp_q
                    break
        
        if st.session_state.quiz_data is None:
             st.session_state.quiz_data = generate_question_data(is_advanced=advanced, force_pattern=force_p)
        
        # 選択肢生成
        q = st.session_state.quiz_data
        correct = q['correct']
        options = [correct]
        
        if advanced:
            # 5%刻みの選択肢
            multipliers = [0.85, 0.90, 0.95, 1.05, 1.10, 1.15]
            selected_mults = random.sample(multipliers, 3)
            for m in selected_mults:
                options.append(correct * m)
        else:
            # 桁ズレや20%ズレ
            if q['pattern'] == 2: # %計算
                options.extend([correct * 0.8, correct * 1.2, correct * 1.5])
            else: # 掛け算系
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
        col1, col2 = st.columns(2)
        for i, opt in enumerate(q['options']):
            btn_label = format_japanese_answer(opt)
            target_col = col1 if i % 2 == 0 else col2
            if target_col.button(f"{btn_label}", key=f"q_{st.session_state.current_q_idx}_opt_{i}", use_container_width=True):
                st.session_state.quiz_answered = True
                st.session_state.user_choice = opt
                st.rerun()
    else:
        user_val = st.session_state.user_choice
        correct_val = q['correct']
        pattern_used = q['pattern']
        
        calc_str = ""
        v1 = q['raw_val1']
        v2 = q['raw_val2']
        pct = q['raw_pct']
        lbl1 = format_number_with_unit_label(v1)
        
        if pattern_used == 1: 
            lbl2 = format_number_with_unit_label(v2)
            calc_str = f"{lbl1} × {lbl2} = {format_japanese_answer(correct_val)}"
        elif pattern_used == 2: 
            calc_str = f"{lbl1} × {pct}% = {format_japanese_answer(correct_val)}"
        elif pattern_used == 3: 
            lbl2 = format_number_with_unit_label(v2)
            calc_str = f"{lbl1} × {lbl2} × {pct}% = {format_japanese_answer(correct_val)}"
        elif pattern_used == 4: 
            calc_str = f"{lbl1} × {v2}年 = {format_japanese_answer(correct_val)}"

        ratio = user_val / correct_val if correct_val != 0 else 0
        is_correct = False
        
        # 4択なので、ほぼ一致していれば正解
        if 0.99 <= ratio <= 1.01: 
            st.success("🎉 正解！")
            is_correct = True
        else:
            st.error(f"❌ 不正解... 正解は 「{format_japanese_answer(correct_val)}」")
        
        st.info(f"🧮 計算イメージ: {calc_str}")

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
            st.success("🧩 4択クイズ")
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
            st.info("📊 入力式テスト")
            if st.button("基礎編", key="train_basic_btn", use_container_width=True):
                init_game_state()
                st.session_state.page = "training"
                st.rerun()
            if st.button("上級編", key="train_adv_btn", use_container_width=True):
                init_game_state()
                st.session_state.page = "training_advanced"
                st.rerun()
            st.caption("誤差2%以内で満点。基礎は丸い数字、上級は実戦的。")

        st.write("")
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
