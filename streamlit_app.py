# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
from src.setup import initialize_environment
from src.utils import read_html_file, fetch_eia_report, fetch_ai_analysis, bar_chart

st.set_page_config(layout="wide")

# Initialize the environment
initialize_environment()

st.title("EIA Report AI Analyzer")

# Create two columns for the layout
with st.container():
    left_column, right_column = st.columns([1, 1], gap="small")

    with left_column:
        # Picture
        st.image("https://a.c-dn.net/b/1OXvJJ/crude-oil-facts_body_CrudeOil.jpg", caption="", width=500)
        # Tradeview
        tradeview_html = read_html_file("tradeview.html")
        components.html(tradeview_html, height=500, width=900)

    with right_column:
        st.header("EIA Report")
        st.write("Select the date for EIA Report and after clicking on 'Fetch and Analyze Report' button")
        # Use the date input widget
        report_date = st.date_input("Report Date", key='report_date')

        if st.button("Fetch and Analyze Report"):
            try:
                # Fetch the dataframe EIA Report
                eia_df = fetch_eia_report(report_date)
                st.subheader("Weekly EIA data")
                st.markdown(eia_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

                # AI analysis display
                result = fetch_ai_analysis(eia_df)

                # Rating
                st.subheader("AI Rating: ")
                st.write(f"""{result['rating']}/10""")

                # Rating bar
                rating_bar_html = bar_chart(result['rating'])
                st.markdown(rating_bar_html, unsafe_allow_html=True)

                # Analysis
                st.subheader("AI Analysis")
                st.write(result['analysis'])
            except Exception as e:
                st.error(e)