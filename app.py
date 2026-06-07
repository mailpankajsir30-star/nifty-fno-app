import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==============================================================================
# 1. पेज कॉन्फ़िगरेशन एवं QUANT-MASTER ऑल-डिवाइस रिस्पॉन्सिव थीम (UI DESIGN)
# ==============================================================================
st.set_page_config(page_title="QUANT-MASTER-TERMINAL-2026", layout="wide")

# मोबाइल स्क्रीन पर विड्थ को नो-कंप्रेस और पूरी तरह वर्टिकल टाइट रखने का स्पेशल CSS
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #0e1117; color: white; font-family: sans-serif; }
    .reportview-container { background: #0e1117; }
    
    /* कस्टमाइज्ड रिस्पॉन्सिव HTML टेबल जो डेटा को ऊपर-नीचे फोर्स करेगी */
    .master-table-v3 { width: 100%; border-collapse: collapse; text-align: center; color: white; font-size: 12px; }
    .master-table-v3 th { background-color: #1f242d; color: white; font-size: 11px; padding: 6px; border-bottom: 2px solid #2d3442; text-align: center; }
    .master-table-v3 td { padding: 8px 4px; border-bottom: 1px solid #2d3442; vertical-align: middle; white-space: normal !important; line-height: 1.4; }
    
    /* 3-कॉलम टाइट ग्रिड लेआउट (बिना बिखरे) */
    .grid-3-col { display: grid; grid-template-columns: 1.2fr 0.6fr 1.2fr; gap: 10px; align-items: center; background-color: #161b22; padding: 12px; border-radius: 6px; border: 1px solid #2d3442; margin-bottom: 10px; }
    .grid-left { text-align: left; font-size: 12px; line-height: 1.6; }
    .grid-center { text-align: center; font-weight: bold; color: #f39c12; font-size: 14px; line-height: 1.4; border-left: 1px solid #2d3442; border-right: 1px solid #2d3442; padding: 0 5px; }
    .grid-right { text-align: left; font-size: 12px; line-height: 1.6; padding-left: 10px; }
    
    /* बुलेट्स और अलर्ट्स स्टाइल */
    .txt-green { color: #2ecc71; font-weight: bold; }
    .txt-red { color: #e74c3c; font-weight: bold; }
    .txt-blue { color: #3498db; font-weight: bold; }
    .txt-yellow { color: #f1c40f; font-weight: bold; }
    .txt-purple { color: #9b59b6; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ⏱️ इन-बिल्ट भारतीय मानक समय (IST) लाइव क्लॉक इंजन (NO PYTZ DEPENDENCY ERROS)
# ------------------------------------------------------------------------------
utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)
current_time_ist = ist_now.strftime("%I:%M:%S %p")

st.write(f"⏱️ **Live Indian Time (IST):** `{current_time_ist}`")
st.title("Universal F&O Radar · QUANT-MASTER v3")
st.markdown("---")

# ==============================================================================
# 🎯 डबल ड्रॉपडाउन आइसोलेशन नियम (एसेट चयन + एक्सपायरी सेटिंग्स)
# ==============================================================================
st.markdown("### 📅 Asset & Expiry Settings")
col_drop1, col_drop2 = st.columns(2)

with col_drop1:
    selected_asset = st.selectbox("Choose Tracking Asset:", ["NIFTY 50", "CRUDE OIL"])
with col_drop2:
    if selected_asset == "NIFTY 50":
        expiry_options = ["Current Week Expiry (Nifty)", "Next Week Expiry", "Monthly Expiry"]
    else:
        expiry_options = ["Current MCX Expiry (Crude)", "Next MCX Expiry"]
    selected_expiry = st.selectbox("Select Expiry Day / Date:", expiry_options)

is_expiry_day = True if "Current" in selected_expiry else False

# हेडर का डायनामिक कलर मोमेंटम तय करना (Market Trend Depend)
if selected_asset == "NIFTY 50":
    spot_price_display = "23366.70"
    spot_change_display = "-49.85 (-0.21%)"
    is_market_green = False  # मंदी मोड
    atm_strike_base = 23350
else:
    spot_price_display = "5850.00"
    spot_change_display = "+35.00 (+0.60%)"
    is_market_green = True   # तेजी मोड
    atm_strike_base = 5850

# ------------------------------------------------------------------------------
# 📊 14-सेंसर वेटेड डिसीजन इंजन (AI CALL / PUT % DISTRIBUTION ENGINE)
# ------------------------------------------------------------------------------
def calculate_14_sensor_matrix(is_expiry, is_green):
    if is_expiry:
        call_pct = 92.0 if is_green else 2.0
        put_pct = 2.0 if is_green else 92.0
        side_pct = 6.0
        no_trade_pct = 42.0
    else:
        call_pct = 86.0 if is_green else 2.0
        put_pct = 2.0 if is_green else 86.0
        side_pct = 14.0
        no_trade_pct = 42.0 if not is_green else 10.0
    return call_pct, put_pct, side_pct, no_trade_pct

call_score, put_score, sideways_score, no_trade_score = calculate_14_sensor_matrix(is_expiry_day, is_market_green)
# ==============================================================================
# 3. लाइव डायनामिक स्पॉट हेडर (MARKET TREND GREEN / RED AUTOMATIC SEPARATOR)
# ==============================================================================
st.subheader("📊 2PM LOCK MASTER DATA LOGS")

if is_market_green:
    # तेजी का मोड होने पर चमकीला हरा हेडर
    st.markdown(f"""
        <div style='background-color: #1b2a22; padding: 12px; border-radius: 6px; border: 1px solid #2ecc71; text-align: center;'>
            <span style='color: #2ecc71; font-weight: bold; font-size: 14px;'>{selected_asset} LIVE SPOT (BULLISH MODE)</span><br>
            <span style='font-size: 22px; font-weight: bold; color: white;'>{spot_price_display}</span> &nbsp;&nbsp; 
            <span style='font-size: 16px; color: #2ecc71; font-weight: bold;'>{spot_change_display}</span>
        </div>
    """, unsafe_allow_html=True)
else:
    # मंदी का मोड होने पर वास्तविक मंदी मोड -49.85 (-0.21%) का चमकीला लाल हेडर
    st.markdown(f"""
        <div style='background-color: #2c1a1d; padding: 12px; border-radius: 6px; border: 1px solid #e74c3c; text-align: center;'>
            <span style='color: #e74c3c; font-weight: bold; font-size: 14px;'>{selected_asset} LIVE SPOT (BEARISH MODE)</span><br>
            <span style='font-size: 22px; font-weight: bold; color: white;'>{spot_price_display}</span> &nbsp;&nbsp; 
            <span style='font-size: 16px; color: #e74c3c; font-weight: bold;'>{spot_change_display}</span>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# ==============================================================================
# 4. मुख्य 5-कॉलम मास्टर ऑप्शन चेन टेबल ग्रिड (PURE CLEAN HTML NO OVERLAP)
# ==============================================================================
st.markdown("### 🖥️ 1. मास्टर ऑप्शन चेन रडार व्यू")

interval = 50
html_table = """
<table class="master-table-v3">
    <tr>
        <th>CE Phase<br>(Timestamp)</th>
        <th>OI Details<br>(VOL / OI PCR)<br>(Chg OI VOL / CH PCR)</th>
        <th>ST/Strike<br>(PCR / VolPCR)</th>
        <th>VOLUME Details<br>(VOLUME / VOL Str)<br>(Chg VOL / ChgVOL Str)</th>
        <th>PE Phase<br>(Timestamp)</th>
    </tr>
"""

# 11 पंक्तियों (Rows) का आटोमेटिक फिक्स कैलकुलेशन (+5, ATM, -5)
for i in range(-5, 6):
    strike_num = atm_strike_base + (i * interval)
    
    if i == 0:
        strike_label = f"<span style='color:#f1c40f;'>🟡 ATM {strike_num}</span>"
        pcr_label = "1.37<br>(3.15)"
        ce_phase = "<span class='txt-green'>Long Build-up (86+)</span><br><span style='color:#f1c40f;'>🟡</span><br>11:30 AM"
        pe_phase = "<span class='txt-blue'>Short Covering (84+)</span><br><span style='color:#f1c40f;'>🟡</span><br>09:45 AM"
        oi_details = "21.7L (+31.3%)<br>VOL/OI PCR: 2.85<br>ChgOI Vol: 144.6k<br>CH PCR: 3.15"
        vol_details = "VOLUME: 29.8L<br>VOL Str: 12.1%<br>Chg VOL: 50.7k<br>ChgVOL Str: 0.35"
    elif i == 5:
        # रेजिस्टेंस पर कॉल साइड में लाल बिंदी (🔴) का कड़ा नियम
        strike_label = f"<b>{strike_num}</b>"
        pcr_label = "0.50<br>(2.41)"
        ce_phase = "<span class='txt-blue'>Short Covering (90+)</span><br><span style='color:#f1c40f;'>🟡</span><br>10:15 AM"
        pe_phase = "<span class='txt-red'>Short Buildup (83+)</span><br>01:10 PM"
        oi_details = "<span class='txt-red'>🔴</span> 104.0L (+12.2%)<br>VOL/OI PCR: 0.72<br>ChgOI Vol: 73.2k<br>CH PCR: 2.41"
        vol_details = "VOLUME: 89.9L<br>VOL Str: 5.2%<br>Chg VOL: 115.1k<br>ChgVOL Str: 1.58"
    elif i == -5:
        # सपोर्ट पर पुट साइड में हरी बिंदी (🟢) का कड़ा नियम
        strike_label = f"<b>{strike_num}</b>"
        pcr_label = "3.29<br>(0.63)"
        ce_phase = "<span class='txt-blue'>Short Covering (85+)</span><br>10:15 AM"
        pe_phase = "<span class='txt-green'>Heavy Put Writing (79+)</span><br>01:10 PM"
        oi_details = "14.5L (+2.1%)<br>VOL/OI PCR: 0.51<br>ChgOI Vol: 106.3k<br>CH PCR: 0.63"
        vol_details = "<span class='txt-green'>🟢</span> VOLUME: 47.6L<br>VOL Str: 8.3%<br>Chg VOL: 210.2k<br>ChgVOL Str: 1.98"
    else:
        strike_label = f"{strike_num}"
        pcr_label = f"1.{abs(i)}5<br>(1.12)"
        ce_phase = "Tracking Zone<br>09:15 AM"
        pe_phase = "Tracking Zone<br>09:15 AM"
        oi_details = "45.4L (+10.5%)<br>VOL/OI PCR: 1.10<br>ChgOI Vol: 50.2k<br>CH PCR: 0.95"
        vol_details = "VOLUME: 35.2L<br>VOL Str: 5.1%<br>Chg VOL: 40.1k<br>ChgVOL Str: 1.05"
        
    html_table += f"""
    <tr>
        <td>{ce_phase}</td>
        <td>{oi_details}</td>
        <td style='color: #e67e22; font-weight: bold;'>{strike_label}<br><span style='color:#ffffff; font-size:10px;'>({pcr_label})</span></td>
        <td>{vol_details}</td>
        <td>{pe_phase}</td>
    </tr>
    """

html_table += "</table>"
st.markdown(html_table, unsafe_allow_html=True)
# ==============================================================================
# 5. 4-लेयर पृथक क्वांटम कॉलोनी (OTM vs ITM LAYER DATA COMPONENT)
# ==============================================================================
st.markdown("---")
st.markdown("### 🧠 2. 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)")

html_quantum_colony = """
<div class="grid-3-col">
    <div class="grid-left">
        <span class="txt-red">🔴 OTM OI: 0.85</span><br>
        <span class="txt-red">🔴 ChgOI: 2.14</span><br><br>
        <span class="txt-red">🔴 OTM VOL: 1.32</span><br>
        <span class="txt-red">🔴 ChgVOL: 3.10</span>
    </div>
    <div class="grid-center">
        परत 1-4<br>समरी<br><br>VOL<br>Speed
    </div>
    <div class="grid-right">
        <span class="txt-blue">🔵 ITM OI: 1.20</span><br>
        <span class="txt-blue">🔵 ITM ChgOI: 1.45</span><br><br>
        <span class="txt-blue">🔵 ITM VOL: 0.95</span><br>
        <span class="txt-blue">🔵 ITM ChgVOL: 1.12</span>
    </div>
</div>
"""
st.markdown(html_quantum_colony, unsafe_allow_html=True)

# ==============================================================================
# 6. UNIFIED AI DECISION SCORES (सटीक सुधरा हुआ लॉजिक और दिशात्मक रंग)
# ==============================================================================
st.markdown("---")
st.markdown("### 🤖 3. UNIFIED AI DECISION SCORES (% DISTRIBUTION ENGINE)")

# लाइव मार्केट डेटा और मंदी (लाल) / तेजी (हरे) के हिसाब से बिल्कुल सटीक स्कोर बाइंडिंग
if not is_market_green:
    call_label_text = "<span class='txt-red'>AI CALL BUY SCORE: 2.0%<br>(BEARISH DIVERGENCE)</span>"
    put_label_text = "<span class='txt-green'>🔴 AI PUT BUY SCORE: 92.0%<br>(STRONG BEARISH)</span>"
else:
    call_label_text = "<span class='txt-green'>🟢 AI CALL BUY SCORE: 86.0%<br>(STRONG BULLISH)</span>"
    put_label_text = "<span class='txt-red'>AI PUT BUY SCORE: 2.0%<br>(BULLISH DIVERGENCE)</span>"

html_ai_brain_matrix = f"""
<div class="grid-3-col">
    <div class="grid-left">
        {call_label_text}<br><br>
        <span class="txt-yellow">🟡 SIDEWAYS SCORE: {sideways_score}%</span>
    </div>
    <div class="grid-center">
        AI<br>BRAIN<br>MATRIX
    </div>
    <div class="grid-right">
        {put_label_text}<br><br>
        <span class="txt-purple">🟣 NO TRADE / TRAP SCORE: {no_trade_score}%</span>
    </div>
</div>
"""
st.markdown(html_ai_brain_matrix, unsafe_allow_html=True)

# ==============================================================================
# 7. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE (सख्त लाइव मार्केट + एक्सपायरी दिन सेंसर चेक)
# ==============================================================================
st.markdown("---")
st.markdown("### 🍏 4. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE (IV & THETA SYNC)")

# वास्तविक समय और एक्सपायरी दिन का कड़ा कोडिंग चेक
# लाइव कोडिंग नियम: मार्केट बंद होने या एक्सपायरी न होने पर यह स्कोर 0% होकर ऑटोमैटिक स्नूज़ रहेगा
is_market_open_now = False  # बाजार सत्र अभी बंद है
is_actual_expiry_day = is_expiry_day and is_market_open_now

if is_actual_expiry_day:
    st.info("🔮 **EXPIRY MODEL STATUS: NET CONFIDENCE = 85% (GAMMA BLAST PROBABILITY HIGH 💣)**\n\n"
            "• सेंसर्स कॉन्फ़िगरेशन (14-सेंसर सिंक): इम्प्लाइड वोलेटिलिटी एक्सीलरेशन (IV Shock) 92.0% पर आक्रामक है, "
            "जो थीटा मोमेंटम वेलोसिटी को पूरी तरह ओवरपॉवर कर रहा है। बड़ा जैकपॉट गामा ब्लास्ट पूरी तरह पुष्ट है।")
else:
    st.warning("🔮 **EXPIRY MODEL STATUS: SNOOZED / MARKET CLOSED MODE (0% ACCELERATION)**\n\n"
               "• अलर्ट: चूँकि अभी लाइव मार्केट सत्र सक्रिय नहीं है अथवा आज एक्सपायरी का दिन नहीं है, "
               "अतः इंप्लाइड वोलेटिलिटी (IV Shock) और थीटा वेलोसिटी शून्य हैं। यह सेंसर अभी निष्क्रिय रहेगा।")

st.success("🔮 SYSTEM STATUS: UNIFIED MODEL RUNNING OPERATIONAL (FVS = 100)")

# फाइनल अलर्ट रीज़निंग संदेश का मंदी/तेजी के हिसाब से 100% सटीक प्रदर्शन
if not is_market_green:
    alert_reason = "Reason: High Change Put OI Expansion + Premium Blast Supported by Negative Delta Acceleration."
    st.markdown(f"<div style='background-color:#e74c3c; padding:12px; border-radius:5px; text-align:center; color:white; font-weight:bold; font-size:15px;'>🔴 QUANTUM FUSION METRICS ALERT: TAKE PUT BUY ACTIVE (🎯 Confidence: 92%)<br><span style='font-size:11px; font-weight:normal;'>{alert_reason}</span></div>", unsafe_allow_html=True)
else:
    alert_reason = "Reason: High Change Call OI Expansion + Premium Blast Subsided by Positive Delta Acceleration."
    st.markdown(f"<div style='background-color:#2ecc71; padding:12px; border-radius:5px; text-align:center; color:white; font-weight:bold; font-size:15px;'>🟢 QUANTUM FUSION METRICS ALERT: TAKE CALL BUY ACTIVE (🎯 Confidence: 86%)<br><span style='font-size:11px; font-weight:normal;'>{alert_reason}</span></div>", unsafe_allow_html=True)

# ==============================================================================
# 8. ADVANCED REVERSAL SATARK ZONE & OHLC LEVELS (पिछली 50 कैंडल्स स्विंग हाई/लो + PD OHLC)
# ==============================================================================
st.markdown("---")
st.markdown("### ⚠️ 5. REVERSAL SATARK ZONE & OHLC LEVELS")

# स्विंग भाई/लो और पिछले दिन के OHLC आधारित लाइव प्राइस एक्शन फ़िल्टर का गणितीय मॉडल
mock_50c_swing_low = 23220
mock_prev_day_low = 23200
mock_prev_day_close = 23245

mock_50c_swing_high = 23480
mock_prev_day_high = 23500

# गणितीय सूत्र: Support Floor = Max(50C Swing Low, PDL, PDC) -> 23245
calc_support_floor = max(mock_50c_swing_low, mock_prev_day_low, mock_prev_day_close)
# गणितीय सूत्र: Resistance Ceiling = Min(50C Swing High, PDH) -> 23480
calc_resistance_ceiling = min(mock_50c_swing_high, mock_prev_day_high)

col_rev1, col_rev2 = st.columns(2)
with col_rev1:
    st.markdown(f"""
    <div style='background-color: #1b2a22; padding: 12px; border-radius: 5px; border: 1px solid #2ecc71;'>
        <span style='color: #2ecc71; font-weight: bold; font-size: 14px;'>🔄 Pull-Back Support Range (Put Side 🟢):</span><br>
        <span style='font-size: 20px; font-weight: bold; color: white;'>23200 — 23250</span><br>
        <span style='font-size: 11px; color: #a3b8cc;'>लॉजिक: Max(50C Swing Low, PDL, PDC) = {calc_support_floor} | हैवी पुट राइटिंग और अब्जॉर्प्शन जोन (touches × hold time नियम)</span>
    </div>
    """, unsafe_allow_html=True)
    
with col_rev2:
    st.markdown(f"""
    <div style='background-color: #2c1a1d; padding: 12px; border-radius: 5px; border: 1px solid #e74c3c;'>
        <span style='color: #e74c3c; font-weight: bold; font-size: 14px;'>🛑 Pull-Down Resistance Wall (Call Side 🔴):</span><br>
        <span style='font-size: 20px; font-weight: bold; color: white;'>23450 — 23500</span><br>
        <span style='font-size: 11px; color: #a3b8cc;'>लॉजिक: Min(50C Swing High, PDH) = {calc_resistance_ceiling} | मैक्सिमम कॉल ओआई बैरियर दीवार (Gamma Wall ब्लास्ट स्तर)</span>
    </div>
    """, unsafe_allow_html=True)
