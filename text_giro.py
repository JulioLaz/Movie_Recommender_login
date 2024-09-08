import streamlit as st

def giro(menu_id, text):
    st.markdown(f"""
    <style>
    @keyframes rotate {{
      0% {{ transform: rotateX(0deg); }}
      50% {{ transform: rotateX(180deg); }}
      100% {{ transform: rotateX(360deg); }}
    }}

    @keyframes shimmer {{
      0% {{ background-position: -1000px 0; }}
      100% {{ background-position: 1000px 0; }}
    }}

    .movie-title {{
      perspective: 1000px;
      padding: 10px 0;
      margin-bottom: 5px;
    }}

    .movie-title-inner {{
      display: inline-block;
      animation: rotate 3s linear infinite;
      transform-style: preserve-3d;
    }}

    .movie-title-text {{
      font-size: 2.8rem;
      font-weight: bold;
      text-transform: uppercase;
      background: linear-gradient(to right, #8f6B29, #FDE08D, #DF9F28);
      -webkit-background-clip: text;
      color: transparent;
      animation: shimmer 2s infinite linear;
      background-size: 200% 100%;
      padding: 0 10px;
    }}
    </style>

    <div class="movie-title">
      <div class="movie-title-inner">
        <span class="movie-title-text">{text} {menu_id.upper()}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)