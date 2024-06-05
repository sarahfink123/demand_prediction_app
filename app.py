import streamlit as st
import pandas as pd
import requests
import os
import time
import asyncio
import folium
from concurrent.futures import ProcessPoolExecutor
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import plotly.express as px

st.set_page_config(
        page_title="Demand predictor",
        page_icon='🛏️',
        layout="wide",
    )

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

css_path = os.path.join('..', 'demand_prediction_app', 'style.css')
with open(css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

async def async_request(url, params):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: requests.get(url, params=params))
    return response.json()

#Title
logo_path = os.path.join('..', 'demand_prediction_app', 'images', 'hoTELLme_logo_blue.svg')
with open(logo_path, "r") as file:
    svg_content = file.read()

# Display the SVG file using st.image
st.image(svg_content)
#Tabs
tab1, tab2, tab3, tab4 = st.tabs(['Cancellation', 'Target country', 'Average daily rate', 'Meal'])

with tab1:
    #Intro
    st.markdown('''
    The cancellation predictor tells you if a hotel booking will be cancelled with an accurate probability. To predict the cancellation probability for an individual booking, please insert the booking parameters.
                ''')
    st.markdown('''
    ######
                ''')

    #Input
    st.markdown('''
    ##### Insert booking data:
                ''')
    #adr
        #Range with toggle bar
    adr = st.slider('Average daily rate in US $:', 0, 1000, 108)
    st.caption('The average daily rate for bookings is 108.')
    st.markdown('''######''')
    adr_plus = adr + 20
    adr_minus = adr - 20
    #Columns
    columns_1 = st.columns(2)
    #country
    dict_of_countries = {
    'PRT': 'Portugal', 'GBR': 'Great Britain', 'ESP': 'Spain', 'FRA': 'France', 'DEU': 'Germany',
    }
    country_nationalities = sorted(dict_of_countries.values())
        #Select from drop down
    country_name = columns_1[0].selectbox('Origin country of customer:', country_nationalities)
    country_code = ([key for key, value in dict_of_countries.items() if value == country_name][0])
    #arrival_date_month
        #Select from drop down
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = columns_1[1].selectbox('Month of arrival:', months)
    st.markdown('''######''')
    #Columns
    columns_2 = st.columns(2)
    #lead_time
        #Range with toggle bar
    lead_time = columns_2[0].slider('Days between time of booking and arrival:', 1, 100, 80)
    st.caption('The average delta between booking and arrival is 80 days.')
    lead_time_plus = lead_time + 20
    lead_time_minus = lead_time - 20
    #number of stays in nights
        #range with toggle bar
    total_stay = columns_2[1].slider('Booked nights:', 1, 60, 3)
    st.markdown('''######''')
    #Columns
    columns_3 = st.columns(2)
    #FUEL_PRCS
        #Range with toggle bar
    FUEL_PRCS = columns_3[0].slider('Current fuel price in US $:', 110, 205, 157)
    columns_3[0].caption('The average fuel price at the time of bookings is 157 US $.')
    #INFLATION
        #Range with toggle bar
    INFLATION = columns_3[1].slider('Current inflation in %:', 0.0, 10.0, 2.0)
    columns_3[1].caption('The average inflation rate at the time of bookings is 2.04 %.')
    st.markdown('''######''')

    url = 'https://demand-predictor-g6vy2lia4a-ew.a.run.app/predict_is_canceled?'
    #https://meal-predictor-g6vy2lia4a-ew.a.run.app/predict_is_canceled?lead_time=342&arrival_date_month=July&total_stay=0&adr=0&FUEL_PRCS=194&country=PRT&INFLATION=1.8

    if url == '':
        #Dummy prediction
        #Prediction needs to be given out as probability_is_cancelled and stored accordingly.
        if st.button('Check cancellation probability (dummy)'):
            if month in ['October', 'November', 'December']:
                probability_is_cancelled = 0.8
                probability_is_cancelled_plus_adr = 0.9
                probability_is_cancelled_minus_adr = 0.7
                probability_is_cancelled_plus_lead_time = 0.87
                probability_is_cancelled_minus_lead_time = 0.67
            elif month in ['June', 'July', 'August', 'September']:
                probability_is_cancelled = 0.6
                probability_is_cancelled_plus_adr = 0.7
                probability_is_cancelled_minus_adr = 0.5
                probability_is_cancelled_plus_lead_time = 0.73
                probability_is_cancelled_minus_lead_time = 0.37
            else:
                probability_is_cancelled = 0.3
                probability_is_cancelled_plus_adr = 0.4
                probability_is_cancelled_minus_adr = 0.2
                probability_is_cancelled_plus_lead_time = 0.53
                probability_is_cancelled_minus_lead_time = 0.23
            st.markdown('''
                ######
                ''')
            st.markdown('''
                ##### Cancellation probabilities
                ''')
            columns_7 = st.columns(3)
            columns_7[0].metric('Cancellation probability:', f'{probability_is_cancelled * 100:.0f}  %', 'current booking')
            columns_7[1].metric('Cancellation probability:', f'{probability_is_cancelled_plus_adr * 100:.0f}  %', '+20 $ daily rate')
            columns_7[2].metric('Cancellation probability:', f'{probability_is_cancelled_minus_adr * 100:.0f}  %', '-20 $ daily rate')
            columns_7[1].metric('Cancellation probability:', f'{probability_is_cancelled_plus_lead_time * 100:.0f}  %', '+20 days lead time')
            columns_7[2].metric('Cancellation probability:', f'{probability_is_cancelled_minus_lead_time * 100:.0f}  %', '-20 days lead time')
    else:
        params = {
            'country': country_code,
            'FUEL_PRCS':FUEL_PRCS,
            'lead_time': lead_time,
            'adr': adr,
            'arrival_date_month': month,
            'total_stay': total_stay,
            'INFLATION': INFLATION,
    }
        params_adr_plus = {
            'country': country_code,
            'FUEL_PRCS':FUEL_PRCS,
            'lead_time': lead_time,
            'adr': adr_plus,
            'arrival_date_month': month,
            'total_stay': total_stay,
            'INFLATION': INFLATION,
    }
        params_adr_minus = {
            'country': country_code,
            'FUEL_PRCS':FUEL_PRCS,
            'lead_time': lead_time,
            'adr': adr_minus,
            'arrival_date_month': month,
            'total_stay': total_stay,
            'INFLATION': INFLATION,
    }
        params_lead_time_plus = {
            'country': country_code,
            'FUEL_PRCS':FUEL_PRCS,
            'lead_time': lead_time_plus,
            'adr': adr,
            'arrival_date_month': month,
            'total_stay': total_stay,
            'INFLATION': INFLATION,
    }
        params_lead_time_minus = {
            'country': country_code,
            'FUEL_PRCS':FUEL_PRCS,
            'lead_time': lead_time_minus,
            'adr': adr,
            'arrival_date_month': month,
            'total_stay': total_stay,
            'INFLATION': INFLATION,
    }

