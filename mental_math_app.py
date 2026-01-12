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
MAX_LIMIT = 10**14
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
        .flashcard-q {
            font-size: 42px; 
            font-weight: bold; 
            color: #F8FAFC; 
            text-align: center;
            font-family: 'Consolas', 'Monaco', monospace;
            padding: 40px 0;
        }
        .flashcard-a {
            font-size: 42px; 
            font-weight: bold; 
            color: #FACC15; 
            text-align: center;
            padding: 20px 0;
            border-top: 1px dashed #334155;
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

    if filter_mode:
        df = df[df["mode"] == filter_mode]
        if df.empty:
            st.info(f"ランキングデータはまだありません。")
            return

    df = df.sort_values(by=["score", "duration"], ascending=[False, True]).reset_index(drop=True)
    
    display_df = df[["nickname", "score", "duration", "timestamp"]].copy()
    display_df["rank"] = display_df.index + 1
    display_df["duration"] = display_df["duration"].apply(lambda x: f"{int(x//60)}分{int(x%60)}秒")
    display_df.columns = ["ニックネーム", "スコア/正解数", "タイム", "日付", "順位"]
    display_df = display_df[["順位", "ニックネーム", "スコア/正解数", "タイム", "日付"]]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ==========================================
# 共通関数: 数値フォーマット・生成
# ==========================================
def format_japanese_answer(num):
    try:
        # 小数の場合は整数に丸める（概算なので）
        int_num = int(num)
    except:
        return str(num)
    if int_num == 0: return "0"
    
    sign = ""
    if int_num < 0:
        sign = "-"
        int_num = abs(int_num)

    units = [(10**12, "兆"), (10**8, "億"), (10**4, "万"), (1, "")]
    result = []
    remaining = int_num
    for unit_val, unit_name in units:
        if remaining >= unit_val:
            val = remaining // unit_val
            remaining %= unit_val
            result.append(f"{val:,}{unit_name}")
    
    return sign + "".join(result) if result else "0"

def format_number_with_unit_label(value):
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

def get_mental_math_tip(pattern):
    common_tips = [
        "💡 **コツ:** 数字の「0」を一旦無視して、ゼロ以外の数字同士を掛け算しましょう。最後に無視した0の個数を合計して付け足すと簡単です。",
        "💡 **コツ:** 「万」は0が4つ、「億」は0が8つです。単位を0に置き換えて桁数を整理してみましょう。",
        "💡 **コツ:** 概算の場合、有効数字（上1〜2桁）だけで計算し、あとは桁数を合わせるのがスピードアップの鍵です。",
        "💡 **コツ:** 3桁ごとのカンマ「,」の位置を意識しましょう。1,000(千)、1,000,000(百万)、1,000,000,000(十億)が区切りです。"
    ]
    pct_tips = [
        "💡 **コツ:** 10%は「桁を1つ減らす」、1%は「桁を2つ減らす」ことと同じです。これを基準に倍数で考えましょう。",
        "💡 **コツ:** 5%は「10%の半分」、20%は「10%の2倍」と考えると計算が早くなります。",
        "💡 **コツ:** ×0.5 (50%) は「半分にする（÷2）」、×0.25 (25%) は「半分の半分（÷4）」と同じです。",
        "💡 **コツ:** 「70%」などは「100% - 30%」と考えたほうが引き算で早く解ける場合があります。"
    ]
    fx_tips = [
        "💡 **コツ:** 為替計算（円貨→外貨）は「割り算」ですが、概算では「掛け算（逆数）」でアタリをつけるのが有効です。",
        "💡 **コツ:** 1ドル=150円の場合、「2ドル=300円」「10ドル=1500円」と基準を作っておくと早いです。",
        "💡 **コツ:** 1円に近いレートの通貨（タカなど）は、そのまま日本円と同じ感覚で、最後に係数（1.2など）を掛けると楽です。",
        "💡 **コツ:** ユーロやポンドなど高い通貨は、ドルよりも「少し高い」という感覚で補正しましょう。"
    ]
    
    if pattern in [2, 3]: return random.choice(common_tips + pct_tips)
    elif pattern in [5, 6]: return random.choice(common_tips + fx_tips)
    else: return random.choice(common_tips)

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
    { "pattern": 4, "template": "新規事業のPL計画。年間固定費 <b>{label1}円</b> が <b>{label2}</b> かかる見通しです。<br>固定費の総額は？", "range1": (5000000, 500000000), "range2": (2, 5), "suffix2": "年", "unit1":"円", "unit2":"年間" },
    
    # --- パターン5: 為替 (外貨 -> 円) ---
    { "pattern": 5, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>現地売上 <b>{label1}{currency}</b> は日本円でいくら？", "currency": "ドル", "rate_range": (130, 160), "range1": (1000, 1000000), "unit1": "ドル", "unit2": "円/ドル" },
    { "pattern": 5, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>輸入コスト <b>{label1}{currency}</b> は日本円でいくら？", "currency": "ユーロ", "rate_range": (140, 170), "range1": (1000, 500000), "unit1": "ユーロ", "unit2": "円/ユーロ" },
    { "pattern": 5, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>ロンドン支社の利益 <b>{label1}{currency}</b> は日本円でいくら？", "currency": "ポンド", "rate_range": (180, 210), "range1": (1000, 100000), "unit1": "ポンド", "unit2": "円/ポンド" },
    { "pattern": 5, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>資源購入費 <b>{label1}{currency}</b> は日本円でいくら？", "currency": "豪ドル", "rate_range": (90, 110), "range1": (10000, 1000000), "unit1": "豪ドル", "unit2": "円/豪ドル" },
    { "pattern": 5, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>中国工場のコスト <b>{label1}{currency}</b> は日本円でいくら？", "currency": "元", "rate_range": (19, 23), "range1": (10000, 5000000), "unit1": "元", "unit2": "円/元" },
    # 追加: タイ、バングラデシュ、ブラジル
    { "pattern": 5, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>バンコク支店の売上 <b>{label1}{currency}</b> は日本円でいくら？", "currency": "バーツ", "rate_range": (4.0, 5.0), "range1": (10000, 10000000), "unit1": "バーツ", "unit2": "円/バーツ" },
    { "pattern": 5, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>ダッカ工場の経費 <b>{label1}{currency}</b> は日本円でいくら？", "currency": "タカ", "rate_range": (1.1, 1.4), "range1": (100000, 50000000), "unit1": "タカ", "unit2": "円/タカ" },
    { "pattern": 5, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>サンパウロでの調達費 <b>{label1}{currency}</b> は日本円でいくら？", "currency": "レアル", "rate_range": (20, 30), "range1": (5000, 500000), "unit1": "レアル", "unit2": "円/レアル" },

    # --- パターン6: 為替 (円 -> 外貨) ---
    { "pattern": 6, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>予算 <b>{label1}円</b> は約何{currency}？", "currency": "ドル", "rate_range": (130, 160), "range1": (1000000, 100000000), "unit1": "円", "unit2": "円/ドル" },
    { "pattern": 6, "template": "為替レートが 1{currency} = <b>{rate}円</b> のとき、<br>手持ち資金 <b>{label1}円</b> は約何{currency}？", "currency": "ユーロ", "rate_range": (140, 170), "range1": (1000000, 50000000), "unit1": "円", "unit2": "円/ユーロ" }
]

def generate_question_data(is_advanced=False, force_pattern=None, simple_amounts=None, simple_pct=None):
    if simple_amounts is None: simple_amounts = not is_advanced
    if simple_pct is None: simple_pct = not is_advanced

    if force_pattern:
        candidates = [s for s in SCENARIOS if s['pattern'] == force_pattern]
    else:
        # 上級編では全パターン、基礎編ではパターン1,2,4,5から選択
        if is_advanced:
            candidates = SCENARIOS
        else:
            candidates = [s for s in SCENARIOS if s['pattern'] in [1, 2, 4, 5]]
        
    scenario = random.choice(candidates)
    pattern = scenario['pattern']
    
    val1 = get_random_val(scenario['range1'][0], scenario['range1'][1], simple=simple_amounts)
    val2 = 1
    pct = 0
    
    # 為替レート (val2として使用)
    if 'rate_range' in scenario:
        min_r, max_r = scenario['rate_range']
        # 範囲が小数の場合または値が小さい場合は小数レートも許容
        if isinstance(min_r, float) or isinstance(max_r, float) or max_r < 10:
             val2 = round(random.uniform(min_r, max_r), 2)
             # simpleモードなら小数第一位までにする
             if simple_amounts:
                 val2 = round(val2, 1)
        else:
            if simple_amounts:
                # 5刻みなどに丸める (範囲が狭い場合は1刻み)
                step = 5
                if max_r - min_r < step: step = 1
                val2 = random.choice(list(range(min_r, max_r+1, step)))
            else:
                val2 = random.randint(min_r, max_r)
    elif 'range2' in scenario:
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
    elif pattern in [5, 6]: # 為替レート
        label2 = f"{val2}"
        
    correct_val = 0
    q_currency = scenario.get('currency', '')
    
    if pattern == 1: correct_val = val1 * val2
    elif pattern == 2: correct_val = val1 * (pct / 100.0)
    elif pattern == 3: correct_val = val1 * val2 * (pct / 100.0)
    elif pattern == 4: correct_val = val1 * val2
    elif pattern == 5: # 外貨 -> 円 (掛け算)
        correct_val = val1 * val2
    elif pattern == 6: # 円 -> 外貨 (割り算)
        correct_val = int(val1 / val2)

    q_text = scenario['template'].format(label1=label1, label2=label2, pct=pct, rate=val2, currency=q_currency)
    
    unit1 = scenario.get('unit1', '')
    unit2 = scenario.get('unit2', '')
    if pattern == 4: unit2 = suffix2
    if pattern == 5: unit2 = f"円/{q_currency}"
    if pattern == 6: 
        unit1 = "円"
        unit2 = f"円/{q_currency}"
    
    correct_unit = "円"
    if pattern == 6: correct_unit = q_currency
    
    return {
        "q_text": q_text,
        "correct": correct_val,
        "pattern": pattern,
        "raw_val1": val1, "raw_val2": val2, "raw_pct": pct,
        "unit1": unit1, "unit2": unit2,
        "correct_unit": correct_unit,
        "is_advanced": is_advanced
    }

# ==========================================
# フラッシュカード用データ生成
# ==========================================
def generate_flashcard_data():
    if 'flash_history' not in st.session_state:
        st.session_state.flash_history = []

    while True:
        p1 = random.randint(2, 10) 
        p2 = random.randint(2, 10) 
        
        if p1 + p2 > 13: 
            continue
            
        val1 = 10**p1
        val2 = 10**p2
        
        def to_label(v):
            if v >= 10**8:
                if v % 10**8 == 0: return f"{v//10**8}億"
                else: return f"{v//10**8}億{v%10**8}..."
            elif v >= 10**4:
                if v % 10**4 == 0: return f"{v//10**4}万"
            return f"{v:,}"
            
        l1 = to_label(val1)
        l2 = to_label(val2)
        q_text = f"{l1} × {l2}"
        
        if q_text in st.session_state.flash_history:
            continue
            
        st.session_state.flash_history.append(q_text)
        if len(st.session_state.flash_history) > 10:
            st.session_state.flash_history.pop(0)
            
        return {
            "q_text": q_text,
            "correct": val1 * val2
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
    st.session_state.flash_state = "question"

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

    st.markdown("---")
    st.write("### 📝 結果詳細")
    for h in st.session_state.history:
        label = h['result_label']
        color = '#FACC15' if ('⭕' in label or '点' in label and int(label.replace('点',''))>=8) else '#EF4444'
        st.markdown(f"""
        <div class="history-row">
            <span style="color:{color}; font-weight:bold; margin-right:10px; min-width:50px;">{label}</span>
            <span style="color:#E2E8F0; margin-right:15px; flex-grow:1;">{h['formula_kanji']}</span>
            <span style="color:#38BDF8; font-family:monospace;">{h['time']:.1f}s</span>
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
            # 上級: 後半は難しいパターン
            if st.session_state.current_q_idx > 6: 
                # パターン3(3要素)か6(割り算)
                force_p = random.choice([3, 6])
        else:
            # 基礎: パターン3, 6は出さない
            while True:
                temp_q = generate_question_data(is_advanced=False)
                if temp_q['pattern'] not in [3, 6]:
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
    
    unit_label = "円"
    if q.get('correct_unit'):
        unit_label = q['correct_unit']
    
    user_ans = st.number_input(
        f"概算解答を入力 ({unit_label})", 
        value=0, step=1, format="%d",
        key=f"train_ans_{st.session_state.current_q_idx}"
    )
    
    if user_ans > 0:
        st.markdown(f"<p style='color:#FACC15; font-weight:bold;'>入力プレビュー: {user_ans:,} {unit_label}</p>", unsafe_allow_html=True)
    
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
        c_unit = q.get('correct_unit', '円')
        
        calc_str_arabic = ""
        if pattern_used == 1: calc_str_arabic = f"{v1:,} × {v2:,} = {correct_val:,.0f}"
        elif pattern_used == 2: calc_str_arabic = f"{v1:,} × {pct}% = {correct_val:,.0f}"
        elif pattern_used == 3: calc_str_arabic = f"{v1:,} × {v2:,} × {pct}% = {correct_val:,.0f}"
        elif pattern_used == 4: calc_str_arabic = f"{v1:,} × {v2} = {correct_val:,.0f}"
        elif pattern_used == 5: calc_str_arabic = f"{v1:,} × {v2:,} = {correct_val:,.0f}"
        elif pattern_used == 6: calc_str_arabic = f"{v1:,} ÷ {v2:,} = {correct_val:,.0f}"

        f_v1 = format_japanese_answer(v1) + u1
        f_ans = format_japanese_answer(correct_val) + c_unit
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
        elif pattern_used == 5: # 外貨->円
            calc_str_kanji = f"{f_v1} × {v2}円 ＝ {f_ans}"
        elif pattern_used == 6: # 円->外貨
            calc_str_kanji = f"{f_v1} ÷ {v2}円 ＝ {f_ans}"

        points, diff_pct, is_perfect = calculate_score(user_ans, correct_val)
        
        if len(st.session_state.history) < st.session_state.current_q_idx:
            st.session_state.history.append({
                "result_label": f"{points}点",
                "points": points,
                "formula_kanji": calc_str_kanji,
                "time": st.session_state.current_q_time
            })

        st.markdown(f"あなたの回答: **{user_ans:,}** {c_unit}")
        st.info(f"🧮 計算イメージ: {calc_str_arabic}")
        st.markdown(f"**正解:** <span style='font-size: 20px; color: #FACC15;'>{format_japanese_answer(correct_val)}</span>{c_unit} <span style='font-size: 14px; color: #888;'>({correct_val:,})</span>", unsafe_allow_html=True)
        
        if is_perfect:
            st.markdown(f"<div style='background-color:rgba(250, 204, 21, 0.2); padding:10px; border-radius:5px; text-align:center; color:#FACC15; font-weight:bold; margin-bottom:10px;'>🏆 ピタリ賞！ 獲得ポイント: {points}点</div>", unsafe_allow_html=True)
        elif points >= 8:
            st.success(f"⭕ 素晴らしい！ 獲得ポイント: {points}点 (ズレ: {diff_pct:.2f}%)")
        elif points >= 1:
            st.warning(f"🔺 まずまず！ 獲得ポイント: {points}点 (ズレ: {diff_pct:.2f}%)")
        else:
            st.error(f"❌ 残念... 獲得ポイント: {points}点 (ズレ: {diff_pct:.2f}%)")
            st.info(get_mental_math_tip(pattern_used))

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
            # 上級: 後半は難しいパターン
            if st.session_state.current_q_idx > 6:
                force_p = random.choice([3, 6])
        else:
            # 基礎: パターン3, 6は出さない
            while True:
                temp_q = generate_question_data(is_advanced=False)
                if temp_q['pattern'] not in [3, 6]:
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
                options.append(int(correct * m)) # 整数丸め
        else:
            if q['pattern'] == 2:
                options.extend([int(correct * 0.8), int(correct * 1.2), int(correct * 1.5)])
            else:
                options.append(int(correct * 10))
                options.append(int(correct / 10))
                rnd = int(correct * 2) if correct > 0 else 1
                options.append(rnd)

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
            # 答えの単位
            unit = q.get('correct_unit', '')
            if unit == '円':
                btn_label = format_japanese_answer(opt) + unit
            else:
                btn_label = f"{opt:,} {unit}"

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
        c_unit = q.get('correct_unit', '円')
        
        calc_str_arabic = ""
        if pat == 1: calc_str_arabic = f"{v1:,} × {v2:,} = {correct_val:,.0f}"
        elif pat == 2: calc_str_arabic = f"{v1:,} × {pct}% = {correct_val:,.0f}"
        elif pat == 3: calc_str_arabic = f"{v1:,} × {v2:,} × {pct}% = {correct_val:,.0f}"
        elif pat == 4: calc_str_arabic = f"{v1:,} × {v2} = {correct_val:,.0f}"
        elif pat == 5: calc_str_arabic = f"{v1:,} × {v2:,} = {correct_val:,.0f}"
        elif pat == 6: calc_str_arabic = f"{v1:,} ÷ {v2:,} = {correct_val:,.0f}"

        f_v1 = format_japanese_answer(v1) + u1
        f_ans = format_japanese_answer(correct_val) + c_unit
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
        elif pat == 5: 
            calc_str_kanji = f"{f_v1} × {v2}円 ＝ {f_ans}"
        elif pat == 6: 
            calc_str_kanji = f"{f_v1} ÷ {v2}円 ＝ {f_ans}"

        ratio = user_val / correct_val if correct_val != 0 else 0
        is_correct = (0.99 <= ratio <= 1.01)
        
        if len(st.session_state.history) < st.session_state.current_q_idx:
            st.session_state.history.append({
                "is_correct": is_correct,
                "result_label": "⭕" if is_correct else "❌",
                "formula_kanji": calc_str_kanji,
                "time": st.session_state.current_q_time
            })
        
        if is_correct: 
            st.success("🎉 正解！")
        else:
            st.error(f"❌ 不正解... 正解は 「{format_japanese_answer(correct_val)}」")
            st.info(get_mental_math_tip(pat))
        
        st.info(f"🧮 計算イメージ: {calc_str_arabic}")

        if st.button("次の問題へ", type="primary"):
            if is_correct: st.session_state.score += 1
            next_question()
            st.rerun()

# ==========================================
# モード3: フラッシュカード (桁感特訓)
# ==========================================
def mode_flashcard():
    st.markdown("## ⚡ フラッシュカード（桁感特訓）")
    
    if st.button("トップに戻る"):
        st.session_state.page = "home"
        st.rerun()
        
    st.caption("エンドレスモード: タップして次々と答えを確認しましょう。")

    if st.session_state.quiz_data is None:
        st.session_state.quiz_data = generate_flashcard_data()
        st.session_state.flash_state = "question"

    q = st.session_state.quiz_data

    st.markdown(f"""
    <div class="css-card">
        <div class="flashcard-q">{q['q_text']}</div>
        {"<div class='flashcard-a'>" + format_japanese_answer(q['correct']) + "</div>" if st.session_state.flash_state == "answer" else ""}
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.flash_state == "question":
        if st.button("答えを見る", type="primary", use_container_width=True):
            st.session_state.flash_state = "answer"
            st.rerun()
    else:
        if st.button("次の問題へ", type="primary", use_container_width=True):
            st.session_state.quiz_data = None
            st.session_state.flash_state = "question"
            st.rerun()

# ==========================================
# モード4: 暗算のTips集
# ==========================================
def mode_tips():
    st.markdown("## 💡 暗算・概算のコツ")
    
    if st.button("トップに戻る"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown("---")

    st.markdown("### 1. 桁数と「0」の数")
    st.info("""
    大きな数字の計算では、まず「0」の数を把握することが基本です。
    
    * **万**: 0が **4つ** (10,000)
    * **億**: 0が **8つ** (100,000,000)
    * **兆**: 0が **12個** (1,000,000,000,000)
    
    例: **300万 × 50万** の場合
    1. 数字部分: 3 × 5 = 15
    2. 0の数: 「万(4つ)」＋「万(4つ)」＋ 300の0(2つ) ＋ 50の0(1つ) = 合計11個
    3. 11個の0は「億(8つ)」と「000」
    4. 答え: **1兆5000億**
    """)

    st.markdown("### 2. パーセント計算の近道")
    st.success("""
    パーセント計算は「基準となる数字」から推測すると早いです。
    
    * **10%**: 桁を1つ減らす（÷10）
    * **1%**: 桁を2つ減らす（÷100）
    * **5%**: 「10%」の半分
    * **20%**: 「10%」の2倍
    * **50%**: 半分にする（÷2）
    * **25%**: 半分の半分にする（÷4）
    
    例: **1200万円の 15%**
    * 10% = 120万円
    * 5% = 60万円（120万の半分）
    * 合計 = 180万円
    """)

    st.markdown("### 3. ビジネス概算の極意")
    st.warning("""
    ビジネスの現場では、1円単位の正確さよりも「桁が合っているか」「大まかな規模感は正しいか」が重要視されます。
    
    * **上2桁で計算する**: 「1,234,567円」は「120万円」として計算しても、概算としては十分です。
    * **カンマを意識する**: 「,」は3桁ごとに打たれます。千、百万、十億の位置を視覚的に覚えましょう。
    """)

    st.markdown("---")
    if st.button("トップに戻る", key="back_bottom"):
        st.session_state.page = "home"
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

        if st.button("⚡ フラッシュカード（桁感特訓）", use_container_width=True):
            init_game_state()
            st.session_state.page = "flashcard"
            st.rerun()
        st.caption("「100×1万」など、0の数を瞬時に把握するエンドレスモード。")
        
        if st.button("💡 暗算のコツ (Tips)", use_container_width=True):
            st.session_state.page = "tips"
            st.rerun()

        st.write("")
        st.markdown("---")
        st.subheader("🏆 最新ランキング")
        
        tab1, tab2, tab3, tab4 = st.tabs(["お気軽(基礎)", "お気軽(上級)", "チャレンジ(基礎)", "チャレンジ(上級)"])
        
        with tab1:
            display_ranking("お気軽(基礎)")
        with tab2:
            display_ranking("お気軽(上級)")
        with tab3:
            display_ranking("チャレンジ(基礎)")
        with tab4:
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
    elif st.session_state.page == "flashcard":
        mode_flashcard()
    elif st.session_state.page == "tips":
        mode_tips()

if __name__ == "__main__":
    main()
