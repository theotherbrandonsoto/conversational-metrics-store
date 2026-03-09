import streamlit as st
import duckdb
import pandas as pd

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Metrics Store Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Connect to DuckDB ─────────────────────────────────────────
@st.cache_resource
def get_connection():
    return duckdb.connect(
        "/Users/brandon_soto/VS Code/metrics-store/data/metrics_store.duckdb"
    )

conn = get_connection()

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_metrics():
    return conn.execute("SELECT * FROM core_metrics").df()

@st.cache_data
def load_customers():
    return conn.execute("SELECT * FROM dim_customers").df()

@st.cache_data
def load_subscriptions():
    return conn.execute("SELECT * FROM fct_subscriptions").df()

metrics_df      = load_metrics()
customers_df    = load_customers()
subscriptions_df = load_subscriptions()

# ── Header ────────────────────────────────────────────────────
st.title("📊 Metrics Store Dashboard")
st.caption("Powered by dbt + DuckDB · Single source of truth for all business metrics")
st.divider()

# ── Top KPIs ─────────────────────────────────────────────────
total_mrr        = metrics_df["mrr"].sum()
total_active     = metrics_df["active_customers"].sum()
total_churned    = metrics_df["churned_customers"].sum()
total_customers  = total_active + total_churned
overall_churn    = round(100 * total_churned / total_customers, 2)
total_at_risk    = metrics_df["at_risk_customers"].sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total MRR",          f"${total_mrr:,.0f}")
k2.metric("Active Customers",   f"{total_active:,}")
k3.metric("Overall Churn Rate", f"{overall_churn}%")
k4.metric("At-Risk Customers",  f"{total_at_risk:,.0f}")

st.divider()

# ── MRR by Plan ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 MRR by Plan")
    st.bar_chart(
        metrics_df.set_index("plan_type")["mrr"],
        color="#4f8bf9"
    )

with col2:
    st.subheader("📉 Churn Rate by Plan (%)")
    st.bar_chart(
        metrics_df.set_index("plan_type")["churn_rate_pct"],
        color="#f94f4f"
    )

st.divider()

# ── Engagement & Health ───────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("⚡ Avg Weekly Usage Hours by Plan")
    st.bar_chart(
        metrics_df.set_index("plan_type")["avg_weekly_usage_hours"],
        color="#4ff9a0"
    )

with col4:
    st.subheader("⚠️ At-Risk Customers by Plan")
    st.bar_chart(
        metrics_df.set_index("plan_type")["at_risk_customers"],
        color="#f9a84f"
    )

st.divider()

# ── Full Metrics Table ────────────────────────────────────────
st.subheader("📋 Full Metrics Store Output")
st.dataframe(
    metrics_df.style.format({
        "mrr":                    "${:,.0f}",
        "avg_revenue_per_user":   "${:,.2f}",
        "churn_rate_pct":         "{:.2f}%",
        "avg_weekly_usage_hours": "{:.2f}",
        "avg_tenure_months":      "{:.2f}",
        "avg_support_tickets":    "{:.2f}",
    }),
    use_container_width=True
)

st.divider()

# ── Customer Segments ─────────────────────────────────────────
st.subheader("👥 Customer Segments")
col5, col6 = st.columns(2)

with col5:
    tenure_counts = customers_df["tenure_segment"].value_counts().reset_index()
    tenure_counts.columns = ["segment", "count"]
    st.write("**By Tenure**")
    st.dataframe(tenure_counts, use_container_width=True, hide_index=True)

with col6:
    activity_counts = customers_df["activity_status"].value_counts().reset_index()
    activity_counts.columns = ["status", "count"]
    st.write("**By Activity Status**")
    st.dataframe(activity_counts, use_container_width=True, hide_index=True)

st.divider()

# ── Footer ────────────────────────────────────────────────────
st.caption("Architecture: CSV → dbt (staging → marts → metrics) → DuckDB → Streamlit")