#         if st.button('Check cancellation probability'):
#             with st.spinner('Building crazy AI magic...'):
#                 response = requests.get(url, params=params)
#                 response_adr_plus = requests.get(url, params=params_adr_plus)
#                 response_adr_minus = requests.get(url, params=params_adr_minus)
#                 response_lead_time_plus = requests.get(url, params=params_lead_time_plus)
#                 response_lead_time_minus = requests.get(url, params=params_lead_time_minus)
#                 if (response.status_code and response_adr_plus.status_code) == 200:
#                     probability_is_cancelled = response.json()['prediction probability']
#                     probability_is_cancelled_adr_plus = response_adr_plus.json()['prediction probability']
#                     probability_is_cancelled_adr_minus = response_adr_minus.json()['prediction probability']
#                     probability_is_cancelled_lead_time_plus = response_lead_time_plus.json()['prediction probability']
#                     probability_is_cancelled_lead_time_minus = response_lead_time_minus.json()['prediction probability']
#                     st.markdown('''
        #Get api model prediction
        if st.button('Check cancellation probability'):
            with st.spinner('Building crazy AI magic...'):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                tasks = [
                    async_request(url, params),
                    async_request(url, params_adr_plus),
                    async_request(url, params_adr_minus),
                    async_request(url, params_lead_time_plus),
                    async_request(url, params_lead_time_minus)
                ]
                responses = loop.run_until_complete(asyncio.gather(*tasks))
                response, response_adr_plus, response_adr_minus, response_lead_time_plus, response_lead_time_minus = responses
                if all([response, response_adr_plus, response_adr_minus, response_lead_time_plus, response_lead_time_minus]):
                    probability_is_cancelled = response['prediction probability']
                    probability_is_cancelled_adr_plus = response_adr_plus['prediction probability']
                    probability_is_cancelled_adr_minus = response_adr_minus['prediction probability']
                    probability_is_cancelled_lead_time_plus = response_lead_time_plus['prediction probability']
                    probability_is_cancelled_lead_time_minus = response_lead_time_minus['prediction probability']
                    st.markdown('''
                        ######
                        ''')
                    average_cancellation = 0.2844
                    st.markdown('''
                        ##### Cancellation probability for booking data:
                        ''')
                    delta = probability_is_cancelled - average_cancellation
                    change = 'higher' if delta > 0 else 'lower'
                    st.metric('', f'{probability_is_cancelled * 100:.0f}  %', f'{(delta) * 100:.0f} % {change} than the average cancellation rate', delta_color="inverse", label_visibility="collapsed")
                    st.markdown('''
                        ######
                        ''')
                    st.markdown('''
                        ##### Cancellation probabilities if the booking data were different:
                        ''')
                    columns_71 = st.columns(2)
                    columns_71[0].metric('If the daily rate were 20 $ higher:', f'{probability_is_cancelled_adr_plus * 100:.0f}  %', f'{(probability_is_cancelled_adr_plus - probability_is_cancelled) * 100:.0f} % change', delta_color="inverse")
                    columns_71[1].metric('If the daily rate were 20 $ lower:', f'{probability_is_cancelled_adr_minus * 100:.0f}  %', f'{(probability_is_cancelled_adr_minus - probability_is_cancelled) * 100:.0f} % change', delta_color="inverse")
                    columns_71[0].metric('If the customers booked 20 days earlier:', f'{probability_is_cancelled_lead_time_plus * 100:.0f}  %', f'{(probability_is_cancelled_lead_time_plus - probability_is_cancelled) * 100:.0f} % change', delta_color="inverse")
                    columns_71[1].metric('If the customers booked 20 days later:', f'{probability_is_cancelled_lead_time_minus * 100:.0f}  %', f'{(probability_is_cancelled_lead_time_minus - probability_is_cancelled) * 100:.0f} % change', delta_color="inverse")
                else:
                    st.write('Error in API call')

