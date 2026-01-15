# Real Streaming Data Analysis Guide

Your AI-Assisted Insights Agent can connect to **real global streaming services data** from Kaggle with 113 platforms and 2+ billion subscribers.

---

## ⚠️ Prerequisites: Download the Dataset

Before using `06_configs/config_kaggle.yaml`, you must download the Kaggle dataset:

### Option 1: Using Kaggle CLI (Recommended)

```bash
# Install kaggle CLI if needed
pip install kaggle

# Download and extract to 03_data/ folder
kaggle datasets download -d sureshkumarpalus/global-streaming-services-dataset
unzip global-streaming-services-dataset.zip -d 03_data/
```

### Option 2: Manual Download

1. Visit: https://www.kaggle.com/datasets/sureshkumarpalus/global-streaming-services-dataset
2. Click "Download" (requires free Kaggle account)
3. Extract the ZIP contents to the `03_data/` folder

### Verify Installation

After downloading, your `03_data/` folder should contain:
```
03_data/
├── paid_video_streaming_services.csv
├── free_video_streaming_services.csv
├── paid_video_market_summary.csv
└── paid_video_growth_predictions.csv
```

---

## 📊 Dataset Overview

### Data Source
**Kaggle: Global Streaming Services Dataset**
- Dataset: `sureshkumarpalus/global-streaming-services-dataset`
- Last Updated: 2024
- Quality: Comprehensive market data with historical trends

### What's Included

#### 4 Data Files
1. **Paid Video Streaming Services** (78 services)
2. **Free Video Streaming Services** (35 services)
3. **Market Summary** (aggregate metrics)
4. **Growth Predictions** (2025+ forecasts)

#### Key Metrics Available
- **2,071 million subscribers** (2.07 billion)
- **78 paid streaming platforms**
- **35 free streaming platforms**
- **$19.6 billion** in monthly revenue
- **Historical data**: 2020-2024 trends
- **Growth predictions**: 2025+ forecasts

---

## 🎯 What You Can Analyze

### 1. Subscriber Metrics

**Available Data:**
- Total subscribers by platform
- Subscriber growth trends (2020-2024)
- Year-over-year growth rates
- Subscriber projections for 2025+
- Market share by service

**Example Questions:**
```
✓ "What are the top 10 streaming services by subscribers?"
✓ "How many total subscribers are there globally?"
✓ "What's the year-over-year growth from 2023 to 2024?"
✓ "Which service has the fastest subscriber growth?"
✓ "Show me Netflix's subscriber trajectory from 2020 to 2024"
```

**Sample Insights:**
- Netflix leads with **301.6M subscribers**
- Amazon Prime Video: **220M subscribers**
- Disney+: **131.6M subscribers**
- Industry grew **13.24% YoY** (2023-2024)

---

### 2. Revenue & Pricing

**Available Data:**
- Monthly subscription prices
- Annual subscription prices
- Average Revenue Per User (ARPU)
- Total revenue estimates
- Price positioning by service

**Example Questions:**
```
✓ "What's the average monthly subscription price?"
✓ "Which services have the highest ARPU?"
✓ "Compare Netflix pricing vs Disney+ pricing"
✓ "What's the price range across all services?"
✓ "Show me premium vs budget tier pricing"
```

**Sample Insights:**
- Average price: **$13.21/month**
- Average ARPU: **$13.20**
- Price range: $0 (free) to $30+/month
- Total market revenue: **$19.6B/month**

---

### 3. Churn & Retention

**Available Data:**
- Churn rate by service
- Average industry churn
- Churn correlation with pricing
- Churn by engagement level

**Example Questions:**
```
✓ "What's the average churn rate across services?"
✓ "Which platforms have the lowest churn?"
✓ "How does churn correlate with pricing?"
✓ "Compare churn rates: high engagement vs low engagement services"
✓ "What's Netflix's churn rate?"
```

