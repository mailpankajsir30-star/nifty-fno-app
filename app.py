import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Ultimate VSA & OI Matrix")

# सीएसएस स्टाइलिंग: इमेज की तरह डार्क और प्रोफेशनल ग्रिड लुक देने के लिए
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stDataFrame td, .stDataFrame th { text-align: center !important; font-family: monospace; }
    div[data-testid="stMetricValue"] { font-size: 24px !important; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 एडवांस्ड क्वांटिटेटिव VSA + OI मैट्रिक्स डैशबोर्ड")

# 1. डेटा इंजन (इमेज के लेआउट से सटीक सिंक करने के लिए गणितीय डेटा मॉडल)
def generate_exact_ui_data():
    underlying_value = 23350.0  # इमेज के अनुसार ATM 23350 है
    strikes = [23600, 23550, 23500, 23450, 23400, 23350, 23300, 23250, 23200, 23150, 23100]
    
    rows = []
    for s in strikes:
        is_atm = "🟡 ATM " if s == 23350 else ""
        
        # सिमुलेटेड ओआई और चेंज इन ओआई (Lakhs में)
        ce_oi = np.random.uniform(50, 150) if s >= 23350 else np.random.uniform(20, 60)
        pe_oi = np.random.uniform(20, 60) if s >= 23350 else np.random.uniform(60, 180)
        ce_chg = np.random.uniform(-10, 40)
        pe_chg = np.random.uniform(-5, 50)
        
        # पीसीआर कैलकुलेशन
        strike_pcr = round(pe_oi / ce_oi, 2) if ce_oi > 0 else 1.0
        vol_pcr = round(np.random.uniform(0.8, 1.6), 2)
        
        # इमेज के अनुसार टारगेट प्रोबेबिलिटी और अलर्ट्स का लॉजिक
        target_pro = "65%" if s == 23350 else f"{np.random.randint(40, 58)}%"
        
        other_alerts = "5C Micro" if s == 23350 else "Structure"
        if s == 23500: other_alerts = "PE OB"
        elif s == 23550: other_alerts = "CE OB"
        elif s == 23150: other_alerts = "AI Blast"
        
        rows.append({
            "ST/Matrices": f"{is_atm}{s}",
            "CE/PE Phase": "Short Unwind",
            "VOL PCR": vol_pcr,
            "Target Pro%": target_pro,
            "Other": other_alerts,
            "CE OI (Lk)": round(ce_oi, 1),
            "PE OI (Lk)": round(pe_oi, 1),
            "CE ChgOI": round(ce_chg, 1),
            "PE ChgOI": round(pe_chg, 1),
            "Strike PCR": strike_pcr,
            "strike_num": s,
            "ce_raw_oi": ce_oi, "pe_raw_oi": pe_oi,
            "ce_raw_chg": ce_chg, "pe_raw_chg": pe_chg,
            "vol_pcr_raw": vol_pcr
        })
    return underlying_value, pd.DataFrame(rows)

underlying_value, df_matrix = generate_exact_ui_data()

# 2. +5 / -5 कंबाइंड सेपरेट मैट्रिक्स कैलकुलेशन
atm_idx = df_matrix[df_matrix['strike_num'] == 23350].index[0]
combined_11 = df_matrix.iloc[max(0, atm_idx-5):min(len(df_matrix), atm_idx+6)]

# कंबाइंड पीसीआर गणना
total_pe_oi = combined_11['pe_raw_oi'].sum()
total_ce_oi = combined_11['ce_raw_oi'].sum()
total_pe_chg = combined_11['pe_raw_chg'].sum()
total_ce_chg = combined_11['ce_raw_chg'].sum()

p5_minus5_oi_pcr = round(total_pe_oi / total_ce_oi, 2) if total_ce_oi > 0 else 1.0
p5_minus5_chg_pcr = round(total_pe_chg / total_ce_chg, 2) if total_ce_chg > 0 else 1.0
p5_minus5_vol_pcr = round(combined_11['vol_pcr_raw'].mean(), 2)

# 3. यूआई ग्रिड डिस्प्ले
st.subheader("📋 प्रोप्राइटरी हाइब्रिड डेटा मैट्रिक्स")

display_cols = ["ST/Matrices", "CE/PE Phase", "VOL PCR", "Target Pro%", "Other", "CE OI (Lk)", "PE OI (Lk)", "CE ChgOI", "PE ChgOI", "Strike PCR"]

def color_exact_ui(val):
    if "Short Unwind" in str(val): return 'color: #ff9933; font-weight: bold;'
    if "Structure" in str(val): return 'color: #ff3333;'
    if "PE OB" in str(val) or "Upward" in str(val): return 'color: #00ff00;'
    if "CE OB" in str(val): return 'color: #ff3333;'
    if "5C Micro" in str(val): return 'color: #cc66ff; font-weight: bold;'
    if "AI Blast" in str(val): return 'color: #ffff33; font-weight: bold;'
    if "🟡 ATM" in str(val): return 'background-color: #332b00; color: #ffff00; font-weight: bold;'
    return ''

styled_matrix = df_matrix[display_cols].style.map(color_exact_ui)
st.dataframe(styled_matrix, use_container_width=True, hide_index=True)

# 4. +5 / -5 पृथक मैट्रिक्स कॉलोनी
st.markdown("---")
st.subheader("🎯 पृथक मैट्रिक्स कॉलोनी (+5 / -5 रेंज सिग्नल्स)")

c1, c2, c3 = st.columns(3)
c1.metric("⚡ +5/-5 VOL PCR (RVOL Speed)", p5_minus5_vol_pcr)
c2.metric("📊 +5/-5 OI PCR (Major Support)", p5_minus5_oi_pcr)
c3.metric("🔥 +5/-5 Chg OI PCR (Instant Momentum)", p5_minus5_chg_pcr)

# 5. बॉटम सिग्नल्स पैनल्स
st.markdown("---")
st.subheader("🧠 Probability Fusion & Expansion Engine")

bc1, bc2, bc3, bc4 = st.columns(4)
bc1.error("💥 GAMMA BLAST: HIGH STRENGTH")
bc2.warning("🌀 CONSO STATUS: 2% (SQUEEZE)")
bc3.info("📉 INSTITUTIONAL VWAP: 23415")
bc4.success("🎯 AI CALL% / PUT%: 70% / 30%")

# 6. लोअर कैंडलस्टिक चार्ट
np.random.seed(10)
chart_close = 23450.0 + np.cumsum(np.random.normal(-5, 12, 40))
chart_open = chart_close + np.random.normal(0, 4, 40)
chart_high = np.maximum(chart_open, chart_close) + np.random.uniform(1, 8, 40)
chart_low = np.minimum(chart_open, chart_close) - np.random.uniform(1, 8, 40)

fig = go.Figure()
fig.add_trace(go.Candlestick(
    open=chart_open, high=chart_high, low=chart_low, close=chart_close,
    name="Price Action", increasing_line_color='#00ff00', decreasing_line_color='#ff3333'
))
fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark", height=300, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)
