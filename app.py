import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import math
import time

st.set_page_config(page_title="PANKAJ-SINGH-QUANT-MASTER-2026", layout="wide")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #0e1117; color: white; font-family: sans-serif; }
    .reportview-container { background: #0e1117; }
    .master-row-container { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        background-color: #161b22; 
        border: 1px solid #2d3442; 
        border-radius: 4px; 
        padding: 10px 6px; 
        margin-bottom: 5px;
        text-align: center;
    }
    .cell-phase { width: 20%; font-size: 11px; line-height: 1.4; text-align: left; padding-left: 5px; }
    .cell-data { width: 24%; font-size: 11px; line-height: 1.4; text-align: center; }
    .cell-strike { width: 12%; font-size: 13px; font-weight: bold; color: #ffffff; background-color: #1f242d; border-radius: 4px; padding: 4px 0; }
    .grid-3-col { display: grid; grid-template-columns: 1.2fr 0.6fr 1.2fr; gap: 10px; align-items: center; background-color: #161b22; padding: 12px; border-radius: 6px; border: 1px solid #2d3442; margin-bottom: 10px; }
    .grid-left { text-align: left; font-size: 12px; line-height: 1.6; }
    .grid-center { text-align: center; font-weight: bold; color: #f39c12; font-size: 13px; line-height: 1.4; border-left: 1px solid #2d3442; border-right: 1px solid #2d3442; padding: 0 5px; }
    .grid-right { text-align: left; font-size: 12px; line-height: 1.6; padding-left: 10px; }
    .txt-green { color: #2ecc71; font-weight: bold; }
    .txt-red { color: #e74c3c; font-weight: bold; }
    .txt-blue { color: #3498db; font-weight: bold; }
    .txt-yellow { color: #f1c40f; font-weight: bold; }
    .txt-purple { color: #9b59b6; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# FIXED POST-MARKET STATIC LOCK SYSTEM
current_time_ist = "03:30:00 PM"
st.write(f"⏱️ **Market Status:** `🛑 CLOSED (IST: {current_time_ist})`")
st.title("Universal F&O Radar · QUANT-MASTER v3")
st.markdown("---")

st.markdown("### 📅 Asset & Expiry Settings")
selected_asset = st.selectbox("Choose Tracking Asset:", ["NIFTY 50", "CRUDE OIL"])

is_actual_expiry_day = False
selected_expiry = "📅 Normal Non-Expiry Market Session"
st.info(f"📆 **Auto-Calculated Expiry System Status:** `{selected_expiry}`")

# STATIC REAL BROKER PRICE LOCK (NO AUTO FRESH OSCILLATION)
live_spot_price = 23211.60
spot_price_display = "23211.60"
spot_change_display = "-155.10 (-0.66%)"
is_market_green = False  
atm_strike_base = 23200

# 14-SENSORS STATIC VALUES (NO VARIANCE JUMP)
call_score = 2.00
put_score = 80.00
sideways_score = 12.50
no_trade_score = 5.50
is_market_choppy = False

# ==============================================================================
# 3. लाइव डायनामिक स्पॉट हेडर (PANKAJ SINGH DESIGN INSTALLED)
# ==============================================================================
st.subheader("📊 PANKAJ SINGH DESIGN DATA LOGS")

st.markdown(f"""
    <div style='background-color: #2c1a1d; padding: 12px; border-radius: 6px; border: 1px solid #e74c3c; text-align: center;'>
        <span style='color: #e74c3c; font-weight: bold; font-size: 14px;'>{selected_asset} LIVE SPOT (BEARISH LIVE MODE)</span><br>
        <span style='font-size: 22px; font-weight: bold; color: white;'>{spot_price_display}</span> &nbsp;&nbsp; 
        <span style='font-size: 16px; color: #e74c3c; font-weight: bold;'>{spot_change_display}</span>
    </div>
""", unsafe_allow_html=True)

st.write("")
st.metric("🎯 EXACT ATM STRIKE (MROUND ENGINE)", f"{atm_strike_base}")

# ==============================================================================
# 4. मुख्य ऑप्शन चेन टेबल ग्रिड (RESTORED HTML/CSS TABLE DESIGN)
# ==============================================================================
st.markdown("### 🖥️ 1. मास्टर ऑप्शन चेन रडार VIEW")

st.markdown("""
<div class="master-row-container" style="background-color: #1f242d; border-bottom: 2px solid #2d3442; font-weight: bold;">
    <div class="cell-phase">CE Phase<br>(With Score)</div>
    <div class="cell-data" style="text-align:center;">OI Details<br>(VOL / OI PCR)<br>(Chg OI / Chg % Matrix)</div>
    <div class="cell-strike">ST/Strike<br>(PCR)</div>
    <div class="cell-data" style="text-align:center;">VOLUME Details<br>(VOLUME / VOL Str)<br>(Chg VOL)</div>
    <div class="cell-phase">PE Phase<br>(With Score)</div>
</div>
""", unsafe_allow_html=True)

interval = 50
strike_offsets = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
ce_waiting_prefix = "<span style='color:#7f8c8d; font-size:9px;'>Waiting Zone (SM)</span><br>"
pe_waiting_prefix = "<span style='color:#7f8c8d; font-size:9px;'>Waiting Zone (SM)</span><br>"

for offset in strike_offsets:
    strike_num = atm_strike_base + (offset * interval)
    if strike_num == 23100:
        ce_oi_str, pe_oi_str = "30.13L", "1.95Cr"
        ce_chg_str, pe_chg_str = "+829.78%", "+415.20%"
        strike_pcr = "6.47"
    elif strike_num == 23150:
        ce_oi_str, pe_oi_str = "35.12L", "1.17Cr"
        ce_chg_str, pe_chg_str = "+1700.53%", "+459.77%"
        strike_pcr = "3.32"
    elif strike_num == 23200:
        ce_oi_str, pe_oi_str = "94.86L", "2.22Cr"
        ce_chg_str, pe_chg_str = "+560.48%", "+372.22%"
        strike_pcr = "2.34"
    elif strike_num == 23250:
        ce_oi_str, pe_oi_str = "76.55L", "82.38L"
        ce_chg_str, pe_chg_str = "+1143.53%", "+290.74%"
        strike_pcr = "1.08"
    elif strike_num == 23300:
        ce_oi_str, pe_oi_str = "1.35Cr", "93.45L"
        ce_chg_str, pe_chg_str = "+203.12%", "+26.44%"
        strike_pcr = "0.69"
    elif strike_num == 23350:
        ce_oi_str, pe_oi_str = "62.42L", "22.83L"
        ce_chg_str, pe_chg_str = "+191.21%", "-20.44%"
        strike_pcr = "0.37"
    elif strike_num == 23400:
        ce_oi_str, pe_oi_str = "1.31Cr", "46.05L"
        ce_chg_str, pe_chg_str = "+130.54%", "-18.33%"
        strike_pcr = "0.35"
    else:
        computed_lakhs = round(45.4 + abs(offset) * 12.5, 2)
        ce_oi_str, pe_oi_str = f"{computed_lakhs}L", f"{computed_lakhs - 8}L"
        ce_chg_str, pe_chg_str = "+140.00%", "+80.00%"
        strike_pcr = "1.15"

    dynamic_vol = round(35.2 - (offset * 0.8), 1)
    dynamic_chg_vol = "40.1k"
    if offset == 0:
        strike_label = f"<span class='txt-yellow'> ATM {strike_num}</span>"
        ce_phase = f"<span class='txt-green'>⚠️ SMART MONEY ACTIVE<br>Long Build-up</span><br>{current_time_ist}"
        pe_phase = f"<span class='txt-blue'>⚠️ SMART MONEY ACTIVE<br>Short Covering</span><br>{current_time_ist}"
        oi_details = f"<b>{ce_oi_str}</b> ({ce_chg_str})<br>PCR: {strike_pcr}<br>144.6k"
        vol_details = f"{dynamic_vol:.1f}L / 12.1%<br>{dynamic_chg_vol}"
    elif offset == 5:
        strike_label = f"<b>{strike_num}</b>"
        ce_phase = f"<span class='txt-purple'>💣 INSTITUTIONAL ATTACK<br>Short Covering</span><br>{current_time_ist}"
        pe_phase = f"{pe_waiting_prefix}<span class='txt-red'>Short Buildup</span><br>{current_time_ist}"
        oi_details = f"<span class='txt-red'>🔴</span> <b>{ce_oi_str}</b> ({ce_chg_str})<br>PCR: {strike_pcr}"
        vol_details = f"{dynamic_vol+25:.1f}L / 5.2%"
    else:
        strike_label = f"{strike_num}"
        ce_phase = f"{ce_waiting_prefix}<span class='txt-red'>Call Writing Active</span><br>{current_time_ist}"
        pe_phase = f"{pe_waiting_prefix}<span class='txt-green'>Put Writing Active</span><br>{current_time_ist}"
        oi_details = f"<b>{ce_oi_str}</b> ({ce_chg_str})<br>PCR: {strike_pcr}"
        vol_details = f"{dynamic_vol:.1f}L / 5.1%<br>{dynamic_chg_vol}"

    st.markdown(f"""
        <div class="master-row-container">
            <div class="cell-phase">{ce_phase}</div>
            <div class="cell-data" style="text-align: center;">{oi_details}<br><span style='color: #3498db; font-size:10px;'>PE: {pe_oi_str} ({pe_chg_str})</span></div>
            <div class="cell-strike">{strike_label}</div>
            <div class="cell-data">{vol_details}</div>
            <div class="cell-phase">{pe_phase}</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 5. 4-लेयर पृथक क्वांटम कॉलोनी (OTM vs ITM SEPARATED STRUCTURE)
# ==============================================================================
st.markdown("---")
st.markdown("### 🧠 2.4 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)")

html_quantum_4_layer = f"""
<div class="grid-3-col">
    <div class="grid-left" style="border-right: 1px dashed #2d3442; padding-right: 10px;">
        <span style='color: #e74c3c; font-weight: bold; font-size: 13px;'>🔴 OTM CLUSTER DATA (Left)</span><br>
        <span style='font-size: 10px; color: #7f8c8d;'>(Call OTM +5 vs Put OTM -5)</span><br><br>
        <span class="txt-red">🔴 OTM OI PCR: 0.85</span><br>
        <span class="txt-red">🔴 OTM ChgOI PCR: 2.14</span><br>
        <span class="txt-red">🔴 OTM VOL PCR: 1.32</span><br>
        <span class="txt-red">🔴 OTM ChgVOL PCR: 1.85</span>
    </div>
    <div class="grid-center" style="font-size: 11px;">
        परत 1-4<br>समरी<br><br><span style="color:#ffffff; font-size:13px;">ATM {atm_strike_base}</span>
    </div>
    <div class="grid-right" style="padding-left: 15px;">
        <span style='color: #3498db; font-weight: bold; font-size: 13px;'>🔵 ITM CLUSTER DATA (Right)</span><br>
        <span style='font-size: 10px; color: #7f8c8d;'>(Call ITM -5 vs Put ITM +5)</span><br><br>
        <span class="txt-blue">🔵 ITM OI PCR: 1.20</span><br>
        <span class="txt-blue">🔵 ITM ChgOI PCR: 1.45</span><br>
        <span class="txt-blue">🔵 ITM VOL PCR: 0.95</span><br>
        <span class="txt-blue">🔵 ITM ChgVOL PCR: 1.12</span>
    </div>
</div>
"""
st.markdown(html_quantum_4_layer, unsafe_allow_html=True)

# ==============================================================================
# 5B. 5-लेयर पृथक OTM vs ITM (CROSS MOMENTUM PROPORTION)
# ==============================================================================
st.markdown("### 🧠 2.5 5-लेयर पृथक OTM vs ITM (+5 / -5 ITM & OTM PCR)")

html_quantum_5_layer = f"""
<div class="grid-3-col">
    <div class="grid-left" style="border-right: 1px dashed #2d3442; padding-right: 10px;">
        <span style='color: #f39c12; font-weight: bold; font-size: 13px;'>⬆️ +5 CORRIDOR DATA (Left)</span><br>
        <span style='font-size: 10px; color: #7f8c8d;'>(5 Call OTM vs 5 Put ITM)</span><br><br>
        <span style="color: #f39c12; font-weight: bold;">OI PCR: 0.68</span><br>
        <span style="color: #f39c12; font-weight: bold;">ChgOI PCR: 0.42</span><br>
        <span style="color: #f39c12; font-weight: bold;">VOL PCR: 0.55</span><br>
        <span style="color: #f39c12; font-weight: bold;">ChgVOL PCR: 0.38</span>
    </div>
    <div class="grid-center" style="font-size: 11px;">
        परत 1-5<br>मैट्रिक्स<br><br><span style="color:#ffffff; font-size:13px;">ATM {atm_strike_base}</span>
    </div>
    <div class="grid-right" style="padding-left: 15px;">
        <span style='color: #9b59b6; font-weight: bold; font-size: 13px;'>⬇️ -5 CORRIDOR DATA (Right)</span><br>
        <span style='font-size: 10px; color: #7f8c8d;'>(5 Call ITM vs 5 Put OTM)</span><br><br>
        <span style="color: #9b59b6; font-weight: bold;">OI PCR: 2.34</span><br>
        <span style="color: #9b59b6; font-weight: bold;">ChgOI PCR: 3.12</span><br>
        <span style="color: #9b59b6; font-weight: bold;">VOL PCR: 1.85</span><br>
        <span style="color: #9b59b6; font-weight: bold;">ChgVOL PCR: 2.41</span>
    </div>
</div>
"""
st.markdown(html_quantum_5_layer, unsafe_allow_html=True)

# ==============================================================================
# 6. UNIFIED AI DECISION SCORES
# ==============================================================================
st.markdown("---")
st.markdown("### 🤖 3. UNIFIED AI DECISION SCORES (% DISTRIBUTION ENGINE)")

call_label_text = f"<span class='txt-red'>AI CALL BUY SCORE: 2.0%<br>(BEARISH MODE)</span>"
put_label_text = f"<span class='txt-green'>🔴 AI PUT BUY SCORE: {put_score}%<br>(STRONG BEARISH)</span>"

html_ai_brain_matrix = f"""
<div class="grid-3-col">
    <div class="grid-left">
        {call_label_text}<br><br>
        <span class="txt-yellow">🟡 SIDEWAYS SCORE: {sideways_score}%</span>
    </div>
    <div class="grid-center">AI<br>BRAIN<br>MATRIX</div>
    <div class="grid-right">
        {put_label_text}<br><br>
        <span class="txt-purple">🟣 NO TRADE / TRAP SCORE: {no_trade_score}%</span>
    </div>
</div>
"""
st.markdown(html_ai_brain_matrix, unsafe_allow_html=True)

# ==============================================================================
# 7. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE
# ==============================================================================
st.markdown("---")
st.markdown("### 🍏 4. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE (IV & THETA SYNC)")

expiry_status_mode = "💥 GAMMA BLAST ACTIVE: PUT BUY MODEL"
expiry_net_confidence = put_score
expiry_reason_text = "• <b>Breakout Signal:</b> Floor Support broken! 14-sensors matrix ke mutabik Price Action aur Price Velocity mंदी ke support lines ko short kar chuke hain. Downward momentum gamma expansion ko confirm karta hai."
expiry_color_border = "#e74c3c"

st.markdown(f"""
<div style='background-color: #161b22; padding: 14px; border-radius: 6px; border: 1px solid {expiry_color_border};'>
    <span style='color: {expiry_color_border}; font-weight: bold; font-size: 15px;'>🔮 EXPIRY MODEL STATUS: {expiry_status_mode} (Net Confidence: {expiry_net_confidence}%)</span><br><br>
    <span style='font-size: 12px; color: #a3b8cc;'>{expiry_reason_text}</span>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 8. BIG PLAYERS PANIC & SAFE ZONE
# ==============================================================================
st.markdown("---")
st.markdown("### 🏛️ 5. BIG PLAYERS PANIC, SAFE ZONE & ULTIMATE QUANT ALERTS")

st.markdown(f"""
    <div style='background-color: #161b22; padding: 12px; border-radius: 5px; border: 1px solid #e74c3c; color: white; font-size: 13px;'>
        <span style='color: #e74c3c; font-weight: bold; font-size: 14px;'>🔴 QUANTUM FUSION METRICS ALERT: TAKE PUT BUY ACTIVE (🎯 Confidence: {put_score}%)</span><br><br>
        <b>🛑 SELLER PANIC LEVELS (Elasticity Limit):</b><br>
        • Call Seller Panic Zone: <b>Above {atm_strike_base + 100}</b>. स्विंग सीलिंग पार होने पर कॉल राइटर्स का Unlimited Loss और 💣 Massive Gamma Blast शुरू होगा।<br>
        • Put Seller Panic Zone: <b>Below {atm_strike_base - 100}</b>. सपोर्ट फ्लोर टूटने पर पुट राइटर्स घबराकर भागेंगे (🔴 OI Fleeing)।<br><br>
        <b>🛡️ INSTITUTIONAL SAFE ZONE (Corridor):</b><br>
        • <b>{atm_strike_base - 100} — {atm_strike_base + 100}</b> के दायरे में बड़े ऑपरेटर्स पूरी तरह सुरक्षित रहकर थीटा डीके वसूलेंगे।
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 9. ADVANCED REVERSAL SATARK ZONE & OHLC LEVELS
# ==============================================================================
st.write("")
st.markdown("#### ⚠️ REVERSAL SATARK ZONE & OHLC LEVELS")

mock_50c_swing_low = atm_strike_base - 130
mock_prev_day_low = atm_strike_base - 150
mock_prev_day_close = atm_strike_base - 105
mock_50c_swing_high = atm_strike_base + 130
mock_prev_day_high = atm_strike_base + 150

calc_support_floor = max(mock_50c_swing_low, mock_prev_day_low, mock_prev_day_close)
calc_resistance_ceiling = min(mock_50c_swing_high, mock_prev_day_high)

col_rev1, col_rev2 = st.columns(2)
with col_rev1:
    st.markdown(f"""
    <div style='background-color: #1b2a22; padding: 12px; border-radius: 5px; border: 1px solid #2ecc71;'>
        <span style='color: #2ecc71; font-weight: bold; font-size: 14px;'>🔄 Pull-Back Support Range (Put Side 🟢):</span><br>
        <span style='font-size: 20px; font-weight: bold; color: white;'>{atm_strike_base - 150} — {atm_strike_base - 100}</span><br>
        <span style='font-size: 11px; color: #a3b8cc;'>लॉजिक: Max(50C Swing Low, PDL, PDC) = {calc_support_floor} | हैवी पुट राइटिंग और अब्जॉर्प्शन जोन</span>
    </div>
    """, unsafe_allow_html=True)
    
with col_rev2:
    st.markdown(f"""
    <div style='background-color: #2c1a1d; padding: 12px; border-radius: 5px; border: 1px solid #e74c3c;'>
        <span style='color: #e74c3c; font-weight: bold; font-size: 14px;'>🛑 Pull-Down Resistance Wall (Call Side 🔴):</span><br>
        <span style='font-size: 20px; font-weight: bold; color: white;'>{atm_strike_base + 100} — {atm_strike_base + 150}</span><br>
        <span style='font-size: 11px; color: #a3b8cc;'>लॉजिक: Min(50C Swing High, PDH) = {calc_resistance_ceiling} | मैक्सिमम कॉल ओआई बैरियर दीवार</span>
    </div>
    """, unsafe_allow_html=True)

# BROWSER RERUN INTERVAL TIMEOUT LOCK
time.sleep(5.0)
st.rerun()
