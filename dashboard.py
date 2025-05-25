import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="Big Basket Dashboard", layout="wide")

# --- Load Dataset ---
df = pd.read_csv(os.path.join("data", "cleaned_bigbasket.csv"))  
df_original = pd.read_csv(os.path.join("data", "BigBasket_Products.csv"))  

# --- Data Preprocessing ---
df["discount_percent"] = ((df["market_price"] - df["sale_price"]) / df["market_price"]) * 100
df["rating"] = df["rating"].fillna(0)
df["brand"] = df["brand"].fillna("Unknown")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Products")
category_filter = st.sidebar.multiselect("Select Category", sorted(df["category"].unique()))
brand_filter = st.sidebar.multiselect("Select Brand", sorted(df["brand"].unique()))

filtered_df = df.copy()
if category_filter:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]
if brand_filter:
    filtered_df = filtered_df[filtered_df["brand"].isin(brand_filter)]

# --- Main Title ---
st.title("🛒 Indian Grocery (Big Basket) - Product Dashboard")

# --- Download Dataset Section ---
st.subheader("📥 Download the Datasets")
st.markdown("""
    You can download both the original dataset and the preprocessed dataset used in this dashboard.
    The original dataset includes all the raw product details, while the preprocessed dataset has additional calculations and cleaned data.
""")

# Download Original Dataset
st.download_button(
    label="Download Original Dataset (CSV)",
    data=df_original.to_csv(index=False),
    file_name="bigbasket_original.csv",
    mime="text/csv"
)

# Download Preprocessed Dataset
st.download_button(
    label="Download Preprocessed Dataset (CSV)",
    data=df.to_csv(index=False),
    file_name="bigbasket_preprocessed.csv",
    mime="text/csv"
)

# --- Tabs ---
tabs = st.tabs(["📊 Overview", "📦 Products", "📈 Analytics", "📋 Suggestions"])

# ============================
# 📊 Overview Tab
# ============================
with tabs[0]:
    st.subheader("📌 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("🛍️ Total Products", len(filtered_df))
    col2.metric("💰 Avg. Sale Price", f"₹{filtered_df['sale_price'].mean():.2f}")
    col3.metric("📉 Avg. Discount %", f"{filtered_df['discount_percent'].mean():.1f}%")

    st.markdown("---")
    st.subheader("📦 Top 10 Categories by Product Count")
    fig_cat = px.bar(filtered_df['category'].value_counts().nlargest(10),
                     labels={'value': 'Product Count', 'index': 'Category'},
                     title="Top Categories")
    st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("🏷️ Top 10 Brands by Product Count")
    fig_brand = px.bar(filtered_df['brand'].value_counts().nlargest(10),
                       labels={'value': 'Product Count', 'index': 'Brand'},
                       title="Top Brands")
    st.plotly_chart(fig_brand, use_container_width=True)

# ============================
# 📦 Products Tab
# ============================
with tabs[1]:
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("💲 Sale Price Distribution")
        fig_price = px.histogram(filtered_df, x="sale_price", nbins=50,
                                 title="Sale Price Distribution")
        st.plotly_chart(fig_price, use_container_width=True)

    with col5:
        st.subheader("⭐ Ratings Distribution")
        fig_rating = px.histogram(filtered_df, x="rating", nbins=20,
                                  title="Product Rating Distribution")
        st.plotly_chart(fig_rating, use_container_width=True)

# ============================
# 📈 Analytics Tab
# ============================
with tabs[2]:
    st.subheader("🎯 Discount % vs. Sale Price")
    fig_disc = px.scatter(filtered_df, x="discount_percent", y="sale_price",
                          color="category", opacity=0.6,
                          title="Discount vs. Sale Price by Category")
    st.plotly_chart(fig_disc, use_container_width=True)

# ============================
# 📋 Suggestions Tab
# ============================
with tabs[3]:
    st.subheader("📋 Business Suggestions & Insights")
    try:
        with open("reports/suggestion.txt", "r", encoding="utf-8") as f:
            suggestions = f.read()

        # Modern UI Styling for Suggestions
        styled_html = f"""
        <div style="
            background-color: #2c3e50;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #34495e;
            font-family: 'Arial', sans-serif;
            color: #ecf0f1;
            font-size: 16px;
            white-space: pre-wrap;
            line-height: 1.8;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        ">
        {suggestions}
        </div>
        """

        st.markdown(styled_html, unsafe_allow_html=True)
        st.download_button("📥 Download Suggestions", suggestions, file_name="suggestions.txt", use_container_width=True)

    except FileNotFoundError:
        st.warning("⚠️ Suggestions report not found. Please generate it first.")
