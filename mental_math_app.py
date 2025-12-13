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
MAX_LIMIT = 10**12
MIN_LIMIT = 100
TOTAL_QUESTIONS = 10

# ==========================================
# 共通関数
# ==========================================
def format_japanese_answer(num):
    int_num = int(num)
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

def generate_random_number_with_unit():
    base = random.randint(10, 9999) 
    unit_type = random.choices(["", "万", "億"], weights=[1, 5, 4])[0]
    val = 0
    label = ""
    if unit_type == "億":
        val = base * (10**8)
        label = f"{base:,}億"
    elif unit_type == "万":
        val = base * (10**4)
        label = f"{base:,}万"
    else:
        val = base * 100 
        label = f"{val:,}"
    return val, label

def generate_random_count():
    base = random.randint(1, 9999)
    unit_type = random.choices(["", "万"], weights=[8, 2])[0]
    if unit_type == "万":
        val = base * 10000
        label = f"{base:,}万"
    else:
        val = base
        label = f"{base:,}"
    return val, label

# ==========================================
# ゲーム進行管理
# ==========================================
def init_game_state():
    st.session_state.current_q_idx = 1
    st.session_state.score = 0
    st.session_state.game_finished = False
    st.session_state.train_active = False
    st.session_state.quiz_data = None
    st.session_state.quiz_answered = False

def next_question():
    if st.session_state.current_q_idx >= TOTAL_QUESTIONS:
        st.session_state.game_finished = True
    else:
        st.session_state.current_q_idx += 1
        st.session_state.train_active = False
        st.session_state.quiz_data = None
        st.session_state.quiz_answered = False

# ==========================================
# モード1：トレーニング
# ==========================================
def mode_training():
    st.markdown("## 💪 概算入力トレーニング")
    
    if st.session_state.game_finished:
        st.markdown(f"""
        <div class="css-card" style="text-align: center;">
            <h3 style="color: #38BDF8;">MISSION COMPLETE</h3>
            <p style="font-size: 24px; color: #E2E8F0;">SCORE: <span style="color: #FACC15; font-weight: bold; font-size: 32px;">{st.session_state.score}</span> / {TOTAL_QUESTIONS}</p>
        </div>
        """, unsafe_allow_html=True)
        
        rate = st.session_state.score
        if rate >= 9:
            st.success("🏆 評価: S (神レベル) - Perfect Calculation!")
        elif rate >= 7:
            st.info("🥇 評価: A (上級者) - Excellent Work.")
        elif rate >= 4:
            st.warning("🥈 評価: B (普通) - Good Job.")
        else:
            st.error("🥉 評価: C (修行中) - Keep Practice.")
            
        st.write("")
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

    if not st.session_state.train_active:
        while True:
            digit_range1 = random.randint(3, 9)
            digit_range2 = random.randint(2, 6)
            num1 = random.randint(10**(digit_range1-1), 10**digit_range1)
            num2 = random.randint(10**(digit_range2-1), 10**digit_range2)
            ans = num1 * num2
            if ans <= MAX_LIMIT:
                st.session_state.train_num1 = num1
                st.session_state.train_num2 = num2
                st.session_state.train_active = True
                break

    st.markdown("### Question")
    with st.container():
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 0.5, 2])
        with c1: st.metric("数値 A", f"{st.session_state.train_num1:,}")
        with c2: st.markdown("<h2 style='text-align: center; color: #64748B;'>×</h2>", unsafe_allow_html=True)
        with c3: st.metric("数値 B", f"{st.session_state.train_num2:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    user_ans = st.number_input(
        "概算解答を入力", 
        value=0.0, 
        step=10000.0, 
        format="%.0f", 
        key=f"train_ans_{st.session_state.current_q_idx}"
    )
    
    if not st.session_state.quiz_answered:
        if st.button("答え合わせ"):
            st.session_state.quiz_answered = True
            st.rerun()
    else:
        ans = st.session_state.train_num1 * st.session_state.train_num2
        diff_pct = ((user_ans - ans) / ans * 100) if ans != 0 else 0
        
        st.info(f"🧮 計算イメージ: {st.session_state.train_num1:,.0f} × {st.session_state.train_num2:,.0f} = {ans:,.0f}")
        st.markdown(f"**正解:** <span style='font-size: 20px; color: #FACC15;'>{format_japanese_answer(ans)}</span>", unsafe_allow_html=True)
        
        is_correct = False
        if abs(diff_pct) <= 20:
            st.success(f"⭕ 正解！ (ズレ: {diff_pct:.1f}%)")
            is_correct = True
        else:
            st.error(f"❌ 不正解... (ズレ: {diff_pct:.1f}%)")

        if st.button("次の問題へ", type="primary"):
            if is_correct: st.session_state.score += 1
            next_question()
            st.rerun()