**Sample Insights:**
- Industry average churn: **2.51%**
- High engagement services: Lower churn
- Premium services: Competitive churn rates

---

### 4. Content & Engagement

**Available Data:**
- Content types (Movies, TV Shows, Originals, Sports, etc.)
- Engagement clusters (High, Medium, Low)
- Content distribution by platform
- Engagement by content type

**Example Questions:**
```
✓ "How many services offer original content?"
✓ "What content types have the most subscribers?"
✓ "List all sports streaming services"
✓ "Which platforms are in the high engagement cluster?"
✓ "Compare engagement: Netflix vs Hulu vs Disney+"
```

**Sample Insights:**
- **8 services** in High Engagement cluster
- **13 services** in Medium Engagement cluster
- **57 services** in Low Engagement cluster
- Movies + TV Shows + Originals = **1,110.9M subscribers**

---

### 5. Demographics & User Behavior

**Available Data:**
- Age group distribution (18-24, 25-34, 35-44, 45-54, 55-64, 65+)
- Device usage (Android, iOS, Web, Smart TV, Gaming Console)
- Platform preferences by age
- Multi-device usage patterns

**Example Questions:**
```
✓ "Which age group has the highest streaming adoption?"
✓ "What percentage of users watch on Smart TVs?"
✓ "Compare mobile usage (iOS vs Android) across services"
✓ "Which services are most popular with 18-24 year olds?"
✓ "Show me device distribution for Netflix"
```

**Available Demographics:**
- 6 age group segments
- 5 device categories
- Platform-specific breakdowns

---

### 6. Market Share & Competition

**Available Data:**
- Parent companies
- Global availability (countries)
- Launch years
- Service categories
- Market positioning

**Example Questions:**
```
✓ "What's Netflix's global market share?"
✓ "How many services does Disney own?"
✓ "Which services are available in 100+ countries?"
✓ "List all Amazon-owned streaming platforms"
✓ "Compare market share: US services vs international"
```

**Sample Insights:**
- Netflix: **14.6% global market share**
- Disney owns multiple services (Disney+, Hulu, ESPN+, etc.)
- Many services have global reach (100+ countries)

---

### 7. Growth & Predictions

**Available Data:**
- Historical growth (2020-2024)
- Predicted subscriber counts (2025+)
- Growth rate projections
- Revenue forecasts
- Market expansion predictions

**Example Questions:**
```
✓ "What's the predicted growth for 2025?"
✓ "Which services are projected to grow fastest?"
✓ "Show me Netflix's growth prediction"
✓ "What's the industry growth rate forecast?"
✓ "Compare historical growth vs predicted growth"
```

**Sample Insights:**
- 2023-2024 growth: **+13.24%**
- Predictions available for all 78 paid services
- Revenue projections included

---

### 8. Parent Companies & Ownership

**Available Data:**
- Parent company for each service
- Multi-platform portfolios
- Corporate consolidation trends

**Example Questions:**
```
✓ "How many services does Amazon own?"
✓ "List all Disney streaming platforms"
✓ "What services are owned by Warner Bros?"
✓ "Show me independent vs corporate-owned services"
✓ "Which parent company has the most platforms?"
```

**Major Players:**
- **Netflix Inc** (Netflix)
- **Amazon** (Prime Video, Freevee)
- **The Walt Disney Company** (Disney+, Hulu, ESPN+, Star+)
- **Warner Bros Discovery** (Max/HBO Max, Discovery+)
- **Paramount Global** (Paramount+, Pluto TV)
- **NBCUniversal** (Peacock)
- **Apple** (Apple TV+)
- Plus international giants: Tencent, Alibaba, Zee, etc.

---

### 9. Free vs Paid Services

**Available Data:**
- 78 paid services
- 35 free services
- Comparison metrics
- Business model analysis

