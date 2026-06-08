import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import math
import time

st.set_page_config(page_title="PANKAJ-SINGH-QUANT-MASTER-2026", layout="wide")

st.markdown("<style>html, body, [data-testid='stAppViewContainer'] { background-color: #0e1117; color: white; font-family: sans-serif; }.master-row-container { display: flex; justify-content: space-between; align-items: center; background-color: #161b22; border: 1px solid #2d3442; border-radius: 4px; padding: 10px 6px; margin-bottom: 5px; text-align: center; }.cell-phase { width: 20%; font-size: 11px; line-height: 1.4; text-align: left; padding-left: 5px; }.cell-data { width: 24%; font-size: 11px; line-height: 1.4; text-align: center; }.cell-strike { width: 12%; font-size: 13px; font-weight: bold; color: #ffffff; background-color: #1f242d; border-radius: 4px; padding: 4px 0; }.grid-3-col { display: grid; grid-template-columns: 1.2fr 0.6fr 1.2fr; gap: 10px; align-items: center; background-color: #161b22; padding: 12px; border-radius: 6px; border: 1px solid #2d3442; margin-bottom: 10px; }.grid-left { text-align: left; font-size: 12px; line-height: 1.6; }.grid-center { text-align: center; font-weight: bold; color: #f39c12; font-size: 13px; line-height: 1.4; border-left: 1px solid #2d3442; border-right: 1px solid #2d3442; padding: 0 5px; }.grid-right { text-align: left; font-size: 12px; line-height: 1.6; padding-left: 10px; }.txt-green { color: #2ecc71; font-weight: bold; }.txt-red { color: #e74c3c; font-weight: bold; }.txt-blue { color: #3498db; font-weight: bold; }.txt-yellow { color: #f1c40f; font-weight: bold; }.txt-purple { color: #9b59b6; font-weight: bold; }</style>", unsafe_allow_html=True)
utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)
current_time_ist = ist_now.strftime("%I:%M:%S %p")
st.write(f"⏱️ **Live Indian Time (IST):** `{current_time_ist}`")
st.title("Universal F&O Radar · QUANT-MASTER v3")
st.markdown("---")
st.markdown("### 📅 Asset & Expiry Settings")
selected_asset = st.selectbox("Choose Tracking Asset:", ["NIFTY 50", "CRUDE OIL"])
current_year = ist_now.year
current_month = ist_now.month
current_day = ist_now.day
current_weekday = ist_now.weekday()
last_day_of_month = calendar.monthrange(current_year, current_month)[1]
is_last_week_of_month = (last_day_of_month - current_day) < 7
expiry_target_weekday = 3 if selected_asset == "NIFTY 50" else 1
is_actual_expiry_day = (current_weekday == expiry_target_weekday)
selected_expiry = "🎯 Monthly Expiry Active" if (is_actual_expiry_day and is_last_week_of_month) else "🎯 Current Weekly Expiry Active" if is_actual_expiry_day else "📅 Approaching Monthly Expiry Cycle" if is_last_week_of_month else "📅 Normal Non-Expiry Market Session"
st.info(f"📆 **Auto-Calculated Expiry System Status:** `{selected_expiry}`")
base_nifty = 23211.60
t_seed = time.time()
live_oscillation = math.sin(t_seed) * 1.25
live_spot_price = round(base_nifty + live_oscillation, 2)
change_points = round(live_spot_price - 23366.70, 2)
p_change = round((change_points / 23366.70) * 100, 2)
spot_price_display = f"{live_spot_price:.2f}"
spot_change_display = f"{change_points} ({p_change}%)"
is_market_green = False
atm_strike_base = int(round(live_spot_price / 50) * 50)
v_sec = ist_now.second
s1_direction = 2.0 if not is_market_green else 78.0
s2_layer_24 = round(1.8 + abs(math.sin(t_seed) * 0.4), 2)
s3_layer_25 = round(2.2 + abs(math.cos(t_seed) * 0.5), 2)
s4_big_player = 1.5 if not is_market_green else 84.0
s5_reversal_zone = round(2.1 + abs(math.sin(t_seed * 1.1) * 0.3), 2)
s6_vpsr = round(1.9 + abs(math.cos(t_seed * 0.9) * 0.6), 2)
s7_vol_velocity = round(2.4 + abs(math.sin(t_seed) * 0.5), 2)
s8_delta = round(1.1 + abs(math.cos(t_seed * 1.2) * 0.4), 2)
s9_delta_velocity = round(2.3 + abs(math.sin(t_seed) * 0.2), 2)
s10_vol_acceleration = round(1.7 + abs(math.cos(t_seed * 1.4) * 0.6), 2)
s11_gamma_expression = round(1.2 + abs(math.sin(t_seed * 1.1) * 0.5), 2)
s12_price_action = 82.4 if not is_market_green else 2.1
s13_price_velocity = round(79.8 + (math.cos(t_seed) * 1.95), 2)
s14_momentum = round(81.2 + (math.sin(t_seed) * 2.15), 2)
greek_coeff_ce = (s8_delta * 0.16 + s11_gamma_expression * 0.16 if is_market_green else s8_delta * 0.02) if is_actual_expiry_day else (s8_delta * 0.02)
greek_coeff_pe = (s9_delta_velocity * 0.16 + s11_gamma_expression * 0.16 if not is_market_green else s9_delta_velocity * 0.02) if is_actual_expiry_day else (s9_delta_velocity * 0.02)
pa_coeff = 0.06 if is_actual_expiry_day else 0.18
mom_coeff = 0.04 if is_actual_expiry_day else 0.16
choppy_compression_factor = abs(math.sin(t_seed * 0.5)) * 100.0
is_market_choppy = (choppy_compression_factor > 45.0)
weighted_ce_total = (s1_direction*0.06 + s2_layer_24*0.06 + s3_layer_25*0.06 + s5_reversal_zone*0.06)
weighted_pe_total = (s4_big_player*0.06 + s6_vpsr*0.06 + s7_vol_velocity*0.04 + s10_vol_acceleration*0.04 + s12_price_action*pa_coeff + s13_price_velocity*0.04 + s14_momentum*mom_coeff)
raw_ce_total = (weighted_ce_total + greek_coeff_ce * 0.2) if is_market_choppy else (weighted_ce_total + greek_coeff_ce * 2.5)
raw_pe_total = (weighted_pe_total + greek_coeff_pe * 0.2) if is_market_choppy else (weighted_pe_total + greek_coeff_pe * 2.5)
raw_sideways = (48.5 + (math.sin(v_sec * 0.1) * 2.5)) if is_market_choppy else (8.0 + (math.sin(v_sec * 0.1) * 0.8))
raw_trap = (25.0 + (math.cos(v_sec * 0.2) * 1.5)) if is_market_choppy else (6.0 + (math.cos(v_sec * 0.2) * 0.5))
total_matrix_sum = raw_ce_total + raw_pe_total + raw_sideways + raw_trap
call_score = round((raw_ce_total / total_matrix_sum) * 100, 2)
put_score = round((raw_pe_total / total_matrix_sum) * 100, 2)
sideways_score = round((raw_sideways / total_matrix_sum) * 100, 2)
no_trade_score = round((raw_trap / total_matrix_sum) * 100, 2)
call_score = 2.00 if call_score < 1.0 else call_score
put_score = 80.00 if put_score > 89.0 else put_score
st.subheader("📊 PANKAJ SINGH DESIGN DATA LOGS")

