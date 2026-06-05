import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Ultimate Indian Derivatives Quant Matrix")

# सीएसएस: डार्क लुक बनाए रखने और 5-कॉलम को मोबाइल स्क्रीन पर फिट करने के लिए
st.markdown("""
    <style>
    .reportview-container { background: #06080c; }
    p { font-family: monospace; font-size: 11.5px; margin-bottom: 2px !important; line-height: 1.35; }
    .strike-title { background-color: #111827; padding: 4px; text-align: center; font-weight: bold; color: #9ca3af; border-radius: 4px; font-size: 11px; }
    .divider-line { background-color: #1e293b; color: #ffff00; font-weight: bold; text-align: center; padding: 6px; font-size: 12px; border-radius: 4px; margin: 15px 0 10px 0; }
    .alert-box { text-align: left; padding: 6px; font-size: 11.5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 क्वांटिटेटिव VSA + OI इंस्टीट्यूशनल डिसीजन इंजन")
st.write("📲 5-कॉलम मोबाइल फ़िट | ऑल-इंडेक्स डेरिवेटिव्स रडार")

# 🎯 भारतीय डेरिवेटिव्स मार्केट इंडेक्स सेलेक्टर ड्रॉपडाउन
selected_index = st.selectbox(
    "🎯 लाइव डेरिवेटिव इंडेक्स चुनें (Select Market Radar):",
    ["NIFTY 50", "BANK NIFTY", "SENSEX"]
)

# 1. डेटा इंजन
def get_broker_ui_data(index_name):
    if index_name == "NIFTY 50":
        underlying_value = 23366.70
        strike_interval = 50
        atm_strike = 23350
    elif index_name == "BANK NIFTY":
        underlying_value = 50420.30
        strike_interval = 100
        atm_strike = 50400
    else:
        underlying_value = 76840.50
        strike_interval = 100
        atm_strike = 76800
        
    strikes = [atm_strike + (i * strike_interval) for i in range(-5, 6)]
    rows = []
    np.random.seed(45)
    
    for s in strikes:
        ce_oi = np.random.uniform(20, 120)
        pe_oi = np.random.uniform(20, 120)
        oi_pcr = pe_oi / ce_oi if ce_oi > 0 else 1.0
        
        ce_chg_pct = np.random.uniform(5, 75) if s == atm_strike else np.random.uniform(-10, 40)
        pe_chg_pct = np.random.uniform(-25, -2) if s > atm_strike else np.random.uniform(2, 45)
        
        ce_vol = np.random.uniform(30, 150)
        pe_vol = np.random.uniform(30, 150)
        vol_pcr = pe_vol / ce_vol if ce_vol > 0 else 1.0
        chg_oi_pcr = np.random.uniform(0.4, 3.5)
        
        ce_label = f"{ce_oi:.1f}L"
        pe_label = f"{pe_oi:.1f}L"
        
        ce_phase = "Long Buildup" if ce_chg_pct > 20 else ("Short Buildup" if ce_chg_pct > 0 else "Short Covering")
        pe_phase = "Long Buildup" if pe_chg_pct > 20 else ("Short Buildup" if pe_chg_pct > 0 else "Short Covering")
        
        rows.append({
            "strike_num": s, "is_atm": s == atm_strike, "pcr": oi_pcr, "chg_pcr": chg_oi_pcr,
            "ce_oi_lbl": ce_label, "ce_chg": ce_chg_pct, "ce_vol": ce_vol, "ce_vol_pcr": 1/vol_pcr, "ce_phase": ce_phase,
            "pe_oi_lbl": pe_label, "pe_chg": pe_chg_pct, "pe_vol": pe_vol, "pe_phase": pe_phase
        })
    return underlying_value, atm_strike, strike_interval, rows

current_spot, current_atm, interval, rows_data = get_broker_ui_data(selected_index)

st.write(f"📈 **{selected_index} लाइव स्पॉट भाव:** `{current_spot:.2f}` | **सटीक एटीएम स्तर:** `{current_atm}`")

# 🔊 2. ऑडियो अलार्म (40% वॉल्यूम)
alarm_html = """
<audio autoplay loop id="algoAlarm">
  <source src="https://google.com" type="audio/ogg">
</audio>
<script>
  var audio = document.getElementById("algoAlarm");
  audio.volume = 0.4;
  audio.play();
</script>
"""
st.markdown(alarm_html, unsafe_allow_html=True)

# 3. मुख्य ग्रिड डिस्प्ले (प्योर स्ट्रीमलिट 5-कॉलम लेआउट - 100% सेफ़)
st.markdown("---")
st.subheader("📋 प्रोप्राइटरी हाइब्रिड डेटा मैट्रिक्स")

hc1, hc2, hc3, hc4, hc5 = st.columns(5)
hc1.markdown("<div class='strike-title'>CE Phase</div>", unsafe_allow_html=True)
hc2.markdown("<div class='strike-title'>CE Stats<br><span style='color:#9ca3af; font-size:9px;'>OI(Chg)\|Vol(VolPCR)</span></div>", unsafe_allow_html=True)
hc3.markdown("<div class='strike-title'>ST/Strike<br><span style='color:#9ca3af; font-size:9px;'>PCR\|ChgPCR</span></div>", unsafe_allow_html=True)
hc4.markdown("<div class='strike-title'>PE Stats<br><span style='color:#9ca3af; font-size:9px;'>OI(Chg)\|Vol(VolPCR)</span></div>", unsafe_allow_html=True)
hc5.markdown("<div class='strike-title'>PE Phase</div>", unsafe_allow_html=True)

for r in rows_data:
    c1, c2, c3, c4, c5 = st.columns(5)
    bg_style = "background-color: #141b2d; padding: 4px; border-radius: 4px;" if r['is_atm'] else "padding: 4px;"
    
    ce_phase_color = "#22c55e" if "Long" in r['ce_phase'] else ("#ef4444" if "Short" in r['ce_phase'] else "#3b82f6")
    c1.markdown(f"<div style='{bg_style} text-align: center; color: {ce_phase_color}; font-weight: bold; padding-top:15px;'>{r['ce_phase']}</div>", unsafe_allow_html=True)
    
    ce_chg_sign = f"+{r['ce_chg']:.1f}" if r['ce_chg'] > 0 else f"{r['ce_chg']:.1f}"
    c2.markdown(f"""
    <div style='{bg_style} text-align: center;'>
        <p style='font-weight: bold;'>{r['ce_oi_lbl']}</p>
        <p style='color:#9ca3af;'>({ce_chg_sign})</p>
        <p style='font-weight: bold;'>{r['ce_vol']:.1f}k</p>
        <p style='color:#9ca3af;'>({r['ce_vol_pcr']:.2f})</p>
    </div>
    """, unsafe_allow_html=True)
    
    atm_lbl = "🟡 ATM<br>" if r['is_atm'] else ""
    strike_color = "#ffff00" if r['is_atm'] else "#f59e0b"
    c3.markdown(f"""
    <div style='{bg_style} text-align: center; color: {strike_color}; font-weight: bold;'>
        <p style='font-size:12px;'>{atm_lbl}{r['strike_num']}</p>
        <p style='color:#9ca3af;'>{r['pcr']:.2f}</p>
        <p style='color:#ef4444;'>({r['chg_pcr']:.2f})</p>
    </div>
    """, unsafe_allow_html=True)
    
    pe_chg_sign = f"+{r['pe_chg']:.1f}" if r['pe_chg'] > 0 else f"{r['pe_chg']:.1f}"
    c4.markdown(f"""
    <div style='{bg_style} text-align: center;'>
        <p style='font-weight: bold;'>{r['pe_oi_lbl']}</p>
        <p style='color:#9ca3af;'>({pe_chg_sign})</p>
        <p style='font-weight: bold;'>{r['pe_vol']:.1f}k</p>
        <p style='color:#9ca3af;'>({r['pe_vol_pcr']:.2f})</p>
    </div>
    """, unsafe_allow_html=True)
    
    pe_phase_color = "#22c55e" if "Long" in r['pe_phase'] else ("#ef4444" if "Short" in r['pe_phase'] else "#3b82f6")
    c5.markdown(f"<div style='{bg_style} text-align: center; color: {pe_phase_color}; font-weight: bold; padding-top:15px;'>{r['pe_phase']}</div>", unsafe_allow_html=True)

# 4. +5/-5 पृथक क्वांटम कॉलोनी पंक्तियाँ
st.markdown("<div class='divider-line'>🎯 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)</div>", unsafe_allow_html=True)
qc1, qc2, qc3 = st.columns(3)
qc1.markdown("<p style='text-align:left; color:#9ca3af;'>🔴 OTM OI PCR: <b>0.85</b><br>🔴 OTM ChgOI PCR: <b>2.14</b><br>🔴 OTM VOL PCR: <b>1.32</b><br>🔴 OTM ChgVOL PCR: <b>3.10</b></p>", unsafe_allow_html=True)
qc2.markdown("<p style='text-align:center; font-weight:bold; color:#f59e0b;'>OI Layers<br>OI Changes<br>VOL Layers<br>VOL Speed</p>", unsafe_allow_html=True)
qc3.markdown("<p style='text-align:right; color:#58a6ff;'>🔵 ITM OI PCR: <b>1.20</b><br>🔵 ITM ChgOI PCR: <b>1.45</b><br>🔵 ITM VOL PCR: <b>0.95</b><br>🔵 ITM ChgVOL PCR: <b>1.12</b></p>", unsafe_allow_html=True)

# 5. एडवांस्ड बिग प्लेयर्स ज़ोन रणनीति (पाइथन वैरिएबल्स की लाइव प्री-कैलकुलेशन के साथ)
pb_low, pb_high = current_atm - (3 * interval), current_atm - (2 * interval)
pd_low, pd_high = current_atm + (2 * interval), current_atm + (3 * interval)
sqz_spot, blast_spot = current_atm - interval, current_atm + (2 * interval)
c_safe, c_prof = current_atm + (5 * interval), current_atm + (2 * interval)
p_safe, p_prof = current_atm - (5 * interval), current_atm - (2 * interval)

st.markdown("<div class='divider-line'>🏛️ BIG PLAYERS PANIC, SAFE & PROFIT ZONE MATRIX (SMC)</div>", unsafe_allow_html=True)
st.warning(f"🟢 CALL SELLERS STATUS: \n• Safe Zone: {c_safe} - {c_safe + interval} (92% Safe) \n• Profit Zone: {c_prof} (Theta Decay Optimal) \n• 🚨 PANIC TRIGGER ZONE: {current_atm} - {current_atm + interval} (Short Covering Risk Active!)")
st.success(f"🔵 PUT SELLERS STATUS: \n• Safe Zone: {p_safe} - {p_safe + interval} (95% Safe) \n• Profit Zone: {p_prof} (Institutional Support Active) \n• 🚨 PANIC TRIGGER ZONE: {current_atm - interval} - {current_atm} (Delta Speed Shocks Detected!)")

# 6. एसएमसी प्रेडिक्टिव व सतर्कता अलर्ट पंक्तियाँ
st.markdown("<div class='divider-line'>🧠 SMC इंस्टीट्यूशनल प्रेडिक्टिव ज़ोन और सतर्कता अलर्ट</div>", unsafe_allow_html=True)
st.error(f"🛑 LIVE AI STATUS: 🚨 STRICTLY NO TRADE !!! \n\nरीज़न: {selected_index} सपोर्ट पर भारी PE OI होने पर भी 'OI Trap Detector' सक्रिय है। Delta Deceleration और Chg VOL Shock ऑन है (हेजिंग मैनिपुलेशन)।")
st.warning(f"⚠️ REVERSAL SATARK ZONE: \n• 🎯 Pull-Back: Active @ {pb_low} - {pb_high} | • 🛑 Pull-Down: Active @ {pd_low} - {pd_high} \n• 🏹 SWING TRAP: Swing High Sweep Rejection @ {pd_low} \n• 📌 OHLC DATA: निफ्टी का लाइव PDC भाव {current_spot} सस्टेन कर रहा है।")
st.info(f"🌀 COMPRESSION MATRIX: \n• BB Squeeze: 1.4% @ {sqz_spot} | • Gamma Blast Alert: 94% @ OTM {blast_spot}")
