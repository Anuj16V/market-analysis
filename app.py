import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page configuration
st.set_page_config(
    page_title="Hyperliquid Trader & Sentiment Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a sleek, premium dark theme
st.markdown("""
<style>
    /* Dark mode styling */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    /* Custom metric card styling */
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #6366f1;
    }
    .metric-val {
        font-size: 28px;
        font-weight: 700;
        color: #60a5fa;
        margin-top: 5px;
    }
    .metric-val-positive {
        color: #34d399 !important;
    }
    .metric-val-negative {
        color: #f87171 !important;
    }
    .metric-lbl {
        font-size: 14px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Tab customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px 8px 0px 0px !important;
        color: #94a3b8 !important;
        padding: 10px 20px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
        border-color: #3b82f6 !important;
    }
    
    /* Streamlit's native elements */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data():
    regime_stats = pd.read_csv("e:\\prime\\data\\regime_stats.csv")
    dir_stats = pd.read_csv("e:\\prime\\data\\direction_stats.csv")
    trader_sentiment = pd.read_csv("e:\\prime\\data\\trader_sentiment.csv")
    trader_profiles = pd.read_csv("e:\\prime\\data\\trader_profiles.csv")
    daily_cum_pnl = pd.read_csv("e:\\prime\\data\\daily_cumulative_pnl.csv")
    daily_fg = pd.read_csv("e:\\prime\\data\\daily_fg.csv")
    return regime_stats, dir_stats, trader_sentiment, trader_profiles, daily_cum_pnl, daily_fg

regime_stats, dir_stats, trader_sentiment, trader_profiles, daily_cum_pnl, daily_fg = load_data()

# Page Title
st.title("⚡ Hyperliquid Trader & Sentiment Analytics")
st.markdown("Exploring the relationship between trader performance on Hyperliquid and the Crypto Fear & Greed Index.")

# Sidebar
st.sidebar.header("Navigation & Settings")
st.sidebar.markdown("This dashboard analyzes trader behavior and performance against market sentiment from **May 2023 to May 2025**.")

# Quick stats in sidebar
st.sidebar.subheader("Dataset Summary")
st.sidebar.markdown(f"**Total Trades Analyzed:** {regime_stats['trade_count'].sum():,}")
st.sidebar.markdown(f"**Total Volume:** ${regime_stats['total_volume_usd'].sum():,.2f}")
st.sidebar.markdown(f"**Total Realized PnL:** ${regime_stats['total_pnl'].sum():,.2f}")
st.sidebar.markdown(f"**Total Fees Paid:** ${regime_stats['total_fee'].sum():,.2f}")
st.sidebar.markdown(f"**Unique Active Accounts:** {len(trader_profiles)}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌍 Global Analysis", "👤 Trader Profiling", "🪙 Coin Insights", "💡 Strategy & Insights"])

# TAB 1: Global Analysis
with tab1:
    st.header("Global Sentiment & Trader Performance")
    st.markdown("How does market-wide sentiment affect trading volume, win rates, and profitability?")
    
    # Grid of Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-lbl">Total Realized PnL</div>
            <div class="metric-val metric-val-positive">$10.3M</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-lbl">Total Volume Traded</div>
            <div class="metric-val">$1.19B</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-lbl">Average Win Rate</div>
            <div class="metric-val metric-val-positive">81.39%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-lbl">Total Transaction Fees</div>
            <div class="metric-val metric-val-negative">$245,849</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 1: Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Profitability & Fees by Sentiment Regime")
        # Dual axis plot with Plotly
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=regime_stats['fg_classification'],
            y=regime_stats['total_pnl'],
            name="Realized PnL ($)",
            marker_color="#10b981",
            opacity=0.8
        ))
        fig.add_trace(go.Scatter(
            x=regime_stats['fg_classification'],
            y=regime_stats['total_fee'],
            name="Fees Paid ($)",
            yaxis="y2",
            line=dict(color="#ef4444", width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Realized PnL ($)", titlefont=dict(color="#10b981"), tickfont=dict(color="#10b981")),
            yaxis2=dict(title="Fees ($)", titlefont=dict(color="#ef4444"), tickfont=dict(color="#ef4444"), overlaying="y", side="right"),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Observation**: While Fear is the most active regime by volume and generates the most absolute PnL ($3.36M), Extreme Greed yields the highest efficiency with $2.72M in PnL on just $124M in volume (a massive 11.0x profit factor).")
        
    with c2:
        st.subheader("Trade Win Rate & Profit Factor")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=regime_stats['fg_classification'],
            y=regime_stats['win_rate'] * 100,
            name="Win Rate (%)",
            marker_color="#3b82f6",
            text=[f"{x*100:.1f}%" for x in regime_stats['win_rate']],
            textposition='auto',
        ))
        fig.add_trace(go.Scatter(
            x=regime_stats['fg_classification'],
            y=regime_stats['profit_factor'],
            name="Profit Factor",
            yaxis="y2",
            line=dict(color="#f59e0b", width=3, dash='dash'),
            marker=dict(size=8)
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Win Rate (%)", titlefont=dict(color="#3b82f6"), tickfont=dict(color="#3b82f6")),
            yaxis2=dict(title="Profit Factor", titlefont=dict(color="#f59e0b"), tickfont=dict(color="#f59e0b"), overlaying="y", side="right"),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Observation**: Win rates remain consistently above 75% in all regimes, peaking during Extreme Greed (89.17%) and Fear (87.29%). The profit factor peaks at a staggering 11.02 during Extreme Greed.")

    # Row 2: Directional Analysis
    st.subheader("Longs vs. Shorts Sentiment Preference")
    long_short_vol = dir_stats[dir_stats['position_side'].isin(['Long', 'Short'])].copy()
    fig = px.bar(
        long_short_vol,
        x="fg_classification",
        y="total_volume_usd",
        color="position_side",
        barmode="group",
        color_discrete_map={"Long": "#3b82f6", "Short": "#ef4444"},
        labels={"total_volume_usd": "Volume (USD)", "fg_classification": "Sentiment Regime"},
        height=350
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# TAB 2: Trader Profiling
with tab2:
    st.header("Trader Profiling & Segmentation")
    st.markdown("Analyzing how individual traders interact with market sentiment. We have categorized the 32 accounts based on the correlation of their trading performance with the Fear & Greed Index.")
    
    # Row 1: Style Distribution
    style_counts = trader_profiles['trading_style'].value_counts().reset_index()
    style_counts.columns = ['Trading Style', 'Count']
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Distribution of Trading Styles")
        fig = px.pie(
            style_counts,
            values="Count",
            names="Trading Style",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Style Definition Table")
        st.markdown("""
        | Trading Style | Definition | Count | Avg PnL | Key Behavior |
        | --- | --- | --- | --- | --- |
        | **Contrarian** | Negative correlation with sentiment index (< -0.15) | 10 | $261,310 | Thrives in market fear; trades counter-trend. |
        | **Momentum Follower** | Positive correlation with sentiment index (> 0.15) | 12 | $215,840 | Thrives in market greed; rides the bullish momentum. |
        | **Sentiment Insensitive** | Correlation close to zero (-0.15 to 0.15) | 10 | $219,890 | Profits steadily regardless of market sentiment. |
        """)
        
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Row 2: Select a Trader to Explore
    st.subheader("Explore Individual Trader Performance")
    selected_acct = st.selectbox("Select Account", trader_profiles['Account'].tolist())
    
    trader_row = trader_profiles[trader_profiles['Account'] == selected_acct].iloc[0]
    
    tc1, tc2, tc3, tc4 = st.columns(4)
    with tc1:
        st.metric("Trading Style", trader_row['trading_style'])
    with tc2:
        pnl_val = trader_row['total_pnl']
        st.metric("Total Realized PnL", f"${pnl_val:,.2f}")
    with tc3:
        st.metric("Win Rate", f"{trader_row['win_rate']*100:.2f}%")
    with tc4:
        st.metric("Sentiment Correlation", f"{trader_row['sentiment_correlation']:.3f}")
        
    # Trader specific charts
    trader_data = trader_sentiment[trader_sentiment['Account'] == selected_acct]
    
    tx1, tx2 = st.columns(2)
    with tx1:
        st.subheader("Trader PnL by Sentiment Regime")
        fig = px.bar(
            trader_data,
            x="fg_classification",
            y="total_pnl",
            color="fg_classification",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"total_pnl": "PnL ($)", "fg_classification": "Sentiment"},
            height=300
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tx2:
        st.subheader("Trader Win Rate by Sentiment Regime")
        fig = px.bar(
            trader_data,
            x="fg_classification",
            y=trader_data['win_rate'] * 100,
            color="fg_classification",
            color_discrete_sequence=px.colors.qualitative.Safe,
            labels={"y": "Win Rate (%)", "fg_classification": "Sentiment"},
            height=300
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: Coin Insights
with tab3:
    st.header("Coin Specific Sentiment Dynamics")
    st.markdown("Which coins are traded in which sentiment regimes, and which are the most profitable?")
    
    # Heatmap description
    st.subheader("Net realized PnL ($) by Top Coins and Sentiment Regime")
    st.image("e:\\prime\\assets\\coin_performance_sentiment.png", caption="Heatmap of Coin Performance across Sentiments")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    ### Key Insights:
    1. **HYPE Token**:
       - Hyperliquid's native token **HYPE** has the highest volume of trades.
       - It shows massive profits during **Extreme Greed** and **Fear** regimes.
    2. **BTC and ETH (Blue Chips)**:
       - Traders tend to be very profitable on **BTC** during **Fear** and **Extreme Greed** phases.
       - During **Greed**, there is a slight dip in performance, possibly due to over-leveraged longs chasing tops.
    3. **Meme Coins (FARTCOIN, MELANIA, PURR)**:
       - Speculative meme tokens are traded heavily during **Greed** and **Extreme Greed** regimes.
       - Performance on memes drops significantly during **Extreme Fear**, as traders flee to safer assets (like BTC or USD stables).
    """)

# TAB 4: Strategy & Insights
with tab4:
    st.header("Data-Driven Trading Insights & Strategies")
    
    st.subheader("💡 Key Discoveries")
    st.markdown("""
    *   **The Contrarian Edge**: The most profitable trader in the dataset (**Account `0x083384f897ee0f19899168e3b1bec365f52a9012`**, making **$1.60M**) is a **Contrarian**. They make most of their profits during **Extreme Fear** and **Fear** regimes. This aligns with the classic trading adage: *"Be fearful when others are greedy, and greedy when others are fearful."*
    *   **Extreme Greed Scalping**: Under **Extreme Greed** conditions, average trade size is the smallest ($3,112), but win rates are the highest (89.17%) and the profit factor is a staggering 11.02. This indicates that successful traders scale down their size to manage risk near local market tops but take highly accurate, quick-scalp profits.
    *   **Fear Regime Volume Hub**: The **Fear** regime has the highest total volume ($483.3M) and generates the largest aggregate profits ($3.36M). This suggests that market pullbacks create high-liquidity, high-opportunity windows where professional traders step in with larger sizes (avg size $7,816).
    *   **Fees Impact**: Fees consume a very small fraction of PnL for top traders (e.g. Trader 0x0833... paid $7,405 in fees on $1.60M PnL, i.e., 0.46%), indicating that they are positional or swing traders, not high-frequency churners.
    """)
    
    st.subheader("🛠 Proposed Sentiment-Based Strategies")
    
    col_str1, col_str2 = st.columns(2)
    with col_str1:
        st.info("""
        ### Strategy A: The Contrarian "Fear-Buyer"
        *   **Condition**: Fear & Greed Index < 25 (Extreme Fear or Fear)
        *   **Action**: Accumulate spot / Open long positions on BTC and major blue chips.
        *   **Rationale**: The data shows that the highest-performing traders make their largest gains during Fear. Average trade sizes in Fear are the highest ($7,816), indicating high conviction.
        *   **Target Win Rate**: ~87.29%
        """)
        
    with col_str2:
        st.success("""
        ### Strategy B: The Greed "Scalper"
        *   **Condition**: Fear & Greed Index > 75 (Extreme Greed)
        *   **Action**: Scale down trade size by 50-60%. Focus on quick momentum scalps (short duration).
        *   **Rationale**: Under Extreme Greed, the win rate is highest (89.17%) but average trade size is the smallest ($3,112). This represents low-exposure, high-probability setups to harvest quick momentum before a correction.
        *   **Target Profit Factor**: > 10.0
        """)
        
    # Table of top 5 traders for emulation
    st.subheader("Top 5 Traders to Emulate")
    st.dataframe(
        trader_profiles.sort_values(by="total_pnl", ascending=False).head(5)[
            ["Account", "total_trades", "total_pnl", "win_rate", "sentiment_correlation", "trading_style"]
        ]
    )

st.markdown("<br><hr><center>Developed by Antigravity AI | Advanced Agentic Coding Project</center>", unsafe_allow_html=True)
