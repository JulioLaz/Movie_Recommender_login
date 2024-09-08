import streamlit as st

def title_poster_genre(menu_id,text):
    st.markdown(f"""
    <div> <p style="
        background-color:none;
        color:#DF9F28;
        padding:0px;
        text-align:center;
        font-size:2rem;
        animation: pulse 1.5s infinite;
        ">
        <b>{text} {menu_id.upper()}</b>
        </p>
    </div>
    
    <style>
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    </style>
    """, unsafe_allow_html=True)