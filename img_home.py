import streamlit as st

def create_movie_page():
    # Set page config
   #  st.set_page_config(page_title="Movie Recommendations", layout="wide")
   #  tdz.title_poster('', 'Welcome to Movie Recommendations!')
    custom_css = """
    <style>
    .stApp {
        background-image: url("https://i.imgur.com/pkaSdxw.png");
        background-size: cover;
    }
    @keyframes rotate {
        from { transform: rotateY(0deg); }
        to { transform: rotateY(360deg); }
    }
    .rotating-logo {
        animation: rotate 5s linear infinite;
        display: inline-block;
    }
    .center-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 60vh;
    }
    </style>
    """

    # HTML content
      #   <h1 style="color: white; text-align: center; margin-bottom: 20px;">Welcome to Movie Recommendations!</h1>
    html_content = f"""
    {custom_css}
    <div class="center-content">
        <div class="rotating-logo">
            <img src="https://i.imgur.com/ravhd3L.png" alt="Cinemio Logo" style="width: 70vw;">
        </div>
    </div>
    """
      #   <h2 style="color: white; text-align: center; margin-top: 20px;">PRESENTA</h2>

    # Render the HTML content
    st.markdown(html_content, unsafe_allow_html=True)


def create_movie_welcome_page(menu_id):
    custom_css = """
    <style>
    .stApp {
        background-image: url("https://i.imgur.com/pkaSdxw.png");
        background-size: cover;
    }
    .center-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 60vh;
    }
    .menu-explanation {
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .login-invitation {
        background-color: rgba(255, 0, 0, 0.6);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
        text-align: center;
    }
    .text-invitation{
    font-size:1.5rem;

    }
    </style>
    """

    html_content = f"""
    {custom_css}
    <div class="center-content">
        <div class="menu-explanation">
            <h3>Menu Sections:</h3>
            <ul>
                <li><strong>Genres:</strong> Explore movies by your favorite genres.</li>
                <li><strong>Most Populars:</strong> Discover the most popular movies among our users.</li>
                <li><strong>Top Rated:</strong> Explore the highest-rated movies on our platform.</li>
                <li><strong>Community:</strong> Connect with other movie enthusiasts and share your thoughts.</li>
                <li><strong>Big fans:</strong> See what movies have the most dedicated fan base.</li>
                <li><strong>Just for you:</strong> Get personalized movie recommendations (requires login).</li>
                <li><strong>Search movies:</strong> Find specific movies or browse by various criteria.</li>
            </ul>
        </div>
        <div class="login-invitation">
            <p class="text-invitation">Want to rate movies and get personalized recommendations?</p>
            <p class="text-invitation">Use the Login in the menu to get started!</p>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

# if __name__ == "__main__":
#     create_movie_welcome_page()

# if __name__ == "__main__":
#     create_movie_welcome_page()