**Example Questions:**
```
✓ "Compare total subscribers: free vs paid services"
✓ "What's the average ARPU for paid services?"
✓ "List top 5 free streaming platforms"
✓ "How many ad-supported services are there?"
✓ "Which free services have the most users?"
```

**Free Service Leaders:**
- MX Player: **300M users**
- Bilibili: **200M users**
- The Roku Channel: **100M users**

---

### 10. Geographic Reach

**Available Data:**
- Countries available per service
- Global vs regional platforms
- International expansion

**Example Questions:**
```
✓ "Which service is available in the most countries?"
✓ "List all truly global platforms (150+ countries)"
✓ "How many services are available in the US?"
✓ "Compare geographic reach: Netflix vs competitors"
✓ "Which services are region-specific?"
```

**Geographic Insights:**
- Some services available in **190+ countries**
- Regional players dominate specific markets
- Expansion trends visible in historical data

---

## 💡 Business Use Cases

### For Streaming Service Executives

**Strategic Questions:**
```
→ "How does our pricing compare to competitors?"
→ "What's our market share vs industry leaders?"
→ "Where do we rank in subscriber growth?"
→ "How does our churn compare to industry average?"
→ "What content types drive the most engagement?"
```

### For Investors & Analysts

**Investment Questions:**
```
→ "Which services show the strongest growth trajectory?"
→ "What's the total addressable market size?"
→ "Compare ARPU across different business models"
→ "Which parent companies are gaining market share?"
→ "What's the industry growth forecast for 2025?"
```

### For Marketing Teams

**Marketing Questions:**
```
→ "What age groups should we target?"
→ "Which devices do our competitors' users prefer?"
→ "What price point maximizes market penetration?"
→ "How do high engagement services position themselves?"
→ "What content types attract the most subscribers?"
```

### For Product Managers

**Product Questions:**
```
→ "What features correlate with high engagement?"
→ "How many platforms offer originals content?"
→ "What device platforms should we prioritize?"
→ "How does multi-device support affect subscriber growth?"
→ "What content mix do market leaders offer?"
```

---

## 🚀 How to Use This Data

### Method 1: Interactive CLI

```powershell
# Start the CLI
cd /path/to/ai-assisted-insights-agent
$env:06_configs/config_PATH = "06_configs/config_kaggle.yaml"
python -m insights_agent.cli

# Then ask questions
> ask What are the top 5 services by subscribers?
> ask What's the average churn rate?
> ask Compare Netflix vs Disney+ growth
```

### Method 2: Python Scripts

```python
import pandas as pd

# Load the data
df = pd.read_csv("03_data/paid_video_streaming_services.csv")

# Query 1: Top services
top10 = df.nlargest(10, "subscribers_millions")
print(top10[["service_name", "subscribers_millions"]])

# Query 2: Average metrics
avg_price = df["monthly_price_usd"].mean()
avg_churn = df["churn_rate_pct"].mean()
print(f"Avg Price: ${avg_price:.2f}")
print(f"Avg Churn: {avg_churn:.2f}%")

# Query 3: Growth analysis
growth = df[["service_name", "subscribers_2023_millions", "subscribers_2024_millions"]]
growth["yoy_growth"] = ((growth["subscribers_2024_millions"] - growth["subscribers_2023_millions"]) / growth["subscribers_2023_millions"] * 100)
print(growth.nlargest(10, "yoy_growth"))
```

### Method 3: Direct Data Access

All data files are in `03_data/` directory:
- `paid_video_streaming_services.csv`
- `free_video_streaming_services.csv`
- `paid_video_market_summary.csv`
- `paid_video_growth_predictions.csv`

Open with Excel, Power BI, Tableau, or any data tool.

---

## 📈 Sample Analysis Workflows

### Workflow 1: Competitive Analysis

```
1. Ask: "What are the top 10 services by subscribers?"
2. Ask: "What's Netflix's market share?"
3. Ask: "Compare pricing: Netflix vs Disney+ vs Amazon Prime"
4. Ask: "How does Netflix's churn compare to industry average?"
5. Ask: "What's Netflix's subscriber growth from 2020-2024?"
```

