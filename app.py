st.markdown("---")
st.subheader("📋 प्रोप्राइटरी हाइब्रिड डेटा接收 Matrix")

display_cols = [
    "CE Phase", "CE Vol PCR", "CE ChgOI", "CE OI", 
    "ST/Strike", 
    "PE OI", "PE ChgOI", "PE Vol PCR", "PE Phase",
    "Target Pro%", "BB Squeeze", "Gamma Str%", "SMC Alerts", "Strike PCR"
]

def color_locked_master_ui(val):
    if "Long Buildup" in str(val): return 'color: #22c55e; font-weight: bold;'
    if "Short Buildup" in str(val) or "Structure" in str(val): return 'color: #ef4444;'
    if "Short Covering" in str(val): return 'color: #3b82f6; font-weight: bold;'
    if "SQUEEZE" in str(val) or "💥" in str(val) or "🚨" in str(val): return 'background-color: #310707; color: #f59e0b; font-weight: bold;'
    if "🕵️" in str(val) or "🐳" in str(val) or "🏹" in str(val): return 'color: #cc66ff; font-weight: bold;'
    if "🟡" in str(val): return 'background-color: #1a1403; color: #f59e0b; font-weight: bold;'
    return ''

st.dataframe(df[display_cols].style.map(color_locked_master_ui), use_container_width=True, hide_index=True)
st.markdown("---")
st.markdown(f"### 📊 स्ट्राइक समरी (Overall Chain PCR)")
col_tot1, col_tot2 = st.columns(2)
col_tot1.metric("📌 OVERALL OI PCR", f"{(df['pe_raw_oi'].sum() / df['ce_raw_oi'].sum()):.2f}")
col_tot2.metric("🔥 OVERALL Chg OI PCR", f"{(df['pe_raw_chg'].sum() / df['ce_raw_chg'].sum()):.2f}")

st.markdown("---")
st.subheader("🎯 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)")

l1, l2, l3, l4 = st.columns(4)
with l1:
    st.markdown("#### 📑 परत 1: ओपन इंटरेस्ट (OI)")
    st.metric("🔴 OTM OI PCR", f"{otm_oi_pcr:.2f}")
    st.metric("🔵 ITM OI PCR", f"{itm_oi_pcr:.2f}")
with l2:
    st.markdown("#### 🔥 परत 2: चेंज इन OI")
    st.metric("🔴 OTM Chg OI PCR", f"{otm_chg_pcr:.2f}")
    st.metric("🔵 ITM Chg OI PCR", f"{itm_chg_pcr:.2f}")
with l3:
    st.markdown("#### ⚡ परत 3: वॉल्यूम (VOL)")
    st.metric("🔴 OTM VOL PCR", f"{otm_vol_pcr:.2f}")
    st.metric("🔵 ITM VOL PCR", f"{itm_vol_pcr:.2f}")
with l4:
    st.markdown("#### 🚀 परत 4: चेंज इन वॉल्यूम")
    st.metric("🔴 OTM Chg VOL PCR", f"{otm_chg_vol_pcr:.2f}")
    st.metric("🔵 ITM Chg VOL PCR", f"{itm_chg_vol_pcr:.2f}")
