import os
import pickle

import streamlit as st
import hydralit_components as hc
import pandas as pd
from dotenv import load_dotenv

from utils import gen_sequence
from graphs import unilabel_dist_plot, bilable_dist_plot, multiabel_dist_plot
from model_obj import ModelObj

load_dotenv()
BASE_COLOR = os.getenv("BASE_COLOR", "#000060")


st.set_page_config(
    page_title="OFDE",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)
st.markdown("""<style>.main {}</style>""", unsafe_allow_html=True)

if st.session_state.get("df") is None:
    st.session_state.df = pd.read_csv("dataset/onlinefoods.csv").drop(
        columns=["Pin code", "Unnamed: 12"], axis=1
    )
if st.session_state.get("modelObj") is None:
    st.session_state.modelObj = ModelObj()


menu_data = [
    {
        "id": "do",
        "icon": "fas fa-table",
        "label": "Data Overview",
        "ttip": "Get an overview of entire data.",
    },
    {
        "id": "dv",
        "icon": "far fa-chart-bar",
        "label": "Data Visualization",
        "ttip": "Visualization data for insights.",
    },
    {
        "id": "ml",
        "icon": "fas fa-brain",
        "label": "ML Model",
        "ttip": "Predictive model for food data.",
    },
]
over_theme = {
    "txc_inactive": "#FFFFFF",
    "menu_background": BASE_COLOR,
    "txc_active": "#000060",
    "option_active": "aliceblue",
}
menu_id = hc.nav_bar(
    menu_definition=menu_data, home_name="Home", override_theme=over_theme
)


intro_info = (
    """This app is a data explorer for food data.\nCreated by GR 10, EL 3, UMaT 2024."""
)


