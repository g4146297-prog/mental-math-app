import streamlit as st
import random

# ==========================================
# 定数設定
# ==========================================
MAX_LIMIT = 10**12  # 上限: 1兆
MIN_LIMIT = 100     # 下限: 100 (0や極小値を防ぐ)

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
    """「10億円」や「8千」のような表記と実数値を生成する"""
    # ベースの数字（10〜999）
    base = random.randint(10, 999) 
    
    # 単位の決定
    unit_type = random.choices(["", "万", "億"], weights=[1, 5, 4])[0]
    
    val = 0
    label = ""

    if unit_type == "億":
        val = base * (10**8)
        label = f"{base}億"
    elif unit_type == "万":
        val = base * (10**4)
        label = f"{base}万"
    else:
        val = base * 100 
        label = f"{base}00"
        
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

    # 問題生成ロジック
    if 'train_num1' not in st.session_state:
        st.session_state.train_num1 = 0
        st.session_state.train_num2 = 0
        st.session_state.train_active = False

    def generate_train_problem():
        # 条件（1兆以下）を満たすまで再抽選するループ
        while True:
            digit_range1 = random.randint(3, 9) # 桁数を少し調整
            digit_range2 = random.randint(2, 6)
            
            num1 = random.randint(10**(digit_range1-1), 10**digit_range1)
            num2 = random.randint(10**(digit_range2-1), 10**digit_range2)
            
            ans = num1 * num2
            
            # 1兆以下なら採用してループを抜ける
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
            
            st.write(f"正解: **{format_japanese_answer(ans)}** ({ans:,.0f})")
            
            if abs(diff_pct) <= 20:
                st.success(f"素晴らしい！ ズレは {diff_pct:.1f}% です。")
            elif abs(diff_pct) > 100:
                st.error(f"桁が違います。 ズレ: {diff_pct:.1f}%")
            else:
                st.warning(f"おしい！ ズレ: {diff_pct:.1f}%")

# ==========================================
# モード2：新しいクイズ（4択・桁数問題）
# ==========================================
def mode_quiz():
    st.header("🧩 桁数直感クイズ")
    st.caption("正しい桁の答えを選んでください。")

    if st.button("トップに戻る"):
        st.session_state.page = "home"
        st.rerun()

    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
        st.session_state.quiz_answered = False

    # クイズ生成関数
    def generate_quiz():
        # ★修正ポイント: 条件（100以上 1兆以下）を満たすまで再抽選
        while True:
            pattern = random.choice([1, 2, 3])
            
            val1, label1 = generate_random_number_with_unit()
            val2, label2 = generate_random_number_with_unit()
            
            # 各要素単体でも1兆を超えていないか念のためチェック
            if val1 > MAX_LIMIT or val2 > MAX_LIMIT:
                continue

            pct_num = random.choice([10, 20, 30, 40, 50, 5, 15, 25])
            pct_val = pct_num / 100.0
            
            question_text = ""
            correct_val = 0
            
            if pattern == 1:
                label2 += random.choice(["個", "円", "人"])
                question_text = f"{label1} × {label2}"
                correct_val = val1 * val2
                
            elif pattern == 2:
                question_text = f"{label1}円 × {pct_num}%"
                correct_val = val1 * pct_val
                
            elif pattern == 3:
                label2 += "個"
                question_text = f"{label1}円 × {label2} × {pct_num}%"
                correct_val = val1 * val2 * pct_val
            
            # ★判定: 100以上 かつ 1兆以下 ならOK
            if MIN_LIMIT <= correct_val <= MAX_LIMIT: 
                break

        # 選択肢の生成
        options = []
        options.append(correct_val) # 正解
        options.append(correct_val * 10) # 1桁大きい
        options.append(correct_val / 10) # 1桁小さい
        
        # 4つ目の選択肢
        # 正解が100兆に近い(1兆ギリギリ)場合、100倍すると大きすぎるので1/100にするなど調整
        if correct_val * 100 > MAX_LIMIT * 10: # 許容範囲を超えるなら小さくする
            fourth_option = correct_val / 100
        else:
            fourth_option = random.choice([correct_val * 100, correct_val / 100])
            
        options.append(fourth_option)
        random.shuffle(options)
        
        st.session_state.quiz_data = {
            "q_text": question_text,
            "correct": correct_val,
            "options": options
        }
        st.session_state.quiz_answered = False

    if st.session_state.quiz_data is None:
        generate_quiz()

    q = st.session_state.quiz_data
    
    st.markdown("### 問題")
    st.markdown(f"## {q['q_text']} = ?")
    
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
        
        # 判定（桁ズレ比較）
        ratio = user_val / correct_val if correct_val != 0 else 0
        
        if 0.99 <= ratio <= 1.01: 
            st.success("🎉 正解！ お見事です。")
        else:
            st.error(f"❌ 残念... 正解は 「{format_japanese_answer(correct_val)}」 でした。")
            st.caption("桁の感覚を修正しましょう！")
            
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
            st.caption("以前からの機能です。正確な数字を入力して誤差を確認します。")

        with col2:
            st.success("🧩 クイズ形式で確認")
            if st.button("桁数直感クイズ\n(4択式)", use_container_width=True):
                st.session_state.page = "quiz"
                st.rerun()
            st.caption("新機能！「10億円×30%」などの計算結果を、正しい桁の選択肢から選びます。")

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