with tab2:
    #Intro
    st.markdown('''The target country predictor tells you which countries you can target for underutilized time periods. To predict the target country (e.g., for marketing campagins) for a potential booking type, please insert the booking parameters for your aspired booking type.
    ''')
    st.markdown('''
        ######
                ''')

    #Input
    st.markdown('''
    ##### Insert booking data:
                ''')
    #Input
    #Columns
    columns_5 = st.columns(2)
    #hotel
    dict_of_hotels_c = {
        1: 'City Hotel',
        0: 'Resort Hotel'
        }
    hotel_names_c = dict_of_hotels_c.values()
    hotel_name_c = columns_5[0].selectbox('Hotel:', hotel_names_c)
    hotel_c = ([key for key, value in dict_of_hotels_c.items() if value == hotel_name_c][0])
    # st.markdown('''######''')
    #Columns
    columns_51 = st.columns(2)
    #adults
    number_of_adults_c = [1,2,3]
    adults_c = columns_51[0].selectbox('Number of adults:', number_of_adults_c)
    #adr
        #Range with toggle bar
    adr_c = columns_51[1].slider('Potential average daily rate in US $:', 0, 1000, 108)
    #Month
    months_c = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_c = columns_5[1].selectbox('Potential month of arrival:', months_c)
    # st.markdown('''######''')
    #Columns
    columns_6 = st.columns(2)
    #lead_time
        #Range with toggle bar
    lead_time_c = columns_6[0].slider('Days until potential arrival:', 1, 100, 80)
    #number of stays in nights
        #range with toggle bar
    total_stay_c = columns_6[1].slider('Potential number of nights:', 1, 60, 3)
    # st.markdown('''######''')
    #INFLATION
        #Range with toggle bar
    INFLATION_c = st.slider('Current inflation in %:', 0.0, 10.0, 2.0, key='inflation_c')
    dict_of_countries_c = {
    'PRT': 'Portugal', 'GBR': 'Great Britain', 'ESP': 'Spain', 'FRA': 'France', 'DEU': 'Germany',
    }

    # def get_country_coordinates(country_pred):
    # # Construct the URL for the Nominatim API
    #     url_geolocator = "https://nominatim.openstreetmap.org/search?"
    #     params_geo = {
    #         "format": "jsonv2",
    #         "country": country_pred,
    #         "limit": 1
    #     }
    #     response = requests.get(url_geolocator, params=params_geo)
    #     if response.status_code == 200:
    #         data = response.json()
    #         if data:
    #             lat = float(data[0]['lat'])
    #             lon = float(data[0]['lon'])
    #             return lat, lon
    #         else:
    #             return None, None
    #     else:
    #         print("Error:", response.status_code)
    #         return None, None
    def get_country_coordinates(country_pred):
        dict_coordinates = {'Portugal': (39.3999, -8.2245),
            'Great Britain': (55.3781, -3.4360),
            'Spain': (40.4637, -3.7492),
            'France': (46.6034, 1.8883),
            'Germany': (51.1657, 10.4515)
             }
        lat, lon = dict_coordinates[country_pred]
        return lat, lon

    url = ''

    if url == '':
        #Dummy prediction
        #Prediction needs to give out country_code_c and that will be stored as country_code.
        if st.button('Check target country (dummy)'):
            if month_c in ['October', 'November', 'December']:
                country_code_c = 'PRT'
            elif month_c in ['June', 'July', 'August', 'September']:
                country_code_c = 'BRT'
            else: country_code_c = 'DEU'
            #Get dummy prediction
            country_pred = dict_of_countries_c[country_code_c]
            st.metric(f'Your potential bookings will most likely be done by people from:', country_pred)
            lat, lon = get_country_coordinates(country_pred)
            map = folium.Map(location=[lat, lon], zoom_start=2)
            folium.Marker([lat, lon], tooltip=country_pred).add_to(map)
            folium_static(map)
    else:
        params = {
            'adr': adr_c,
            'arrival_date_month': month_c,
            'lead_time': lead_time_c,
            'total_stay': total_stay_c,
            'adults': adults_c,
            'hotel': hotel_c,
            'INFLATION': INFLATION_c,

        }

        #Get api model prediction
        if st.button('Check target country'):
            with st.spinner('Building crazy AI magic...'):
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    country_code_c = response.json()['OUTPUT']
                    country_pred = dict_of_countries_c[country_code_c]
                    st.metric(f'Your potential bookings will most likely be done by people from:', country_pred)
                    lat, lon = get_country_coordinates(country_pred)
                    map = folium.Map(location=[lat, lon], zoom_start=2)
                    folium.Marker([lat, lon], tooltip=country_pred).add_to(map)
                    folium_static(map)
                else:
                    st.write('Error in API call')


