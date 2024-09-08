import streamlit as st
from supabase import create_client
import pandas as pd
from st_login_form import login_form
import just_for_you
user_id = None

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

def register_user(username, password):
    user_data = {
        "username": username,
        "password": password,  # In a real app, you should hash the password
        "last_login": None
    }
    result = supabase.table("users").insert(user_data).execute()
    return result.data

# Function to check if a user exists and password is correct
def authenticate_user(username, password):
    result = supabase.table("users").select("*").eq("username", username).execute()
    if result.data:
        user = result.data[0]
        if user['password_hash'] == password:  # In a real app, you should compare hashed passwords
            # Update last login
            supabase.table("user_login").update({"last_login": "now()"}).eq("user_id", user['user_id']).execute()
            return user
    return None

def login():
    # st.title("Login / Register App")

    client = login_form()

    if st.session_state.get("authenticated"):
        
        if st.session_state.get("username"):
            username = st.session_state.get("username")
            fetch_user_data(username)
            just_for_you.just_for_you_section()

        else:
            st.success("Welcome guest")
            show_user_data(username)
            just_for_you.just_for_you_section()



def show_login_register():
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = authenticate_user(username, password)
            if user:
                st.session_state["authenticated"] = True
                st.session_state["username"] = user['username']
                # st.success(f"Logged in as {user['username']}")
                # show_user_data(username)
                st.rerun()

            else:
                st.error("Invalid username or password")

    with tab2:
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if new_username and new_password:
                result = register_user(new_username, new_password)
                if result:
                    st.success("User registered successfully! Please login.")
                else:
                    st.error("Registration failed")
            else:
                st.warning("Please enter both username and password")

@st.cache_data(ttl=600)
def fetch_user_data(username):
   global user_id
   # response = supabase.table("users").select("user_id").execute()
   # response = supabase.table("users").select("user_id").eq("username", username).execute()
   response = supabase.table("users").select('*').eq("username", username).execute()
   user_id = response.data[0]['user_id']
   st.session_state['user_id'] = user_id
   usuarioid=st.session_state.get("user_id")
   username=st.session_state.get("username")
   st.success(f"Bienvenido {username}, tu id es: {usuarioid}")
#    st.title(usuarioid)
   return response.data

def show_user_data(username):
    rows = fetch_user_data(username)
    df = pd.DataFrame(rows)
    if df.empty:
        st.write("No hay filas en la tabla")
    else:
        st.dataframe(df)



# if __name__ == "__main__":
#     login()
    