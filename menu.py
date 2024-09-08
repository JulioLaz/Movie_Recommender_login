import hydralit_components as hc

def menu():
   menu_data = [
      {'icon': "fas fa-film", 'label': "Genres", 'submenu': [
         {'icon': "🎭", 'label': "Drama"},
         {'icon': "🎬", 'label': "Action"},
         {'icon': "🗺️", 'label': "Adventure"},
         {'icon': "💕", 'label': "Romance"},
         {'icon': "🤠", 'label': "Western"},
         {'icon': "🏛️", 'label': "History"},
         {'icon': "👻", 'label': "Horror"},
         {'icon': "🕵️", 'label': "Mystery"},
         {'icon': "😱", 'label': "Thriller"},
         {'icon': "😂", 'label': "Comedy"},
         # {'icon': "👪", 'label': "Family"},
         {'icon': "🦹", 'label': "Crime"},
         {'icon': "⚔️", 'label': "War"},
         {'icon': "🚀", 'label': "Sci-Fi"},
         {'icon': "🎵", 'label': "Music"},
         {'icon': "🎭", 'label': "Musical"},
         {'icon': "⚽", 'label': "Sport"},
         {'icon': "📜", 'label': "Biography"},
         {'icon': "🎞️", 'label': "Film-Noir"},
         {'icon': "🧙", 'label': "Fantasy"},
         {'icon': "🎨", 'label': "Animation"},
         {'icon': "🎥", 'label': "Documentary"},
         # {'icon': "🔞", 'label': "Adult"},
         # {'icon': "📰", 'label': "News"},
         # {'icon': "📺", 'label': "Reality-TV"}
      ]},

      {'icon': "fas fa-star", 'label': "Most Populars"},
      {'icon': "fas fa-heart", 'label': "Top Rated"},
      {'icon': "fas fa-users", 'label': "Community"},
      {'icon': "fas fa-crown", 'label': "Big fans"},
      {'icon': "fas fa-video", 'label': "Just for you"},
      {'icon': "fa fa-search", 'label': "Search movies"},
   ]
      # {'icon': "🔎", 'label': "Search movies"},

   over_theme = {
      'txc_inactive': '#D3D3D3',     
      'menu_background': '#2C3E50', 
      'txc_active': '#FFFFFF',      
      'option_active': '#000'    
      # 'option_active': '#34495E'    
   }

   menu_id = hc.nav_bar(
      menu_definition=menu_data,
      override_theme=over_theme,
      home_name='Home',
      login_name='Login',
      hide_streamlit_markers=True,
      sticky_nav=False,
      sticky_mode='sticky',
   )
   return menu_data,over_theme,menu_id