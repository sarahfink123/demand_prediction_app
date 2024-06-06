import streamlit as st
import os
import base64

st.set_page_config(
        page_title="Lobby",
        page_icon='🛏️',
        layout="wide",
        initial_sidebar_state="collapsed"
    )

# Function to load an image and convert it to a base64-encoded string
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Path to the image
lobby_path = os.path.join('..', 'demand_prediction_app', 'images', 'HoTELLme_lobby.png')

# Get the base64-encoded image string
base64_image = get_base64_image(lobby_path)

# Define CSS style for background
style = f"""
<style>
.stApp {{
    background-image: url('data:image/png;base64,{base64_image}');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
}}

</style>
"""

# Inject the CSS style
st.markdown(style, unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
                /* Optionally, hide the footer */
                .streamlit-footer {display: none;}
                /* Hide your specific div class, replace class name with the one you identified */
                .st-emotion-cache-uf99v8 {display: none;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

col1 = st.columns(10)
col1[9].link_button('→', 'https://hotellme.streamlit.app/intro', type='primary')