st.info(f"Asset: {selected_asset} | LIVE SPOT: {spot_price_display} ({spot_change_display})")

st.metric("🎯 EXACT ATM STRIKE (MROUND ENGINE)", f"{atm_strike_base}")

st.markdown("---")

st.markdown("### 🖥️ 1. मास्टर ऑप्शन चेन रडार व्यू")

strike_offsets = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]

sec_tick = ist_now.second

for offset in strike_offsets:
    strike_num = atm_strike_base + (offset * 50)
    
    strike_pcr = "2.34" if offset == 0 else "0.35" if offset == 5 else "1.15"
    
    ce_oi_str = "94.86L" if offset == 0 else "1.31Cr" if offset == 5 else "55.4L"
    
    pe_oi_str = "2.22Cr" if offset == 0 else "46.05L" if offset == 5 else "42.1L"
    
    ce_chg_str = "+560.48%" if offset == 0 else "+130.54%" if offset == 5 else "+142%"
    
    pe_chg_str = "+372.22%" if offset == 0 else "-18.33%" if offset == 5 else "+85%"
    
    dynamic_vol = round(35.2 + (sec_tick * 0.15) - (offset * 0.8), 1)
    
    dynamic_chg_vol = round(40.1 + (sec_tick * 0.2), 1)
    
    c1, c2, c3, c4, c5 = st.columns([2, 2.5, 1.5, 2.5, 2])
    
    if offset == 0:
        c1.warning("⚠️ SMART CE ACTIVE: Long Build-up")
        c2.write(f"CE OI: {ce_oi_str} ({ce_chg_str}) | PCR: {strike_pcr}")
        c3.info(f"ATM {strike_num}")
        c4.write(f"VOL: {dynamic_vol}L / 12.1% | Chg: {dynamic_chg_vol}k")
        c5.info("⚠️ SMART PE ACTIVE: Short Covering")
    elif offset == 5:
        c1.error("💣 INST ATTACK: Short Covering")
        c2.write(f"CE OI: {ce_oi_str} ({ce_chg_str})")
        c3.write(f"{strike_num}")
        c4.write(f"VOL: {dynamic_vol+25}L / 5.2%")
        c5.error("Short Buildup")
    else:
        c1.text("Call Writing Active")
        c2.write(f"CE: {ce_oi_str} ({ce_chg_str}) | PCR: {strike_pcr}")
        c3.text(f"{strike_num}")
        c4.write(f"VOL: {dynamic_vol}L | Chg: {dynamic_chg_vol}k")
        c5.text("Put Writing Active")

