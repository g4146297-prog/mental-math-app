import streamlit as st
import random

# ==========================================
# デザイン設定 (CSS) - 案C: データ＆デジタル
# ==========================================
def apply_custom_design():
    # 案C: 黒ベース & ネオンカラー & グリッド感
    # 背景: 漆黒 / アクセント: シアン(青緑) & マゼンタ(赤紫)
    custom_css = """
    <style>
        /* 全体の背景色とフォント */
        .stApp {
            background-color: #050505; /* ほぼ真っ黒 */
            color: #E0E0E0;
            font-family: 'Roboto Mono', 'Courier New', monospace; /* 等幅フォント */
        }
        
        /* ヘッダーの装飾 - デジタル感 */
        h1, h2, h3 {
            color: #00F0FF; /* ネオンシアン */
            font-family: 'Orbitron', 'Roboto Mono', monospace;
            text-transform: uppercase; /* 大文字統一 */
            letter-spacing: 0.1em;
            border-bottom: 2px solid #00F0FF; /* 下線 */
            padding-bottom: 5px;
            display: inline-block;
        }
        
        /* ボタンのデザイン (プライマリー) - サイバーパンク風 */
        div.stButton > button:first-child {
            background-color: transparent;
            color: #00F0FF;
            border: 1px solid #00F0FF;
            border-radius: 0px; /* 角ばらせる */
            box-shadow: 0 0 5px #00F0FF;
            font-family: 'Roboto Mono', monospace;
            font-weight: bold;
            transition: all 0.2s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #00F0FF;
            color: #000;
            box-shadow: 0 0 15px #00F0FF;
        }
        
        /* 通常ボタン (セカンダリー) */
        div.stButton > button:nth-child(2) {
            background-color: transparent;
            color: #FF0055; /* マゼンタ */
            border: 1px solid #FF0055;
            border-radius: 0px;
            font-family: 'Roboto Mono', monospace;
        }
        div.stButton > button:nth-child(2):hover {
            background-color: rgba(255, 0, 85, 0.2);
            box-shadow: 0 0 10px #FF0055;
        }

        /* メトリクス (数字表示) - 電光掲示板風 */
        [data-testid="stMetricValue"] {
            color: #FF0055; /* ネオンマゼンタ */
            font-family: 'Courier New', monospace;
            font-weight: bold;
            text-shadow: 0 0 5px #FF0055;
        }
        [data-testid="stMetricLabel"] {
            color: #888;
            font-size: 0.8em;
            text-transform: uppercase;
        }

        /* カード風コンテナ (HUD風) */
        .css-card {
            background-color: #111;
            border: 1px solid #333;
            border-left: 3px solid #00F0FF;
            padding: 20px;
            margin-bottom: 20px;
            background-image: linear-gradient(0deg, transparent 24%, rgba(0, 240, 255, .05) 25%, rgba(0, 240, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 240, 255, .05) 75%, rgba(0, 240, 255, .05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(0, 240, 255, .05) 25%, rgba(0, 240, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 240, 255, .05) 75%, rgba(0, 240, 255, .05) 76%, transparent 77%, transparent);
            background-size: 30px 30px; /* グリッド線 */
        }
        
        /* info/successボックスのカスタマイズ */
        .stAlert {
            background-color: #0A0A0A;
            border: 1px solid #444;
            color: #EEE;
            border-radius: 0px;
        }
        
        /* プログレスバー */
        .stProgress > div > div > div > div {
            background-color: #00F0FF;
            border-radius: 0px;
        }
        
        /* キャプション */
        .stCaption {
            color: #666;
            font-family: 'Roboto Mono', monospace;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 定数設定
# ==========================================
MAX_LIMIT = 10**12  # 上限: 1兆
MIN_LIMIT = 100     # 下限: 100
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
    st.markdown("## >> SYSTEM: TRAINING_MODE")
    
    if st.session_state.game_finished:
        st.markdown(f"""
        <div class="css-card" style="text-align: center;">
            <h3 style="color: #00F0FF; border:none;">SESSION TERMINATED</h3>
            <p style="font-size: 24px; color: #FFF;">RESULT: <span style="color: #FF0055; font-weight: bold; font-size: 32px;">{st.session_state.score}</span> / {TOTAL_QUESTIONS}</p>
        </div>
        """, unsafe_allow_html=True)
        
        rate = st.session_state.score
        if rate >= 9:
            st.success("STATUS: RANK S [GOD_MODE]")
        elif rate >= 7:
            st.info("STATUS: RANK A [EXPERT]")
        elif rate >= 4:
            st.warning("STATUS: RANK B [NORMAL]")
        else:
            st.error("STATUS: RANK C [NOVICE]")
            
        st.write("")
        c1, c2 = st.columns(2)
        if c1.button("RETRY_SESSION", type="primary"):
            init_game_state()
            st.rerun()
        if c2.button("RETURN_ROOT"):
            st.session_state.page = "home"
            st.rerun()
        return

    progress = st.session_state.current_q_idx / TOTAL_QUESTIONS
    st.progress(progress)
    st.caption(f"SEQ: {st.session_state.current_q_idx}/{TOTAL_QUESTIONS} | DATA_ACC: {st.session_state.score}")
    
    if st.button("ABORT (RETURN)"):
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

    st.markdown("### >> INPUT_DATA")
    # デザイン調整用コンテナ
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 0.5, 2])
    with c1: st.metric("VAL_A", f"{st.session_state.train_num1:,}")
    with c2: st.markdown("<h2 style='text-align: center; color: #444; border:none;'>×</h2>", unsafe_allow_html=True)
    with c3: st.metric("VAL_B", f"{st.session_state.train_num2:,}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    user_ans = st.number_input(
        "ENTER ESTIMATE:", 
        value=0.0, 
        step=10000.0, 
        format="%.0f", 
        key=f"train_ans_{st.session_state.current_q_idx}"
    )
    
    if not st.session_state.quiz_answered:
        if st.button("EXECUTE_CHECK"):
            st.session_state.quiz_answered = True
            st.rerun()
    else:
        ans = st.session_state.train_num1 * st.session_state.train_num2
        diff_pct = ((user_ans - ans) / ans * 100) if ans != 0 else 0
        
        st.info(f"CALC_LOG: {st.session_state.train_num1:,.0f} × {st.session_state.train_num2:,.0f} = {ans:,.0f}")
        st.markdown(f"**TRUE_VAL:** <span style='font-size: 20px; color: #00F0FF; font-family: monospace;'>{format_japanese_answer(ans)}</span>", unsafe_allow_html=True)
        
        is_correct = False
        if abs(diff_pct) <= 20:
            st.success(f"[OK] DIFF: {diff_pct:.1f}%")
            is_correct = True
        else:
            st.error(f"[FAIL] DIFF: {diff_pct:.1f}%")

        if st.button("NEXT_SEQ >>", type="primary"):
            if is_correct: st.session_state.score += 1
            next_question()
            st.rerun()

# ==========================================
# モード2：クイズ
# ==========================================
def mode_quiz():
    st.markdown("## >> SYSTEM: QUIZ_MODE")
    
    if st.session_state.game_finished:
        st.markdown(f"""
        <div class="css-card" style="text-align: center;">
            <h3 style="color: #00F0FF; border:none;">SESSION TERMINATED</h3>
            <p style="font-size: 24px; color: #FFF;">RESULT: <span style="color: #FF0055; font-weight: bold; font-size: 32px;">{st.session_state.score}</span> / {TOTAL_QUESTIONS}</p>
        </div>
        """, unsafe_allow_html=True)

        rate = st.session_state.score
        if rate >= 9:
            st.success("EVAL: CEO_CLASS [OPTIMAL]")
        elif rate >= 7:
            st.info("EVAL: DIRECTOR_CLASS [HIGH]")
        elif rate >= 4:
            st.warning("EVAL: MANAGER_CLASS [NORMAL]")
        else:
            st.error("EVAL: NOVICE [LOW]")
        
        st.write("")
        c1, c2 = st.columns(2)
        if c1.button("RETRY_SESSION", type="primary"):
            init_game_state()
            st.rerun()
        if c2.button("RETURN_ROOT"):
            st.session_state.page = "home"
            st.rerun()
        return

    progress = st.session_state.current_q_idx / TOTAL_QUESTIONS
    st.progress(progress)
    st.caption(f"SEQ: {st.session_state.current_q_idx}/{TOTAL_QUESTIONS} | DATA_ACC: {st.session_state.score}")

    if st.button("ABORT (RETURN)"):
        st.session_state.page = "home"
        st.rerun()

    if st.session_state.quiz_data is None:
        while True:
            pattern = random.choice([1, 2, 3])
            val1, label1 = generate_random_number_with_unit()
            if pattern in [1, 3]:
                val2, label2 = generate_random_count()
            else:
                val2, label2 = generate_random_number_with_unit()

            pct_num = random.choice([10, 20, 30, 40, 50, 5, 15, 25])
            pct_val = pct_num / 100.0
            
            question_text = ""
            correct_val = 0
            
            if pattern == 1:
                templates = [
                    f"単価 **{label1}円** の商品が **{label2}個** 売れた。<br>売上推定値は？",
                    f"1人あたり **{label1}円** のコスト発生。対象 **{label2}人**。<br>総費用推定値は？",
                    f"月商 **{label1}円** の店舗を **{label2}店舗** 運営中。<br>全店月商合計は？",
                    f"契約単価 **{label1}円** × サブスク会員 **{label2}人**。<br>月間売上は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * val2
            elif pattern == 2:
                templates = [
                    f"売上高 **{label1}円** 。営業利益率 **{pct_num}%** 。<br>営業利益は？",
                    f"市場規模 **{label1}円** 。シェア **{pct_num}%** 獲得。<br>自社売上は？",
                    f"予算 **{label1}円** 。進捗率 **{pct_num}%** 消化。<br>消化金額は？",
                    f"投資額 **{label1}円** 。リターン率 **{pct_num}%** 。<br>利益額は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * pct_val
            elif pattern == 3:
                templates = [
                    f"単価 **{label1}円** × 販売数 **{label2}個** × 利益率 **{pct_num}%**。<br>利益額は？",
                    f"客単価 **{label1}円** × 来店数 **{label2}人** × 原価率 **{pct_num}%**。<br>原価総額は？",
                    f"案件単価 **{label1}円** × 件数 **{label2}件** × 成約率 **{pct_num}%**。<br>成約売上は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * val2 * pct_val
            
            if MIN_LIMIT <= correct_val <= MAX_LIMIT: 
                break

        options = []
        options.append(correct_val)
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
            "raw_val1": val1, "raw_val2": val2, "raw_pct": pct_num
        }
        st.session_state.quiz_answered = False

    q = st.session_state.quiz_data
    
    # 問題カード表示 (CSSクラス適用)
    st.markdown(f"""
    <div class="css-card">
        <h3 style="margin-top:0; color: #00F0FF; border:none;">>> QUERY_DATA</h3>
        <p style="font-size: 18px; line-height: 1.6; color: #EEE;">{q['q_text']}</p>
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

        ratio = user_val / correct_val if correct_val != 0 else 0
        is_correct = False
        
        if 0.99 <= ratio <= 1.01: 
            st.success("RESULT: [PASS] CORRECT")
            is_correct = True
        else:
            st.error(f"RESULT: [FAIL] TRUE_VAL = {format_japanese_answer(correct_val)}")
        
        st.info(f"CALC_LOG:\n{calc_str}")

        if st.button("NEXT_SEQ >>", type="primary"):
            if is_correct: st.session_state.score += 1
            next_question()
            st.rerun()

