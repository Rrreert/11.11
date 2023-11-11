import streamlit as st
import plotly.express as px
from pysurvival.utils import load_model

if 'model_deep' not in st.session_state:
    st.session_state["model_deep"] = load_model('DeepSurv.zip')
    st.session_state["model_nmtlr"] = load_model('NMTLR.zip')
model_deep = st.session_state["model_deep"]
model_nmtlr = st.session_state["model_nmtlr"]


def get_select1():
    dic = {
        "Age": ["≤ 66", "> 66, ≤ 77", "> 77"],
        "Race": ["American Indian/Alaska Native", "Asian or Pacific Islander",
                 "Black", "White"],
        "Marital_status": ["Married", "Other"],
        "Histological_type": ["8170", "8171", "8172", "8173", "8174", "8175"],
        "Grade": ["Moderately differentiated; Grade II", "Poorly differentiated; Grade III",
                  "Undifferentiated; anaplastic; Grade IV", "Well differentiated; Grade I"],
        "T": ["T1", "T2", "T3a", "T3b", "T4"],
    }
    return dic


def get_select2():
    dic = {
        "N": ["N0", "N1"],
        "M": ["M0", "M1"],
        "AFP": ["Negative/normal; within normal limits", "Positive/elevated"],
        "Tumor_size": ["> 62 mm", "≤ 62 mm"],
        "Surgery": ["Lobectomy", "Local tumor destruction", "No", "Wedge or segmental resection"],
        "Chemotherapy": ["No/Unknown", "Yes"]
    }
    return dic


def plot_sur(pd_data):
    if st.session_state['display']:
        fig = px.line(pd_data, x="Time", y="Survival", color='Patients', range_y=[0, 1])
    else:
        fig = px.line(pd_data.loc[pd_data['Patients'] == pd_data['Patients'].to_list()[-1], :], x="Time", y="Survival",
                      range_y=[0, 1])
    fig.update_layout(title={
        'text': 'Estimated Survival Probability',
        'y': 1,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            size=25
        )
    },
        plot_bgcolor="LightGrey",
        xaxis_title="Time, month",
        yaxis_title="Survival probability",
    )
    st.plotly_chart(fig, use_container_width=True)


with st.sidebar:
    col1, col2 = st.columns([5, 5])
    with col1:
        for _ in get_select1():
            st.selectbox(_, get_select1()[_], index=None, key=_)
    with col2:
        for _ in get_select2():
            st.selectbox(_, get_select2()[_], index=None, key=_)

if st.sidebar.button("Predict", type="primary"):
    st.write(get_select1()["Age"].index(st.session_state["Age"]) + 1)