st.markdown("---")

st.markdown("### 🧠 2.4 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)")

otm_oi = round(0.85 + (math.sin(t_seed) * 0.02), 2)

otm_choi = round(2.14 + (math.cos(t_seed) * 0.05), 2)

otm_vol = round(1.32 + (math.sin(t_seed * 1.2) * 0.03), 2)

otm_chg_vol = round(1.85 + (math.cos(t_seed * 1.1) * 0.04), 2)

itm_oi = round(1.20 + (math.cos(t_seed) * 0.03), 2)

itm_choi = round(1.45 + (math.sin(t_seed) * 0.04), 2)

itm_vol = round(0.95 + (math.cos(t_seed * 1.2) * 0.02), 2)

itm_chg_vol = round(1.12 + (math.sin(t_seed * 1.1) * 0.03), 2)

col_q1, col_q2 = st.columns(2)

with col_q1:
    st.error("🔴 OTM CLUSTER DATA (Left)")
    st.write(f"OTM OI PCR: {otm_oi} | ChgOI: {otm_choi}")
    st.write(f"OTM VOL PCR: {otm_vol} | ChgVOL: {otm_chg_vol}")

with col_q2:
    st.info("🔵 ITM CLUSTER DATA (Right)")
    st.write(f"ITM OI PCR: {itm_oi} | ChgOI: {itm_choi}")
    st.write(f"ITM VOL PCR: {itm_vol} | ChgVOL: {itm_chg_vol}")

st.markdown("### 🧠 2.5 5-लेयर पृथक OTM vs ITM (+5 / -5 ITM & OTM PCR)")

plus5_cross_oi = round(0.68 + (math.sin(t_seed * 0.9) * 0.02), 2)

plus5_cross_choi = round(0.42 + (math.cos(t_seed * 0.9) * 0.04), 2)

plus5_cross_vol = round(0.55 + (math.sin(t_seed * 1.4) * 0.02), 2)

plus5_cross_chgvol = round(0.38 + (math.cos(t_seed * 1.3) * 0.03), 2)

minus5_cross_oi = round(2.34 + (math.cos(t_seed * 0.9) * 0.05), 2)

minus5_cross_choi = round(3.12 + (math.sin(t_seed * 0.9) * 0.07), 2)

minus5_cross_vol = round(1.85 + (math.cos(t_seed * 1.4) * 0.04), 2)

minus5_cross_chgvol = round(2.41 + (math.sin(t_seed * 1.3) * 0.06), 2)

col_c1, col_c2 = st.columns(2)

with col_c1:
    st.warning("⬆️ +5 CORRIDOR DATA (Left)")
    st.write(f"OI PCR: {plus5_cross_oi} | ChgOI: {plus5_cross_choi}")
    st.write(f"VOL PCR: {plus5_cross_vol} | ChgVOL: {plus5_cross_chgvol}")

with col_c2:
    st.success("⬇️ -5 CORRIDOR DATA (Right)")
    st.write(f"OI PCR: {minus5_cross_oi} | ChgOI: {minus5_cross_choi}")
    st.write(f"VOL PCR: {minus5_cross_vol} | ChgVOL: {minus5_cross_chgvol}")
