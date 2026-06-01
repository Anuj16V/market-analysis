# market-analysis

# Hyperliquid Trader Performance & Market Sentiment Analysis Report
**Analysis Window:** May 2023 – May 2025  
**Data Sources:** Hyperliquid Trader Logs (211,224 rows) & Crypto Fear & Greed Index (2,644 daily entries)

---

## 1. Executive Summary
This analysis explores the relationship between trader performance on the Hyperliquid exchange and Bitcoin market sentiment (Fear & Greed Index). By combining trade execution logs with daily market sentiment scores, we uncovered key patterns in trader profitability, win rates, sizing, and style dynamics. 

### Key Findings:
1. **The Contrarian Premium:** The top trader in the dataset (**Account `0x0833...`**, generating **$1.60M** in realized PnL) is a **Contrarian**. They make their largest profits when the market is in *Extreme Fear* or *Fear*.
2. **Extreme Greed Scalping Efficiency:** While trade sizes shrink to their lowest average ($3,112) during *Extreme Greed*, win rates peak at **89.17%** and the Profit Factor reaches an extraordinary **11.02**. Successful traders scale down exposure but achieve near-perfect execution.
3. **Fear Regime Liquidity Hub:** The *Fear* regime accounts for the largest aggregate trading volume (**$483.3M**) and absolute profits (**$3.36M**). This represents the main accumulation window for professional traders, who deploy their largest average size ($7,816 per trade).

---

## 2. Sentiment Regime Performance Comparison
Realized trade metrics across different sentiment stages show a clear contrast in behavior and performance:

| Sentiment Regime | Trade Count | Total Volume (USD) | Avg Trade Size (USD) | Gross Profit (USD) | Gross Loss (USD) | Net Realized PnL (USD) | Win Rate | Profit Factor | Avg PnL / Trade | Taker/Crossed % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Extreme Fear** | 21,400 | $114.5M | $5,349 | $1.38M | -$636.3K | **$739.1K** | 76.22% | 2.16 | $34.54 | 56.70% |
| **Fear** | 61,837 | $483.3M | $7,816 | $3.95M | -$593.6K | **$3.36M** | 87.29% | 6.66 | $54.29 | 60.10% |
| **Neutral** | 37,686 | $180.2M | $4,782 | $1.68M | -$389.3K | **$1.29M** | 82.39% | 4.32 | $34.31 | 61.90% |
| **Greed** | 50,303 | $288.6M | $5,736 | $3.21M | -$1.06M | **$2.15M** | 76.89% | 3.03 | $42.74 | 61.40% |
| **Extreme Greed** | 39,992 | $124.5M | $3,112 | $2.99M | -$270.9K | **$2.72M** | 89.17% | 11.02 | $67.89 | 62.20% |

### Key Metrics Analysis:
*   **Conviction Sizing in Fear:** Traders enter positions with the largest size in **Fear** (average trade size of **$7,816**). This shows high conviction when markets pull back.
*   **Deleveraging in Extreme Greed:** In **Extreme Greed**, average trade size drops to **$3,112** (a 60% reduction from Fear). Traders scale down capital exposure as market tops form, yet they capture highly accurate profits (win rate **89.17%**).
*   **Taker Aggressiveness:** The maker/taker ratio (Crossed = True/False) shows that aggressiveness increases slightly as sentiment improves, rising from **56.7%** taker trades in Extreme Fear to **62.2%** in Extreme Greed.

---

## 3. Trader Segmentation & Profiling
We analyzed the 32 unique trading accounts and grouped them into three styles based on their correlation with daily market sentiment scores:

1.  **Contrarians (10 accounts, correlation < -0.15):** Profit primarily when market sentiment is low (buying fear).
2.  **Momentum Followers (12 accounts, correlation > 0.15):** Profit when market sentiment is high (chasing greed).
3.  **Sentiment Insensitive (10 accounts, correlation -0.15 to 0.15):** Steady returns regardless of market cycles (possibly automated grid bots or market makers).

### Top 5 Performers Summary:
*   **Trader `0x0833...` (Contrarian):** **$1.60M PnL**, 3,818 trades, 79.27% win rate. Correlation: **-0.374**. This trader represents the classic contrarian whale who accumulates in panic.
*   **Trader `0xbaaa...` (Sentiment Insensitive):** **$940K PnL**, 21,192 trades, 99.12% win rate. Correlation: **-0.061**. A highly active bot execution pattern.
*   **Trader `0x513b...` (Sentiment Insensitive):** **$840K PnL**, 12,236 trades, 89.55% win rate. Correlation: **0.101**. Steady profit maker.
*   **Trader `0xbee1...` (Momentum Follower):** **$836K PnL**, 40,184 trades, 76.31% win rate. Correlation: **0.291**. Highly active trend-following trader who performs best during Greed.
*   **Trader `0x4acb...` (Contrarian):** **$677K PnL**, 4,356 trades, 94.85% win rate. Correlation: **-0.154**. Excellent execution stats.

---

## 4. Coin-Specific Dynamics
*   **HYPE (Hyperliquid Native Token):** The most active token by trade volume. Yields substantial returns during both *Extreme Greed* and *Fear* phases.
*   **BTC & ETH (Blue Chips):** Generate stable, high-win-rate PnL during *Fear* (underlying accumulation) and *Extreme Greed* (top distribution).
*   **Meme Coins (FARTCOIN, MELANIA, PURR):** Activity and profitability are highly concentrated in *Greed* and *Extreme Greed*. In *Extreme Fear*, trading activity drops to near zero as capital flees risk-on assets.

---

## 5. Strategic Insights & Playbooks

### Strategy Playbook A: The Contrarian "Fear-Accumulator"
*   **Condition:** Fear & Greed Index < 25 (Fear / Extreme Fear).
*   **Action:** Open spot/long perpetual positions on BTC, ETH, and major layer-1 tokens.
*   **Rationale:** The data shows that the top-performing trader (`0x0833...`) generates the largest PnL in these zones, matching the highest average trade size ($7,816) used by professional traders.
*   **Historical Win Rate:** **87.29%** in Fear.

### Strategy Playbook B: The "Greed Scalper"
*   **Condition:** Fear & Greed Index > 75 (Extreme Greed).
*   **Action:** Reduce position sizes by 60%, trade shorter durations, and lock in quick profits.
*   **Rationale:** Win rates are highest here (89.17%), but average trade size is small ($3,112). This represents low-exposure, high-probability setups to capture final trend extensions before a market correction.
*   **Historical Profit Factor:** **11.02**.

---

## 6. Accessing the Interactive App & Code

### Launching the Dashboard:
To interactively explore this data, select individual traders, filter by sentiment, and view visualizations, run the Streamlit app:
```powershell
streamlit run app.py
```
This will open a gorgeous dashboard on your local machine at http://localhost:8501/.

### Notebook Codebase:
The data science pipeline is fully documented and structured in the Jupyter notebook:
- `analysis.ipynb` (contains all cleaning, merging, modeling, profiling, and matplotlib visualizations).
