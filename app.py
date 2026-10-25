import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Enterprise Analytics // Command Center",
    page_icon=None,
    layout="wide",
)

# Professional Institutional Dark Mode CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 18px 22px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    
    h1, h2, h3 {
        color: #f0f6fc;
        font-weight: 500;
        letter-spacing: -0.01em;
    }
    
    .stButton>button, div.stDownloadButton>button {
        background-color: #238636;
        color: #ffffff;
        font-weight: 500;
        border-radius: 6px;
        border: 1px solid rgba(240,246,252,0.1);
        padding: 0.5rem 1rem;
        transition: background-color 0.15s ease;
    }
    .stButton>button:hover, div.stDownloadButton>button:hover {
        background-color: #2ea043;
    }
    
    [data-testid="stDataFrame"] {
        border: 1px solid #30363d;
        border-radius: 6px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    "<p style='color: #8b949e; font-size: 11px; font-weight: 600;"
    " text-transform: uppercase; letter-spacing: 0.1em; margin-bottom:"
    " 2px;'>Operations Division // Advanced Sales Intelligence Suite</p>",
    unsafe_allow_html=True,
)
st.title("Executive Command Center")
st.markdown(
    "<p style='color: #8b949e; font-size: 14px;'>Multi-dimensional"
    " operational telemetry, margin analytics, and discount sensitivity"
    " modeling.</p>",
    unsafe_allow_html=True,
)
st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)


# 2. Advanced Data Ingestion Layer
@st.cache_data
def load_data():
  data = {
      "Transaction_ID": range(1001, 1201),
      "Date": pd.date_range(start="2026-01-01", periods=200, freq="D"),
      "Region": ["North", "South", "East", "West"] * 50,
      "Category": [
          "Electronics",
          "Apparel",
          "Home Goods",
          "Groceries",
          "Logistics",
      ]
      * 40,
      "Units_Sold": [(x % 15) + 1 for x in range(200)],
      "Unit_Price": [((x % 8) + 12) * 25 for x in range(200)],
      "Discount": [0.0, 0.05, 0.1, 0.15, 0.2] * 40,
      "Cost_Price": [((x % 8) + 8) * 15 for x in range(200)],
  }
  df = pd.DataFrame(data)
  df["Total_Sales"] = df["Units_Sold"] * df["Unit_Price"] * (1 - df["Discount"])
  df["Total_Cost"] = df["Units_Sold"] * df["Cost_Price"]
  df["Gross_Profit"] = df["Total_Sales"] - df["Total_Cost"]
  df["Profit_Margin_%"] = (df["Gross_Profit"] / df["Total_Sales"]) * 100
  return df


df = load_data()

# 3. Sidebar Filtering & Parameter Controls
st.sidebar.markdown(
    "<p style='color: #f0f6fc; font-weight: 600; font-size: 12px;"
    " text-transform: uppercase; letter-spacing: 0.05em;'>Global Parameters</p>",
    unsafe_allow_html=True,
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
date_range = st.sidebar.date_input(
    "Temporal Range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

selected_region = st.sidebar.selectbox(
    "Region Filter", options=["All"] + list(df["Region"].unique())
)
selected_category = st.sidebar.selectbox(
    "Category Filter", options=["All"] + list(df["Category"].unique())
)

# Apply Filters
filtered_df = df.copy()
if len(date_range) == 2:
  start_d, end_d = date_range
  filtered_df = filtered_df[
      (filtered_df["Date"].dt.date >= start_d)
      & (filtered_df["Date"].dt.date <= end_d)
  ]

if selected_region != "All":
  filtered_df = filtered_df[filtered_df["Region"] == selected_region]
if selected_category != "All":
  filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# 4. Global KPI Metrics Bar
total_revenue = filtered_df["Total_Sales"].sum()
total_profit = filtered_df["Gross_Profit"].sum()
avg_margin = (
    filtered_df["Profit_Margin_%"].mean() if not filtered_df.empty else 0
)
total_units = filtered_df["Units_Sold"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gross Revenue", f"₹ {total_revenue:,.2f}")
col2.metric("Gross Profit", f"₹ {total_profit:,.2f}")
col3.metric("Avg Profit Margin", f"{avg_margin:.1f}%")
col4.metric("Total Volume Sold", f"{total_units:,}")

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# 5. Multi-Tab Professional Layout
tab1, tab2, tab3 = st.tabs(
    ["Executive Overview", "Product & Discount Intelligence", "Granular Ledger"]
)

with tab1:
  st.subheader("High-Level Operational Trends")
  c1, c2 = st.columns(2)

  with c1:
    if not filtered_df.empty:
      cat_sales = (
          filtered_df.groupby("Category")[["Total_Sales", "Gross_Profit"]]
          .sum()
          .reset_index()
      )
      fig_bar = px.bar(
          cat_sales,
          x="Category",
          y=["Total_Sales", "Gross_Profit"],
          title="Revenue vs Profitability by Category",
          template="plotly_dark",
          barmode="group",
          color_discrete_sequence=["#58a6ff", "#3fb950"],
      )
      fig_bar.update_layout(
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          height=380,
          margin=dict(t=40, b=20, l=20, r=20),
          font=dict(size=12, color="#8b949e"),
      )
      st.plotly_chart(fig_bar, use_container_width=True)

  with c2:
    if not filtered_df.empty:
      time_sales = (
          filtered_df.groupby("Date")[["Total_Sales", "Gross_Profit"]]
          .sum()
          .reset_index()
      )
      fig_line = px.line(
          time_sales,
          x="Date",
          y=["Total_Sales", "Gross_Profit"],
          title="Temporal Velocity: Revenue & Profit",
          template="plotly_dark",
          color_discrete_sequence=["#58a6ff", "#d29922"],
      )
      fig_line.update_layout(
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          height=380,
          margin=dict(t=40, b=20, l=20, r=20),
          font=dict(size=12, color="#8b949e"),
      )
      st.plotly_chart(fig_line, use_container_width=True)

  # Regional Distribution sub-section
  st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
  if not filtered_df.empty:
    reg_sales = (
        filtered_df.groupby("Region")["Total_Sales"].sum().reset_index()
    )
    fig_pie = px.pie(
        reg_sales,
        names="Region",
        values="Total_Sales",
        title="Revenue Distribution by Region",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4,
    )
    fig_pie.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(size=12, color="#8b949e"),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
  st.subheader("Pricing & Discount Sensitivity Analysis")
  if not filtered_df.empty:
    fig_scatter = px.scatter(
        filtered_df,
        x="Discount",
        y="Total_Sales",
        color="Category",
        size="Units_Sold",
        title="Impact of Discounting on Revenue Output",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=450,
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(size=12, color="#8b949e"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
  else:
    st.warning("No data available for current parameter filters.")

with tab3:
  st.subheader("Transactional Data Ledger")
  st.dataframe(filtered_df, use_container_width=True)

  col_exp1, _ = st.columns([2, 8])
  with col_exp1:
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Filtered Ledger (CSV)",
        data=csv_data,
        file_name="executive_sales_ledger.csv",
        mime="text/csv",
    )