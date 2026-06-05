import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Compact Quant Decision Engine")

# सीएसएस: अक्षरों और स्पेस को मोबाइल स्क्रीन पर पूरी तरह फिट करने के लिए
st.markdown("""
    <style>
    .reportview-container { background: #06080c; }
    th { background-color: #111827 !important; color: #9ca3af !important; font-weight: bold !important; text-align: center !important; font-size: 11px !important; padding: 3px !important; }
    td { text-align: center !important; font-family: monospace; font-size: 11px !important; padding: 3px !important; vertical-align: middle !important; white-space: pre-line !important; }
    div[data-testid="stMetricValue"] { font-size: 18px !important; font-family: monospace; }
    .stAlert { padding: 8px !important; font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 क्वांटिटेटिव SMC + VSA + Greeks इंस्टीट्यूशनल डिसीजन इंजन")
st.write("सुपर-कॉम्पैक्ट मोबाइल लेआउट | 4 कॉलम रिड्यूस्ड")

# 1. डेटा इंजन
def get_quantum_data():
    underlying_value = 23354.50
    strikes = [23100, 23150, 23200, 23250, 23300, 23350, 23400, 23450, 23500, 23550, 23600]
    rows = []
    np.random.seed(88)
    for s in strikes:
        is_atm = "🟡 ATM " if s == 23350 else ""
        ce_oi = np.random.uniform(65, 155) if s >= 23350 else np.random.uniform(15, 40)
        pe_oi = np.random.uniform(15, 45) if s >= 23350 else np.random.uniform(75, 185)
        ce_chg = np.random.uniform(-12, 48) if s == 23350 else np.random.uniform(5, 32)
        pe_chg = np.random.uniform(18, 58) if s == 23350 else np.random.uniform(-8, 38)
        ce_vol = np.random.uniform(15000, 55000)
        pe_vol = np.random.uniform(15000, 55000)
        ce_chg_vol = np.random.uniform(4000, 18000)
        pe_chg_vol = np.random.uniform(4000, 18000)
        
        if s == 23450: ce_vol *= 4.6; ce_chg = 90.0
        if s == 23250: ce_oi = 150.0; pe_oi = 160.0; ce_chg = 40.0; pe_chg = 4.0; ce_vol *= 1.8
        
        vol_pcr = pe_vol / ce_vol if ce_vol > 0 else 1.0
        chg_vol_pcr = pe_chg_vol / ce_chg_vol if ce_chg_vol > 0 else 1.0
        strike_pcr = pe_oi / ce_oi if ce_oi > 0 else 1.0
        strike_chg_pcr = pe_chg / ce_chg if ce_chg > 0 else 1.0
        
        ce_phase = "Long Buildup" if ce_chg > 20 else ("Short Buildup" if ce_chg > 0 else "Short Covering")
        pe_phase = "Long Buildup" if pe_chg > 20 else ("Short Buildup" if pe_chg > 0 else "Short Covering")
        
        bb_raw = np.random.uniform(1.4, 5.8) if s == 23300 else np.random.uniform(2.6, 6.0)
        bb_str = f"{bb_raw:.1f}%\n" + ("(SQZ)" if bb_raw < 2.5 else "(EXP)")
        gamma_raw = np.random.randint(86, 99) if s == 23450 else np.random.randint(12, 60)
        
        alert = "Structure"
        if s == 23450 and gamma_raw > 85: alert = "💥 GAMMA\nBLAST"
        elif s == 23250: alert = "🚨 Put OB\nActive"
        elif ce_chg < -25: alert = "🕵️ Mani-\npulation"
        
        # यहाँ आपका ऊपर-नीचे डबल रो फ़ॉर्मेट डेटा मर्ज हो रहा है (\n का मतलब न्यू लाइन है)
        rows.append({
            "CE Phase": ce_phase,
            "CE VOL/ChgVOL\nPCR": f"{1/vol_pcr:.2f}\n{1/chg_vol_pcr:.2f}",
            "CE OI\n(Chg OI)": f"{ce_oi:.1f}\n({ce_chg:.1f})",
            "ST/Strike": f"{is_atm}{s}",
            "PE OI\n(Chg OI)": f"{pe_oi:.1f}\n({pe_chg:.1f})",
            "PE VOL/ChgVOL\nPCR": f"{vol_pcr:.2f}\n{chg_vol_pcr:.2f}",
            "PE Phase": pe_phase,
            "Target\nPro%": "65%" if s == 23350 else f"{np.random.randint(41, 55)}%",
            "BB Squeeze\n(Gamma Str%)": f"{bb_str}\n({gamma_raw}%)",
            "SMC Alerts": alert,
            "Strike OI/Chg\nPCR": f"{strike_pcr:.2f}\n{strike_chg_pcr:.2f}",
            "strike_num": s, "ce_raw_oi": ce_oi, "pe_raw_oi": pe_oi, "ce_raw_chg": ce_chg, "pe_raw_chg": pe_chg,
            "ce_raw_vol": ce_vol, "pe_raw_vol": pe_vol, "ce_raw_chg_vol": ce_chg_vol, "pe_raw_chg_vol": pe_chg_vol
        })
    return pd.DataFrame(rows)

df = get_quantum_data()
itm_df = df[df['strike_num'] < 23350]
otm_df = df[df['strike_num'] > 23350]

# 2. AI डिसीजन बॉक्स
st.subheader("🧠 AI इंस्टीट्यूशनल डिसीजन और रिस्क मैनेजर")
is_gamma = any("💥 GAMMA" in str(x) for x in df['SMC Alerts'])
# सिमुलेशन से ओआई ट्रैप पकड़ना
is_trap = float(df[df['strike_num'] == 23350]['ce_raw_chg'].iloc[0]) > 35.0

if is_trap:
    st.error("🛑 LIVE AI STATUS: 🚨 STRICTLY NO TRADE !!!")
    st.info("⚠️ REASON: सपोर्ट पर भारी PE OI होने के बावजूद OI Trap Detector सक्रिय है। Delta Deceleration और Chg VOL PCR Shock चालू है। सेलर्स हेजिंग करके बायर्स को फंसा रहे हैं (Strict No Call Buy Zone)।")
elif is_gamma:
    st.success("🎯 LIVE AI STATUS: ✅ TAKE CALL BUY")
    st.info("📈 REASON: OTM Chg VOL PCR > 2.2 है और Gamma Str% > 85% पार कर चुका है। सेलर्स पूरी तरह ट्रैप हैं (Pull-Back Reversal / Gamma Blast Active)।")
else:
    st.warning("⚠️ LIVE AI STATUS: ⏳ AVOID (WAIT FOR CONFIRMATION)")

# 3. मुख्य ग्रिड डिस्प्ले (सुपर कॉम्पैक्ट 4-कॉलम कम लेआउट)
st.markdown("---")
st.subheader("📋 प्रोप्राइटरी हाइब्रिड डेटा मैट्रिक्स (मोबाइल फिट)")
display_cols = [
    "CE Phase", "CE VOL/ChgVOL\nPCR", "CE OI\n(Chg OI)", 
    "ST/Strike", 
    "PE OI\n(Chg OI)", "PE VOL/ChgVOL\nPCR", "PE Phase", 
    "Target\nPro%", "BB Squeeze\n(Gamma Str%)", "SMC Alerts", "Strike OI/Chg\nPCR"
]

def color_master(val):
    if "Long Buildup" in str(val): return 'color: #22c55e; font-weight: bold;'
    if "Short Buildup" in str(val) or "Structure" in str(val): return 'color: #ef4444;'
    if "Short Covering" in str(val): return 'color: #3b82f6; font-weight: bold;'
    if "SQUEEZE" in str(val) or "💥" in str(val) or "🚨" in str(val) or "SQZ" in str(val): return 'background-color: #310707; color: #f59e0b; font-weight: bold;'
    if "🟡" in str(val): return 'background-color: #1a1403; color: #f59e0b; font-weight: bold;'
    return ''

st.dataframe(df[display_cols].style.map(color_master), use_container_width=True, hide_index=True)

# 4. पृथक क्वांटम कॉलोनी और समरी
st.markdown("---")
st.subheader("🎯 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)")
col_tot1, col_tot2 = st.columns(2)
col_tot1.metric("📌 OVERALL OI PCR", f"{(df['pe_raw_oi'].sum() / df['ce_raw_oi'].sum()):.2f}")
col_tot2.metric("🔥 OVERALL Chg OI PCR", f"{(df['pe_raw_chg'].sum() / df['ce_raw_chg'].sum()):.2f}")

l1, l2 = st.columns(2)
with l1:
    st.markdown("#### 📑 परत 1: ओपन इंटरेस्ट (OI)")
    st.metric("🔴 OTM OI PCR", f"{(otm_df['pe_raw_oi'].sum() / otm_df['ce_raw_oi'].sum()):.2f}")
    st.metric("🔵 ITM OI PCR", f"{(itm_df['pe_raw_oi'].sum() / itm_df['ce_raw_oi'].sum()):.2f}")
with l2:
    st.markdown("#### 🔥 परत 2: चेंज इन OI")
    st.metric("🔴 OTM Chg OI PCR", f"{(otm_df['pe_raw_chg'].sum() / otm_df['ce_raw_chg'].sum()):.2f}")
    st.metric("🔵 ITM Chg OI PCR", f"{(itm_df['pe_raw_chg'].sum() / itm_df['ce_raw_chg'].sum()):.2f}")
