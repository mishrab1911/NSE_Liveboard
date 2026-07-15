import streamlit as st
import pandas as pd

from datetime import datetime
from zoneinfo import ZoneInfo

from streamlit_autorefresh import st_autorefresh

from database import DatabaseManager
from historical_database import HistoricalDatabase
from config import COMPANIES


import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# DATABASE OBJECTS
# ==========================================================

db = DatabaseManager()
history_db = HistoricalDatabase()


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="NSE Live Dashboard",
    page_icon="📈",
    layout="wide"
)


# ==========================================================
# LOAD CSS
# ==========================================================

with open("styles/dashboard.css") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True
    )


# ==========================================================
# AUTO REFRESH
# ==========================================================

st_autorefresh(
    interval=3000,
    key="refresh"
)

# ==========================================================
# HEADER
# ==========================================================

top1, top2, top3, top4 = st.columns([7,1,2.3,2.3])

# ===================================================
# TITLE
# ===================================================

with top1:

    st.markdown("""
    # 📈 NSE LIVE STOCK DASHBOARD
    ### Real-Time NSE Market Monitoring
    """)

# ===================================================
# LIVE
# ===================================================

with top2:

    st.markdown(
        """
        <div style="
        color:#00ff00;
        font-size:36px;
        font-weight:bold;
        margin-top:15px;
        animation: blink 1s infinite;
        ">
        ● LIVE
        </div>

        <style>
        @keyframes blink {
            50% {
                opacity:0;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# ===================================================
# DIGITAL CLOCK
# ===================================================

with top3:

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    st.markdown(
        f"""
        <div style="
        text-align:center;
        padding-top:30px;
        ">

        <div style="
        color:#ff4444;
        font-size:20px;
        font-weight:bold;
        margin-bottom:1px;
        ">
        IST (India)
        </div>

        <div style="
        color:#ff4444;
        font-size:44px;
        font-weight:bold;
        line-height:1;
        ">
        {now.strftime("%H:%M:%S")}
        </div>

        <div style="
        color:black;
        font-size:18px;
        margin-top:2px;
        ">
        {now.strftime("%d-%b-%Y")}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ===================================================
# ANALOG CLOCK
# ===================================================

with top4:

    st.components.v1.html(
    """
    <html>

    <body style="
    margin:0;
    background:#071633;
    display:flex;
    justify-content:center;
    align-items:center;
    ">

    <canvas id="clock" width="240" height="260"></canvas>

    <script>

    const canvas =
    document.getElementById("clock");

    const ctx =
    canvas.getContext("2d");

    function drawClock(){

        ctx.clearRect(0,0,220,220);


        const cx = 110;
        const cy = 125;
        const radius = 65;


        ctx.beginPath();

        ctx.arc(
            cx,
            cy,
            radius,
            0,
            Math.PI * 2
        );

        ctx.strokeStyle = "#ff4444";
        ctx.lineWidth = 5;
        ctx.stroke();

        ctx.fillStyle = "#ff4444";
        ctx.font = "18px Arial";



        ctx.fillText("12",103,52);
        ctx.fillText("3",185,130);
        ctx.fillText("6",107,210);
        ctx.fillText("9",25,130);



        const now = new Date();

        let hour = now.getHours() % 12;
        let minute = now.getMinutes();
        let second = now.getSeconds();

        function drawHand(
            angle,
            length,
            width,
            color
        ){

            ctx.beginPath();

            ctx.lineWidth = width;

            ctx.strokeStyle = color;

            ctx.moveTo(cx,cy);

            ctx.lineTo(
                cx + length * Math.sin(angle),
                cy - length * Math.cos(angle)
            );

            ctx.stroke();
        }

        drawHand(
            (hour + minute/60) * Math.PI/6,
            40,
            6,
            "white"
        );

        drawHand(
            minute * Math.PI/30,
            55,
            4,
            "#cccccc"
        );

        drawHand(
            second * Math.PI/30,
            60,
            2,
            "#ff4444"
        );

        ctx.beginPath();

        ctx.arc(
            cx,
            cy,
            5,
            0,
            Math.PI*2
        );

        ctx.fillStyle = "#ff4444";

        ctx.fill();
    }

    setInterval(
        drawClock,
        1000
    );

    drawClock();

    </script>

    </body>

    </html>
    """,
    height=220
    )
# ==========================================================
# TOP FILTERS
# ==========================================================

f1, f2, f3 = st.columns([4,4,1])

with f1:

    company = st.selectbox(
        "🏢 Company",
        list(COMPANIES.keys())
    )

with f2:

    duration = st.selectbox(
        "⏱ Duration",
        [
            "15 Minutes",
            "1 Hour",
            "24 Hours"
        ]
    )


duration_map = {
    "15 Minutes": 15,
    "1 Hour": 60,
    "24 Hours": 1440
}

symbol = COMPANIES[company]

history = db.get_price_history(
    symbol,
    duration_map[duration]
)

if history:

    df = pd.DataFrame(
        history,
        columns=["Datetime", "Price"]
    )

    df["Datetime"] = pd.to_datetime(
        df["Datetime"]
    )

else:

    df = pd.DataFrame(
        columns=["Datetime", "Price"]
    )


# ==========================================================
# KPI ROW
# ==========================================================

if not df.empty:

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">Current Price</div>
            <div class="metric-value">
            ₹ {round(df['Price'].iloc[-1],2)}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">Highest</div>
            <div class="metric-value">
            ₹ {round(df['Price'].max(),2)}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">Lowest</div>
            <div class="metric-value">
            ₹ {round(df['Price'].min(),2)}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k4:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">Records</div>
            <div class="metric-value">
            {len(df)}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================================
# HISTORICAL FILTERS
# ==========================================================
st.markdown("<br><br> ", unsafe_allow_html=True)

st.divider()

hf1, hf2 = st.columns(2)

with hf1:

    hist_company = st.selectbox(
        "📚 Company",
        list(COMPANIES.keys()),
        key="hist_company"
    )

with hf2:

    hist_period = st.selectbox(
        "📅 Period",
        [
            "5 Day",
            "1 Month",
            "6 Month",
            "1 Year",
            "10 Year"
        ]
    )

hist_symbol = COMPANIES[hist_company]

history_data = history_db.get_history(
    hist_symbol
)

df_hist = pd.DataFrame(
    history_data,
    columns=[
        "Datetime",
        "Price"
    ]
)

if not df_hist.empty:

    df_hist["Datetime"] = pd.to_datetime(
        df_hist["Datetime"]
    )

    if hist_period == "5 Day":
        df_hist = df_hist.tail(5)

    elif hist_period == "1 Month":
        df_hist = df_hist.tail(30)

    elif hist_period == "6 Month":
        df_hist = df_hist.tail(180)

    elif hist_period == "1 Year":
        df_hist = df_hist.tail(365)


# ==========================================================
# QUADRANT DASHBOARD
# ==========================================================

row1_col1, row1_col2 = st.columns(2)

with row1_col1:

    st.subheader("📈 Live Price Trend")

    if not df.empty:

        fig = px.line(
            df,
            x="Datetime",
            y="Price",
            template="plotly_dark"
        )

        # fig.update_layout(
        #     height=400
        # )
        
        

        fig.update_layout(
            height=500,

            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),

            xaxis=dict(
                tickfont=dict(
                    size=20
                ),
                title_font=dict(
                    size=24
                )
            ),

            yaxis=dict(
                tickfont=dict(
                    size=20
                ),
                title_font=dict(
                    size=24
                )
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


with row1_col2:

    st.subheader("📊 Historical Analysis")

    if not df_hist.empty:

        fig2 = px.bar(
            df_hist,
            x="Datetime",
            y="Price",
            template="plotly_dark"
        )

        # fig2.update_layout(
        #     height=400
        # )
        
        

        fig2.update_layout(
            height=500,

            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),

            xaxis=dict(
                tickfont=dict(
                    size=20
                ),
                title_font=dict(
                    size=24
                )
            ),

            yaxis=dict(
                tickfont=dict(
                    size=20
                ),
                title_font=dict(
                    size=24
                )
            )
        )



        st.plotly_chart(
            fig2,
            use_container_width=True
        )


# ==========================================================
# SECOND ROW OF QUADRANTS
# ==========================================================

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.data_editor(
        df.tail(50),
        use_container_width=True,
        height=650,
        disabled=True
    )


with row2_col2:
    st.subheader("📊 Historical Statistics")

    c1,c2 = st.columns(2)

    with c1:

        st.metric(
            "Highest",
            round(df_hist["Price"].max(),2)
        )

        st.metric(
            "Lowest",
            round(df_hist["Price"].min(),2)
        )

    with c2:

        st.metric(
            "Average",
            round(df_hist["Price"].mean(),2)
        )

        st.metric(
            "Records",
            len(df_hist)
        )


# Scheduler


import streamlit as st
import threading
import time

from scheduler import run_scheduler_once

def scheduler_loop():
    while True:
        try:
            run_scheduler_once()
            print("Data Updated")
        except Exception as e:
            print(e)

        time.sleep(3)

if "scheduler_started" not in st.session_state:
    threading.Thread(
        target=scheduler_loop,
        daemon=True
    ).start()

    st.session_state.scheduler_started = True

st.title("NSE Liveboard")
st.write("Scheduler running every 3 seconds")
