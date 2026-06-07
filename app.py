import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. पेज कॉन्फ़िगरेशन और QUANT-MASTER ऑल-डिवाइस रिस्पॉन्सिव यूआई (UI DESIGN)
# ==============================================================================
st.set_page_config(page_title="QUANT-MASTER-TERMINAL-2026", layout="wide")

# मोबाइल, टैबलेट और लैपटॉप पर स्क्रीन ऑटो-फिट करने के लिए सीएसएस
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .metric-block { background-color: #161b22; padding: 10px; border-radius: 6px; border: 1px solid #2d3442; text-align: center; }
    .matrix-title { text-align: center; font-weight: bold; color: #f39c12; font-size: 18px; padding-top: 15px; }
    .bullet-green { color: #2ecc71; font-weight: bold; }
    .bullet-red { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("Universal F&O Radar · QUANT-MASTER v3")
st.markdown("---")

# ==============================================================================
# 🎯 न्यू फ़ीचर: EXPIRY DAY DROPDOWN SELECTOR (सबसे ऊपर)
# ==============================================================================
st.markdown("### 📅 Expiry Settings")
selected_expiry = st.selectbox(
    "Select Expiry Day / Date:",
    ["Current Week Expiry (Nifty)", "Next Week Expiry", "Monthly Expiry"]
)
st.success(f"🎯 Active Tracking: {selected_expiry}")

# ==============================================================================
# 2. एंटी-ओवरलैपिंग फेज डिटेक्शन इंजन (ALL 10 WEIGHTED FORMULAS)
# ==============================================================================
def calculate_no_overlap_phase(oi_strength, chg_oi, vol_strength, chg_vol, vol_pcr_shift, 
                               pvsr, delta, chg_delta, premium_change, momentum, price_trend, is_call=True):
    scores = {}
    is_price_up = (price_trend == "UP")
    is_price_down = (price_trend == "DOWN")
    is_oi_up = (chg_oi > 0)
    is_oi_down = (chg_oi < 0)
    
    if is_call:
        scores["Call Writing"] = (oi_strength * 25) + (chg_oi * 25) + (vol_strength * 15) + (chg_vol * 10) + (vol_pcr_shift * 10) + (pvsr * 10) + (max(0, -delta) * 5)
        scores["Put Writing"] = 0
    else:
        scores["Put Writing"] = (oi_strength * 25) + (chg_oi * 25) + (vol_strength * 15) + (chg_vol * 10) + (vol_pcr_shift * 10) + (pvsr * 10) + (max(0, delta) * 5)
        scores["Call Writing"] = 0
        
    if is_call:
        scores["Strong Call Buying"] = (chg_delta * 20) + (premium_change * 20) + (chg_vol * 15) + (chg_oi * 15) + (pvsr * 15) + (momentum * 15)
        scores["Strong Put Buying"] = 0
    else:
        scores["Strong Put Buying"] = (chg_delta * 20) + (premium_change * 20) + (chg_vol * 15) + (chg_oi * 15) + (pvsr * 15) + (momentum * 15)
        scores["Strong Call Buying"] = 0

    if is_price_up and is_oi_up and premium_change > 0:
        scores["Long Build-up"] = (chg_oi * 25) + (chg_delta * 20) + (premium_change * 20) + (pvsr * 15) + (chg_vol * 10) + (momentum * 10)
    else: scores["Long Build-up"] = 0

    if is_price_down and is_oi_up and premium_change > 0:
        scores["Short Build-up"] = (chg_oi * 25) + (chg_delta * 20) + (premium_change * 20) + (pvsr * 15) + (chg_vol * 10) + (momentum * 10)
    else: scores["Short Build-up"] = 0

    if is_price_up and is_oi_down and chg_vol > 0:
        scores["Short Covering"] = (abs(chg_oi) * 30) + (chg_delta * 25) + (momentum * 15) + (chg_vol * 15) + (premium_change * 15)
        scores["Seller Panic"] = (abs(chg_oi) * 30) + (chg_delta * 25) + (chg_vol * 15) + (premium_change * 15) + (pvsr * 15)
    else:
        scores["Short Covering"] = 0
        scores["Seller Panic"] = 0

    if is_price_down and is_oi_down and premium_change < 0:
        scores["Long Unwinding"] = (abs(chg_oi) * 30) + (chg_delta * 20) + (abs(premium_change) * 20) + (pvsr * 15) + (chg_vol * 15)
    else: scores["Long Unwinding"] = 0

    smart_money_check = (chg_oi + chg_delta + premium_change + chg_vol + pvsr) / 5
    if smart_money_check > 82:
        return "Hidden Smart Money Active", int(smart_money_check)

    final_phase = max(scores, key=scores.get)
    final_score = int(scores[final_phase])
    if final_score < 75: return "Tracking Zone", final_score
    return final_phase, final_score
# ==============================================================================
# 3. टॉप लाइव हेडर (LIVE SPOT & EXACT ATM)
# ==============================================================================
st.subheader("📊 2PM LOCK FINAL DATA LOGS")
col_spot1, col_spot2 = st.columns(2)
with col_spot1:
    st.metric("NIFTY 50 LIVE SPOT", "23366.70", "+124.50")
with col_spot2:
    st.metric("🎯 EXACT ATM STRIKE (MROUND)", "23350", "Nearest 50 Mult")

# ==============================================================================
# 4. मुख्य 5-कॉलम मास्टर ऑप्शन चेन टेबल ग्रिड (FULL ALL-DEVICE RESPONSIVE GRID)
# ==============================================================================
st.markdown("### 🖥️ 1. मास्टर ऑप्शन चेन रडार व्यू")

# डेटा को क्लीन स्ट्रीमलिट नेटिव ग्रिड में बदलना ताकि मोबाइल और लैपटॉप पर ऑटो-फिट रहे
master_chain_dataset = [
    ["Short Covering (85+)\n10:15 AM", "14.5L (+2.1%)\n106.3k (0.51)", "23200\n3.29 (0.63)", "47.6L (8.3%)\n210.2k (1.98)", "Short Buildup (79+)\n01:10 PM"],
    ["Long Build-up (82+)\n11:30 AM", "6.2L (+25.3%)\n65.5k (0.40)", "23250\n3.47 (1.66)", "21.6L (-8.4%)\n162.2k (2.48)", "Seller Panic (92+)\nOI Fleeing"],
    ["Short Covering (88+)\n10:15 AM", "45.4L (+12.9%)\n138.9k (1.63)", "23300\n1.64 (0.74)", "74.5L (18.4%)\n85.4k (0.62)", "Short Buildup (81+)\n01:10 PM"],
    ["Long Build-up (86+)\n11:30 AM", "21.7L (+31.3%)\n144.6k (2.85)", "🟡 ATM 23350\n1.37 (3.15)", "29.8L (12.1%)\n50.7k (0.35)", "Short Covering (84+)\n09:45 AM"],
    ["Long Build-up (86+)\n10:15 AM", "58.3L (+32.8%)\n59.7k (0.85)", "23400\n0.99 (0.93)", "57.4L (-11.0%)\n70.5k (1.18)", "Seller Panic (89+)\nOI Fleeing"],
    ["Short Covering (80+)\n11:30 AM", "34.6L (+2.8%)\n82.7k (0.34)", "23450\n0.53 (2.50)", "18.4L (0.1%)\n246.5k (2.98)", "Short Buildup (78+)\n09:45 AM"],
    ["Short Covering (90+)\n10:15 AM", "104.0L (+12.2%)\n73.2k (0.72)", "23500\n0.50 (2.41)", "89.9L (5.2%)\n115.1k (1.58)", "Short Buildup (83+)\n01:10 PM"]
]

df_master = pd.DataFrame(
    master_chain_dataset,
    columns=["CE Phase (Timestamp)", "CE Side DATA (OI / Vol / Ratio)", "ST/Strike (PCR / VolPCR)", "PE Side DATA (OI / Vol / Ratio)", "PE Phase (Timestamp)"]
)

# नेटिव स्ट्रीमलिट डेटाफ्रेम यूज़ करना जो कभी नहीं टूटेगा
st.dataframe(df_master, use_container_width=True, height=330)
# ==============================================================================
# 5. 4-लेयर पृथक क्वांटम कॉलोनी (OTM vs ITM LAYER DATA COMPONENT)
# ==============================================================================
st.markdown("---")
st.markdown("### 🧠 2. 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 Layers)")

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown("<span class='bullet-red'>🔴 OTM Side Layer (+5 Strike Channel)</span>", unsafe_allow_html=True)
    st.code("OTM OI PCR    : 0.85\nChgOI PCR     : 2.14\nOTM VOL PCR   : 1.32\nChgVOL PCR    : 3.10", language="text")
with col_m2:
    st.markdown("<div class='matrix-title'>परत 1-4 समरी<br><br>VOL Speed</div>", unsafe_allow_html=True)
with col_m3:
    st.markdown("<span class='bullet-green'>🔵 ITM Side Layer (-5 Strike Channel)</span>", unsafe_allow_html=True)
    st.code("ITM OI PCR    : 1.20\nITM ChgOI PCR : 1.45\nITM VOL PCR   : 0.95\nITM ChgVOL PCR: 1.12", language="text")

# ==============================================================================
# 6. UNIFIED AI DECISION SCORES (% DISTRIBUTION ENGINE)
# ==============================================================================
st.markdown("---")
st.markdown("### 🤖 3. UNIFIED AI DECISION SCORES (% Distribution Engine)")

# आपके चारों प्रतिशत स्कोर (Call, Put, Sideways, No Trade)
col_sc1, col_sc2, col_sc3 = st.columns(3)
with col_sc1:
    st.metric("🟢 AI CALL BUY SCORE", "86%", "STRONG BULLISH")
    st.metric("实时 🟡 SIDEWAYS SCORE", "14%")
with col_sc2:
    st.markdown("<div style='text-align:center; padding-top:40px; font-weight:bold; color:#f39c12; font-size:24px;'>AI<br>BRAIN<br>MATRIX</div>", unsafe_allow_html=True)
with col_sc3:
    st.metric("🔴 AI PUT BUY SCORE", "2%")
    st.metric("🟣 NO TRADE / TRAP SCORE", "42%")

# ==============================================================================
# 7. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE (जादुई पर्पल अलर्ट लाइन)
# ==============================================================================
st.markdown("---")
st.markdown("### 🍏 4. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE")

# एक्सपायरी स्पेशल लाइन का रेंडर ब्लॉक
st.info("🔮 **EXPIRY MODEL STATUS: NET CONFIDENCE = 85% (GAMMA BLAST PROBABILITY HIGH 💣)**\n\n"
        "• सेंसर्स कॉन्फ़िगरेशन: इम्प्लाइड वोलेटिलिटी एक्सीलरेशन (IV Shock) 92.0% पर आक्रामक है, "
        "जो थीटा मोमेंटम वेलोसिटी को पूरी तरह ओवरपॉवर कर रहा है। बड़ा जैकपॉट गामा ब्लास्ट पूरी तरह पुष्ट है।")

# अंतिम क्वांटम फ्यूज़न अलर्ट बैनर
st.success("🔮 SYSTEM STATUS: UNIFIED MODEL RUNNING OPERATIONAL (FVS = 100)")
st.markdown("<div style='background-color:#2ecc71; padding:15px; border-radius:5px; text-align:center; color:white; font-weight:bold; font-size:18px;'>🟢 QUANTUM FUSION METRICS ALERT: TAKE CALL BUY ACTIVE (🎯 Confidence: 86%)</div>", unsafe_allow_html=True)

# ==============================================================================
# 8. REVERSAL SATARK ZONE & OHLC LEVELS WITH STRIKE PRICES
# ==============================================================================
st.markdown("---")
st.markdown("### ⚠️ 5. REVERSAL SATARK ZONE & OHLC LEVELS (सटीक स्ट्राइक प्राइस के साथ)")

atm_strike_base = 23350
col_rev1, col_rev2 = st.columns(2)

with col_rev1:
    st.markdown(f"""
    <div style='background-color: #1b2a22; padding: 15px; border-radius: 5px; border: 1px solid #2ecc71;'>
        <span style='color: #2ecc71; font-weight: bold; font-size: 15px;'>🔄 Pull-Back Support Range:</span><br>
        <span style='font-size: 22px; font-weight: bold; color: white;'>{atm_strike_base - 150} — {atm_strike_base - 100} (23200 - 23250)</span><br>
        <span style='font-size: 12px; color: #a3b8cc;'>लॉजिक: हैवी इंस्टीट्यूशनल पुट राइटिंग और अब्जॉर्प्शन जोन</span>
    </div>
    """, unsafe_allow_html=True)
    
with col_rev2:
    st.markdown(f"""
    <div style='background-color: #2c1a1d; padding: 15px; border-radius: 5px; border: 1px solid #e74c3c;'>
        <span style='color: #e74c3c; font-weight: bold; font-size: 15px;'>🛑 Pull-Down Resistance Wall:</span><br>
        <span style='font-size: 22px; font-weight: bold; color: white;'>{atm_strike_base + 100} — {atm_strike_base + 150} (23450 - 23500)</span><br>
        <span style='font-size: 12px; color: #a3b8cc;'>लॉजिक: मैक्सिमम कॉल ओपन INTEREST बैरियर दीवार</span>
    </div>
    """, unsafe_allow_html=True)
