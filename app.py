import streamlit as st
import folium

from streamlit_folium import st_folium
from weather import get_weather
from terrain import get_terrain
from utils.predict import predict_risk
from utils.auth import render_user_menu
from utils.chat_widget import render_chat_widget

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Landslide Risk Predictor",
    page_icon="🏔️",
    layout="wide"
)

# =========================
# LOAD CSS
# =========================

with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

render_user_menu()

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown(
    """
    <div class="sidebar-title">
    <span class="brand-mark">▲</span> Landslide AI
    </div>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <div class="sidebar-status">
        <span class="status-dot"></span>
        <div><strong>System Status</strong><b>Operational</b><small>All systems normal</small></div>
    </div>
    """,
    unsafe_allow_html=True
    )

    st.markdown("<div class='sidebar-section-label'>Recent conversations</div>", unsafe_allow_html=True)
    messages = st.session_state.get("messages", [])
    user_prompts = [message["content"] for message in messages if message["role"] == "user"]

    if user_prompts:
        for history_index, prompt in enumerate(reversed(user_prompts[-6:])):
            history_title = prompt.strip().replace("\n", " ")
            if len(history_title) > 30:
                history_title = f"{history_title[:30]}..."
            if st.button(history_title, key=f"sidebar_history_{history_index}", use_container_width=True):
                st.switch_page("pages/7_AI_Assistant.py")
    else:
        st.markdown("<div class='sidebar-empty-history'>No conversations yet.<br>Ask the assistant about your location.</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-profile-divider'></div>", unsafe_allow_html=True)
    current_user = st.session_state.get("user")
    profile_label = f"👤 {current_user['name']}" if current_user else "👤 Open profile"
    if st.button(profile_label, key="sidebar_profile_button", use_container_width=True):
        st.switch_page("pages/9_Profile.py")

# =========================
# HEADER
# =========================

st.markdown("<div class='dashboard-shell-anchor'></div>", unsafe_allow_html=True)

st.markdown(
"""
<div class="main-title">
<span class="main-brand-mark">▲</span> Landslide Risk Predictor
</div>

<div class="subtitle">
AI/ML-based landslide susceptibility prediction for Northeast India.
</div>
""",
unsafe_allow_html=True
)

st.markdown("<div class='section-kicker'>01 <span>Location</span></div>", unsafe_allow_html=True)

# =========================
# LOCATION INPUT
# =========================

col1, col2, col3 = st.columns([3,3,2])

with col1:
    latitude = st.number_input(
    "Latitude",
    value=24.5000
)
    

with col2:
    longitude = st.number_input(
    "Longitude",
    value=93.5000
)
st.session_state["latitude"] = latitude
st.session_state["longitude"] = longitude


with col3:
    st.write("")
    st.write("")
    analyze_clicked = st.button(
        "Analyze Location",
        use_container_width=True
    )

# =========================
# WEATHER VALUES
# =========================

weather = get_weather(latitude, longitude)

if weather:
    temperature = weather["temperature"]
    humidity = weather["humidity"]
    rain = weather["rain"]
else:
    temperature = "N/A"
    humidity = "N/A"
    rain = "N/A"

# =========================
# TERRAIN VALUES
# =========================

terrain = get_terrain(latitude, longitude)

if terrain:
    elevation = terrain["elevation"]
else:
    elevation = "N/A"

# =========================
# RISK PREDICTION
# =========================

if weather and terrain:
    risk_score = predict_risk(
        temperature=weather["temperature"],
        humidity=weather["humidity"],
        rainfall=weather["rain"],
        elevation=terrain["elevation"]
    )
else:
    risk_score = 0

if risk_score < 30:
    risk_level = "Low Risk"
elif risk_score < 70:
    risk_level = "Moderate Risk"
else:
    risk_level = "High Risk"

render_chat_widget(latitude, longitude)

# =========================
# MAP SECTION
# =========================

st.subheader("🗺️ Terrain Map")

terrain_map = folium.Map(
    location=[latitude, longitude],
    zoom_start=10
)

folium.Marker(
    [latitude, longitude],
    tooltip="Selected Location",
    popup=f"Lat: {latitude}, Lon: {longitude}"
).add_to(terrain_map)

st_folium(
    terrain_map,
    width=None,
    height=305
)

st.divider()

# =========================
# INFO CARDS
# =========================

col1, col2, col3 = st.columns(3)

# Weather Card

with col1:

    st.markdown(
    f"""
    <div class="card weather-card">
        <div class="card-kicker">02 &nbsp; Current Weather</div>
        <p class="card-caption">Live conditions at selected location</p>
        <h2>{temperature} °C</h2>
        <p>Humidity: {humidity}%</p>
        <p>Rain: {rain} mm</p>
    </div>
    """,
    unsafe_allow_html=True
    )

# Terrain Card

with col2:

    st.markdown(
    f"""
    <div class="card terrain-card">
        <div class="card-kicker">03 &nbsp; Terrain Overview</div>
        <p class="card-caption">Key terrain metrics</p>
        <h2>{elevation} m</h2>
        <p>Elevation</p>
    </div>
    """,
    unsafe_allow_html=True
    )

# Risk Card

with col3:

    st.markdown(
    f"""
    <div class="card risk-card">
        <div class="card-kicker">04 &nbsp; Risk Prediction</div>
        <p class="card-caption">AI/ML model prediction</p>
        <h2>{risk_score}%</h2>
        <p>{risk_level}</p>
    </div>
    """,
    unsafe_allow_html=True
    )

st.divider()

# =========================
# ALERT SECTION
# =========================

st.markdown("## 🚨 Recent Alerts")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
    """
    <div class="alert-card">
        🔴 High Risk Detected
    </div>
    """,
    unsafe_allow_html=True
    )

with c2:
    st.markdown(
    """
    <div class="alert-card">
        🟠 Heavy Rainfall Warning
    </div>
    """,
    unsafe_allow_html=True
    )

with c3:
    st.markdown(
    """
    <div class="alert-card">
        🟢 Data Updated Successfully
    </div>
    """,
    unsafe_allow_html=True
    )