# ==========================================
# メイン
# ==========================================
def main():
    st.set_page_config(page_title="BizMath_Dojo", page_icon="📟")
    apply_custom_design() # ★CSS適用
    
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'current_q_idx' not in st.session_state:
        init_game_state()

    if st.session_state.page == "home":
        st.markdown("<h1 style='text-align: center; border:none;'>BIZ_MATH_DOJO <span style='font-size:0.5em; color:#FF0055;'>v2.0</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>NUMERIC SENSE OPTIMIZATION PROTOCOL</p>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(">> TRAINING_MODE")
            if st.button("INIT_TRAINING\n[INPUT]", use_container_width=True):
                init_game_state()
                st.session_state.page = "training"
                st.rerun()
            st.caption("SEQ: 10 | TOLERANCE: 20%")
        with col2:
            st.success(">> QUIZ_MODE")
            if st.button("INIT_SCENARIO\n[SELECT]", use_container_width=True):
                init_game_state()
                st.session_state.page = "quiz"
                st.rerun()
            st.caption("SEQ: 10 | TYPE: 4-CHOICE")

        st.write("")
        st.write("")
        st.markdown("---")
        st.subheader(">> REFERENCE_DATA")
        bk1, bk2 = st.columns(2)
        with bk1:
            st.markdown("SRC: **Fermi Estimation** ([LINK](https://amazon.co.jp))")
        with bk2:
            st.markdown("SRC: **Financial Analysis** ([LINK](https://amazon.co.jp))")

    elif st.session_state.page == "training":
        mode_training()
    elif st.session_state.page == "quiz":
        mode_quiz()

if __name__ == "__main__":
    main()