with tab3:
    #Intro
    st.markdown('''
    The average daily rate predictor tells you at which average daily rate customers usually book. To predict the average daily rate for certain booking data, please insert the booking parameters of the booking.
                ''')
    st.markdown('''
    ######
                ''')

    #Input
    st.markdown('''
    ##### Insert booking data:
                ''')
    columns_a1 = st.columns(2)
    #hotel
    dict_of_hotels_a = {
        1: 'City Hotel',
        0: 'Resort Hotel'
        }
    hotel_names_a = dict_of_hotels_a.values()
    hotel_name_a = columns_a1[0].selectbox('Hotel:', hotel_names_a, key='Hotel_a')
    hotel_a = ([key for key, value in dict_of_hotels_a.items() if value == hotel_name_a][0])
    #Month
    months_a = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_a = columns_a1[1].selectbox('Potential month of arrival:', months_a, key='month_a')
    month_index = months_a.index(month_a)
    month_a_plus_index = (month_index + 1) % len(months_a)
    month_a_minus_index = (month_index - 1) % len(months_a)
    month_a_plus = months_a[month_a_plus_index] if month_a_plus_index != 0 else 'January'
    month_a_minus = months_a[month_a_minus_index] if month_a_minus_index != 11 else 'December'
    month_a_plus_name = months_a[month_a_plus_index] if month_a_plus_index != 0 else 'January'
    month_a_minus_name = months_a[month_a_minus_index] if month_a_minus_index != 11 else 'December'
    #Columns
    columns_a2 = st.columns(2)
    #Number of adults
    number_of_adults_a = [1,2,3]
    adults_a = columns_a2[0].selectbox('Number of adults:', number_of_adults_a, key='adults_a')
    #Columns
    columns_a3 = st.columns(2)
    #lead_time
        #Range with toggle bar
    lead_time_a = columns_a2[1].slider('Days until potential arrival:', 1, 100, 80, key='lead_time_a')
    lead_time_a_plus = lead_time + 20
    lead_time_a_minus = lead_time - 20
    #number of stays in nights
        #range with toggle bar
    total_stay_a = columns_a3[0].slider('Potential number of nights:', 1, 60, 3, key='total_stay_a')
    #INFLATION
        #Range with toggle bar
    INFLATION_a = columns_a3[1].slider('Current inflation in %:', 0.0, 10.0, 2.0, key='INFLATION_a')

    url_a = ''

    #adr beeinflusst bei lead time

    if url_a == '':
        #Dummy prediction
        #Prediction needs to be given out as average_daily_rate and stored accordingly.
        if st.button('Check average daily rate (dummy)'):
            if month in ['October', 'November', 'December']:
                average_daily_rate_a = 200
                average_daily_rate_a_plus_lead_time = 213
                average_daily_rate_a_minus_lead_time = 180
                average_daily_rate_a_plus_month = 232
                average_daily_rate_a_minus_month = 170
            elif month in ['June', 'July', 'August', 'September']:
                average_daily_rate_a = 140
                average_daily_rate_a_plus_lead_time = 183
                average_daily_rate_a_minus_lead_time = 120
                average_daily_rate_a_plus_month = 192
                average_daily_rate_a_minus_month = 70
            else:
                average_daily_rate_a = 70
                average_daily_rate_a_plus_lead_time = 83
                average_daily_rate_a_minus_lead_time = 60
                average_daily_rate_a_plus_month = 92
                average_daily_rate_a_minus_month = 30
            st.markdown('''
                ######
                ''')
            mean_average_daily_rate_a = 107.86
            st.markdown('''
                ##### Average daily rate:
                ''')
            delta_a = average_daily_rate_a - mean_average_daily_rate_a
            change_a = 'higher' if delta_a > 0 else 'lower'
            st.metric('', f'{average_daily_rate_a}  US $', f'{delta_a} % {change_a} than the mean average daily rate', label_visibility="collapsed")
            st.markdown('''
            ######
            ''')
            st.markdown('''
            ##### Average daily rate if the booking data were different:
            ''')
            columns_82 = st.columns(2)
            columns_82[0].metric('If the customers booked 20 days earlier:', f'{average_daily_rate_a_plus_lead_time}  US $', f'{(average_daily_rate_a_plus_lead_time - average_daily_rate_a)} % change')
            columns_82[1].metric('If the customers booked 20 days later:', f'{average_daily_rate_a_minus_lead_time}  US $', f'{(average_daily_rate_a_minus_lead_time - average_daily_rate_a)} % change')
            columns_82[0].metric(f'If the customer booked for {month_a_plus_name}:', f'{average_daily_rate_a_plus_month}  US $', f'{(average_daily_rate_a_plus_month - average_daily_rate_a)} % change')
            columns_82[1].metric(f'If the customers booked for {month_a_minus_name}:', f'{average_daily_rate_a_minus_month}  US $', f'{(average_daily_rate_a_minus_month - average_daily_rate_a)} % change')

    else:
        params_a = {
            'hotel': hotel_a,
            'month': month_a,
            'adults': adults_a,
            'lead_time': lead_time_a,
            'total_stay': total_stay_a,
            'INFLATION': INFLATION_a,
            'ALLE FEATURES': adr,
    }
        params_a_lead_time_plus = {
            'hotel': hotel_a,
            'month': month_a,
            'adults': adults_a,
            'lead_time': lead_time_a_plus,
            'total_stay': total_stay_a,
            'INFLATION': INFLATION_a,
            'ALLE FEATURES': adr,
    }
        params_a_lead_time_minus = {
            'hotel': hotel_a,
            'month': month_a,
            'adults': adults_a,
            'lead_time': lead_time_a_minus,
            'total_stay': total_stay_a,
            'INFLATION': INFLATION_a,
            'ALLE FEATURES': adr,
    }
        params_a_month_plus = {
            'hotel': hotel_a,
            'month': month_a_plus,
            'adults': adults_a,
            'lead_time': lead_time_a,
            'total_stay': total_stay_a,
            'INFLATION': INFLATION_a,
            'ALLE FEATURES': adr,
    }
        params_a_month_minus = {
            'hotel': hotel_a,
            'month': month_a_minus,
            'adults': adults_a,
            'lead_time': lead_time_a,
            'total_stay': total_stay_a,
            'INFLATION': INFLATION_a,
            'ALLE FEATURES': adr,
    }


        #Get api model prediction
        if st.button('Check average daily rate'):
            with st.spinner('Building crazy AI magic...'):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                tasks_a = [
                    async_request(url_a, params_a),
                    async_request(url_a, params_a_lead_time_plus),
                    async_request(url_a, params_a_lead_time_minus),
                    async_request(url_a, params_a_month_plus),
                    async_request(url_a, params_a_month_minus)
                ]
                responses_a = loop.run_until_complete(asyncio.gather(*tasks_a))
                response_a, response_a_lead_time_plus, response_a_lead_time_minus, response_a_month_plus, response_a_month_minus = responses_a
                if all([response_a, response_a_lead_time_plus, response_a_lead_time_minus, response_a_month_plus, response_a_month_minus]):
                    average_daily_rate_a = response_a['prediction probability']
                    average_daily_rate_a_plus_lead_time = response_a_lead_time_plus['prediction probability']
                    average_daily_rate_a_minus_lead_time = response_a_lead_time_minus['prediction probability']
                    average_daily_rate_a_plus_month = response_a_month_plus['prediction probability']
                    average_daily_rate_a_minus_month = response_a_month_minus['prediction probability']
                    st.markdown('''
                    ######
                    ''')
                    mean_average_daily_rate_a = 107.86
                    st.markdown('''
                        ##### Average daily rate:
                        ''')
                    delta_a = average_daily_rate_a - mean_average_daily_rate_a
                    change_a = 'higher' if delta_a > 0 else 'lower'
                    st.metric('', f'{average_daily_rate_a}  US $', f'{delta_a} % {change_a} than the mean average daily rate', label_visibility="collapsed")
                    st.markdown('''
                    ######
                    ''')
                    st.markdown('''
                    ##### Average daily rate if the booking data were different:
                    ''')
                    columns_82 = st.columns(2)
                    columns_82[0].metric('If the customers booked 20 days earlier:', f'{average_daily_rate_a_plus_lead_time}  US $', f'{(average_daily_rate_a_plus_lead_time - average_daily_rate_a)} % change')
                    columns_82[1].metric('If the customers booked 20 days later:', f'{average_daily_rate_a_minus_lead_time}  US $', f'{(average_daily_rate_a_minus_lead_time - average_daily_rate_a)} % change')
                    columns_82[0].metric(f'If the customer booked for {month_a_plus_name}:', f'{average_daily_rate_a_plus_month}  US $', f'{(average_daily_rate_a_plus_month - average_daily_rate_a)} % change')
                    columns_82[1].metric(f'If the customers booked for {month_a_minus_name}:', f'{average_daily_rate_a_minus_month}  US $', f'{(average_daily_rate_a_minus_month - average_daily_rate_a)} % change')
                else:
                    st.write('Error in API call')

