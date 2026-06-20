
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Product Feature Usage Dashboard",
    page_icon="📊",
    layout="wide"
)
# Your dashboard content
#st.title("Product Feature Usage Dashboard")

# =====================================================
# LOAD EXCEL FILE
# =====================================================

@st.cache_data

def load_data():
    df = pd.read_excel(
        r"C:\Users\LENOVO\Desktop\major project\survey dataset.xlsx"
    )

    return df


df = load_data()

# =====================================================
# DATA CLEANING
# =====================================================

# Convert Yes/No into numeric

df["Uses_docs_numeric"] = df["Uses_docs"].map({
    "Yes": 1,
    "No": 0
})

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

selected_device = st.sidebar.multiselect(
    "Select Device",
    options=df["Device"].unique(),
    default=df["Device"].unique()
)

selected_frequency = st.sidebar.multiselect(
    "Usage Frequency",
    options=df["Frequency"].unique(),
    default=df["Frequency"].unique()
)

selected_year = st.sidebar.multiselect(
    "Academic Year",
    options=df["Year"].unique(),
    default=df["Year"].unique()
)

# Apply Filters

df = df[
    (df["Device"].isin(selected_device)) &
    (df["Frequency"].isin(selected_frequency)) &
    (df["Year"].isin(selected_year))
]

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.main-title {
    font-size: 46px;
    font-weight: 700;
    color: #061B4E;
}

.sub-title {
    font-size: 22px;
    color: gray;
    margin-top: -15px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

left, right = st.columns([5, 4])

with left:

    st.markdown("""
    <div class='main-title'>
        Product Feature Usage & Adoption Analysis
    </div>

    <div class='sub-title'>
        Case Study: Google Drive & Google Docs
    </div>
    """, unsafe_allow_html=True)

with right:

    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Cohort Analysis",
            "Funnel Analysis",
            "Survey Results",
            "Users"
        ],
        icons=[
            "speedometer2",
            "people",
            "filter",
            "clipboard-data",
            "person"
        ],
        default_index=0,
        orientation="horizontal"
    )

st.divider()

# =====================================================
# DASHBOARD
# =====================================================

if selected == "Dashboard":

    st.title("Executive Dashboard")

    total_users = df["User_Id"].nunique()

    overall_adoption = round(
        df["Uses_docs_numeric"].mean() * 100,
        1
    )

    avg_adoption_days = round(
        df["Adoption_days"].mean(),
        1
    )

    daily_users = len(
        df[df["Frequency"] == "Daily"]
    )

    awareness_rate = round(
        (len(df[df["Awareness"] == "Yes"]) / len(df)) * 100,
        1
    )

    proficient_users = len(
        df[df["Proficiency"] == "Advanced"]
    )

    # KPI CARDS

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Users", total_users)
    c2.metric("Overall Adoption", f"{overall_adoption}%")
    c3.metric("Avg Adoption Days", avg_adoption_days)

    c4, c5, c6 = st.columns(3)

    c4.metric("Daily Active Users", daily_users)
    c5.metric("Awareness Rate", f"{awareness_rate}%")
    c6.metric("Advanced Users", proficient_users)

    st.write("")

    # FEATURE ADOPTION DATA

    feature_df = (
        df.groupby("Feature")["User_Id"]
        .count()
        .reset_index()
    )

    feature_df.columns = [
        "Feature",
        "Users"
    ]

    # FREQUENCY DATA

    frequency_df = (
        df["Frequency"]
        .value_counts()
        .reset_index()
    )

    frequency_df.columns = [
        "Frequency",
        "Users"
    ]

    # PROFICIENCY DATA

    proficiency_df = (
        df["Proficiency"]
        .value_counts()
        .reset_index()
    )

    proficiency_df.columns = [
        "Proficiency",
        "Users"
    ]

    left_chart, right_chart = st.columns([2, 1])

    # FEATURE ADOPTION CHART

    with left_chart:

        st.subheader("Feature Adoption Rate")

        fig1 = px.bar(
            feature_df,
            x="Users",
            y="Feature",
            orientation="h",
            text="Users",
            color="Users"
        )

        fig1.update_layout(
            height=500,
            template="plotly_white"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # FREQUENCY CHART

    with right_chart:

        st.subheader("Usage Frequency")

        fig2 = px.pie(
            frequency_df,
            names="Frequency",
            values="Users",
            hole=0.5
        )

        fig2.update_layout(
            height=500,
            template="plotly_white"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.write("")

    # PROFICIENCY CHART

    st.subheader("User Proficiency Distribution")

    fig3 = px.bar(
        proficiency_df,
        x="Proficiency",
        y="Users",
        text="Users",
        color="Users"
    )

    fig3.update_layout(
        height=450,
        template="plotly_white"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =====================================================
# COHORT ANALYSIS
# =====================================================

elif selected == "Cohort Analysis":

    st.title("Cohort Retention Analysis")

    cohort_df = pd.crosstab(
        df["Year"],
        df["Frequency"]
    )

    st.subheader("Cohort Retention Table")

    st.dataframe(
        cohort_df,
        use_container_width=True
    )

    st.subheader("Cohort Heatmap")

    fig = px.imshow(
        cohort_df,
        text_auto=True,
        color_continuous_scale="Blues",
        aspect="auto"
    )

    fig.update_layout(
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# FUNNEL ANALYSIS
# =====================================================

elif selected == "Funnel Analysis":

    st.title("Funnel Analysis")

    awareness = len(df[df["Awareness"] == "Yes"])

    uses_docs = len(df[df["Uses_docs"] == "Yes"])

    advanced_users = len(
        df[df["Proficiency"] == "Advanced"]
    )

    daily_users = len(
        df[df["Frequency"] == "Daily"]
    )

    funnel_df = pd.DataFrame({

        "Stage": [
            "Awareness",
            "Uses Docs",
            "Advanced Users",
            "Daily Users"
        ],

        "Users": [
            awareness,
            uses_docs,
            advanced_users,
            daily_users
        ]
    })

    fig = px.funnel(
        funnel_df,
        x="Users",
        y="Stage"
    )

    fig.update_layout(
        height=600,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# SURVEY RESULTS
# =====================================================

elif selected == "Survey Results":

    st.title("Survey Results")

    awareness_df = (
        df["Awareness"]
        .value_counts()
        .reset_index()
    )

    awareness_df.columns = [
        "Awareness",
        "Users"
    ]

    feature_df = (
        df["Feature"]
        .value_counts()
        .reset_index()
    )

    feature_df.columns = [
        "Feature",
        "Users"
    ]

    left_chart, right_chart = st.columns(2)

    with left_chart:

        st.subheader("Awareness Distribution")

        fig1 = px.pie(
            awareness_df,
            names="Awareness",
            values="Users",
            hole=0.5
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with right_chart:

        st.subheader("Popular Features")

        fig2 = px.bar(
            feature_df,
            x="Feature",
            y="Users",
            text="Users",
            color="Users"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# =====================================================
# USERS ANALYTICS
# =====================================================

elif selected == "Users":

    st.title("Users Analytics")

    st.subheader("User Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Device Distribution")

    device_df = (
        df["Device"]
        .value_counts()
        .reset_index()
    )

    device_df.columns = [
        "Device",
        "Users"
    ]

    fig = px.pie(
        device_df,
        names="Device",
        values="Users",
        hole=0.5
    )

    fig.update_layout(
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
