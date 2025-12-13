import streamlit as st
import random

# --- 設定: 日本語の単位変換関数 (可読性向上のため) ---
def format_japanese_units(num):
    if num == 0:
        return "0"
    
    units = [
        (10**12, "兆"),
        (10**8, "億"),
        (10**4, "万"),
        (1, "")
    ]
    
    result = []
    remaining = num
    
    for unit_val, unit_name in units:
        if remaining >= unit_val:
            val = remaining // unit_val
            remaining %= unit_val
            result.append(f"{val:,}{unit_name}")
    
    return "".join(result)

# --- アプリのメインロジック ---
def main():
    st.title("💼 ビジネス概算力トレーニング")
    st.caption("正確さよりも「桁の感覚」と「規模感」を掴むための練習アプリです。")

    # セッション状態で問題を保持
    if 'num1' not in st.session_state:
        st.session_state.num1 = 0
        st.session_state.num2 = 0
        st.session_state.has_problem = False

    # 新しい問題を生成する関数
    def generate_problem():
        # ビジネスシーンを想定し、幅広い桁数からランダムに生成
        # 例: 単価(数千円) × 数量(数万個) や 予算(数十億円) × 係数 など
        # 1,000 〜 100億 の範囲でランダムな桁数を決定
        digit_range1 = random.randint(3, 10) # 10^3 ～ 10^10
        digit_range2 = random.randint(2, 6)  # 10^2 ～ 10^6
        
        st.session_state.num1 = random.randint(10**(digit_range1-1), 10**digit_range1)
        st.session_state.num2 = random.randint(10**(digit_range2-1), 10**digit_range2)
        
        # 解答欄をクリアするためにリラン
        st.session_state.user_input = 0.0
        st.session_state.has_problem = True

    # --- UI構成 ---
    
    # サイドバーで操作
    with st.sidebar:
        st.write("### コントロール")
        if st.button("新しい問題を出題", type="primary"):
            generate_problem()

    # 問題表示エリア
    if st.session_state.has_problem:
        st.markdown("### 【問題】 以下の掛け算の答えを概算してください")
        
        col1, col2, col3 = st.columns([2, 0.5, 2])
        with col1:
            st.metric(label="数値 A", value=f"{st.session_state.num1:,}")
        with col2:
            st.markdown("## ×")
        with col3:
            st.metric(label="数値 B", value=f"{st.session_state.num2:,}")

        st.divider()

        # 入力フォーム
        user_answer = st.number_input(
            "あなたの概算解答を入力してください（単位: 円/個など）", 
            value=0.0, 
            format="%.0f",
            step=10000.0,
            key="user_input_key"
        )

        # 解答ボタン
        if st.button("答え合わせ"):
            actual_answer = st.session_state.num1 * st.session_state.num2
            
            # 0除算回避
            if actual_answer == 0:
                diff_percent = 0
            else:
                diff_percent = ((user_answer - actual_answer) / actual_answer) * 100

            diff_amount = user_answer - actual_answer

            st.markdown("---")
            st.subheader("📊 結果分析")

            # 結果指標の表示
            res_col1, res_col2, res_col3 = st.columns(3)
            with res_col1:
                st.metric("正解 (数値)", f"{actual_answer:,.0f}")
                st.caption(f"読み: {format_japanese_units(actual_answer)}")
            with res_col2:
                # 色分け: 誤差が±10%以内ならNormal、それ以外はInverse(赤)など
                st.metric("乖離額", f"{diff_amount:+,.0f}")
            with res_col3:
                st.metric("乖離率", f"{diff_percent:+.2f}%", delta_color="inverse")

            # フィードバックメッセージ
            if abs(diff_percent) <= 10:
                st.success("素晴らしい感覚です！ビジネス実務レベルの概算です。")
            elif abs(diff_percent) <= 30:
                st.info("おしい！桁感覚は合っています。")
            elif abs(diff_percent) > 100:
                st.error("桁が違っている可能性があります。コンマの位置を確認しましょう。")
            else:
                st.warning("もう少し精度を上げましょう。")

            st.write(f"あなたの解答: {format_japanese_units(int(user_answer))}")

    else:
        st.info("サイドバーの「新しい問題を出題」ボタンを押してスタートしてください。")

if __name__ == "__main__":
    main()

st.divider()
    st.subheader("📚 おすすめの参考書")
    st.write("数字感覚をさらに磨くために、プロも読む書籍を紹介します。（※ここはAmazonアフィリエイトリンクなどを想定）")

    # カラムを分けて書籍を表示する例
    book_col1, book_col2 = st.columns(2)
    
    with book_col1:
        # 実際の画像やリンクはAmazonアソシエイトなどから取得します
        st.markdown("""
        **[仮] 外資系コンサルのフェルミ推定** こういう計算のプロであるコンサルタントの思考法が学べます。  
        [Amazonで見る >](https://www.amazon.co.jp)
        """)
        
    with book_col2:
        st.markdown("""
        **[仮] 決算書の読み方・作り方** 100兆円規模の企業の決算書を読み解く基礎体力がつきます。  
        [Amazonで見る >](https://www.amazon.co.jp)
        """)