# ==========================================
# モード2：クイズ (通常 & 上級共通)
# ==========================================
def mode_quiz(advanced=False):
    title = "🧩 ビジネス概算クイズ（上級）" if advanced else "🧩 ビジネス概算クイズ（４択式）"
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
        
        st.write("")
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

    if st.session_state.quiz_data is None:
        while True:
            # ★問題パターンの恣意的な制御ロジック
            # 第1問〜第6問: 基礎編 [パターン1(個数), 2(%), 4(年数)]
            if st.session_state.current_q_idx <= 6:
                pattern = random.choice([1, 2, 4])
            # 第7問〜第10問: 応用編 [パターン3(3要素計算)]
            else:
                pattern = 3

            # val1生成（金額）
            val1, label1 = generate_random_number_with_unit()
            
            # val2生成（パターンによって個数か年数か分岐）
            if pattern == 4:
                val2 = random.randint(3, 15)
                label2 = f"{val2}年"
            elif pattern in [1, 3]:
                val2, label2 = generate_random_count()
            else:
                val2, label2 = generate_random_number_with_unit() # ダミー

            # %生成
            if advanced:
                pct_num = random.randint(1, 99)
            else:
                pct_num = random.choice([10, 20, 30, 40, 50, 5, 15, 25])
            
            pct_val = pct_num / 100.0
            
            question_text = ""
            correct_val = 0
            
            # --- 問題文分岐 ---
            if pattern == 1:
                templates = [
                    f"単価 <b>{label1}円</b> の商品が <b>{label2}個</b> 売れた。<br>売上推定値は？",
                    f"1人あたり <b>{label1}円</b> のコストがかかる研修に <b>{label2}人</b> が参加します。<br>総費用推定値は？",
                    f"月商 <b>{label1}円</b> の店舗を <b>{label2}店舗</b> 運営しています。<br>全店の月商合計は？",
                    f"契約単価 <b>{label1}円</b> のサブスク会員が <b>{label2}人</b> います。<br>毎月の売上は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * val2
            elif pattern == 2:
                templates = [
                    f"売上高 <b>{label1}円</b> に対して、営業利益率は <b>{pct_num}%</b> です。<br>営業利益は？",
                    f"市場規模 <b>{label1}円</b> の業界で、シェア <b>{pct_num}%</b> を獲得しました。<br>自社の売上は？",
                    f"予算 <b>{label1}円</b> のうち、すでに <b>{pct_num}%</b> を消化しました。<br>消化した金額は？",
                    f"投資額 <b>{label1}円</b> に対して、リターン（利回り）が <b>{pct_num}%</b> ありました。<br>利益額は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * pct_val
            elif pattern == 3:
                templates = [
                    f"単価 <b>{label1}円</b> の商品を <b>{label2}個</b> 販売し、利益率は <b>{pct_num}%</b> でした。<br>利益額は？",
                    f"客単価 <b>{label1}円</b> で <b>{label2}人</b> が来店し、原価率は <b>{pct_num}%</b> です。<br>原価の総額は？",
                    f"1件 <b>{label1}円</b> の案件が <b>{label2}件</b> あり、成約率は <b>{pct_num}%</b> でした。<br>成約による売上合計は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * val2 * pct_val
            elif pattern == 4:
                templates = [
                    f"子会社株式の減損テスト。将来CF <b>{label1}円</b> が <b>{label2}</b> 続くと仮定します。<br>割引前のCF総額は？",
                    f"投資案件の評価。年間 <b>{label1}円</b> のリターンが <b>{label2}</b> 継続する見込みです。<br>期間累計のリターンは？",
                    f"のれんの減損判定。事業計画では年間 <b>{label1}円</b> の利益が <b>{label2}</b> 発生します。<br>この期間の利益合計は？",
                    f"新規事業のPL計画。年間固定費 <b>{label1}円</b> が <b>{label2}</b> かかる見通しです。<br>固定費の総額は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * val2
            
            if MIN_LIMIT <= correct_val <= MAX_LIMIT: 
                break

        options = []
        options.append(correct_val)
        
        # --- 選択肢生成 ---
        if advanced:
            multipliers = [0.85, 0.90, 0.95, 1.05, 1.10, 1.15]
            selected_mults = random.sample(multipliers, 3)
            for m in selected_mults:
                options.append(correct_val * m)
        else:
            if pattern == 2:
                opt_minus_20 = correct_val * 0.8
                opt_plus_20  = correct_val * 1.2
                opt_random   = correct_val * random.choice([0.6, 1.4, 1.5])
                options.extend([opt_minus_20, opt_plus_20, opt_random])
            else:
                options.append(correct_val * 10) 
                options.append(correct_val / 10) 
                if correct_val * 100 > MAX_LIMIT * 10:
                    options.append(correct_val / 100)
                else:
                    options.append(random.choice([correct_val * 100, correct_val / 100]))
        
        random.shuffle(options)
        
        st.session_state.quiz_data = {
            "q_text": question_text,
            "correct": correct_val,
            "options": options,
            "pattern": pattern,
            "raw_val1": val1, "raw_val2": val2, "raw_pct": pct_num,
            "is_advanced": advanced
        }
        st.session_state.quiz_answered = False

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
        pattern_used = q.get('pattern', 1)
        
        calc_str = ""
        v1 = q['raw_val1']
        v2 = q['raw_val2']
        pct = q['raw_pct']
        
        if pattern_used == 1: calc_str = f"{v1:,.0f} × {v2:,.0f} = {correct_val:,.0f}"
        elif pattern_used == 2: calc_str = f"{v1:,.0f} × {pct}% = {correct_val:,.0f}"
        elif pattern_used == 3: calc_str = f"{v1:,.0f} × {v2:,.0f} × {pct}% = {correct_val:,.0f}"
        elif pattern_used == 4: calc_str = f"{v1:,.0f} × {v2}年 = {correct_val:,.0f}"

        ratio = user_val / correct_val if correct_val != 0 else 0
        is_correct = False
        
        if 0.99 <= ratio <= 1.01: 
            st.success("🎉 正解！")
            is_correct = True
        else:
            st.error(f"❌ 不正解... 正解は 「{format_japanese_answer(correct_val)}」")
        
        st.info(f"🧮 計算イメージ:\n{calc_str}")

        if st.button("次の問題へ", type="primary"):
            if is_correct: st.session_state.score += 1
            next_question()
            st.rerun()

# ==========================================
# メイン
# ==========================================
def main():
    st.set_page_config(page_title="ビジネス数字力道場", page_icon="💼")
    apply_custom_design() # ★CSS適用
    
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'current_q_idx' not in st.session_state:
        init_game_state()

    if st.session_state.page == "home":
        # タイトル
        st.markdown("<h1 style='text-align: center; color: #38BDF8; font-size: 3.5rem; text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);'>💼 ビジネス数字力道場</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94A3B8;'>Advance your mental math skills with professional tools.</p>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        
        col1, col2 = st.columns(2)
        
        # col1: クイズ（4択）
        with col1:
            st.success("🧩 ビジネス概算クイズ（４択式）")
            # 通常モード
            if st.button("シナリオ形式", use_container_width=True):
                init_game_state()
                st.session_state.page = "quiz"
                st.rerun()
            # 上級モード
            if st.button("シナリオ形式（上級）", use_container_width=True):
                init_game_state()
                st.session_state.page = "quiz_advanced"
                st.rerun()
            st.caption("上級は5%刻みの選択肢＆詳細な%計算が出題されます。")

        # col2: トレーニング（入力）
        with col2:
            st.info("📊 ストイックに練習")
            if st.button("概算トレーニング\n(入力式)", use_container_width=True):
                init_game_state()
                st.session_state.page = "training"
                st.rerun()
            st.caption("10問セットの集中モード。")

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
        mode_training()
    elif st.session_state.page == "quiz":
        mode_quiz(advanced=False)
    elif st.session_state.page == "quiz_advanced":
        mode_quiz(advanced=True)

if __name__ == "__main__":
    main()
