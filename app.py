import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Nifty Live FnO Dashboard")

st.title("📊 लाइव निफ्टी ऑप्शन चेन (OI & Change in OI) डैशबोर्ड")
st.write("यह डेटा सीधे मार्केट सोर्स से सिंक होकर आपके मोबाइल पर दिखेगा।")

# डमी/सिम्युलेटेड डेटा जब लाइव मार्केट बंद हो (ताकि ऐप कभी खाली न दिखे)
def get_mock_data():
    underlying_value = 23500.0
    strikes = [23300, 23350, 23400, 23450, 23500, 23550, 23600, 23650, 23700]
    rows = []
    for s in strikes:
        rows.append({
            "CE Chg OI": 1200 if s >= 23500 else -400,
            "CE OI (Lakhs)": round((25000 if s >= 23500 else 8000) / 100, 2),
            "CE Sentiment": "Long Buildup" if s >= 23500 else "Short Covering",
            "Strike Price": s,
            "PE Sentiment": "Short Buildup" if s < 23500 else "Long Unwind",
            "PE OI (Lakhs)": round((30000 if s < 23500 else 5000) / 100, 2),
            "PE Chg OI": 1500 if s < 23500 else -200
        })
    return underlying_value, "11-Jun-2026", rows

# सीधे एनालिसिस मोड चालू करना
underlying_value, expiry_date, rows = get_mock_data()
df = pd.DataFrame(rows)

# यूआई रेंडरिंग
st.sidebar.metric(label="Nifty Price", value=f"{underlying_value:,.2f}")
st.sidebar.write(f"**एक्सपायरी:** {expiry_date}")
st.sidebar.info("🟡 विश्लेषक मोड (मार्केट क्लोज्ड / ऑफलाइन डेटा)")

def color_sentiment(val):
    if "Long" in str(val) or "Covering" in str(val):
        return 'color: #00ff00; font-weight: bold;'
    elif "Short" in str(val):
        return 'color: #ff0000; font-weight: bold;'
    return ''

st.subheader("📋 OI और Change in OI स्क्रीनर टेबल")
# यहाँ हमने नए पाइथन अपडेट के अनुसार एरर फ्री .map() का उपयोग कर दिया है
styled_df = df.style.map(color_sentiment, subset=['CE Sentiment', 'PE Sentiment'])
st.dataframe(styled_df, use_container_width=True, hide_index=True)

st.subheader("📊 कॉल बनाम पुट ओपन इंटरेस्ट (OI) तुलना")
fig = go.Figure()
fig.add_trace(go.Bar(x=df['Strike Price'], y=df['CE OI (Lakhs)'], name='Call OI (Resistance)', marker_color='red'))
fig.add_trace(go.Bar(x=df['Strike Price'], y=df['PE OI (Lakhs)'], name='Put OI (Support)', marker_color='green'))
fig.update_layout(barmode='group', template='plotly_dark', height=400)
st.plotly_chart(fig, use_container_width=True)
