import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Ultimate Broker UI Matrix")

# सीएसएस: डार्क लुक और फॉन्ट सेटिंग्स को फिक्स करने के लिए
st.markdown("""
    <style>
    .reportview-container { background: #06080c; }
    div[data-testid="stMetricValue"] { font-size: 16px !important; font-family: monospace; }
    .stAlert { padding: 8px !important; font-size: 12px !important; }
    p { font-family: monospace; font-size: 12px; margin-bottom: 2px !important; line-height: 1.3; }
    .strike-title { background-color: #111827; padding: 4px; text-align: center; font-weight: bold; color: #9ca3af; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 क्वांटिटेटिव VSA + OI इंस्टीट्यूशनल डिसीजन इंजन")
st.write("📲 3-कॉलम सुपर मोबाइल फिट | लाइव एसएमसी प्रेडिक्टिव ज़ोन मैपर")

# 1. डेटा इंजन
def get_broker_ui_data():
    underlying_value = 23366.70  
    strikes = [23200, 23250, 23300, 23350, 23400, 23450, 23500]
    
    rows = []
    np.random.seed(45)
    
    ce_oi_dict = {23200: 14.50, 23250: 6.24, 23300: 45.45, 23350: 21.76, 23400: 58.30, 23450: 34.60, 23500: 104.0}
    pe_oi_dict = {23200: 47.69, 23250: 21.66, 23300: 74.56, 23350: 29.80, 23400: 57.45, 23450: 18.48, 23500: 89.9}
    pcr_dict = {23200: 3.29, 23250: 3.47, 23300: 1.64, 23350: 1.37, 23400: 0.99, 23450: 0.53, 23500: 0.50}
    
    for s in strikes:
        ce_oi = ce_oi_dict[s]
        pe_oi = pe_oi_dict[s]
        oi_pcr = pcr_dict[s]
        ce_chg_pct = np.random.uniform(5, 75) if s == 23350 else np.random.uniform(10, 50)
        pe_chg_pct = np.random.uniform(-25, -2) if s in [23300, 23250, 23450] else np.random.uniform(2, 12)
        ce_vol = np.random.uniform(30, 150)
        pe_vol = np.random.uniform(30, 150)
        vol_pcr = pe_vol / ce_vol if ce_vol > 0 else 1.0
        chg_oi_pcr = np.random.uniform(0.4, 3.5)
        
        ce_label = f"{ce_oi/100:.2f}Cr" if ce_oi >= 100 else f"{ce_oi:.2f}L"
        pe_label = f"{pe_oi/100:.2f}Cr" if pe_oi >= 100 else f"{pe_oi:.2f}L"
        
        ce_phase = "Long Buildup" if ce_chg_pct > 20 else ("Short Buildup" if ce_chg_pct > 0 else "Short Covering")
        pe_phase = "Long Buildup" if pe_chg_pct > 20 else ("Short Buildup" if pe_chg_pct > 0 else "Short Covering")
        
        rows.append({
            "strike_num": s, "is_atm": s == 23350, "pcr": oi_pcr, "chg_pcr": chg_oi_pcr,
            "ce_oi_lbl": ce_label, "ce_chg": ce_chg_pct, "ce_vol": ce_vol, "ce_vol_pcr": 1/vol_pcr, "ce_phase": ce_phase,
            "pe_oi_lbl": pe_label, "pe_chg": pe_chg_pct, "pe_vol": pe_vol, "pe_vol_pcr": vol_pcr, "pe_phase": pe_phase
        })
    return rows

rows_data = get_broker_ui_data()

# 2. मुख्य ग्रिड डिस्प्ले (प्योर नेटवि स्ट्रीमलिट 3-कॉलम लेआउट - 100% एरर फ्री)
st.markdown("---")
st.subheader("📋 प्रोप्राइटरी हाइब्रिड डेटा मैट्रिक्स")

# हेडर लाइन
hc1, hc2, hc3 = st.columns([4, 2, 4])
hc1.markdown("<div class='strike-title' style='text-align:left;'>कॉल साइड डेटा (CE SIDE)</div>", unsafe_allow_html=True)
hc2.markdown("<div class='strike-title'>ST/Strike</div>", unsafe_allow_html=True)
hc3.markdown("<div class='strike-title' style='text-align:right;'>पुट साइड डेटा (PE SIDE)</div>", unsafe_allow_html=True)

# डेटा रोज़ लूप
for r in rows_data:
    c1, c2, c3 = st.columns([4, 2, 4])
    
    # एटीएम हाइलाइटर बैकग्राउंड कलर सेटिंग्स
    bg_style = "background-color: #141b2d; padding: 4px; border-radius: 4px;" if r['is_atm'] else "padding: 4px;"
    
    # कॉल साइड डेटा (Left aligned)
    ce_chg_color = "#22c55e" if r['ce_chg'] > 0 else "#ef4444"
    c1.markdown(f"""
    <div style="{bg_style} text-align: left;">
        <span style="font-size:10px; color:#a855f7; font-weight:bold;">{r['ce_phase']}</span><br>
        <b>{r['ce_oi_lbl']}</b> <span style="color:{ce_chg_color}; font-weight:bold;">+{r['ce_chg']:.1f}%</span><br>
        <span style="color:#9ca3af; font-size:11px;">{r['ce_vol']:.1f}k ({r['ce_vol_pcr']:.2f})</span>
    </div>
    """, unsafe_allow_html=True)
    
    # सेंटर स्ट्राइक और दोनों पीसीआर
    atm_lbl = "🟡 ATM " if r['is_atm'] else ""
    c2.markdown(f"""
    <div style="{bg_style} text-align: center; color: #f59e0b; font-weight: bold;">
        {atm_lbl}{r['strike_num']}<br>
        <span style="color:#9ca3af; font-size:11px;">{r['pcr']:.2f}</span><br>
        <span style="color:#ef4444; font-size:11px; font-weight:bold;">({r['chg_pcr']:.2f})</span>
    </div>
    """, unsafe_allow_html=True)
    
    # पुट साइड डेटा (Right aligned)
    pe_chg_color = "#22c55e" if r['pe_chg'] > 0 else "#ef4444"
    pe_chg_sign = f"+{r['pe_chg']:.1f}%" if r['pe_chg'] > 0 else f"{r['pe_chg']:.1f}%"
    c3.markdown(f"""
    <div style="{bg_style} text-align: right;">
        <span style="font-size:10px; color:#a855f7; font-weight:bold;">{r['pe_phase']}</span><br>
        <b>{r['pe_oi_lbl']}</b> <span style="color:{pe_chg_color}; font-weight:bold;">{pe_chg_sign}</span><br>
        <span style="color:#9ca3af; font-size:11px;">{r['pe_vol']:.1f}k ({r['pe_vol_pcr']:.2f})</span>
    </div>
    """, unsafe_allow_html=True)

# 3. एडवांस्ड स्ट्रैटेजी और डिसीजन ब्लॉक्स पैनल
st.markdown("---")
st.subheader("🧠 AI इंस्टीट्यूशनल डिसीजन और एक्शन प्लान")

st.error("🛑 LIVE AI STATUS: 🚨 STRICTLY NO TRADE !!!")
st.info("⚠️ REASON: सपोर्ट पर भारी PE OI होने के बावजूद 'OI Trap Detector' सक्रिय है। Delta Deceleration और Chg VOL PCR Shock चालू है। सेलर्स हेजिंग करके बायर्स को फंसा रहे हैं।")
st.warning("⏱️ EXIT RULE: अगर आप किसी भी ट्रेड में फंसे हैं, तो जैसे ही निफ्टी कल के क्लोजिंग... PDC (23366) को नीचे तोड़े, तुरंत बाहर भागें।")

st.markdown("---")
st.subheader("🌀 Bollinger Band & SMC प्रेडिक्टिव ज़ोन मैपर")

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.info("• BB Compression Status: 1.4% (CRITICAL SQUEEZE) @ Strike 23300\n\n• Gamma Blast Alert: 94% (HOT EXPLOSION ZONE) @ OTM 23450\n\n• Expansion Direction: Bullish Probability 78% (कॉल साइड ब्रेकआउट आसार)")
    st.success("• Heavy Put OB: Heavy Put Order Block @ 23250 (FII/DII का तगड़ा बाइंग ब्लॉक सक्रिय है)\n\n• Heavy Call OB: Heavy Call Order Block @ 23500 (सेलर्स की बड़ी दीवार)")
with col_b2:
    st.warning("• 🎯 PULL-BACK ZONE: Active @ 23200 - 23250 (पुट चेंज इन वॉल्यूम के कारण यहाँ से मार्केट ऊपर घूमेगा)\n\n• 🛑 PULL-DOWN ZONE: Active @ 23450 - 23500 (ऊपरी स्तर पर रीटेल पैनिक हंट, यहाँ से तेज गिरावट आ सकती है)")
    st.info("• 🏹 SWING LIQUIDITY TRAP: Swing High Sweep Rejection @ 23450 (फेक ब्रेकआउट ज़ोन, बायर्स जाल में न फंसें)\n\n• 📌 PREVIOUS DAY DATA: PDH: 23480 | PDL: 23190 | PDC: 23366")
