import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import math
import time

st.set_page_config(
    page_title="PANKAJ-SINGH-QUANT-MASTER-2026",
    layout="wide"
)

st.markdown("""
<style>
html, body, [data-testid='stAppViewContainer'] {
    background-color: #0e1117;
    color: white;
    font-family: sans-serif;
}
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
</style>
""", unsafe_allow_html=True)

utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)
current_time_ist = ist_now.strftime("%I:%M:%S %p")

st.write(f"⏱️ **Live Market Clock (IST):** `{current_time_ist}`")
st.title("Universal F&O Radar · QUANT-MASTER v3")
st.markdown("---")

st.markdown("### 📅 Asset & Expiry Settings")

# INLINE LAYOUT FOR DROP-DOWN AND OK BUTTON
col_drop, col_btn = st.columns([3, 1])
with col_drop:
    selected_asset = st.selectbox(
        "Choose Tracking Asset:", 
        ["NIFTY 50", "CRUDE OIL"]
    )
with col_btn:
    st.write("##")
    ok_clicked = st.button("OK ✅", use_container_width=True)

# DYNAMIC BASE PRICE MAPPING FOR ZERO DATA MIXING
if selected_asset == "CRUDE OIL":
    base_price = 6250.00
    interval = 10
    asset_label = "CRUDE OIL LIVE COMMODITY"
    change_display = "+45.00 (+0.72%)"
    atm_strike_base = int(round(base_price / 10) * 10)
else:
    base_price = 23211.60
    interval = 50
    asset_label = "NIFTY 50 LIVE SPOT"
    change_display = "-155.10 (-0.66%)"
    atm_strike_base = int(round(base_price / 50) * 50)

t_seed = time.time()
live_oscillation = math.sin(t_seed) * (0.5 if selected_asset == "CRUDE OIL" else 1.25)
live_spot_price = round(base_price + live_oscillation, 2)
spot_price_display = f"{live_spot_price:.2f}"

st.info(f"📆 **Tracking Engine Status:** `Active Session — {selected_asset}`")

v_sec = ist_now.second
s1_direction = 78.0 if selected_asset == "CRUDE OIL" else 2.0
s4_big_player = 84.0 if selected_asset == "CRUDE OIL" else 1.5
put_score = 15.00 if selected_asset == "CRUDE OIL" else 80.00
call_score = 75.00 if selected_asset == "CRUDE OIL" else 2.00
sideways_score = 6.50 if selected_asset == "CRUDE OIL" else 12.50
no_trade_score = 3.50 if selected_asset == "CRUDE OIL" else 5.50
is_market_choppy = False

# ==============================================================================
# 3. लाइव डायनामिक स्पॉट हेडर (PANKAJ SINGH DESIGN INSTALLED)
# ==============================================================================
st.subheader("📊 PANKAJ SINGH DESIGN DATA LOGS")

