import streamlit as st

def title_poster_just(size,text):
    st.markdown(f"""
    <style>
    @keyframes scroll {{
      0% {{ transform: translateX(50vw); }}
      100% {{ transform: translateX(-70%); }}
    }}

    @keyframes shimmer {{
      0% {{ background-position: -1000px 0; }}
      100% {{ background-position: 1000px 0; }}
    }}

    .movie-title {{
      overflow: hidden;
      background: rgba(0,0,0,.8);
      padding: 5px 0;
      margin-bottom: 5px;
    }}

    .movie-title-inner {{
      display: inline-block;
      white-space: nowrap;
      animation: scroll 6s linear infinite;
    }}

    .movie-title-text {{
      font-size: {size};
      font-weight: bold;
      text-transform: uppercase;
      background: linear-gradient(to right, #8f6B29, #FDE08D, #DF9F28);
      -webkit-background-clip: text;
      color: transparent;
      animation: shimmer 4s infinite linear;
      background-size: 200% 100%;
      padding: 0 20px;
    }}
    </style>

    <div class="movie-title">
      <div class="movie-title-inner">
        <span class="movie-title-text">{text}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

def title_poster(menu_id, text):
    st.markdown(f"""
    <style>
    @keyframes scroll {{
      0% {{ transform: translateX(70%); }}
      100% {{ transform: translateX(-70%); }}
    }}
    
    @keyframes shimmer {{
      0% {{ background-position: -1000px 0; }}
      100% {{ background-position: 1000px 0; }}
    }}
    
    @keyframes filmRoll {{
      0% {{ background-position: 0 0; }}
      100% {{ background-position: -48px 0; }}
    }}
    
    .movie-title-container {{
      position: relative;
      overflow: hidden;
      background: #000;
      padding: 2px 0;
      margin-bottom: 2px;
    }}
    
    .film-strip {{
      height: 24px;
      background-image: url('https://i.imgur.com/kQDOyqB.png');
      background-repeat: repeat-x;
      animation: filmRoll 3s linear infinite;
    }}
    
    .movie-title {{
      overflow: hidden;
      background: none;
      padding: 2px 0;
    }}
    
    .movie-title-inner {{
      display: inline-block;
      white-space: nowrap;
      animation: scroll 4s linear infinite;
    }}
    
    .movie-title-text {{
      font-size: 3.5rem;
      font-weight: bold;
      text-transform: uppercase;
      background: linear-gradient(to right, #8f6B29, #FDE08D, #DF9F28);
      -webkit-background-clip: text;
      color: transparent;
      animation: shimmer 4s infinite linear;
      background-size: 200% 100%;
      padding: 0 20px;
    }}
    </style>
    
    <div class="movie-title-container">
      <div class="film-strip"></div>
      <div class="movie-title">
        <div class="movie-title-inner">
          <span class="movie-title-text">{text} {menu_id.upper()}</span>
        </div>
      </div>
      <div class="film-strip"></div>
    </div>
    """, unsafe_allow_html=True)

# # Example usage
# if __name__ == "__main__":
#     st.set_page_config(page_title="Movie Title Demo", layout="wide")
#     title_poster("Action", "Welcome to")