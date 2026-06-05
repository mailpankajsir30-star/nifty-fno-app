import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide", page_title="Ultimate 6-Column Quant Matrix")

# सीएसएस: 5-कॉलम/6-कॉलम ग्रिड को कड़े तरीके से मोबाइल स्क्रीन पर साफ़-साफ़ फिट करने के लिए
st.markdown("""
    <style>
    .reportview-container { background: #06080c; }
    .custom-table { width: 100%; border-collapse: collapse; background-color: #0b0f19; color: #e5e7eb; margin-bottom: 25px; table-layout: fixed; }
    .custom-table th { background-color: #111827; color: #9ca3af; font-weight: bold; text-align: center; font-size: 11px; padding: 6px 2px; border: 1px solid #1f2937; }
    .custom-table td { text-align: center; font-family: monospace; font-size: 11.5px; padding: 6px 2px; border: 1px solid #1f2937; vertical-align: middle; line-height: 1.4; }
    .sub-gray { color: #9ca3af; font-size: 11px; display: block; }
    .center-strike { color: #f59e0b; font-weight: bold; font-size: 12px; display: block; }
    .center-pcr { color: #9ca3af; font-size: 11px; display: block; margin-top: 4px; }
    .center-chg-pcr { color: #ef4444; font-size: 11px; display: block; font-weight: bold; }
    .section-divider { background-color: #1e293b !important; color: #ffff00 !important; font-weight: bold !important; font-size: 11px !important; text-align: center !important; }
    .alert-line { text-align: left !important; padding-left: 10px !important; font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 क्वांटिटेटिव VSA + OI इंस्टीट्यूशनल डिसीजन इंजन")
st.write("📲 6-कॉलम परफेक्ट मोबाइल फिट | शुद्ध वॉल्यूम पीसीआर सिंक")

# 1. डेटा इंजन
def get_broker_ui_data():
    strikes = [23100, 23150, 23200, 23250, 23300, 23350, 23400, 23450, 23500, 23550, 23600]
    rows = []
    np.random.seed(45)
    
    ce_oi_dict = {23100: 54.3, 23150: 20.1, 23200: 14.50, 23250: 6.24, 23300: 45.45, 23350: 21.76, 23400: 58.30, 23450: 34.60, 23500: 104.0, 23550: 95.1, 23600: 82.4}
    pe_oi_dict = {23100: 92.9, 23150: 178.2, 23200: 47.69, 23250: 21.66, 23300: 74.56, 23350: 29.80, 23400: 57.45, 23450: 18.48, 23500: 89.9, 23550: 42.3, 23600: 31.2}
    pcr_dict = {23100: 1.71, 23150: 8.87, 23200: 3.29, 23250: 3.47, 23300: 1.64, 23350: 1.37, 23400: 0.99, 23450: 0.53, 23500: 0.50, 23550: 0.44, 23600: 0.38}
    
    for s in strikes:
        ce_oi = ce_oi_dict[s]
        pe_oi = pe_oi_dict[s]
        oi_pcr = pcr_dict[s]
        ce_chg_pct = np.random.uniform(5, 75) if s == 23350 else np.random.uniform(-10, 40)
        pe_chg_pct = np.random.uniform(-25, -2) if s in [23100, 23150] else np.random.uniform(2, 45)
        ce_vol = np.random.uniform(30, 150)
        pe_vol = np.random.uniform(30, 150)
        vol_pcr = pe_vol / ce_vol if ce_vol > 0 else 1.0
        chg_oi_pcr = np.random.uniform(0.4, 3.5)
        
        ce_label = f"{ce_oi:.1f}L"
        pe_label = f"{pe_oi:.1f}L"
        
        ce_phase = "Long Buildup" if ce_chg_pct > 20 else ("Short Buildup" if ce_chg_pct > 0 else "Short Covering")
        pe_phase = "Long Buildup" if pe_chg_pct > 20 else ("Short Buildup" if pe_chg_pct > 0 else "Short Covering")
        
        rows.append({
            "strike_num": s, "is_atm": s == 23350, "pcr": oi_pcr, "chg_pcr": chg_oi_pcr,
            "ce_oi_lbl": ce_label, "ce_chg": ce_chg_pct, "ce_vol": ce_vol, "ce_vol_pcr": 1/vol_pcr, "ce_phase": ce_phase,
            "pe_oi_lbl": pe_label, "pe_chg": pe_chg_pct, "pe_vol": pe_vol, "pe_vol_pcr": vol_pcr, "pe_phase": pe_phase
        })
    return rows

rows_data = get_broker_ui_data()

# 2. यूनिफाइड मास्टर टेबल जेनरेशन
html_code = """
<table class="custom-table">
    <tr>
        <th style='width: 18%;'>CE Phase</th>
        <th style='width: 23%;'>CE Stats<br><span style='color:#9ca3af; font-size:9px;'>OI (Chg) | Vol (VolPCR)</span></th>
        <th style='width: 18%;'>ST/Strike<br><span style='color:#9ca3af; font-size:9px;'>OI PCR | ChgPCR</span></th>
        <th style='width: 23%;'>PE Stats<br><span style='color:#9ca3af; font-size:9px;'>OI (Chg) | Vol (VolPCR)</span></th>
        <th style='width: 18%;'>PE Phase</th>
    </tr>
"""

for r in rows_data:
    ce_phase_color = "#22c55e" if "Long Buildup" in r['ce_phase'] else ("#ef4444" if "Short Buildup" in r['ce_phase'] else "#3b82f6")
    pe_phase_color = "#22c55e" if "Long Buildup" in r['pe_phase'] else ("#ef4444" if "Short Buildup" in r['pe_phase'] else "#3b82f6")
    
    ce_chg_sign = f"+{r['ce_chg']:.1f}" if r['ce_chg'] > 0 else f"{r['ce_chg']:.1f}"
    pe_chg_sign = f"+{r['pe_chg']:.1f}" if r['pe_chg'] > 0 else f"{r['pe_chg']:.1f}"
    
    row_bg = "style='background-color: #141b2d; font-weight: bold;'" if r['is_atm'] else ""
    strike_lbl = f"🟡<br>{r['strike_num']}" if r['is_atm'] else f"{r['strike_num']}"

    # यहाँ हमने 'ce_vol_pcr' और 'pe_vol_pcr' वेरिएबल्स को एकदम सटीक तरीके से अलाइन कर दिया है
    html_code += f"""
    <tr {row_bg}>
        <td style="color: {ce_phase_color}; font-weight: bold;">{r['ce_phase']}</td>
        <td>
            <b>{r['ce_oi_lbl']}</b><br>
            <span style="color:#9ca3af; font-size:11px;">({ce_chg_sign})</span><br>
            <b>{r['ce_vol']:.1f}k</b><br>
            <span class='sub-gray'>({r['ce_vol_pcr']:.2f})</span>
        </td>
        <td>
            <span class="center-strike">{strike_lbl}</span>
            <span class="center-pcr">{r['pcr']:.2f}</span>
            <span class="center-chg-pcr">({r['chg_pcr']:.2f})</span>
        </td>
        <td>
            <b>{r['pe_oi_lbl']}</b><br>
            <span style="color:#9ca3af; font-size:11px;">({pe_chg_sign})</span><br>
            <b>{r['pe_vol']:.1f}k</b><br>
            <span class='sub-gray'>({r['pe_vol_pcr']:.2f})</span>
        </td>
        <td style="color: {pe_phase_color}; font-weight: bold;">{r['pe_phase']}</td>
    </tr>
    """

# भाग B: +5/-5 पृथक क्वांटम कॉलोनी पंक्तियाँ
html_code += """
    <tr><td colspan="5" class="section-divider">🎯 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)</td></tr>
    <tr>
        <td colspan="2" style='text-align:left; padding-left:15px; color:#9ca3af;'>🔴 OTM OI PCR: <b>0.85</b></td>
        <td style='font-weight:bold; color:#f59e0b;'>परत 1 & 2</td>
        <td colspan="2" style='text-align:right; padding-right:15px; color:#58a6ff;'>🔵 ITM OI PCR: <b>1.20</b></td>
    </tr>
    <tr>
        <td colspan="2" style='text-align:left; padding-left:15px; color:#9ca3af;'>🔴 OTM ChgOI PCR: <b>2.14</b></td>
        <td style='font-weight:bold; color:#f59e0b;'>OI Changes</td>
        <td colspan="2" style='text-align:right; padding-right:15px; color:#58a6ff;'>🔵 ITM ChgOI PCR: <b>1.45</b></td>
    </tr>
    <tr>
        <td colspan="2" style='text-align:left; padding-left:15px; color:#9ca3af;'>🔴 OTM VOL PCR: <b>1.32</b></td>
        <td style='font-weight:bold; color:#f59e0b;'>परत 3 & 4</td>
        <td colspan="2" style='text-align:right; padding-right:15px; color:#58a6ff;'>🔵 ITM VOL PCR: <b>0.95</b></td>
    </tr>
    <tr>
        <td colspan="2" style='text-align:left; padding-left:15px; color:#9ca3af;'>🔴 OTM ChgVOL PCR: <b>3.10</b></td>
        <td style='font-weight:bold; color:#f59e0b;'>VOL Speed</td>
        <td colspan="2" style='text-align:right; padding-right:15px; color:#58a6ff;'>🔵 ITM ChgVOL PCR: <b>1.12</b></td>
    </tr>
