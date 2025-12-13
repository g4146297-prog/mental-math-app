import streamlit as st
import random

# ==========================================
# 定数設定
# ==========================================
MAX_LIMIT = 10**12  # 上限: 1兆
MIN_LIMIT = 100     # 下限: 100

# ==========================================
# 共通関数：数値のフォーマットなど
# ==========================================
def format_japanese_answer(num):
    """解答表示用のフォーマット（例: 1兆2000億円）"""
    int_num = int(num)
    
    if int_num == 0:
        return "0"
        
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
    """「10億」や「3,000万」のような表記と実数値を生成する（単位文字はつけない）"""
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

# ==========================================
# モード1：従来のトレーニング（入力式）
# ==========================================
def mode_training():
    st.header("💪 概算入力トレーニング")
    st.caption("桁の感覚を養うため、計算結果の数値を入力してください。")
    
    if st.button("トップに戻る"):
        st.session_state.page = "home"
        st.rerun()

    if 'train_num1' not in st.session_state:
        st.session_state.train_num1 = 0
        st.session_state.train_num2 = 0
        st.session_state.train_active = False

    def generate_train_problem():
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

    if st.button("新しい問題を出題", type="primary"):
        generate_train_problem()

    if st.session_state.train_active:
        st.markdown("### 【問題】")
        c1, c2, c3 = st.columns([2, 0.5, 2])
        with c1: st.metric("数値 A", f"{st.session_state.train_num1:,}")
        with c2: st.markdown("## ×")
        with c3: st.metric("数値 B", f"{st.session_state.train_num2:,}")
        
        st.divider()
        user_ans = st.number_input("概算解答を入力", value=0.0, step=10000.0, format="%.0f")
        
        if st.button("答え合わせ"):
            ans = st.session_state.train_num1 * st.session_state.train_num2
            diff_pct = ((user_ans - ans) / ans * 100) if ans != 0 else 0
            
            # トレーニングモードでも計算過程を表示
            st.info(f"🧮 計算イメージ: {st.session_state.train_num1:,.0f} × {st.session_state.train_num2:,.0f} = {ans:,.0f}")
            
            st.write(f"正解: **{format_japanese_answer(ans)}**")
            
            if abs(diff_pct) <= 20:
                st.success(f"素晴らしい！ ズレは {diff_pct:.1f}% です。")
            elif abs(diff_pct) > 100:
                st.error(f"桁が違います。 ズレ: {diff_pct:.1f}%")
            else:
                st.warning(f"おしい！ ズレ: {diff_pct:.1f}%")