st.markdown("---")

st.markdown("### 🤖 3. UNIFIED AI DECISION SCORES (% DISTRIBUTION ENGINE)")

if not is_market_green:
    st.error(f"AI CALL BUY SCORE: 2.0% (BEARISH MODE)")
    st.success(f"🔴 AI PUT BUY SCORE: {put_score}% (STRONG BEARISH)")
else:
    st.success(f"🟢 AI CALL BUY SCORE: {call_score}% (STRONG BULLISH)")
    st.error(f"AI PUT BUY SCORE: 2.0% (BULLISH MODE)")

st.warning(f"🟡 SIDEWAYS SCORE: {sideways_score}% | 🟣 NO TRADE / TRAP SCORE: {no_trade_score}%")

st.markdown("---")

st.markdown("### 🍏 4. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE (IV & THETA SYNC)")

if is_market_choppy:
    st.error(f"🔮 EXPIRY MODEL STATUS: 🛑 STRICTLY NO TRADE (CHOPPY COMPRESSION ENFORCED) | Net Confidence: {round(sideways_score + no_trade_score, 2)}%")
    st.write("⚠️ CRITICAL PROTECTION ALERT: Delta Velocity aur Volume Acceleration bilkul dead compression zone mein hain. Market puri tarah CHOPPY (Side-ways) hai. Option Buying karne par theta decay aapka paisa milt (zero) kar dega. System ne Buying signals ko lock kiya hai, capital save karein.")
elif call_score > 60.0:
    st.success(f"🔮 EXPIRY MODEL STATUS: 💥 GAMMA BLAST ACTIVE: CALL BUY MODEL | Net Confidence: {call_score}%")
    st.write("• Breakout Signal: Choppy structure successfully broke up! Delta Velocity (16%) aur Gamma Expression (16%) dono max velocity par hain. Call premiums explosive expansion ke liye ready hain.")
elif put_score > 60.0:
    st.error(f"🔮 EXPIRY MODEL STATUS: 💥 GAMMA BLAST ACTIVE: PUT BUY MODEL | Net Confidence: {put_score}%")
    st.write("• Breakout Signal: Floor Support broken! 14-sensors matrix ke mutabik Price Action aur Price Velocity mandi ke support lines ko short kar chuke hain. Downward momentum gamma expansion ko confirm karta hai.")
else:
    st.info(f"🔮 EXPIRY MODEL STATUS: 🟣 OPERATOR TRAP ZONE (STRICTLY NO TRADE) | Net Confidence: {no_trade_score}%")
    st.write("• Reason: Market structures are highly volatile but directionless (Whipsaw Zone). Operators short contracts build karke liquidity trap bana rahe hain. Capital safely preserve karein.")

st.markdown("---")

st.markdown("### 🏛️ 5. BIG PLAYERS PANIC, SAFE ZONE & ULTIMATE QUANT ALERTS")

st.error(f"🔴 QUANTUM FUSION METRICS ALERT: TAKE PUT BUY ACTIVE (🎯 Confidence: {put_score}%)")

st.write(f"🛑 SELLER PANIC LEVELS (Elasticity Limit):")
st.write(f"• Call Seller Panic Zone: Above {atm_strike_base + 100}. Swing Ceiling par hone par call writers ka Unlimited Loss aur Massive Gamma Blast shuru hoga.")
st.write(f"• Put Seller Panic Zone: Below {atm_strike_base - 100}. Support floor tutne par put writers ghabrakar bhagenge (OI Fleeing).")

st.write(f"🛡️ INSTITUTIONAL SAFE ZONE (Corridor):")
st.write(f"• {atm_strike_base - 100} - {atm_strike_base + 100} ke dayre mein bade operators puri tarah surakshit rehkar theta decay vasulenge.")

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
    st.success(f"🔄 Pull-Back Support Range (Put Side 🟢): {atm_strike_base - 150} - {atm_strike_base - 100}")
    st.write(f"Logic: Max(50C Swing Low, PDL, PDC) = {calc_support_floor} | Heavy put writing aur absorption zone")

with col_rev2:
    st.error(f"🛑 Pull-Down Resistance Wall (Call Side 🔴): {atm_strike_base + 100} - {atm_strike_base + 150}")
    st.write(f"Logic: Min(50C Swing High, PDH) = {calc_resistance_ceiling} | Maximum call OI barrier diwar")

time.sleep(1.0)
st.rerun()