### Workflow 2: Market Opportunity

```
1. Ask: "What's the total market size in subscribers?"
2. Ask: "What's the year-over-year growth rate?"
3. Ask: "Which content types have the most subscribers?"
4. Ask: "What's the average price point?"
5. Ask: "How many services operate in each engagement cluster?"
```

### Workflow 3: Pricing Strategy

```
1. Ask: "What's the average monthly price?"
2. Ask: "Show me the price range across all services"
3. Ask: "What's the correlation between price and subscribers?"
4. Ask: "How does ARPU vary by engagement level?"
5. Ask: "Which services have premium pricing ($15+)?"
```

### Workflow 4: User Behavior Analysis

```
1. Ask: "Which age group has the highest adoption?"
2. Ask: "What percentage of users prefer Smart TV?"
3. Ask: "Compare device usage across top 5 services"
4. Ask: "Which services attract younger demographics (18-24)?"
5. Ask: "How does device preference correlate with engagement?"
```

---

## 🎓 Advanced Analysis Examples

### 1. Growth Cohort Analysis

```python
df = pd.read_csv("03_data/paid_video_streaming_services.csv")

# Define cohorts by launch year
df["cohort"] = pd.cut(df["launch_year"], 
                       bins=[1990, 2010, 2015, 2020, 2025],
                       labels=["Legacy", "Early Streamers", "Modern", "Recent"])

# Analyze growth by cohort
cohort_growth = df.groupby("cohort").agg({
    "subscribers_millions": "sum",
    "subscribers_2024_millions": "sum"
})
print(cohort_growth)
```

### 2. Price Elasticity Study

```python
# Correlate pricing with subscriber count
price_analysis = df[["monthly_price_usd", "subscribers_millions", "churn_rate_pct"]]
correlation = price_analysis.corr()
print("Price vs Subscribers correlation:", correlation.loc["monthly_price_usd", "subscribers_millions"])
```

### 3. Engagement Segmentation

```python
# Analyze characteristics of high engagement services
high_engagement = df[df["engagement_cluster"] == "High Engagement"]
print("High Engagement Services:")
print(f"  Average Subscribers: {high_engagement['subscribers_millions'].mean():.1f}M")
print(f"  Average Price: ${high_engagement['monthly_price_usd'].mean():.2f}")
print(f"  Average Churn: {high_engagement['churn_rate_pct'].mean():.2f}%")
print(f"  Average ARPU: ${high_engagement['arpu_usd'].mean():.2f}")
```

### 4. Market Share Trends

```python
# Calculate market share for top players
df["market_share"] = (df["subscribers_millions"] / df["subscribers_millions"].sum()) * 100
top_players = df.nlargest(10, "market_share")[["service_name", "market_share"]]
print(top_players)
```

---

## 📊 Key Insights Summary

### Market Size
- **2.07 billion subscribers** globally (paid services)
- **113 streaming platforms** (78 paid + 35 free)
- **$19.6 billion** monthly revenue
- **13.24% YoY growth** (2023-2024)

### Market Leaders
1. **Netflix** - 301.6M subscribers (14.6% market share)
2. **Amazon Prime Video** - 220M subscribers (10.6%)
3. **Disney+** - 131.6M subscribers (6.4%)
4. **Max (HBO Max)** - 128M subscribers (6.2%)
5. **iQiyi** - 125M subscribers (6.0%)

### Pricing Insights
- Average: **$13.21/month**
- Range: $0 (free) to $30+/month
- Average ARPU: **$13.20**
- Premium tier: $15-20/month

### Performance Metrics
- Industry churn: **2.51%** average
- High engagement: **8 services** (10%)
- Medium engagement: **13 services** (17%)
- Low engagement: **57 services** (73%)

