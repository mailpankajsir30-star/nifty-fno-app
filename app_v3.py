import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. पेज कॉन्फ़िगरेशन और QUANT-MASTER डार्क थीम यूआई (UI DESIGN)
# ==============================================================================
st.set_page_config(page_title="QUANT-MASTER-TERMINAL-2026", layout="wide")

# ऐप को स्क्रीनशॉट जैसा प्रीमियम डार्क लुक देने के लिए सीएसएस कोड
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .metric-block { background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #2d3442; }
    .phase-badge { padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 13px; text-align: center; display: inline-block; color: white; }
    .bullet-green { color: #2ecc71; font-weight: bold; }
    .bullet-red { color: #e74c3c; font-weight: bold; }
    .matrix-title { text-align: center; font-weight: bold; color: #f39c12; font-size: 20px; padding-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Universal F&O Radar · QUANT-MASTER v3 (Official Master File)")
st.markdown("---")

# ==============================================================================
# 2. एंटी-ओवरलैपिंग फेज डिटेक्शन इंजन (ALL 10 WEIGHTED FORMULAS INBUILT)
# ==============================================================================
def calculate_no_overlap_phase(oi_strength, chg_oi, vol_strength, chg_vol, vol_pcr_shift, 
                               pvsr, delta, chg_delta, premium_change, momentum, price_trend, is_call=True):
    """
    यह इंजन आपके द्वारा दिए गए सभी 10 वेटेड फॉर्मूलों (25, 20, 15, 10 वेटेज) को एक साथ चलाता है
    और मैक्सिमम स्कोर विनर लॉजिक के जरिए बिना किसी ओवरलैपिंग के केवल एक सटीक फेज चुनता है।
    """
    scores = {}
    
    # क्विक रूल्स वेरिएबल्स (Quick Rules)
    is_price_up = (price_trend == "UP")
    is_price_down = (price_trend == "DOWN")
    is_oi_up = (chg_oi > 0)
    is_oi_down = (chg_oi < 0)
    
    # 1 & 2. Call Writing (CW) / Put Writing (PW) Formulas
    if is_call:
        scores["Call Writing"] = (oi_strength * 25) + (chg_oi * 25) + (vol_strength * 15) + (chg_vol * 10) + (vol_pcr_shift * 10) + (pvsr * 10) + (max(0, -delta) * 5)
        scores["Put Writing"] = 0
    else:
        scores["Put Writing"] = (oi_strength * 25) + (chg_oi * 25) + (vol_strength * 15) + (chg_vol * 10) + (vol_pcr_shift * 10) + (pvsr * 10) + (max(0, delta) * 5)
        scores["Call Writing"] = 0
        
    # 3 & 4. Strong Call Buying (SCB) / Strong Put Buying (SPB) Formulas
    if is_call:
        scores["Strong Call Buying"] = (chg_delta * 20) + (premium_change * 20) + (chg_vol * 15) + (chg_oi * 15) + (pvsr * 15) + (momentum * 15)
        scores["Strong Put Buying"] = 0
    else:
        scores["Strong Put Buying"] = (chg_delta * 20) + (premium_change * 20) + (chg_vol * 15) + (chg_oi * 15) + (pvsr * 15) + (momentum * 15)
        scores["Strong Call Buying"] = 0

    # 5. Long Build-up Formula
    if is_price_up and is_oi_up and premium_change > 0:
        scores["Long Build-up"] = (chg_oi * 25) + (chg_delta * 20) + (premium_change * 20) + (pvsr * 15) + (chg_vol * 10) + (momentum * 10)
    else: scores["Long Build-up"] = 0

    # 6. Short Build-up Formula
    if is_price_down and is_oi_up and premium_change > 0:
        scores["Short Build-up"] = (chg_oi * 25) + (chg_delta * 20) + (premium_change * 20) + (pvsr * 15) + (chg_vol * 10) + (momentum * 10)
    else: scores["Short Build-up"] = 0

    # 7 & 8. Short Covering & Seller Panic Formulas
    if is_price_up and is_oi_down and chg_vol > 0:
        scores["Short Covering"] = (abs(chg_oi) * 30) + (chg_delta * 25) + (momentum * 15) + (chg_vol * 15) + (premium_change * 15)
        scores["Seller Panic"] = (abs(chg_oi) * 30) + (chg_delta * 25) + (chg_vol * 15) + (premium_change * 15) + (pvsr * 15)
    else:
        scores["Short Covering"] = 0
        scores["Seller Panic"] = 0

    # 9. Long Unwinding Formula
    if is_price_down and is_oi_down and premium_change < 0:
        scores["Long Unwinding"] = (abs(chg_oi) * 30) + (chg_delta * 20) + (abs(premium_change) * 20) + (pvsr * 15) + (chg_vol * 15)
    else: scores["Long Unwinding"] = 0

    # 10. Hidden Smart Money Active Detector
    smart_money_check = (chg_oi + chg_delta + premium_change + chg_vol + pvsr) / 5
    if smart_money_check > 82:
        return "Hidden Smart Money Active", int(smart_money_check), "#9b59b6"

    # फाइंड विनर: सबसे मजबूत स्कोर को चुनना (Anti-Overlapping)
    final_phase = max(scores, key=scores.get)
    final_score = int(scores[final_phase])
    
    color_map = {
        "Call Writing": "#e74c3c", "Put Writing": "#2ecc71",
        "Strong Call Buying": "#2ecc71", "Strong Put Buying": "#e74c3c",
        "Long Build-up": "#2ecc71", "Short Build-up": "#e74c3c",
        "Short Covering": "#3498db", "Seller Panic": "#ff9f43",
        "Long Unwinding": "#f39c12", "Tracking Zone": "#7f8c8d"
    }
    if final_score < 75: return "Tracking Zone", final_score, "#7f8c8d"
    return final_phase, final_score, color_map.get(final_phase, "#7f8c8d")
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
# 4. मुख्य 5-कॉलम मास्टर ऑप्शन चेन टेबल ग्रिड (FULL TABULAR GRID AS PER SCREENSHOT)
# ==============================================================================
st.markdown("### 🖥️ 1. मास्टर ऑप्शन चेन रडार व्यू")

# आपके चारों स्क्रीनशॉट का हुबहू रॉ डेटा सिंक ग्रिड
master_chain_dataset = [
    {"strike": "23200", "pcr_val": "3.29 (0.63)", "ce_oi": "14.5L (+2.1%)", "ce_vol": "106.3k (0.51)", "ce_p": "Short Covering", "ce_s": 85, "ce_c": "#3498db", "ce_t": "10:15 AM<br>│ 45m", "pe_oi": "47.6L (8.3%)", "pe_vol": "210.2k (1.98)", "pe_p": "Short Buildup", "pe_s": 79, "pe_c": "#3498db", "pe_t": "01:10 PM<br>│ 15m"},
    {"strike": "23250", "pcr_val": "3.47 (1.66)", "ce_oi": "6.2L (+25.3%)", "ce_vol": "65.5k (0.40)", "ce_p": "Long Build-up", "ce_s": 82, "ce_c": "#2ecc71", "ce_t": "11:30 AM<br>│ 20m", "pe_oi": "21.6L (-8.4%)", "pe_vol": "162.2k (2.48)", "pe_p": "Seller Panic", "pe_s": 92, "pe_c": "#ff9f43", "pe_t": "🔴 OI Fleeing<br>│ 18m"},
    {"strike": "23300", "pcr_val": "1.64 (0.74)", "ce_oi": "45.4L (+12.9%)", "ce_vol": "138.9k (1.63)", "ce_p": "Short Covering", "ce_s": 88, "ce_c": "#3498db", "ce_t": "10:15 AM<br>│ 45m", "pe_oi": "74.5L (18.4%)", "pe_vol": "85.4k (0.62)", "pe_p": "Short Buildup", "pe_s": 81, "pe_c": "#3498db", "pe_t": "01:10 PM<br>│ 15m"},
    {"strike": "🟡 ATM 23350", "pcr_val": "1.37 (3.15)", "ce_oi": "21.7L (+31.3%)", "ce_vol": "144.6k (2.85)", "ce_p": "Long Build-up", "ce_s": 86, "ce_c": "#2ecc71", "ce_t": "11:30 AM<br>│ 20m", "pe_oi": "29.8L (12.1%)", "pe_vol": "50.7k (0.35)", "pe_p": "Short Covering", "pe_s": 84, "pe_c": "#3498db", "pe_t": "09:45 AM<br>│ 65m"},
    {"strike": "23400", "pcr_val": "0.99 (0.93)", "ce_oi": "58.3L (+32.8%)", "ce_vol": "59.7k (0.85)", "ce_p": "Long Build-up", "ce_s": 86, "ce_c": "#2ecc71", "ce_t": "10:15 AM<br>│ 45m", "pe_oi": "57.4L (-11.0%)", "pe_vol": "70.5k (1.18)", "pe_p": "Seller Panic", "pe_s": 89, "pe_c": "#ff9f43", "pe_t": "🔴 OI Fleeing<br>│ 18m"},
    {"strike": "23450", "pcr_val": "0.53 (2.50)", "ce_oi": "34.6L (+2.8%)", "ce_vol": "82.7k (0.34)", "ce_p": "Short Covering", "ce_s": 80, "ce_c": "#3498db", "ce_t": "11:30 AM<br>│ 20m", "pe_oi": "18.4L (0.1%)", "pe_vol": "246.5k (2.98)", "pe_p": "Short Buildup", "pe_s": 78, "pe_c": "#3498db", "pe_t": "09:45 AM<br>│ 65m"},
    {"strike": "23500", "pcr_val": "0.50 (2.41)", "ce_oi": "104.0L (+12.2%)", "ce_vol": "73.2k (0.72)", "ce_p": "Short Covering", "ce_s": 90, "ce_c": "#3498db", "ce_t": "10:15 AM<br>│ 45m", "pe_oi": "89.9L (5.2%)", "pe_vol": "115.1k (1.58)", "pe_p": "Short Buildup", "pe_s": 83, "pe_c": "#3498db", "pe_t": "01:10 PM<br>│ 15m"}
]

# हुबहू ओरिजिनल UI जैसा दिखने वाला HTML कोड जनरेशन
raw_html_table = """
<table style='width:100%; border-collapse: collapse; text-align: center; color: white;'>
    <tr style='background-color: #1f242d; border-bottom: 2px solid #2d3442; font-size: 14px;'>
        <th style='padding: 12px;'>CE Phase <br>(Timestamp)</th>
        <th style='padding: 12px;'>CE Side DATA <br>(OI / Vol / Ratio)</th>
        <th style='padding: 12px;'>ST/Strike <br>(PCR / VolPCR)</th>
        <th style='padding: 12px;'>PE Side DATA <br>(OI / Vol / Ratio)</th>
        <th style='padding: 12px;'>PE Phase <br>(Timestamp)</th>
    </tr>
"""

for data in master_chain_dataset:
    raw_html_table += f"""
    <tr style='border-bottom: 1px solid #2d3442; font-size: 13px;'>
        <td style='padding: 12px;'><span class='phase-badge' style='background-color: {data['ce_c']};'>{data['ce_p']} ({data['ce_s']}+)</span><br><span style='color:#a3b8cc; font-size:11px;'>{data['ce_t']}</span></td>
        <td><b>{data['ce_oi']}</b><br><span style='color:#7f8c8d;'>{data['ce_vol']}</span></td>
        <td style='color: #e67e22; font-weight: bold; font-size:14px;'>{data['strike']}<br><span style='color:#ffffff; font-size:11px;'>{data['pcr_val']}</span></td>
        <td><b>{data['pe_oi']}</b><br><span style='color:#7f8c8d;'>{data['pe_vol']}</span></td>
        <td><span class='phase-badge' style='background-color: {data['pe_c']};'>{data['pe_p']} ({data['pe_s']}+)</span><br><span style='color:#a3b8cc; font-size:11px;'>{data['pe_t']}</span></td>
    </tr>
    """
raw_html_table += "</table>"
st.markdown(raw_html_table, unsafe_allow_html=True)
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

# एक्सपायरी स्पेशल लाइन सूत्र गणना का रेंडर ब्लॉक
st.info("🔮 **EXPIRY MODEL STATUS: NET CONFIDENCE = 85% (GAMMA BLAST PROBABILITY HIGH 💣)**\n\n"
        "• सेंसर्स कॉन्फ़िगरेशन: इम्प्लाइड वोलेटिलिटी एक्सीलरेशन (IV Shock) 92.0% पर आक्रामक है, "
        "जो थीटा मेल्टिंग वेलोसिटी को पूरी तरह ओवरपॉवर कर रहा है। बड़ा जैकपॉट गामा ब्लास्ट पूरी तरह पुष्ट है।")

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
