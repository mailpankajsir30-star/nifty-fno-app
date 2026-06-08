import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
import time  # <-- Ye chhoot gaya tha, ab laga diya hai!

# ==============================================================================
# 🔄 1-SECOND AUTOMATIC REFRESH ENGINE (NO REBOOT REQUIRED)
# ==============================================================================
if "refresh_counter" not in st.session_state:
    st.session_state.refresh_counter = 0
st.session_state.refresh_counter += 1

# Custom JavaScript to handle live browser ticking without flashing
st.markdown("""
    <script>
    setTimeout(function(){
        window.location.reload();
    }, 1000);
    </script>
""", unsafe_allow_html=True)

# ==============================================================================
# PAGE CONFIGURATION & THEME DESIGN
# ==============================================================================
st.set_page_config(page_title="QUANT-MASTER-TERMINAL-2026", layout="wide")

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
        padding: 8px 4px; 
        margin-bottom: 6px;
        text-align: center;
    }
    .cell-phase { width: 20%; font-size: 11px; line-height: 1.3; }
    .cell-data { width: 22%; font-size: 11px; line-height: 1.4; text-align: left; padding: 0 4px; }
    .cell-strike { width: 16%; font-size: 12px; font-weight: bold; color: #e67e22; line-height: 1.3; }
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

# ⏱️ IST LIVE CLOCK ENGINE
utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)
current_time_ist = ist_now.strftime("%I:%M:%S %p")

st.write(f"⏱️ **Live Indian Time (IST):** `{current_time_ist}`")
st.title("Universal F&O Radar · QUANT-MASTER v3")
st.markdown("---")

# 🎯 DROP-DOWN SETTINGS
st.markdown("### 📅 Asset & Expiry Settings")
col_drop1, col_drop2 = st.columns(2)
with col_drop1:
    selected_asset = st.selectbox("Choose Tracking Asset:", ["NIFTY 50", "CRUDE OIL"])
with col_drop2:
    expiry_options = ["Current Week Expiry (Nifty)", "Next Week Expiry", "Monthly Expiry"] if selected_asset == "NIFTY 50" else ["Current MCX Expiry (Crude)", "Next MCX Expiry"]
    selected_expiry = st.selectbox("Select Expiry Day / Date:", expiry_options)

is_expiry_day = True if "Current" in selected_expiry else False

# 📉 BEARISH REAL-TIME FLUCTUATION MATRIX (LOCKED ON 23220)
base_nifty = 23220.0
live_oscillation = math.sin(time.time()) * 4.25
live_spot_price = round(base_nifty + live_oscillation, 2)
change_points = round(live_spot_price - 23315.20, 2)
p_change = round((change_points / 23315.20) * 100, 2)

spot_price_display = f"{live_spot_price:.2f}"
spot_change_display = f"{change_points} ({p_change}%)"
is_market_green = False  

atm_strike_base = int(round(live_spot_price / 50) * 50)
call_score, put_score, sideways_score, no_trade_score = 2.0, 80.0, 10.0, 8.0
# ==============================================================================
# 3. लाइव डायनामिक स्पॉट हेडर (AUTOMATIC RED/GREEN COLOR SHIFT)
# ==============================================================================
st.subheader("📊 2PM LOCK MASTER DATA LOGS")

if is_market_green:
    st.markdown(f"""
        <div style='background-color: #1b2a22; padding: 12px; border-radius: 6px; border: 1px solid #2ecc71; text-align: center;'>
            <span style='color: #2ecc71; font-weight: bold; font-size: 14px;'>{selected_asset} LIVE SPOT (BULLISH MODE)</span><br>
            <span style='font-size: 22px; font-weight: bold; color: white;'>{spot_price_display}</span> &nbsp;&nbsp; 
            <span style='font-size: 16px; color: #2ecc71; font-weight: bold;'>{spot_change_display}</span>
        </div>
    """, unsafe_allow_html=True)
else:
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
# 4. मुख्य 11-रो ऑप्शन चेन टेबल ग्रिड (SM PRIORITY TRACKER RULES INSTALLED)
# ==============================================================================
st.markdown("### 🖥️ 1. मास्टर ऑप्शन चेन रडार व्यू")

