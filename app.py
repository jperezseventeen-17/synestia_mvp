import streamlit as st
import pandas as pd
import plotly.express as px
# import openai # Uncomment when you have your API key ready

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Synestia | AI FP&A",
    page_icon="Fn",
    layout="wide"
)

# --- 2. SIDEBAR & FILE UPLOAD ---
st.sidebar.title("Synestia 🚀")
st.sidebar.write("Automated Financial Planning & Analysis")

uploaded_file = st.sidebar.file_uploader("Upload P&L Data (CSV)", type=["csv"])

# --- 3. HELPER FUNCTION TO GENERATE DUMMY DATA (For Demo Purposes) ---
def load_dummy_data():
    data = {
        'Date': pd.date_range(start='2024-01-01', periods=12, freq='M'),
        'Revenue': [10000, 12000, 15000, 14000, 18000, 22000, 25000, 24000, 28000, 32000, 35000, 38000],
        'Expenses': [8000, 8500, 9000, 9500, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000]
    }
    df = pd.DataFrame(data)
    df['Net Income'] = df['Revenue'] - df['Expenses']
    df['Margin %'] = (df['Net Income'] / df['Revenue']) * 100
    return df

# --- 4. MAIN DASHBOARD LOGIC ---
st.title("Synestia: Intelligent Financial Dashboard")
st.markdown("### Executive Summary")

# Load data (either uploaded or dummy)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Ensure Date is datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
else:
    st.info("👋 No file uploaded yet. Showing **Demo Data** so you can see Synestia in action.")
    df = load_dummy_data()

# Top Level Metrics
col1, col2, col3 = st.columns(3)
total_rev = df['Revenue'].sum()
total_exp = df['Expenses'].sum()
avg_margin = df['Margin %'].mean()

col1.metric("Total Revenue (YTD)", f"${total_rev:,.0f}", "+12%")
col2.metric("Total Expenses (YTD)", f"${total_exp:,.0f}", "-5%")
col3.metric("Avg. Profit Margin", f"{avg_margin:.1f}%", "+2.4%")

st.divider()

# --- 5. VISUALIZATIONS (Using Plotly) ---
c1, c2 = st.columns((2, 1))

with c1:
    st.subheader("Revenue vs. Expenses Trend")
    # Melt the dataframe for easy plotting
    df_melted = df.melt(id_vars=['Date'], value_vars=['Revenue', 'Expenses'], var_name='Category', value_name='Amount')
    fig = px.area(df_melted, x='Date', y='Amount', color='Category', 
                  color_discrete_map={'Revenue': '#636EFA', 'Expenses': '#EF553B'})
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Profit Margin Analysis")
    fig_margin = px.bar(df, x='Date', y='Margin %', color='