### Growth Trends
- **2020**: ~1,200M subscribers
- **2021**: ~1,400M subscribers
- **2022**: ~1,600M subscribers
- **2023**: ~1,829M subscribers
- **2024**: ~2,071M subscribers
- **Forecast 2025+**: Continued growth

---

## 🎯 Next Steps

### 1. Explore the Data Yourself
```powershell
python query_real_data.py
```

### 2. Use the Interactive CLI
```powershell
$env:06_configs/config_PATH = "06_configs/config_kaggle.yaml"
python -m insights_agent.cli
```

### 3. Build Custom Reports
Use the CSV files to create dashboards in:
- Excel
- Power BI
- Tableau
- Google Data Studio
- Jupyter Notebooks

### 4. Integrate with Your Workflow
- Export queries to SQL
- Build automated reports
- Create monitoring alerts
- Generate executive summaries

---

## 📚 Data Dictionary

### Paid Services Dataset Columns

| Column | Type | Description |
|--------|------|-------------|
| service_name | string | Name of streaming service |
| type | string | Service category |
| category | string | Content category |
| countries_available | int | Number of countries service operates in |
| monthly_price_usd | float | Monthly subscription price in USD |
| annual_price_usd | float | Annual subscription price in USD |
| launch_year | int | Year service was launched |
| subscribers_millions | float | Current subscribers (millions) |
| content_type | string | Types of content offered |
| platforms | string | Available platforms (Web, iOS, Android, etc.) |
| is_free | bool | Whether service is free |
| parent_company | string | Parent/owner company |
| age_group_18_24_pct | float | % of users aged 18-24 |
| age_group_25_34_pct | float | % of users aged 25-34 |
| age_group_35_44_pct | float | % of users aged 35-44 |
| age_group_45_54_pct | float | % of users aged 45-54 |
| age_group_55_64_pct | float | % of users aged 55-64 |
| age_group_65_plus_pct | float | % of users aged 65+ |
| device_android_pct | float | % of usage on Android |
| device_ios_pct | float | % of usage on iOS |
| device_web_pct | float | % of usage on Web |
| device_smart_tv_pct | float | % of usage on Smart TV |
| device_gaming_console_pct | float | % of usage on gaming consoles |
| device_other_pct | float | % of usage on other devices |
| engagement_cluster | string | Engagement level (High/Medium/Low) |
| arpu_usd | float | Average Revenue Per User (USD) |
| churn_rate_pct | float | Monthly churn rate (%) |
| subscribers_2020_millions | float | Subscribers in 2020 |
| subscribers_2021_millions | float | Subscribers in 2021 |
| subscribers_2022_millions | float | Subscribers in 2022 |
| subscribers_2023_millions | float | Subscribers in 2023 |
| subscribers_2024_millions | float | Subscribers in 2024 |

### Growth Predictions Dataset Columns

| Column | Type | Description |
|--------|------|-------------|
| current_subscribers | float | Current subscriber count |
| predicted_subscribers | float | Predicted future subscribers |
| growth_rate | float | Projected growth rate |
| projected_growth | float | Projected growth amount |
| predicted_arpu | float | Predicted ARPU |
| predicted_monthly_revenue | float | Predicted monthly revenue |
| service_name | string | Service name |
| type | string | Service type |
| engagement_cluster | string | Engagement level |

---

## ✅ Production Ready

Your agent is now connected to real, comprehensive streaming market data and ready for:

✅ **Market Research** - Analyze industry trends and competitive dynamics  
✅ **Business Intelligence** - Generate reports and dashboards  
✅ **Strategic Planning** - Inform pricing and product decisions  
✅ **Investment Analysis** - Evaluate market opportunities  
✅ **Academic Research** - Study digital media consumption patterns  

---

**🎉 You now have a production-ready AI insights agent with real-world streaming data!**

*Data Source: Kaggle Global Streaming Services Dataset*  
*Last Updated: January 3, 2026*