match menu_id:
    case "Home":
        st.markdown("## Online Food Data Explorer")
        for sequence in intro_info.split("\n"):
            st.write_stream(gen_sequence(sequence))
        st.markdown(
            "Check [here](https://aaron-ontoyin-yin.virtual-world.tech) to reach out to the creator!"
        )

    case "do":
        st.markdown("## Data Overview")

        check_btns_cols = st.columns(5)
        with check_btns_cols[0]:
            st.checkbox("Entire data", value=False, key="do_entire_data")
        with check_btns_cols[1]:
            st.checkbox("Summary", value=True, key="do_summary")
        with check_btns_cols[2]:
            st.checkbox("Data types", value=False, key="do_data_types")
        with check_btns_cols[3]:
            st.checkbox("Missing values", value=False, key="do_missing_values")
        with check_btns_cols[4]:
            st.checkbox("Shape", value=False, key="do_shape")

        if st.session_state.do_entire_data:
            st.markdown("#### Entire Data")
            st.data_editor(
                st.session_state.df, hide_index=True, use_container_width=True
            )
        if st.session_state.do_summary:
            st.markdown("#### Summary of Numerical Colums")
            st.data_editor(st.session_state.df.describe(), use_container_width=True)
        if st.session_state.do_data_types:
            st.markdown("#### Data Types")
            st.data_editor(
                st.session_state.df.dtypes.to_frame().T,
                hide_index=True,
                use_container_width=True,
            )
        if st.session_state.do_missing_values:
            st.markdown("#### Missing Values")
            st.data_editor(
                st.session_state.df.isnull().sum().to_frame().T,
                use_container_width=True,
            )
        if st.session_state.do_shape:
            st.markdown("#### Shape")
            st.write(
                f"The data has {st.session_state.df.shape[0]} rows and {st.session_state.df.shape[1]} columns."
            )

    case "dv":
        st.markdown("## Data Visualization")
        single_label_tab, bi_label_tab, multi_label_tab = st.tabs(
            ["Single Label", "Bi-Label", "Multi-Label"]
        )

        with single_label_tab:
            label_col, plot_type_col = st.columns(2)
            label = label_col.selectbox(
                "Select a label to visualize",
                st.session_state.df.columns,
                key="single_label",
            )
            plot_type = plot_type_col.selectbox(
                "Select a plot type",
                [
                    "histogram",
                    "bar chart",
                    "boxplot",
                    "violin chart",
                    "kde plot",
                    "pie",
                ],
                key="plot_type_single_label",
            )

            st.plotly_chart(
                unilabel_dist_plot(st.session_state.df, label, plot_type),
                use_container_width=True,
            )

        with bi_label_tab:
            label1_col, label2_col, plot_type_col = st.columns(3)
            label1 = label1_col.selectbox(
                "Select the first label to visualize",
                st.session_state.df.columns,
                key="bi_label1",
            )
            label2 = label2_col.selectbox(
                "Select the second label to visualize",
                st.session_state.df.columns,
                key="bi_label2",
                index=1,
            )
            plot_type = plot_type_col.selectbox(
                "Select a plot type",
                [
                    "violin chart",
                    "boxplot",
                ],
                key="plot_type_bi_label",
            )

            st.plotly_chart(
                bilable_dist_plot(st.session_state.df, label1, label2, plot_type),
                use_container_width=True,
            )

        with multi_label_tab:
            label1_col, label2_col, label3_col, label4_col = st.columns(4)
            label1 = label1_col.selectbox(
                "Select the first label to visualize",
                st.session_state.df.columns,
                key="multi_label1",
            )
            label2 = label2_col.selectbox(
                "Select the second label to visualize",
                st.session_state.df.columns,
                key="multi_label2",
                index=1,
            )
            label3 = label3_col.selectbox(
                "Select the third label to visualize",
                st.session_state.df.columns,
                key="multi_label3",
                index=2,
            )
            label4 = label4_col.selectbox(
                "Select the fourth label to visualize",
                [None] + st.session_state.df.columns.to_list(),
                key="multi_label4",
            )

            st.plotly_chart(
                multiabel_dist_plot(
                    st.session_state.df, label1, label2, label3, label4
                ),
                use_container_width=True,
            )
    case "ml":
        model_col, input_col = st.columns(2)
        with model_col:
            st.markdown("## ML Model")
            st.write(
                "Predict `Feedback` as positive or negative given `Age`, `Gender`, `Marital Status`, `Occupation`, `Monthly Income`, `Educational Qualifications`, `Family size`, `latitude`, `longitude`, and `Output`."
            )

            st.markdown("### Model")
            st.markdown(st.session_state.modelObj.model)

            st.markdown("### Model Report")
            st.write(
                st.session_state.modelObj.model_report_hmtl, unsafe_allow_html=True
            )

        with input_col:
            st.markdown("### Predict Feedback")
            input_col1, input_col2, input_col3 = st.columns(3)
            with input_col1:
                age = st.number_input("Age", min_value=0, max_value=100, key="age")
                gender = st.selectbox("Gender", ["Male", "Female"])
                marital_status = st.selectbox(
                    "Marital Status", ["Married", "Single", "Prefer not to say"]
                )
                occupation = st.selectbox(
                    "Occupation",
                    ["Student", "Self Employeed", "Employee", "House wife"],
                )
            with input_col2:
                monthly_income = st.selectbox(
                    "Monthly Income",
                    [
                        "No Income",
                        "Below Rs.10000",
                        "10001 to 25000",
                        "25001 to 50000",
                        "More than 50000",
                    ],
                )
                educational_qualifications = st.selectbox(
                    "Educational Qualifications",
                    ["Graduate", "Post Graduate", "Ph.D", "School", "Uneducated"],
                )
                family_size = st.number_input("Family Size", min_value=1, max_value=6)
                latitude = st.number_input("Latitude", key="latitude")
            with input_col3:
                longitude = st.number_input("Longitude", key="longitude")
                output = st.selectbox("Output", ["Confirmed", "Delivered"])

            prediction = st.session_state.modelObj.predict(
                age=age,
                gender=gender,
                marital_status=marital_status,
                occupation=occupation,
                monthly_income=monthly_income,
                educational_qualifications=educational_qualifications,
                family_size=family_size,
                latitude=latitude,
                longitude=longitude,
                output="Yes" if output == "Delivered" else "No",
            )
            if st.button("Predict"):
                if prediction == "Positive":
                    st.write(
                        "Predicted Feedback: <span style='color:#00ff00'>Positive</span>",
                        unsafe_allow_html=True,
                    )
                    st.balloons()
                elif prediction == "Negative":
                    st.write(
                        "Predicted Feedback: <span style='color:#ff0000'>Negative</span>",
                        unsafe_allow_html=True,
                    )

# st.write()

st.markdown(
    """
    <style>
    #footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #000060;
        color: white;
        text-align: center;
        padding: 1rem;
    }
    #space {
        width: 100%;
        height: 7em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div id="space"></div>
    <div id="footer">Made with ❤️ by GR 10, EL 3, UMaT 2024</div>
    """,
    unsafe_allow_html=True,
)
