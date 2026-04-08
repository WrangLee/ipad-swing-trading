import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.title("⚖️ RiskCalc — Position Sizing")

# Sidebar inputs
st.sidebar.header("🧮 Inputs")
account_size = st.sidebar.number_input("💰 Account ($)", 100, 10000000, 10000, 100)
risk_pct = st.sidebar.slider("🎯 Risk %", 0.25, 5.0, 1.0, 0.25)
ticker = st.sidebar.text_input("📌 Ticker", "AAPL")
entry_price = st.sidebar.number_input("📈 Entry ($)", 0.01, 100000, 150.0, 0.5)
stop_price = st.sidebar.number_input("🛑 Stop ($)", 0.01, 100000, 145.0, 0.5)
target_price = st.sidebar.number_input("🎯 Target ($)", 0.01, 100000, 165.0, 0.5)

if risk_pct > 2.0:
    st.sidebar.warning(f"⚠️ {risk_pct}% is aggressive!")

# Auto-fetch ATR stops
if st.sidebar.button("🛑 Get ATR Stops"):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history("3mo")
        high_low = df['High'] - df['Low']
        high_close = abs(df['High'] - df['Close'].shift())
        low_close = abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
        price = df['Close'].iloc[-1]

        st.sidebar.success(f"**ATR: ${atr:.2f} ({atr/price*100:.1f}%)**")
        stops = [
            (1.0, round(price - atr, 2)),
            (1.5, round(price - atr * 1.5, 2)),
            (2.0, round(price - atr * 2.0, 2)),
        ]
        for mult, stop in stops:
            st.sidebar.write(f"{mult}x ATR: **${stop}**")
    except:
        st.sidebar.error("Error fetching data")

# Calculate
if stop_price >= entry_price:
    st.error("🛑 Stop must be BELOW entry!")
    st.stop()

risk_amount = account_size * (risk_pct / 100)
risk_per_share = entry_price - stop_price
stop_pct = risk_per_share / entry_price * 100
shares = int(risk_amount / risk_per_share)
pos_cost = shares * entry_price
pos_pct = pos_cost / account_size * 100
actual_risk = shares * risk_per_share
actual_risk_pct = actual_risk / account_size * 100

reward_per_share = target_price - entry_price
profit = shares * reward_per_share
target_pct = reward_per_share / entry_price * 100
rr = reward_per_share / risk_per_share
breakeven = 1 / (1 + rr) * 100 if rr > 0 else 100

# Grade
grade = "🟢 EXCELLENT" if rr >= 3 else "🟢 GOOD" if rr >= 2 else "🟡 OK" if rr >= 1.5 else "🔴 POOR"

# Results
col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Shares", shares)
col2.metric("💰 Cost", f"${pos_cost:,.0f}", f"{pos_pct:.0f}% acct")
col3.metric("🛑 Risk", f"${actual_risk:,.0f}", f"{actual_risk_pct:.1f}%")
col4.metric("⚖️ R:R", f"1:{rr:.1f}", grade)

st.subheader("📐 Trade Plan")
col1, col2, col3 = st.columns(3)
col1.markdown(f"**Entry:** ${entry_price:.2f}")
col2.markdown(f"**Stop:** ${stop_price:.2f} (-{stop_pct:.1f}%)")
col3.markdown(f"**Target:** ${target_price:.2f} (+{target_pct:.1f}%)")

st.subheader("📊 Quality Analysis")
st.info(
    f"You need to win **{breakeven:.0f}%** of trades to break even. "
    f"With 50% win rate, each trade EV = **${(0.5*profit) - (0.5*actual_risk):+,.0f}**"
)

# Ruin table
st.subheader("📉 Ruin Risk (at 1% risk)")
col1, col2, col3 = st.columns(3)
ruin_data = []
for losses in [10, 20]:
    remaining = (1 - risk_pct/100)**losses
    ruin_data.append(f"{losses} losses → {remaining*100:.0f}% remaining")
st.text("\n".join(ruin_data))

st.caption("⚖️ RiskCalc | For swing traders | Risk management is your edge!")
