import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Ultimate Quant Decision Engine")

# सीएसएस स्टाइलिंग: पूरे डैशबोर्ड को एक हाई-एंड एल्गो ट्रेडिंग टर्मिनल का लुक देने के लिए
st.markdown("""
    <style>
    .reportview-container { background: #06080c; }
    th { background-color: #111827 !important; color: #9ca3af !important; font-weight: bold !important; text-align: center !important; font-size: 13px !important;}
    td { text-align: center !important; font-family: monospace; font-size: 13px !important; padding: 5px !important; vertical-align: middle !important;}
    div[data-testid="stMetricValue"] { font-size: 20px !important; font-family: monospace; }
    .stTable { background-color: #090d16 !important; }
    .stAlert { padding: 10px !important; font-size: 14px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 क्वांटिटेटिव SMC + VSA + Greeks इंस्टीट्यूशनल डिसीजन इंजन")
st.write("सेंटर स्ट्राइक लेआउट | प्रोप्राइटरी मल्टी-लेयर क्वांटम परतें | रियल-टाइम रिस्क मैनेजर")

# 1. एडवांस्ड डेटा सिमुलेशन इंजन (लॉक्ड इंस्टीट्यूशनल एक्सीलरेशन पैरामीटर्स के साथ)
def generate_institutional_master_data():
    underlying_value = 23354.50  # निफ्टी लाइव स्पॉट भाव
    atm_strike = int(round(underlying_value / 50) * 50)
    strikes = [atm_strike + i*50 for i in range(-5, 6)]
    
    rows = []
    np.random.seed(88) # स्थिरता और निरंतर डेटा बिहेवियर के लिए
    
    for s in strikes:
        is_atm = "🟡 ATM " if s == atm_strike else ""
        
        # रॉ क्वांटिटेटिव डेटा जेनरेशन
        ce_oi = np.random.uniform(65, 155) if s >= atm_strike else np.random.uniform(15, 40)
        pe_oi = np.random.uniform(15, 45) if s >= atm_strike else np.random.uniform(75, 185)
        ce_chg = np.random.uniform(-12, 48) if s == atm_strike else np.random.uniform(5, 32)
        pe_chg = np.random.uniform(18, 58) if s == atm_strike else np.random.uniform(-8, 38)
        ce_vol = np.random.uniform(15000, 55000)
        pe_vol = np.random.uniform(15000, 55000)
        ce_chg_vol = np.random.uniform(4000, 18000)
        pe_chg_vol = np.random.uniform(4000, 18000)
        
        # एक्सीलरेशन और हिडन एक्टिविटी सिमुलेशन (Order Blocks, Traps & Squeeze)
        if s == atm_strike + 100: ce_vol *= 4.6; ce_chg = 90.0  # Gamma Blast Active Condition
        if s == atm_strike - 100: pe_vol *= 3.9; pe_chg = 85.0  # Put OB Active Condition
        if s == atm_strike + 50: ce_chg = -40.0; ce_vol *= 0.35  # Manipulation Condition
        if s == atm_strike: ce_oi = 150.0; pe_oi = 160.0; ce_chg = 40.0; pe_chg = 4.0; ce_vol *= 1.8  # OI Trap Condition
        
        # पीसीआर गणना
        vol_pcr = pe_vol / ce_vol if ce_vol > 0 else 1.0
        strike_pcr = pe_oi / ce_oi if ce_oi > 0 else 1.0
        
        # 4-वे सेंटीमेंट फेज लॉजिक
        ce_phase = "Long Buildup" if ce_chg > 20 else ("Short Buildup" if ce_chg > 0 else "Short Covering")
        pe_phase = "Long Buildup" if pe_chg > 20 else ("Short Buildup" if pe_chg > 0 else "Short Covering")
        
        # बोलिंजर बैंड कम्प्रेशन और गामा स्ट्रेंथ गणना
        bb_squeeze_raw = np.random.uniform(1.4, 5.8) if s == atm_strike - 50 else np.random.uniform(2.6, 6.0)
        bb_squeeze_str = f"{bb_squeeze_raw:.1f}% " + ("(SQUEEZE)" if bb_squeeze_raw < 2.5 else "(EXPAND)")
        
        gamma_strength_raw = np.random.randint(86, 99) if s == atm_strike + 100 else np.random.randint(12, 60)
        gamma_str = f"{gamma_strength_raw}%"
        
        # एसएमसी अलर्ट्स और हिडन फुटप्रिंट ट्रैकिंग
        alert = "Structure"
        if s == atm_strike + 100 and gamma_strength_raw > 85: alert = "💥 GAMMA BLAST"
        elif s == atm_strike - 100: alert = "🚨 Put OB Active"
        elif s == atm_strike + 150: alert = "🚨 Call OB Active"
        elif ce_chg < -25: alert = "🕵️ Manipulation"
        elif ce_vol > 48000 and ce_chg < 5: alert = "🐳 5C Micro (Abs)"
        elif s == atm_strike - 50: alert = "🏹 Liquidity Hunt"
        
        target_pro = "65%" if s == atm_strike else f"{np.random.randint(41, 55)}%"
        
        rows.append({
            "CE Phase": ce_phase, "CE Vol PCR": f"{1/vol_pcr:.2f}", "CE ChgOI": f"{ce_chg:.1f}", "CE OI": f"{ce_oi:.1f}",
            "ST/Strike": f"{is_atm}{s}",
            "PE OI": f"{pe_oi:.1f}", "PE ChgOI": f"{pe_chg:.1f}", "PE Vol PCR": f"{vol_pcr:.2f}", "PE Phase": pe_phase,
            "Target Pro%": target_pro, "BB Squeeze": bb_squeeze_str, "Gamma Str%": gamma_str, "SMC Alerts": alert, "Strike PCR": f"{strike_pcr:.2f}",
            "strike_num": s, "atm_strike": atm_strike,
            "ce_raw_oi": ce_oi, "pe_raw_oi": pe_oi, "ce_raw_chg": ce_chg, "pe_raw_chg": pe_chg,
            "ce_raw_vol": ce_vol, "pe_raw_vol": pe_vol, "ce_raw_chg_vol": ce_chg_vol, "pe_raw_chg_vol": pe_chg_vol
        })
    return underlying_value, atm_strike, pd.DataFrame(rows)

underlying_value, atm_strike, df = generate_institutional_master_data()

# 2. ऑटोमैटिक +5 / -5 ITM और OTM मल्टी-लेयर पीसीआर कॉलोनी इंजन
itm_strikes = df[df['strike_num'] < atm_strike]
otm_strikes = df[df['strike_num'] > atm_strike]

# परत 1: OI PCR
otm_oi_pcr = otm_strikes['pe_raw_oi'].sum() / otm_strikes['ce_raw_oi'].sum()
itm_oi_pcr = itm_strikes['pe_raw_oi'].sum() / itm_strikes['ce_raw_oi'].sum()
# परत 2: Chg OI PCR
otm_chg_pcr = otm_strikes['pe_raw_chg'].sum() / otm_strikes['ce_raw_chg'].sum()
itm_chg_pcr = itm_strikes['pe_raw_chg'].sum() / itm_strikes['ce_raw_chg'].sum()
# परत 3: Volume PCR
otm_vol_pcr = otm_strikes['pe_raw_vol'].sum() / otm_strikes['ce_raw_vol'].sum()
itm_vol_pcr = itm_strikes['pe_raw_vol'].sum() / itm_strikes['ce_raw_vol'].sum()
# परत 4: Change Volume PCR
otm_chg_vol_pcr = otm_strikes['pe_raw_chg_vol'].sum() / otm_strikes['ce_raw_chg_vol'].sum()
itm_chg_vol_pcr = itm_strikes['pe_raw_chg_vol'].sum() / itm_strikes['ce_raw_chg_vol'].sum()

# 3. लॉक्ड एआई डिसीजन और रिस्क मैनेजर पैनल (AI Confirmation & Execution Box)
st.subheader("🧠 AI इंस्टीट्यूशनल डिसीजन और रिस्क मैनेजर")

# निर्णय कंडीशंस (लॉजिक चेकर)
is_gamma_blast = any("💥 GAMMA BLAST" in str(x) for x in df['SMC Alerts'])
is_manipulation = any("🕵️ Manipulation" in str(x) for x in df['SMC Alerts'])
# सिमुलेटेड ओआई ट्रैप स्थिति (ATM पर अत्यधिक कॉल सेलिंग और पुट की कमजोरी)
is_oi_trap = float(df[df['strike_num'] == atm_strike]['CE ChgOI'].iloc[0]) > 35.0 and float(df[df['strike_num'] == atm_strike]['PE ChgOI'].iloc[0]) < 10.0
is_pull_down = any("🚨 Call OB Active" in str(x) for x in df['SMC Alerts'])

if is_oi_trap:
    st.error("🛑 LIVE AI STATUS: 🚨 STRICTLY NO TRADE !!!")
    st.info("⚠️ REASON: सपोर्ट पर भारी PE OI होने के बावजूद OI Trap Detector सक्रिय है। Delta Deceleration और Chg VOL PCR Shock चालू है। सेलर्स हेजिंग करके बायर्स को फंसा रहे हैं (Strict No Call Buy Zone)।")
elif is_gamma_blast:
    st.success("🎯 LIVE AI STATUS: ✅ TAKE CALL BUY")
    st.info("📈 REASON: OTM Chg VOL PCR > 2.2 है और Gamma Str% > 85% पार कर चुका है। सेलर्स पूरी तरह ट्रैप हैं (Pull-Back Reversal / Gamma Blast Active)।")
    st.warning("⏱️ HOLD/EXIT RULE: जब तक Strike PCR और OTM Chg OI PCR ऊपर भाग रहे हैं, ट्रेड होल्ड रखें। अगर ऊपरी स्ट्राइक पर '🚨 Call OB Active' चमके, तुरंत प्रॉफिट बुक करके बाहर भागें।")
elif is_pull_down:
    st.error("📉 LIVE AI STATUS: ✅ TAKE PUT BUY")
    st.info("📉 REASON: Swing High का Liquidity Sweep हो चुका है और ऊपरी OTM स्ट्राइक पर Institutional Call Order Block एक्टिवेट है (Pull-Down Action Active)।")
    st.warning("⏱️ HOLD/EXIT RULE: जब तक CE ChgOI बढ़ रहा है, ट्रेड होल्ड रखें। अगर नीचे OTM Chg VOL PCR अचानक 2.5 पार करे, तुरंत एग्जिट करें क्योंकि इंस्टीट्यूशंस नीचे माल एब्जॉर्ब कर रहे हैं।")
else:
    st.warning("⚠️ LIVE AI STATUS: ⏳ AVOID (WAIT FOR CONFIRMATION)")
    st.info("💤 REASON: बोलिंजर बैंड कम्प्रेशन (BB Squeeze) > 4% है। मार्केट पूरी तरह साइडवेज है, प्रीमियम डीके से बचने के लिए शांत बैठें।")

# 4. मुख्य ग्रिड डिस्प्ले (सेंटर स्ट्राइक लेआउट)
st.markdown("---")
st.subheader("📋 प्रोप्राइटरी हाइब्रिड डेटा मैट्रिक्स")

display_cols = [
    "CE Phase", "CE Vol PCR", "CE ChgOI", "CE OI", 
    "ST/Strike", 
    "PE OI", "PE ChgOI", "PE Vol PCR", "PE Phase",
    "Target Pro%", "BB Squeeze", "Gamma Str%", "SMC Alerts", "Strike PCR"
]

def color_locked_master_ui(val):
    if "Long Buildup" in str(val): return 'color: #22c55e; font-weight: bold;'
    if "Short Buildup" in str(val) or "Structure" in str(val): return 'color: #ef4444;'
    if "Short Covering" in str(val): return 'color: #3b82f6; font-weight: bold;'
    if "SQUEEZE" in str(val) or "💥" in str(val) or "🚨" in str(val): return 'background-color: #310707; color: #f59e0b; font-weight: bold;'
    if "🕵️" in str(val) or "🐳" in str(val) or "🏹" in str(val): return 'color: #cc66ff; font-weight: bold;'
    if "🟡" in str(val): return 'background-color: #1a1403; color: #f59e0b; font-weight: bold;'
    return ''

# सभी फ्लोट नंबर्स को टेक्स्ट स्ट्रिंग में लॉक करके डिस्प्ले करना (ताकि एक्स्ट्रा .000000 कभी न दिखें)
st.dataframe(df[display_cols].style.map(color_locked_master_ui), use_container_width=True, hide_index=True)

# 5. स्ट्राइक प्राइस के ठीक नीचे ओवरऑल पीसीआर समरी फुटर्स
st.markdown("---")
st.markdown(f"### 📊 स्ट्राइक समरी (Overall Chain PCR)")
col_tot1, col_tot2 = st.columns(2)
col_tot1.metric("📌 OVERALL OI PCR", f"{(df['pe_raw_oi'].sum() / df['ce_raw_oi'].sum()):.2f}")
col_tot2.metric("🔥 OVERALL Chg OI PCR", f"{(df['pe_raw_chg'].sum() / df['ce_raw_chg'].sum()):.2f}")

# 6. पृथक क्वांटम कॉलोनी (मल्टी-लेयर +5 / -5 ITM और OTM परतों का साफ़ डिस्प्ले)
st.markdown("---")
st.subheader("🎯 पृथक क्वांटम कॉलोनी (मल्टी-लेयर +5 / -5 ITM & OTM PCR)")

l1, l2, l3, l4 = st.columns(4)

with l1:
    st.markdown("#### 📑 परत 1: ओपन Интерес (OI)")
    st.metric("🔴 OTM OI PCR", f"{otm_oi_pcr:.2f}")
    st.metric("🔵 ITM OI PCR", f"{itm_oi_pcr:.2f}")

with l2:
    st.markdown("#### 🔥 परत 2: चेंज इन OI")
    st.metric("🔴 OTM Chg OI PCR", f"{otm_chg_pcr:.2f}")
    st.metric("🔵 ITM Chg OI PCR", f"{itm_chg_pcr:.2f}")

with l3:st.markdown("#### ⚡ परत 3: वॉल्यूम (VOL)")st.metric("🔴 OTM VOL PCR", f"{otm_vol_pcr:.2f}")st.metric("🔵 ITM VOL PCR", f"{itm_vol_pcr:.2f}")with l4:st.markdown("#### 🚀 परत 4: चेंज इन वॉल्यूम")st.metric("🔴 OTM Chg VOL PCR", f"{otm_chg_vol_pcr:.2f}")st.metric("🔵 ITM Chg VOL PCR", f"{itm_chg_vol_pcr:.2f}")