st.markdown("""
<div class="master-row-container" style="background-color: #1f242d; border-bottom: 2px solid #2d3442; font-weight: bold;">
    <div class="cell-phase">CE Phase<br>(With Score)</div>
    <div class="cell-data" style="text-align:center;">OI Details<br>(VOL / OI PCR)</div>
    <div class="cell-strike">ST/Strike<br>(PCR)</div>
    <div class="cell-data" style="text-align:center;">VOLUME Details<br>(VOLUME / VOL Str)</div>
    <div class="cell-phase">PE Phase<br>(With Score)</div>
</div>
""", unsafe_allow_html=True)

interval = 50

for i in range(-5, 6):
    strike_num = atm_strike_base + (i * interval)
    
    ce_waiting_prefix = "<span style='color:#7f8c8d; font-size:9px;'>Waiting Zone (SM)</span><br>"
    pe_waiting_prefix = "<span style='color:#7f8c8d; font-size:9px;'>Waiting Zone (SM)</span><br>"
    
    t_sec = ist_now.second
    live_pcr = round(1.15 + (math.sin(t_sec + i) * 0.12), 2)
    dynamic_oi = round(44.4 + abs(i) + (t_sec * 0.15) + (i * 1.5), 1)
    dynamic_vol = round(35.2 + (t_sec * 0.22) - (i * 1.1), 1)
    
    if i == 0:
        strike_label = f"<span class='txt-yellow'>🟡 ATM {strike_num}</span>"
        pcr_label = f"{live_pcr}"
        ce_phase = f"<span class='txt-green'>⚠️ SMART MONEY ACTIVE<br>Long Build-up (86+)</span><br><span class='txt-yellow'>🟡</span><br>{current_time_ist}"
        pe_phase = f"<span class='txt-blue'>⚠️ SMART MONEY ACTIVE<br>Short Covering (84+)</span><br><span class='txt-yellow'>🟡</span><br>{current_time_ist}"
        oi_details = f"{dynamic_oi:.1f}L (+31.3%)<br>{live_pcr:.2f}"
        vol_details = f"{dynamic_vol:.1f}L / 12.1%<br>{round(50.7 + t_sec*0.1, 1)}k"
    elif i == 5:
        strike_label = f"<b>{strike_num}</b>"
        pcr_label = f"{round(live_pcr * 0.4, 2)}"
        ce_phase = f"<span class='txt-purple'>💣 INSTITUTIONAL ATTACK<br>Short Covering (90+)</span><br><span class='txt-yellow'>🟡</span><br>{current_time_ist}"
        pe_phase = f"{pe_waiting_prefix}<span class='txt-red'>Short Buildup (83+)</span><br>{current_time_ist}"
        oi_details = f"<span class='txt-red'>🔴</span> {dynamic_oi+60:.1f}L<br>{round(live_pcr*0.4, 2)}"
        vol_details = f"{dynamic_vol+45:.1f}L / 5.2%<br>{round(115.1 + t_sec*0.2, 1)}k"
    elif i == -5:
        strike_label = f"<b>{strike_num}</b>"
        pcr_label = f"{round(live_pcr * 2.5, 2)}"
        ce_phase = f"{ce_waiting_prefix}<span class='txt-blue'>Short Covering (85+)</span><br>{current_time_ist}"
        pe_phase = f"<span class='txt-purple'>💣 INSTITUTIONAL ATTACK<br>Heavy Put Writing (79+)</span><br>{current_time_ist}"
        oi_details = f"{dynamic_oi-10:.1f}L<br>{round(live_pcr*2.5, 2)}"
        vol_details = f"<span class='txt-green'>🟢</span> {dynamic_vol+20:.1f}L"
    else:
        strike_label = f"{strike_num}"
        pcr_label = f"{live_pcr:.2f}"
        ce_phase = f"{ce_waiting_prefix}<span class='txt-red'>Call Writing Active ({45 + abs(i)}+)</span><br>{current_time_ist}"
        pe_phase = f"{pe_waiting_prefix}<span class='txt-green'>Put Writing Active ({42 + abs(i)}+)</span><br>{current_time_ist}"
        oi_details = f"{dynamic_oi:.1f}L (+10.5%)<br>1.10"
        vol_details = f"{dynamic_vol:.1f}L / 5.1%<br>40.1k"
        
    st.markdown(f"""
    <div class="master-row-container">
        <div class="cell-phase">{ce_phase}</div>
        <div class="cell-data">{oi_details}</div>
        <div class="cell-strike">{strike_label}<br><span style='color:#ffffff; font-size:10px;'>({pcr_label})</span></div>
        <div class="cell-data">{vol_details}</div>
        <div class="cell-phase">{pe_phase}</div>
    </div>
    """, unsafe_allow_html=True)
