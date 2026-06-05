import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# वाइड लेआउट और डार्क मोड सेटिंग
st.set_page_config(layout="wide", page_title="Nifty Live FnO Dashboard")

st.title("📊 लाइव निफ्टी ऑप्शन चेन (OI & Change in OI) डैशबोर्ड")
st.write("यह डेटा सीधे NSE की लाइव वेबसाइट से सिंक होकर आपके मोबाइल पर दिखेगा।")

# NSE से लाइव ऑप्शन चेन डेटा फेच करने का फंक्शन
def get_live_option_chain():
    url = "https://nseindia.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    session = requests.Session()
    # कुकीज सेट करना जरूरी है ताकि ब्लॉक न हो
    session.get("https://nseindia.com", headers=headers)
    response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# डेटा प्रोसेसिंग
try:
    raw_data = get_live_option_chain()
    
    if raw_data and 'records' in raw_data:
        underlying_value = raw_data['records']['underlyingValue']
        st.sidebar.metric(label="Nifty Live Price", value=f"{underlying_value:,.2f}")
        
        expiry_date = raw_data['records']['expiryDates']
        st.sidebar.write(f"**करंट एक्सपायरी:** {expiry_date}")
        
        option_data = raw_data['filtered']['data']
        
        # डेटा को टेबल फॉर्मेट में सेट करना
        rows = []
        for market in option_data:
            strike = market['strikePrice']
            
            # CE (Call Option) डेटा
            ce_oi = market.get('CE', {}).get('openInterest', 0)
            ce_chg_oi = market.get('CE', {}).get('changeinOpenInterest', 0)
            
            # PE (Put Option) डेटा
            pe_oi = market.get('PE', {}).get('openInterest', 0)
            pe_chg_oi = market.get('PE', {}).get('changeinOpenInterest', 0)
            
            # सेंटीमेंट का लॉजिक
            ce_phase = "Long Buildup" if ce_chg_oi > 0 else "Long Unwind"
            pe_phase = "Short Buildup" if pe_chg_oi > 0 else "Short Covering"
            
            rows.append({
                "CE Chg OI": ce_chg_oi,
                "CE OI (Lakhs)": round(ce_oi / 100000, 2),
                "CE Sentiment": ce_phase,
                "Strike Price": strike,
                "PE Sentiment": pe_phase,
                "PE OI (Lakhs)": round(pe_oi / 100000, 2),
                "PE Chg OI": pe_chg_oi
            })
            
        df = pd.DataFrame(rows)
        
        # एटीएम (ATM) के पास की 10 स्ट्राइक्स फिल्टर करना
        df['diff'] = (df['Strike Price'] - underlying_value).abs()
        df = df.sort_values('diff').head(10).sort_values('Strike Price').drop(columns=['diff'])
        
        # स्टाइलिंग और कलर कोडिंग
        def color_sentiment(val):
            if "Long" in str(val) or "Covering" in str(val):
                return 'color: #00ff00; font-weight: bold;'
            elif "Short" in str(val):
                return 'color: #ff0000; font-weight: bold;'
            return ''

        st.subheader("📋 लाइव OI और Change in OI स्क्रीनर टेबल")
        
        styled_df = df.style.applymap(color_sentiment, subset=['CE Sentiment', 'PE Sentiment'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # विज़ुअल चार्ट
        st.subheader("📊 कॉल बनाम पुट ओपन INTEREST (OI) तुलना")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Strike Price'], y=df['CE OI (Lakhs)'], name='Call OI (Resistance)', marker_color='red'))
        fig.add_trace(go.Bar(x=df['Strike Price'], y=df['PE OI (Lakhs)'], name='Put OI (Support)', marker_color='green'))
        fig.update_layout(barmode='group', template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("NSE से लाइव डेटा नहीं मिल पा रहा है।")

except Exception as e:
    st.info("मार्केट ऑवर्स (9:15 AM - 3:30 PM) के दौरान डेटा लाइव दिखेगा।")