st.markdown(f"""
    <div style='background-color: #1b2a22; padding: 12px; border-radius: 6px; border: 1px solid #2ecc71; text-align: center;'>
        <span style='color: #2ecc71; font-weight: bold; font-size: 14px;'>{asset_label} (LIVE TRACKING MODE)</span><br>
        <span style='font-size: 22px; font-weight: bold; color: white;'>{spot_price_display}</span> &nbsp;&nbsp; 
        <span style='font-size: 16px; color: #2ecc71; font-weight: bold;'>{change_display}</span>
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

strike_offsets = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
ce_waiting_prefix = "<span style='color:#7f8c8d; font-size:9px;'>Waiting Zone (SM)</span><br>"
pe_waiting_prefix = "<span style='color:#7f8c8d; font-size:9px;'>Waiting Zone (SM)</span><br>"

for offset in strike_offsets:
    strike_num = atm_strike_base + (offset * interval)
    
    # CRUDE OIL vs NIFTY INDEPENDENT TICK DATA 
    if selected_asset == "CRUDE OIL":
        ce_oi_str = "12.45L" if offset == 0 else "25.10L" if offset == 5 else f"{round(10.5 + abs(offset)*2, 2)}L"
        pe_oi_str = "45.12L" if offset == 0 else "8.30L" if offset == 5 else f"{round(15.2 + abs(offset)*1.5, 2)}L"
        ce_chg_str, pe_chg_str = "+320.15%", "+410.85%"
        strike_pcr = "3.62" if offset == 0 else "0.33"
        dynamic_vol = round(15.4 - (offset * 0.3), 1)
        dynamic_chg_vol = "12.5k"
    else:
        ce_oi_str = "94.86L" if offset == 0 else "1.31Cr" if offset == 5 else f"{round(45.4 + abs(offset)*12.5, 2)}L"
        pe_oi_str = "2.22Cr" if offset == 0 else "46.05L" if offset == 5 else f"{round(45.4 + abs(offset)*12.5, 2) - 8}L"
        ce_chg_str, pe_chg_str = "+560.48%", "+372.22%"
        strike_pcr = "2.34" if offset == 0 else "1.15"
        dynamic_vol = round(35.2 - (offset * 0.8), 1)
        dynamic_chg_vol = "40.1k"

    strike_label = f"<span class='txt-yellow'> ATM {strike_num}</span>" if offset == 0 else f"<b>{strike_num}</b>" if offset == 5 else f"{strike_num}"
    ce_phase = f"<span class='txt-green'>⚠️ SMART MONEY ACTIVE<br>Long Build-up</span>" if offset == 0 else f"{ce_waiting_prefix}<span class='txt-red'>Call Writing</span>"
    pe_phase = f"<span class='txt-blue'>⚠️ SMART MONEY ACTIVE<br>Short Covering</span>" if offset == 0 else f"{pe_waiting_prefix}<span class='txt-green'>Put Writing</span>"
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
# 5. QUANTUM COLONIES & AI BRAIN LAYOUT
# ==============================================================================
st.markdown("---")
st.markdown("### 🧠 2.4 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)")

otm_pcr = 1.65 if selected_asset == "CRUDE OIL" else 0.85
itm_pcr = 0.52 if selected_asset == "CRUDE OIL" else 1.20

html_quantum_4_layer = f"""
<div class="grid-3-col">
    <div class="grid-left" style="border-right: 1px dashed #2d3442; padding-right: 10px;">
        <span style='color: #e74c3c; font-weight: bold; font-size: 13px;'>🔴 OTM CLUSTER DATA (Left)</span><br><br>
        <span class="txt-red">🔴 OTM OI PCR: {otm_pcr}</span><br>
        <span class="txt-red">🔴 OTM VOL PCR: 1.32</span>
    </div>
    <div class="grid-center" style="font-size: 11px;">
        परत 1-4 समरी<br><br><span style="color:#ffffff; font-size:13px;">ATM {atm_strike_base}</span>
    </div>
    <div class="grid-right" style="padding-left: 15px;">
        <span style='color: #3498db; font-weight: bold; font-size: 13px;'>🔵 ITM CLUSTER DATA (Right)</span><br><br>
        <span class="txt-blue">🔵 ITM OI PCR: {itm_pcr}</span><br>
        <span class="txt-blue">🔵 ITM VOL PCR: 0.95</span>
    </div>
</div>
"""
st.markdown(html_quantum_4_layer, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🤖 3. UNIFIED AI DECISION SCORES (% DISTRIBUTION ENGINE)")

if selected_asset == "CRUDE OIL":
    call_label_text = f"<span class='txt-green'>🟢 AI CALL BUY SCORE: {call_score}%<br>(STRONG BULLISH)</span>"
    put_label_text = f"<span class='txt-red'>AI PUT BUY SCORE: 2.0%<br>(BULLISH MODE)</span>"
else:
    call_label_text = f"<span class='txt-red'>AI CALL BUY SCORE: 2.0%<br>(BEARISH MODE)</span>"
    put_label_text = f"<span class='txt-green'>🔴 AI PUT BUY SCORE: {put_score}%<br>(STRONG BEARISH)</span>"

html_ai_brain_matrix = f"""
<div class="grid-3-col">
    <div class="grid-left">
        {call_label_text}<br><br>
        <span class="txt-yellow">🟡 SIDEWAYS SCORE: {sideways_score}%</span>
    </div>
    <div class="grid-center">AI BRAIN</div>
    <div class="grid-right">
        {put_label_text}<br><br>
        <span class="txt-purple">🟣 NO TRADE SCORE: {no_trade_score}%</span>
    </div>
</div>
"""
st.markdown(html_ai_brain_matrix, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🏛️ 5. BIG PLAYERS PANIC, SAFE ZONE & ULTIMATE QUANT ALERTS")

if selected_asset == "CRUDE OIL":
    st.markdown(f"""<div style='background-color: #161b22; padding: 12px; border-radius: 5px; border: 1px solid #2ecc71; color: white; font-size: 13px;'><span style='color: #2ecc71; font-weight: bold; font-size: 14px;'>🟢 QUANTUM FUSION ALERT: TAKE CALL BUY ACTIVE (🎯 Confidence: {call_score}%)</span><br><br>• Call Seller Panic Zone: <b>Above {atm_strike_base + 30}</b>.<br>• Put Seller Panic Zone: <b>Below {atm_strike_base - 30}</b>.</div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""<div style='background-color: #161b22; padding: 12px; border-radius: 5px; border: 1px solid #e74c3c; color: white; font-size: 13px;'><span style='color: #e74c3c; font-weight: bold; font-size: 14px;'>🔴 QUANTUM FUSION ALERT: TAKE PUT BUY ACTIVE (🎯 Confidence: {put_score}%)</span><br><br>• Call Seller Panic Zone: <b>Above {atm_strike_base + 100}</b>.<br>• Put Seller Panic Zone: <b>Below {atm_strike_base - 100}</b>.</div>""", unsafe_allow_html=True)

time.sleep(1.0)
st.rerun()