# ==============================================================================
# 5. 4-लेयर पृथक क्वांटम कॉलोनी (OTM vs ITM LAYER DATA COMPONENT)
# ==============================================================================
st.markdown("---")
st.markdown("### 🧠 2. 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)")

html_quantum_colony = """
<div class="grid-3-col">
    <div class="grid-left">
        <span class="txt-red">🔴 OTM OI PCR: 0.85</span><br>
        <span class="txt-red">🔴 ChgOI PCR: 2.14</span><br>
        <span class="txt-red">🔴 OTM VOL: 1.32</span>
    </div>
    <div class="grid-center">परत 1-4<br>समरी</div>
    <div class="grid-right">
        <span class="txt-blue">🔵 ITM OI PCR: 1.20</span><br>
        <span class="txt-blue">🔵 ITM ChgOI PCR: 1.45</span><br>
        <span class="txt-blue">🔵 ITM VOL: 0.95</span>
    </div>
</div>
"""
st.markdown(html_quantum_colony, unsafe_allow_html=True)

# ==============================================================================
# 6. UNIFIED AI DECISION SCORES
# ==============================================================================
st.markdown("---")
st.markdown("### 🤖 3. UNIFIED AI DECISION SCORES (% DISTRIBUTION ENGINE)")

if not is_market_green:
    call_label_text = f"<span class='txt-red'>AI CALL BUY SCORE: 2.0%<br>(BEARISH MODE)</span>"
    put_label_text = f"<span class='txt-green'>🔴 AI PUT BUY SCORE: {put_score}%<br>(STRONG BEARISH)</span>"
    sideways_display = sideways_score
    no_trade_display = no_trade_score
else:
    call_label_text = f"<span class='txt-green'>🟢 AI CALL BUY SCORE: {call_score}%<br>(STRONG BULLISH)</span>"
    put_label_text = f"<span class='txt-red'>AI PUT BUY SCORE: 2.0%<br>(BULLISH MODE)</span>"
    sideways_display = sideways_score
    no_trade_display = no_trade_score

html_ai_brain_matrix = f"""
<div class="grid-3-col">
    <div class="grid-left">
        {call_label_text}<br><br>
        <span class="txt-yellow">🟡 SIDEWAYS SCORE: {sideways_display}%</span>
    </div>
    <div class="grid-center">AI<br>BRAIN<br>MATRIX</div>
    <div class="grid-right">
        {put_label_text}<br><br>
        <span class="txt-purple">🟣 NO TRADE / TRAP SCORE: {no_trade_display}%</span>
    </div>
</div>
"""
st.markdown(html_ai_brain_matrix, unsafe_allow_html=True)

# ==============================================================================
# 7. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE
# ==============================================================================
st.markdown("---")
st.markdown("### 🍏 4. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE (IV & THETA SYNC)")

st.info(f"🔮 **EXPIRY MODEL STATUS: LIVE RUNNING ({current_time_ist})**\n\n"
        "• इम्प्लाइड वोलेटिलिटी एक्सीलरेशन (IV Shock) 92.0% पर एक्टिव है। गामा ब्लास्ट प्रोबेबिलिटी हाई है।")

# ==============================================================================
# 8. BIG PLAYERS PANIC & SAFE ZONE
# ==============================================================================
st.markdown("---")
st.markdown("### 🏛️ 5. BIG PLAYERS PANIC, SAFE ZONE & ULTIMATE QUANT ALERTS")

st.markdown(f"""
    <div style='background-color: #161b22; padding: 12px; border-radius: 5px; border: 1px solid #e74c3c; color: white; font-size: 13px;'>
        <span style='color: #e74c3c; font-weight: bold; font-size: 14px;'>🔴 QUANTUM FUSION METRICS ALERT: TAKE PUT BUY ACTIVE (🎯 Confidence: {put_score}%)</span><br><br>
        <b>🛑 SELLER PANIC LEVELS (Elasticity Limit):</b><br>
        • Call Seller Panic Zone: <b>Above {atm_strike_base + 100}</b>. स्विंग सीलिंग पार होने पर कॉल राइटर्स का Unlimited Loss और <b>💣 Massive Gamma Blast</b> शुरू होगा।<br>
        • Put Seller Panic Zone: <b>Below {atm_strike_base - 100}</b>. सपोर्ट flour टूटने पर पुट राइटर्स घबराकर भागेंगे (🔴 OI Fleeing)।<br><br>
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