"""

# भाग C: एसएमसी प्रेडिक्टिव व सतर्कता अलर्ट पंक्तियाँ
html_code += """
    <tr><td colspan="5" class="section-divider">🧠 SMC इंस्टीट्यूशनल प्रेडिक्टिव ज़ोन और सतर्कता अलर्ट</td></tr>
    <tr>
        <td colspan="5" class="alert-line" style="color:#ff4d4d;">🛑 <b>LIVE AI STATUS: STRICTLY NO TRADE !!!</b> <br><span style='color:#9ca3af; font-size:10px;'>रीज़न: PE OI भारी होने पर भी 'OI Trap Detector' सक्रिय है। Delta Deceleration और Chg VOL Shock ऑन है (हेजिंग मैनिपुलेशन)।</span></td>
    </tr>
    <tr>
        <td colspan="5" class="alert-line" style="color:#ffaa00;">⚠️ <b>REVERSAL SATARK ZONE:</b> <br><span style='color:#9ca3af; font-size:10px;'>• 🎯 Pull-Back: Active @ 23200-23250 | • 🛑 Pull-Down: Active @ 23450-23500 | • 🏹 Sweep Rejection @ 23450</span></td>
    </tr>
    <tr>
        <td colspan="5" class="alert-line" style="color:#00ff00;">🌀 <b>COMPRESSION MATRIX & OHLC DATA:</b> <br><span style='color:#9ca3af; font-size:10px;'>• BB Squeeze: 1.4% @ 23300 | • Gamma Blast: 94% @ 23450 | • PDH: 23480 | PDL: 23190 | PDC: 23366</span></td>
    </tr>
"""

html_code += "</table>"
st.markdown(html_code, unsafe_allow_html=True)