with tab4:
    #Intro
    st.markdown('''
    The meal predictor tells you which meal options customers will probably book. To predict the meal plan for certain booking data, please insert the booking parameters of the booking.
                ''')
    st.markdown('''
    ######
                ''')

    #Input
    st.markdown('''
    ##### Insert booking data:
                ''')
    #Column
    columns_m1 = st.columns(2)
    #Hotel
    hotels_m = ['City Hotel', 'Resort Hotel']
    hotel_m = columns_m1[0].selectbox('Hotel:', hotels_m, key='Hotel_m')
    #Months
    months_m = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_m = columns_m1[1].selectbox('Potential month of arrival:', months_m, key='month_m')
    #Columns
    columns_m2 = st.columns(2)
    #Number of adults
    number_of_adults_m = [1,2,3]
    adults_m = columns_m2[0].selectbox('Number of adults:', number_of_adults_m, key='adults_m')
    #number of stays in nights
        #range with toggle bar
    total_stay_m = columns_m2[1].slider('Potential number of nights:', 1, 60, 3, key='total_stay_m')
    #lead_time
        #Range with toggle bar
    lead_time_m = st.slider('Days until potential arrival:', 1, 100, 80, key='lead_time_m')

    meal_m_dict = {
        'BB': 'Bed and Breakfast',
        'HB': 'Half Board',
        'FB': 'Full Board',
        'SC': 'Self Catering'
        }

    url_m = 'https://meal-predictor-g6vy2lia4a-ew.a.run.app/predict_is_meal?'

    if url_m == '':
        #Dummy prediction
        #Prediction needs to be given out as average_daily_rate and stored accordingly.
        if st.button('Check meal plan (dummy)'):
            if month_m in ['October', 'November', 'December']:
                probability_meal_BB = 0.23
                probability_meal_HB = 0.27
                probability_meal_FB = 0.34
                probability_meal_SC = 0.16
            elif month_m in ['June', 'July', 'August', 'September']:
                probability_meal_BB = 0.14
                probability_meal_HB = 0.54
                probability_meal_FB = 0.09
                probability_meal_SC = 0.23
            else:
                probability_meal_BB = 0.61
                probability_meal_HB = 0.14
                probability_meal_FB = 0.06
                probability_meal_SC = 0.19
            meal_proba_dict = {'probability_meal_BB': probability_meal_BB,  'probability_meal_HB': probability_meal_HB, 'probability_meal_FB': probability_meal_FB, 'probability_meal_SC': probability_meal_SC}
            meal_code_m = max(meal_proba_dict, key=meal_proba_dict.get)[-2:]
            meal_m = meal_m_dict[meal_code_m]
            st.markdown('''
                ######
                ''')
            st.markdown('''
                ##### Most probable meal plan:
                ''')
            st.metric('', f'{meal_m}', label_visibility="collapsed")
            st.markdown('''
            ##### Probability per meal plan:
            ''')
            meal_df = pd.DataFrame(dict(
                probability = [probability_meal_BB, probability_meal_HB, probability_meal_FB, probability_meal_SC],
                meal_plan = ['Bed and Breakfast', 'Half Board', 'Full Board', 'Self Catering']
            ))
            fig_m = px.line_polar(meal_df, r='probability', theta='meal_plan', line_close=True)
            fig_m.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',  # Background color
                radialaxis=dict(
                    visible=True,
                    tickfont=dict(color='#ffffff'),  # Font color
                    showticklabels=True,
                    tickangle=0,
                    dtick=0.1
                ),
                angularaxis=dict(
                    visible=True,
                    tickfont=dict(color='#ffffff'),  # Font color
                ),
                #gridshape='linear'
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Background color
            paper_bgcolor='rgba(0,0,0,0)',  # Background color
            font=dict(color='#ffffff'),  # Font color
            )
            st.plotly_chart(fig_m)

    else:
        params_m = {
            'hotel': hotel_m,
            'is_canceled': 0,
            'lead_time': lead_time_m,
            'adults': adults_m,
            'is_repeated_guest': 0,
            'adr': 99.3,
            'CPI_AVG': 241.176,
            'INFLATION': 2.1,
            'INFLATION_CHG': 0,
            'CSMR_SENT': 93.4,
            'UNRATE': 4.8,
            'INTRSRT': 1.0,
            'GDP': 18775.459,
            'FUEL_PRCS': 161.1,
            'CPI_HOTELS': 0.176265,
            'US_GINI': 41.1,
            'DIS_INC':41852.0,
            'total_stays': total_stay_m,
            'market_segment': 'Online TA',
            'distribution_channel': 'TA/TO',
            'reservation_status': 'Check-Out',
            'country': 'PRT',
            'arrival_date_month': month_m,
    }

        #Get api model prediction
        if st.button('Check meal plan'):
            with st.spinner('Building crazy AI magic...'):
                response_m = requests.get(url_m, params=params_m)
                if (response_m.status_code) == 200:
                    probabilities = response_m.json()['prediction_probability']
                    probability_meal_BB = probabilities['BB']
                    probability_meal_HB = probabilities['HB']
                    probability_meal_FB = probabilities['FB']
                    probability_meal_SC = probabilities['SC']
                    meal_proba_dict = {'probability_meal_BB': probability_meal_BB,  'probability_meal_HB': probability_meal_HB, 'probability_meal_FB': probability_meal_FB, 'probability_meal_SC': probability_meal_SC}
                    meal_code_hp = max(meal_proba_dict, key=meal_proba_dict.get)[-2:]
                    meal_highest_proba = meal_m_dict[meal_code_hp]
                    st.markdown('''
                        ######
                        ''')
                    st.markdown('''
                        ##### Most probable meal plan:
                        ''')
                    st.metric('', f'{meal_highest_proba}', label_visibility="collapsed")
                    st.markdown('''
                    ##### Probability per meal plan:
                    ''')
                    meal_df = pd.DataFrame(dict(
                        probability = [probability_meal_BB, probability_meal_HB, probability_meal_FB, probability_meal_SC],
                        meal_plan = ['Bed and Breakfast', 'Half Board', 'Full Board', 'Self Catering']
                    ))
                    fig_m = px.line_polar(meal_df, r='probability', theta='meal_plan', line_close=True)
                    fig_m.update_layout(
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',  # Background color
                        radialaxis=dict(
                            visible=True,
                            tickfont=dict(color='#ffffff'),  # Font color
                            showticklabels=True,
                            tickangle=0,
                            dtick=0.1
                        ),
                        angularaxis=dict(
                            visible=True,
                            tickfont=dict(color='#ffffff'),  # Font color
                        ),
                        #gridshape='linear'
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',  # Background color
                    paper_bgcolor='rgba(0,0,0,0)',  # Background color
                    font=dict(color='#ffffff'),  # Font color
                    )
                    st.plotly_chart(fig_m)
                else:
                    st.write('Error in API call')
