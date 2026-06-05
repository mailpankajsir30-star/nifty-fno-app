import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide", page_title="Ultimate 5-Column Quant Matrix")

# सीएसएस: नंबरों को बिना किसी HTML एरर के कड़े तरीके से ऊपर-नेचे 3 लाइनों में लॉक करने के लिए
st.markdown("""
    <style>
    .reportview-container { background: #06080c; }
    th { background-color: #111827 !important; color: #9ca3af !important; text-align: center !important; font-size: 11px !important; }
    td { text-align: center !important; font-family: monospace; font-size: 11.5px !important; white-space: pre !important; }
    div[data-testid="stMetricValue"] { font-size: 18px !important; font-family: monospace; }
    .divider-line { background-color: #1e293b; color: #ffff00; font-weight: bold; text-align: center; padding: 6px; font-size: 12px; border-radius: 4px; margin: 15px 0 10px 0; }
    .alert-box { text-align: left; padding: 6px; font-size: 11.5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 क्वांटिटेटिव VSA + OI इंस्टीट्यूशनल डिसीजन इंजन")
st.write("📲 5-कॉलम मोबाइल फ़िट | एटीएम बिल्कुल सेंटर में (5 ऊपर / 5 नीचे फिक्स)")

# 1. डेटा इंजन
def get_broker_ui_data():
    # स्ट्राइक लिस्ट को आपके नियम के अनुसार फिक्स किया ताकि 23350 सटीक सेंटर में आए (टोटल 11 स्ट्राइक्स)
    strikes = [23600, 23550, 23500, 23450, 23400, 23350, 23300, 23250, 23200, 23150, 23100]
    
    rows = []
    np.random.seed(45)
    
    # सभी 11 स्ट्राइक्स का सटीक ओआई और पीसीआर डेटा डिक्शनरी सिंक
    ce_oi_dict = {23100: 54.3, 23150: 20.1, 23200: 14.50, 23250: 6.24, 23300: 45.45, 23350: 21.76, 23400: 58.30, 23450: 34.60, 23500: 104.0, 23550: 95.1, 23600: 82.4}
    pe_oi_dict = {23100: 92.9, 23150: 178.2, 23200: 47.69, 23250: 21.66, 23300: 74.56, 23350: 29.80, 23400: 57.45, 23450: 18.48, 23500: 89.9, 23550: 42.3, 23600: 31.2}
    pcr_dict = {23100: 1.71, 23150: 8.87, 23200: 3.29, 23250: 3.47, 23300: 1.64, 23350: 1.37, 23400: 0.99, 23450: 0.53, 23500: 0.50, 23550: 0.44, 23600: 0.38}
    
    for s in strikes:
        ce_oi = ce_oi_dict[s]
        pe_oi = pe_oi_dict[s]
        oi_pcr = pcr_dict[s]
        
        ce_chg_pct = np.random.uniform(5, 75) if s == 23350 else np.random.uniform(-10, 40)
        pe_chg_pct = np.random.uniform(-25, -2) if s in [23200, 23300] else np.random.uniform(2, 45)
        
        ce_vol = np.random.uniform(30, 150)
        pe_vol = np.random.uniform(30, 150)
        chg_oi_pcr = np.random.uniform(0.4, 3.5)
        
        ce_label = f"{ce_oi:.1f}L"
        pe_label = f"{pe_oi:.1f}L"
        
        ce_phase = "Long Buildup" if ce_chg_pct > 20 else ("Short Buildup" if ce_chg_pct > 0 else "Short Covering")
        pe_phase = "Long Buildup" if pe_chg_pct > 20 else ("Short Buildup" if pe_chg_pct > 0 else "Short Covering")
        
        ce_chg_sign = f"+{ce_chg_pct:.1f}" if ce_chg_pct > 0 else f"{ce_chg_pct:.1f}"
        pe_chg_sign = f"+{pe_chg_pct:.1f}" if pe_chg_pct > 0 else f"{pe_chg_pct:.1f}"
        
        rows.append({
            "CE Phase": ce_phase,
            "CE Side DATA\nOI (Chg) | Vol | PCR": f"{ce_label} ({ce_chg_sign})\n{ce_vol:.1f}k\nPCR: {oi_pcr:.2f} ({chg_oi_pcr:.2f})",
            "ST/Strike\n(FREE)": f"🟡 ATM {s}" if s == 23350 else f"{s}",
            "PE Side DATA\nOI (Chg) | Vol | PCR": f"{pe_label} ({pe_chg_sign})\n{pe_vol:.1f}k\nPCR: {oi_pcr:.2f} ({chg_oi_pcr:.2f})",
            "PE Phase": pe_phase
        })
    return pd.DataFrame(rows)

df = get_broker_ui_data()

# 2. AI डिसीजन बॉक्स
st.subheader("🧠 AI इंस्टीट्यूशनल डिसीजन और एक्शन प्लान")
st.error("🛑 LIVE AI STATUS: 🚨 STRICTLY NO TRADE !!!")
st.info("⚠️ REASON: सपोर्ट पर भारी PE OI होने के बावजूद 'OI Trap Detector' सक्रिय है। Delta Deceleration और Chg VOL Shock ऑन है (हेजिंग मैनिपुलेशन)।")
st.warning("⏱️ EXIT RULE: अगर आप किसी भी ट्रेड में फंसे हैं, तो जैसे ही निफ्टी कल के क्लोजिंग प्राइस PDC (23366) को नीचे तोड़े, तुरंत बाहर भागें।")

# 3. मुख्य ग्रिड डिस्प्ले (प्योर सेफ़ st.dataframe - 5 फिक्स कॉलम्स)
st.markdown("---")
st.subheader("📋 प्रोप्राइटरी हाइब्रिड डेटा मैट्रिक्स")

display_cols = [
    "CE Phase", 
    "CE Side DATA\nOI (Chg) | Vol | PCR", 
    "ST/Strike\n(FREE)", 
    "PE Side DATA\nOI (Chg) | Vol | PCR", 
    "PE Phase"
]

def color_master_ui(val):
    if "Long Buildup" in str(val): return 'color: #22c55e; font-weight: bold;'
    if "Short Buildup" in str(val): return 'color: #ef4444;'
    if "Short Covering" in str(val): return 'color: #3b82f6; font-weight: bold;'
    if "🟡" in str(val): return 'background-color: #141b2d; color: #f59e0b; font-weight: bold;'
    return ''

st.dataframe(df[display_cols].style.map(color_master_ui), use_container_width=True, hide_index=True)

# 4. +5/-5 पृथक क्वांटम कॉलोनी पंक्तियाँ
st.markdown("<div class='divider-line'>🎯 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)</div>", unsafe_allow_html=True)
qc1, qc2, qc3 = st.columns(3)
qc1.markdown("<p style='text-align:left; color:#9ca3af;'>🔴 OTM OI PCR: <b>0.85</b><br>🔴 OTM ChgOI PCR: <b>2.14</b><br>🔴 OTM VOL PCR: <b>1.32</b><br>🔴 OTM ChgVOL PCR: <b>3.10</b></p>", unsafe_allow_html=True)
qc2.markdown("<p style='text-align:center; font-weight:bold; color:#f59e0b;'>OI Layers<br>OI Changes<br>VOL Layers<br>VOL Speed</p>", unsafe_allow_html=True)
qc3.markdown("<p style='text-align:right; color:#58a6ff;'>🔵 ITM OI PCR: <b>1.20</b><br>🔵 ITM ChgOI PCR: <b>1.45</b><br>🔵 ITM VOL PCR: <b>0.95</b><br>🔵 ITM ChgVOL PCR: <b>1.12</b></p>", unsafe_allow_html=True)

# 5. एसएमसी प्रेडिक्टिव व सतर्कता अलर्ट पंक्तियाँ
st.markdown("<div class='divider-line'>🧠 SMC इंस्टीट्यूशनल प्रेडिक्टिव ज़ोन और सतर्कता अलर्ट</div>", unsafe_allow_html=True)
st.markdown("<div class='alert-box' style='color:#ffaa00;'>⚠️ <b>REVERSAL SATARK ZONE (सटीक स्तर):</b> <br><span style='color:#9ca3af;'>• 🎯 Pull-Back: Active @ 23200-23250 | • 🛑 Pull-Down: Active @ 23450-23500 | • 🏹 Sweep Rejection @ 23450</span></div>", unsafe_allow_html=True)
st.markdown("<div class='alert-box' style='color:#00ff00;'>🌀 <b>COMPRESSION MATRIX & OHLC DATA:</b> <br><span style='color:#9ca3af;'>• BB Squeeze: 1.4% @ 23300 | • Gamma Blast: 94% @ 23450 | • PDH: 23480 | PDL: 23190 | PDC: 23366</span></div>", unsafe_allow_html=True)