# ==========================================
# モード2：新しいクイズ（4択・ビジネス文章問題）
# ==========================================
def mode_quiz():
    st.header("🧩 ビジネス概算クイズ")
    st.caption("表示されるビジネスシーンの数字を概算し、正しい答えを選んでください。")

    if st.button("トップに戻る"):
        st.session_state.page = "home"
        st.rerun()

    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
        st.session_state.quiz_answered = False

    def generate_quiz():
        while True:
            pattern = random.choice([1, 2, 3])
            
            val1, label1 = generate_random_number_with_unit()
            val2, label2 = generate_random_number_with_unit()
            
            if val1 > MAX_LIMIT or val2 > MAX_LIMIT:
                continue

            pct_num = random.choice([10, 20, 30, 40, 50, 5, 15, 25])
            pct_val = pct_num / 100.0
            
            question_text = ""
            correct_val = 0
            
            # --- ビジネス文章のテンプレート ---
            if pattern == 1:
                templates = [
                    f"単価 **{label1}円** の商品が **{label2}個** 売れました。売上はいくら？",
                    f"1人あたり **{label1}円** のコストがかかる研修に **{label2}人** が参加します。総費用は？",
                    f"月商 **{label1}円** の店舗を **{label2}店舗** 運営しています。全店の月商合計は？",
                    f"契約単価 **{label1}円** のサブスク会員が **{label2}人** います。毎月の売上は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * val2
                
            elif pattern == 2:
                templates = [
                    f"売上高 **{label1}円** に対して、営業利益率は **{pct_num}%** です。営業利益は？",
                    f"市場規模 **{label1}円** の業界で、シェア **{pct_num}%** を獲得しました。自社の売上は？",
                    f"予算 **{label1}円** のうち、すでに **{pct_num}%** を消化しました。消化した金額は？",
                    f"投資額 **{label1}円** に対して、リターン（利回り）が **{pct_num}%** ありました。利益額は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * pct_val
                
            elif pattern == 3:
                templates = [
                    f"単価 **{label1}円** の商品を **{label2}個** 販売し、利益率は **{pct_num}%** でした。利益額は？",
                    f"客単価 **{label1}円** で **{label2}人** が来店し、原価率は **{pct_num}%** です。原価の総額は？",
                    f"1件 **{label1}円** の案件が **{label2}件** あり、成約率は **{pct_num}%** でした。成約による売上合計は？"
                ]
                question_text = random.choice(templates)
                correct_val = val1 * val2 * pct_val
            
            # 条件チェック
            if MIN_LIMIT <= correct_val <= MAX_LIMIT: 
                break

        # --- 選択肢の生成ロジック ---
        options = []
        options.append(correct_val) # 正解

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
        
        # ★修正：計算過程表示のために生の値を保存しておく
        st.session_state.quiz_data = {
            "q_text": question_text,
            "correct": correct_val,
            "options": options,
            "pattern": pattern,
            "raw_val1": val1,
            "raw_val2": val2,
            "raw_pct": pct_num
        }
        st.session_state.quiz_answered = False

    if st.session_state.quiz_data is None:
        generate_quiz()

    q = st.session_state.quiz_data
    
    st.markdown("### 問題")
    st.markdown(f"##### {q['q_text']}")
    
    st.write("")

    if not st.session_state.quiz_answered:
        col1, col2 = st.columns(2)
        for i, opt in enumerate(q['options']):
            btn_label = format_japanese_answer(opt)
            target_col = col1 if i % 2 == 0 else col2
            
            if target_col.button(f"{btn_label}", key=f"opt_{i}", use_container_width=True):
                st.session_state.quiz_answered = True
                st.session_state.user_choice = opt
                st.rerun()
    
    else:
        user_val = st.session_state.user_choice
        correct_val = q['correct']
        pattern_used = q.get('pattern', 1)
        
        # --- ★追加：計算過程の文字列作成 ---
        calc_str = ""
        v1 = q['raw_val1']
        v2 = q['raw_val2']
        pct = q['raw_pct']
        
        if pattern_used == 1:
            calc_str = f"{v1:,.0f} × {v2:,.0f} = {correct_val:,.0f}"
        elif pattern_used == 2:
            calc_str = f"{v1:,.0f} × {pct}% = {correct_val:,.0f}"
        elif pattern_used == 3:
            calc_str = f"{v1:,.0f} × {v2:,.0f} × {pct}% = {correct_val:,.0f}"

        # 判定
        ratio = user_val / correct_val if correct_val != 0 else 0
        
        if 0.99 <= ratio <= 1.01: 
            st.success("🎉 正解！ お見事です。")
        else:
            st.error(f"❌ 残念... 正解は 「{format_japanese_answer(correct_val)}」 でした。")
        
        # 計算過程を表示（アラビア数字のみ）
        st.info(f"🧮 計算イメージ:\n{calc_str}")

        if st.button("次の問題へ", type="primary"):
            generate_quiz()
            st.rerun()

# ==========================================
# トップページ
# ==========================================
def main():
    st.set_page_config(page_title="ビジネス数字力道場", page_icon="💼")
    
    if 'page' not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.title("💼 ビジネス数字力道場")
        st.markdown("ビジネスに必要な「数字の規模感」と「暗算力」を鍛えるアプリです。")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📊 ストイックに練習")
            if st.button("概算トレーニング\n(入力式)", use_container_width=True):
                st.session_state.page = "training"
                st.rerun()
            st.caption("単純な計算式で、桁の感覚と入力精度を鍛えます。")

        with col2:
            st.success("🧩 ビジネス概算クイズ")
            if st.button("シナリオ形式\n(4択式)", use_container_width=True):
                st.session_state.page = "quiz"
                st.rerun()
            st.caption("「売上」「コスト」「利益」などの具体的シーンで概算力を試します。")

        st.divider()
        st.subheader("📚 おすすめの学習資料")
        st.write("フェルミ推定や計数感覚を養うための書籍です。")
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
