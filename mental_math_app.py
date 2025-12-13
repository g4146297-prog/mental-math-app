import streamlit as st
import random

# ==========================================
# デザイン設定 (CSS) - 案B: フレンドリー＆ライト
# ==========================================
def apply_custom_design():
    # 案B: 白ベース & パステルカラー
    # 背景: アリスブルー / アクセント: ソフトブルー & コーラルピンク/オレンジ
    custom_css = """
    <style>
        /* 全体の背景色 */
        .stApp {
            background-color: #F0F8FF; /* 非常に薄い水色 */
            color: #576574; /* 柔らかいグレー */
        }
        
        /* ヘッダーの装飾 */
        h1, h2, h3 {
            color: #0984E3; /* 親しみやすいブルー */
            font-family: "Helvetica Neue", Arial, sans-serif;
            font-weight: 700;
        }
        
        /* ボタンのデザイン (プライマリー) - 丸みを帯びた形状 */
        div.stButton > button:first-child {
            background-color: #74B9FF; /* パステルブルー */
            color: white;
            border-radius: 30px; /* カプセル型 */
            border: none;
            box-shadow: 0 4px 10px rgba(116, 185, 255, 0.3);
            font-weight: bold;
            padding: 0.5rem 1.5rem;
            transition: all 0.2s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #0984E3;
            transform: scale(1.03);
            box-shadow: 0 6px 15px rgba(9, 132, 227, 0.3);
        }
        
        /* 通常ボタン (セカンダリー) */
        div.stButton > button:nth-child(2) {
            background-color: #FFFFFF;
            color: #74B9FF;
            border: 2px solid #74B9FF;
            border-radius: 30px;
        }
        div.stButton > button:nth-child(2):hover {
            background-color: #F0F8FF;
        }

        /* メトリクス (数字表示) - 温かみのある色 */
        [data-testid="stMetricValue"] {
            color: #FF7675; /* パステルコーラル/オレンジ */
            font-family: sans-serif;
            font-weight: 800;
        }
        [data-testid="stMetricLabel"] {
            color: #B2BEC3;
        }

        /* カード風コンテナ (ポップで浮いている感じ) */
        .css-card {
            background-color: #FFFFFF;
            padding: 25px;
            border-radius: 20px; /* 角丸を大きく */
            box-shadow: 0 10px 25px rgba(0,0,0,0.05); /* ふわっとした影 */
            margin-bottom: 20px;
            border: 2px solid #E1E8EE;
        }
        
        /* info/successボックスのカスタマイズ */
        .stAlert {
            background-color: #FFFFFF;
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        /* プログレスバー */
        .stProgress > div > div > div > div {
            background-color: #FF7675; /* コーラルピンクで進捗表示 */
            border-radius: 10px;
        }
        
        /* キャプション */
        .stCaption {
            color: #636E72;
            font-weight: 500;
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
    st.markdown("## 💪 概算入力トレーニング")
    
    if st.session_state.game_finished:
        # リザルトカード
        st.markdown(f"""
        <div class="css-card" style="text-align: center;">
            <h3 style="color: #0984E3;">Good Job!</h3>
            <p style="font-size: 24px; color: #636E72;">SCORE: <span style="color: #FF7675; font-weight: bold; font-size: 32px;">{st.session_state.score}</span> / {TOTAL_QUESTIONS}</p>
        </div>
        """, unsafe_allow_html=True)
        
        rate = st.session_state.score
        if rate >= 9:
            st.success("🏆 評価: S (神レベル) - すごい！完璧です！")
        elif rate >= 7:
            st.info("🥇 評価: A (上級者) - さすがです！")
        elif rate >= 4:
            st.warning("🥈 評価: B (普通) - いい感じです！")
        else:
            st.error("🥉 評価: C (修行中) - ドンマイ！次いこう！")
            
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
    # デザイン調整用コンテナ
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 0.5, 2])
    with c1: st.metric("数値 A", f"{st.session_state.train_num1:,}")
    with c2: st.markdown("<h2 style='text-align: center; color: #B2BEC3;'>×</h2>", unsafe_allow_html=True)
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
        st.markdown(f"**正解:** <span style='font-size: 20px; color: #FF7675;'>{format_japanese_answer(ans)}</span>", unsafe_allow_html=True)
        
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
# モード2：クイズ
# ==========================================
def mode_quiz():
    st.markdown("## 🧩 ビジネス概算クイズ")
    
    if st.session_state.game_finished:
        st.markdown(f"""
        <div class="css-card" style="text-align: center;">
            <h3 style="color: #0984E3;">Finished!</h3>
            <p style="font-size: 24px; color: #636E72;">SCORE: <span style="color: #FF7675; font-weight: bold; font-size: 32px;">{st.session_state.score}</span> / {TOTAL_QUESTIONS}</p>
        </div>
        """, unsafe_allow_html=True)

        rate = st.session_state.score
        if rate >= 9:
            st.success("🏆 評価: CEO級 - すばらしい経営感覚！")
        elif rate >= 7:
            st.info("🥇 評価: 部長級 - 安定してます！")
        elif rate >= 4:
            st.warning("🥈 評価: 課長級 - 基礎OKです！")
        else:
            st.error("🥉 評価: 新人級 - まだまだ伸びしろアリ！")
        
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
                    f"単価 **{label1}円** の商品が **{label2}個** 売れました。<br>売上はいくら？",
                    f"1人あたり **{label1}円** のコストがかかる研修に **{label2}人** が参加します。<br>総費用は？",
                    f"月商 **{label1}円** の店舗を **{label2}店舗** 運営しています。<br>全店の月商合計は？",
                    f"契約単価 **{label1}円** のサブスク会員が **{label2}人** います。<br>毎月の売上は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * val2
            elif pattern == 2:
                templates = [
                    f"売上高 **{label1}円** に対して、営業利益率は **{pct_num}%** です。<br>営業利益は？",
                    f"市場規模 **{label1}円** の業界で、シェア **{pct_num}%** を獲得しました。<br>自社の売上は？",
                    f"予算 **{label1}円** のうち、すでに **{pct_num}%** を消化しました。<br>消化した金額は？",
                    f"投資額 **{label1}円** に対して、リターン（利回り）が **{pct_num}%** ありました。<br>利益額は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * pct_val
            elif pattern == 3:
                templates = [
                    f"単価 **{label1}円** の商品を **{label2}個** 販売し、利益率は **{pct_num}%** でした。<br>利益額は？",
                    f"客単価 **{label1}円** で **{label2}人** が来店し、原価率は **{pct_num}%** です。<br>原価の総額は？",
                    f"1件 **{label1}円** の案件が **{label2}件** あり、成約率は **{pct_num}%** でした。<br>成約による売上合計は？"
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
        <h3 style="margin-top:0; color: #0984E3;">Question</h3>
        <p style="font-size: 18px; line-height: 1.6; color: #2D3436;">{q['q_text']}</p>
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
        st.markdown("<h1 style='text-align: center; color: #0984E3;'>💼 ビジネス数字力道場</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #636E72;'>数字のセンスを磨く、<br>毎日の脳トレ習慣を始めましょう。</p>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("📊 ストイックに練習")
            if st.button("概算トレーニング\n(入力式)", use_container_width=True):
                init_game_state()
                st.session_state.page = "training"
                st.rerun()
            st.caption("10問集中チャレンジ！")
        with col2:
            st.success("🧩 ビジネス概算クイズ")
            if st.button("シナリオ形式\n(4択式)", use_container_width=True):
                init_game_state()
                st.session_state.page = "quiz"
                st.rerun()
            st.caption("4択サクサク実戦モード！")

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
        mode_quiz()

if __name__ == "__main__":
    main()
