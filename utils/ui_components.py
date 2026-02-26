import streamlit as st

def status_box(title, value, emoji="✅"):

    st.markdown(f"""
    <div style="padding:15px;background:#f0f2f6;border-radius:10px">
    <h4>{emoji} {title}</h4>
    <p>{value}</p>
    </div>
    """, unsafe_allow_html=True)


def recommendation_card(title, explanation):

    st.markdown(f"""
    <div style="
        padding:20px;
        border-radius:12px;
        background:#ffffff;
        box-shadow:0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom:15px">

        <h3>🎬 {title}</h3>
        <p>{explanation}</p>
    </div>
    """, unsafe_allow_html=True)