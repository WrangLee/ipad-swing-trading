import streamlit as st

# Page config
st.set_page_config(
    page_title="📊 Swing Trading Suite",
    page_icon="📊",
    layout="wide"
)

st.title("📊 iPad Swing Trading Suite")
st.markdown("**All 7 apps in one place. Touch-friendly. Free forever.**")

# Daily workflow tabs
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 SwingFinder\n(Find Stocks)", use_container_width=True, height=120):
        st.switch_page("pages/2_swingfinder.py")

with col2:
    if st.button("⚖️ RiskCalc\n(Position Sizing)", use_container_width=True, height=120):
        st.switch_page("pages/3_riskcalc.py")

with col3:
    if st.button("📓 TradeReview\n(Journal)", use_container_width=True, height=120):
        st.switch_page("pages/4_tradereview.py")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚦 MarketPulse\n(Market Health)", use_container_width=True, height=120):
        st.switch_page("pages/5_marketpulse.py")

with col2:
    if st.button("🌍 MacroLens\n(Economic Regime)", use_container_width=True, height=120):
        st.switch_page("pages/6_macrolens.py")

with col3:
    if st.button("📡 CatalystRadar\n(Earnings Check)", use_container_width=True, height=120):
        st.switch_page("pages/7_catalystradar.py")

with st.columns(1)[0]:
    if st.button("🧠 TechnicianPro\n(Auto Patterns)", use_container_width=True, height=120):
        st.switch_page("pages/8_technicianpro.py")

st.markdown("---")
st.caption(
    "💡 **Daily Workflow:**\n"
    "1. MarketPulse → Is market OK today?\n"
    "2. MacroLens → Economic regime check\n"
    "3. SwingFinder → Find candidates\n"
    "4. CatalystRadar → No earnings risks?\n"
    "5. TechnicianPro → Auto pattern analysis\n"
    "6. RiskCalc → Size position\n"
    "7. TradeReview → Log trades\n\n"
    "**Built for iPad Safari. Free hosting forever.**"
)
