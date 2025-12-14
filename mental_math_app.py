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
            st.info(f"「{filter_mode}」のランキングはまだありません。")
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
    
    # 基礎編は単位付き、上級編はカンマ区切り
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
    elif pattern ==
