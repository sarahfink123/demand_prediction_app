import streamlit as st

st.set_page_config(
    page_title="Hotel booking predictor", # => Quick reference - Streamlit
    page_icon="🏩",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

CSS = """
h1 {
    color: #ffffff;
}
p {
    color: #ffffff;
}
button[kind='secondary'] {
    color: #ffffff;
    background-color: #FF4B4B;
}
div[data-testid='stTickBarMax'] {
    color: #ffffff;
}
div[data-testid='stTickBarMin'] {
    color: #ffffff;
}
div[data-testid='stThumbValue'] {
    color: #ffffff;
}

.stApp {
    background-color: #20365e;
    background-size: cover;
}
"""
Slider_Cursor = st.markdown('''
    <style>
        div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
            background-color: #ffffff;
        }
    </style>''', unsafe_allow_html=True)

Slider_Number = st.markdown('''
    <style>
        div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
            color: #ffffff;
        }
    </style>''', unsafe_allow_html=True)

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

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

#Title
'''
# Hotel booking predictor
'''
#Intro
st.markdown('''
Predict the cancellation propability for a specific booking:
            ''')

dummy_data = 0.5

#Input
#adr
    #Range with toggle bar
adr = st.slider('Average daily rate ($):', 0, 1000, 100)
#Columns
columns_1 = st.columns(2)
#country
country_nationalities = ['German', 'French']
    #Select from drop down
country = columns_1[0].selectbox('Nationality of customer:', country_nationalities)
#arrival_date_month
    #Select from drop down
months = [1,2,3,4,5,6,7,8,9,10,11,12]
month = columns_1[1].selectbox('Month of arrival:', months)
#Columns
columns_2 = st.columns(2)
#lead_time
    #Range with toggle bar
lead_time = columns_2[0].slider('Days between time of booking and arrival:', 1, 100, 30)
#stays_in_week_nights
    #range with toggle bar
stays_in_week_nights = columns_2[1].slider('Booked weekday nights:', 0, 50, 3)
#Columns
columns_3 = st.columns(2)
#FUEL_PRCS
    #Range with toggle bar
FUEL_PRCS = columns_3[0].slider('Current fuel price:', 113, 204, 150)
#INFLATION
    #Range with toggle bar
INFLATION = columns_3[1].slider('Current inflation:', 1.6, 2.3, 2.0)

#Get prediction

#Dummy prediction
if month > 9:
    dummy_data = 0.8
elif month > 5:
    dummy_data = 0.6
else: dummy_data = 0.3

if st.button('Check cancellation probability'):
    if dummy_data < 0.5:
        st.success(f'Congrats! The cancellation probability for this booking is {dummy_data * 100:.0f} %')
    elif dummy_data < 0.8:
        st.warning(f'Watch out! The cancellation probability for this booking is {dummy_data * 100:.0f} %')
    else:
        st.error(f'Oh no! The cancellation probability for this booking is {dummy_data * 100:.0f} %')
