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


st.set_page_config(
        page_title="Demand predictor",
        page_icon="🏩",
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
'''
# HOTEL BOOKING PREDICTOR
'''

tab1, tab2, tab3, tab4 = st.tabs(['Cancellation', 'Target country', 'Average daily rate', 'Meal'])

with tab1:
    #Intro
    st.markdown('''
    The cancellation predictor tells you if a hotel booking will be cancelled with an acurate probability. To predict the cancellation probability for an individual booking, please insert the booking parameters of the booking.
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
    adr = st.slider('Average daily rate in US $: (The average daily rate for bookings is 108.)', 0, 1000, 108)
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
    country_name = columns_1[0].selectbox('Nationality of customer:', country_nationalities)
    country_code = ([key for key, value in dict_of_countries.items() if value == country_name][0])
    #arrival_date_month
        #Select from drop down
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = columns_1[1].selectbox('Month of arrival:', months)
    #Columns
    columns_2 = st.columns(2)
    #lead_time
        #Range with toggle bar
    lead_time = columns_2[0].slider('Days between time of booking and arrival: (The average delta between booking and arrival is 80 days.)', 1, 100, 80)
    lead_time_plus = lead_time + 20
    lead_time_minus = lead_time - 20
    #number of stays in nights
        #range with toggle bar
    total_stay = columns_2[1].slider('Booked nights:', 0, 57, 3)
    #Columns
    columns_3 = st.columns(2)
    #FUEL_PRCS
        #Range with toggle bar
    FUEL_PRCS = columns_3[0].slider('Current fuel price in US $: (The average fuel price at the time of bookings is 157.)', 113, 204, 157)
    #INFLATION
        #Range with toggle bar
    INFLATION = columns_3[1].slider('Current inflation: (The average inflation rate at the time of bookings is 2.04.)', 1.6, 2.3, 2.0)


    url = 'https://demand-predictor-g6vy2lia4a-ew.a.run.app/predict?'
    #ALT: url = 'https://demand-prediction-g6vy2lia4a-ew.a.run.app/predict?'
    #https://demand-predictor-g6vy2lia4a-ew.a.run.app/predict?lead_time=342&arrival_date_month=July&total_stay=0&adr=0&FUEL_PRCS=194&country=PRT&INFLATION=1.8
    #https://demand-predictor-g6vy2lia4a-ew.a.run.app/predict?lead_time=342&arrival_date_month=July&total_stay=0&adr=0&FUEL_PRCS=194&country=PRT&INFLATION=1.8
    #https://demand-predictor-g6vy2lia4a-ew.a.run.app/predict?country=ALB&FUEL_PRCS=157&lead_time=30&adr=108&arrival_date_month=January&total_stay=3&INFLATION=2.0

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
    st.markdown('''The target country predictor tells you which countries you can target for underutilized time periods. To predict the target country (e.g., for marketing campagins) for a potential booking type, please insert the booking parameters for your aspired booking type:
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
    #Columns
    columns_51 = st.columns(2)
    #adults
    number_of_adults_c = [1,2,3]
    adults_c = columns_51[0].selectbox('Number of adults:', number_of_adults_c)
    #adr
        #Range with toggle bar
    adr_c = columns_51[1].slider('Potential average daily rate ($):', 0, 1000, 108)
    #Month
    months_c = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_c = columns_5[1].selectbox('Potential month of arrival:', months_c)
        #Columns
    columns_6 = st.columns(2)
    #lead_time
        #Range with toggle bar
    lead_time_c = columns_6[0].slider('Days until potential arrival:', 1, 100, 80)
    #number of stays in nights
        #range with toggle bar
    total_stay_c = columns_6[1].slider('Potential number of nights:', 0, 57, 3)
    #INFLATION
        #Range with toggle bar
    INFLATION_c = st.slider('Current inflation:', 1.6, 2.3, 2.0)


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
    total_stay_a = columns_a3[0].slider('Potential number of nights:', 0, 57, 3, key='total_stay_a')
    #INFLATION
        #Range with toggle bar
    INFLATION_a = columns_a3[1].slider('Current inflation:', 1.6, 2.3, 2.0, key='INFLATION_a')


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
    The meal predictor tells you which meal options customers will probably book. To predict the meal type for certain booking data, please insert the booking parameters of the booking.
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
    dict_of_hotels_m = {
        1: 'City Hotel',
        0: 'Resort Hotel'
        }
    hotel_names_m = dict_of_hotels_m.values()
    hotel_name_m = columns_m1[0].selectbox('Hotel:', hotel_names_m, key='Hotel_m')
    hotel_m = ([key for key, value in dict_of_hotels_m.items() if value == hotel_name_m][0])
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
    total_stay_m = columns_m2[1].slider('Potential number of nights:', 0, 57, 3, key='total_stay_m')
    #lead_time
        #Range with toggle bar
    lead_time_m = st.slider('Days until potential arrival:', 1, 100, 80, key='lead_time_m')

    meal_m_dict = {
        'BB': 'Bed and Breakfast',
        'HB': 'Half Board',
        'FB': 'Full Board',
        'SC': 'Self Catering'
        }

    url_m = ''

    if url_m == '':
        #Dummy prediction
        #Prediction needs to be given out as average_daily_rate and stored accordingly.
        if st.button('Check meal type (dummy)'):
            if month in ['October', 'November', 'December']:
                meal_code_m = 'HB'
            elif month in ['June', 'July', 'August', 'September']:
                meal_code_m = 'FB'
            else:
                meal_code_m = 'BB'
            meal_m = meal_m_dict[meal_code_m]
            st.markdown('''
                ######
                ''')
            st.markdown('''
                ##### Probable meal type:
                ''')
            st.metric('', f'{meal_m}', label_visibility="collapsed")

    else:
        params_m = {
            'lead_time': lead_time_m
    }

        # #Get api model prediction
        # if st.button('Check average daily rate'):
        #     with st.spinner('Building crazy AI magic...'):
        #         response_m = requests.get(url_m, params_m=params_m)
        #         if (response_m.status_code) == 200:
        #             meal_m = response_m.json()['adr']
        #             st.markdown('''
        #                 ######
        #                 ''')
        #             st.markdown('''
        #                 ##### Average daily rate:
        #                 ''')
        #             st.metric('', f'{meal * 100:.0f}  US $', f'{(delta_a) * 100:.0f} % {change_A} than the mean average daily rate', label_visibility="collapsed")
        #         else:
        #             st.write('Error in API call')





#OLD api call (in case something breaks)
# with tab1:
#     #Intro
#     st.markdown('''
#     The cancellation predictor tells you if a hotel booking will be cancelled with an acurate probability. To predict the cancellation probability for an individual booking, please insert the booking parameters of the booking.
#                 ''')
#     st.markdown('''
#     ######
#                 ''')

#     #Input
#     st.markdown('''
#     ##### Insert booking data:
#                 ''')
#     #adr
#         #Range with toggle bar
#     adr = st.slider('Average daily rate in US $: (The average daily rate for bookings is 108.)', 0, 1000, 108)
#     adr_plus = adr + 20
#     adr_minus = adr - 20
#     #Columns
#     columns_1 = st.columns(2)
#     #country
#     dict_of_countries = {
#         'PRT': 'Portugal', 'GBR': 'Great Britain', 'USA': 'United States', 'ESP': 'Spain', 'IRL': 'Ireland',
#         'FRA': 'France', 'ROU': 'Romania', 'NOR': 'Norway', 'OMN': 'Oman', 'ARG': 'Argentina', 'POL': 'Poland',
#         'DEU': 'Germany', 'BEL': 'Belgium', 'CHE': 'Switzerland', 'CN': 'China', 'GRC': 'Greece', 'ITA': 'Italy',
#         'NLD': 'Netherlands', 'DNK': 'Denmark', 'RUS': 'Russia', 'SWE': 'Sweden', 'AUS': 'Australia', 'EST': 'Estonia',
#         'CZE': 'Czech Republic', 'BRA': 'Brazil', 'FIN': 'Finland', 'MOZ': 'Mozambique', 'BWA': 'Botswana', 'LUX': 'Luxembourg',
#         'SVN': 'Slovenia', 'ALB': 'Albania', 'IND': 'India', 'CHN': 'China', 'MEX': 'Mexico', 'MAR': 'Morocco', 'UKR': 'Ukraine',
#         'SMR': 'San Marino', 'LVA': 'Latvia', 'PRI': 'Puerto Rico', 'SRB': 'Serbia', 'CHL': 'Chile', 'AUT': 'Austria', 'BLR': 'Belarus',
#         'LTU': 'Lithuania', 'TUR': 'Turkey', 'ZAF': 'South Africa', 'AGO': 'Angola', 'ISR': 'Israel', 'CYM': 'Cayman Islands', 'ZMB': 'Zambia',
#         'CPV': 'Cape Verde', 'ZWE': 'Zimbabwe', 'DZA': 'Algeria', 'KOR': 'South Korea', 'CRI': 'Costa Rica', 'HUN': 'Hungary', 'ARE': 'United Arab Emirates',
#         'TUN': 'Tunisia', 'JAM': 'Jamaica', 'HRV': 'Croatia', 'HKG': 'Hong Kong', 'IRN': 'Iran', 'GEO': 'Georgia', 'AND': 'Andorra', 'GIB': 'Gibraltar',
#         'URY': 'Uruguay', 'JEY': 'Jersey', 'CAF': 'Central African Republic', 'CYP': 'Cyprus', 'COL': 'Colombia', 'GGY': 'Guernsey', 'KWT': 'Kuwait',
#         'NGA': 'Nigeria', 'MDV': 'Maldives', 'VEN': 'Venezuela', 'SVK': 'Slovakia', 'FJI': 'Fiji', 'KAZ': 'Kazakhstan', 'PAK': 'Pakistan', 'IDN': 'Indonesia',
#         'LBN': 'Lebanon', 'PHL': 'Philippines', 'SEN': 'Senegal', 'SYC': 'Seychelles', 'AZE': 'Azerbaijan', 'BHR': 'Bahrain', 'NZL': 'New Zealand', 'THA': 'Thailand',
#         'DOM': 'Dominican Republic', 'MKD': 'North Macedonia', 'MYS': 'Malaysia', 'ARM': 'Armenia', 'JPN': 'Japan', 'LKA': 'Sri Lanka', 'CUB': 'Cuba', 'CMR': 'Cameroon',
#         'BIH': 'Bosnia and Herzegovina', 'MUS': 'Mauritius', 'COM': 'Comoros', 'SUR': 'Suriname', 'UGA': 'Uganda', 'BGR': 'Bulgaria', 'CIV': 'Ivory Coast', 'JOR': 'Jordan',
#         'SYR': 'Syria', 'SGP': 'Singapore', 'BDI': 'Burundi', 'SAU': 'Saudi Arabia', 'VNM': 'Vietnam', 'PLW': 'Palau', 'QAT': 'Qatar', 'EGY': 'Egypt', 'PER': 'Peru',
#         'MLT': 'Malta', 'MWI': 'Malawi', 'ECU': 'Ecuador', 'MDG': 'Madagascar', 'ISL': 'Iceland', 'UZB': 'Uzbekistan', 'NPL': 'Nepal', 'BHS': 'Bahamas', 'MAC': 'Macau',
#         'TGO': 'Togo', 'TWN': 'Taiwan', 'DJI': 'Djibouti', 'STP': 'Sao Tome and Principe', 'KNA': 'Saint Kitts and Nevis', 'ETH': 'Ethiopia', 'IRQ': 'Iraq', 'HND': 'Honduras',
#         'RWA': 'Rwanda', 'KHM': 'Cambodia', 'MCO': 'Monaco', 'BGD': 'Bangladesh', 'IMN': 'Isle of Man', 'TJK': 'Tajikistan', 'NIC': 'Nicaragua', 'BEN': 'Benin', 'VGB': 'British Virgin Islands',
#         'TZA': 'Tanzania', 'GAB': 'Gabon', 'GHA': 'Ghana', 'TMP': 'East Timor', 'GLP': 'Guadeloupe', 'KEN': 'Kenya', 'LIE': 'Liechtenstein', 'GNB': 'Guinea-Bissau', 'MNE': 'Montenegro',
#         'UMI': 'United States Minor Outlying Islands', 'MYT': 'Mayotte', 'FRO': 'Faroe Islands', 'MMR': 'Myanmar', 'PAN': 'Panama', 'BFA': 'Burkina Faso', 'LBY': 'Libya', 'MLI': 'Mali',
#         'NAM': 'Namibia', 'BOL': 'Bolivia', 'PRY': 'Paraguay', 'BRB': 'Barbados', 'ABW': 'Aruba', 'AIA': 'Anguilla', 'SLV': 'El Salvador', 'DMA': 'Dominica', 'PYF': 'French Polynesia',
#         'GUY': 'Guyana', 'LCA': 'Saint Lucia', 'ATA': 'Antarctica', 'GTM': 'Guatemala', 'ASM': 'American Samoa', 'MRT': 'Mauritania', 'NCL': 'New Caledonia', 'KIR': 'Kiribati',
#         'SDN': 'Sudan', 'ATF': 'French Southern Territories', 'SLE': 'Sierra Leone', 'LAO': 'Laos'
#     }
#     country_nationalities = sorted(dict_of_countries.values())
#         #Select from drop down
#     country_name = columns_1[0].selectbox('Nationality of customer:', country_nationalities)
#     country_code = ([key for key, value in dict_of_countries.items() if value == country_name][0])
#     #arrival_date_month
#         #Select from drop down
#     months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#     month = columns_1[1].selectbox('Month of arrival:', months)
#     #Columns
#     columns_2 = st.columns(2)
#     #lead_time
#         #Range with toggle bar
#     lead_time = columns_2[0].slider('Days between time of booking and arrival: (The average delta between booking and arrival is 80 days.)', 1, 100, 30)
#     lead_time_plus = lead_time + 20
#     lead_time_minus = lead_time - 20
#     #number of stays in nights
#         #range with toggle bar
#     total_stay = columns_2[1].slider('Booked nights:', 0, 57, 3)
#     #Columns
#     columns_3 = st.columns(2)
#     #FUEL_PRCS
#         #Range with toggle bar
#     FUEL_PRCS = columns_3[0].slider('Current fuel price in US $: (The average fuel price at the time of bookings is 157.)', 113, 204, 157)
#     #INFLATION
#         #Range with toggle bar
#     INFLATION = columns_3[1].slider('Current inflation: (The average inflation rate at the time of bookings is 2.04.)', 1.6, 2.3, 2.0)


#     url = 'https://demand-prediction-g6vy2lia4a-ew.a.run.app/predict?'

#     if url == '':
#         #Dummy prediction
#         #Prediction needs to be given out as probability_is_cancelled and stored accordingly.
#         if st.button('Check cancellation probability (dummy)'):
#             if month in ['October', 'November', 'December']:
#                 probability_is_cancelled = 0.8
#             elif month in ['June', 'July', 'August', 'September']:
#                 probability_is_cancelled = 0.6
#             else:
#                 probability_is_cancelled = 0.3
#             if month in ['October', 'November', 'December']:
#                 probability_is_cancelled_plus_adr = 0.9
#             elif month in ['June', 'July', 'August', 'September']:
#                 probability_is_cancelled_plus_adr = 0.7
#             else:
#                 probability_is_cancelled_plus_adr = 0.4
#             if month in ['October', 'November', 'December']:
#                 probability_is_cancelled_minus_adr = 0.7
#             elif month in ['June', 'July', 'August', 'September']:
#                 probability_is_cancelled_minus_adr = 0.5
#             else:
#                 probability_is_cancelled_minus_adr = 0.2
#             if month in ['October', 'November', 'December']:
#                 probability_is_cancelled_plus_lead_time = 0.87
#             elif month in ['June', 'July', 'August', 'September']:
#                 probability_is_cancelled_plus_lead_time = 0.73
#             else:
#                 probability_is_cancelled_plus_lead_time = 0.53
#             if month in ['October', 'November', 'December']:
#                 probability_is_cancelled_minus_lead_time = 0.67
#             elif month in ['June', 'July', 'August', 'September']:
#                 probability_is_cancelled_minus_lead_time = 0.37
#             else:
#                 probability_is_cancelled_minus_lead_time = 0.23
#             st.markdown('''
#                 ######
#                 ''')
#             st.markdown('''
#                 ##### Cancellation probabilities
#                 ''')
#             columns_7 = st.columns(3)
#             columns_7[0].metric('Cancellation probability:', f'{probability_is_cancelled * 100:.0f}  %', 'current booking')
#             columns_7[1].metric('Cancellation probability:', f'{probability_is_cancelled_plus_adr * 100:.0f}  %', '+20 $ daily rate')
#             columns_7[2].metric('Cancellation probability:', f'{probability_is_cancelled_minus_adr * 100:.0f}  %', '-20 $ daily rate')
#             columns_7[1].metric('Cancellation probability:', f'{probability_is_cancelled_plus_lead_time * 100:.0f}  %', '+20 days lead time')
#             columns_7[2].metric('Cancellation probability:', f'{probability_is_cancelled_minus_lead_time * 100:.0f}  %', '-20 days lead time')
#     else:
#         params = {
#             'country': country_code,
#             'FUEL_PRCS':FUEL_PRCS,
#             'lead_time': lead_time,
#             'adr': adr,
#             'arrival_date_month': month,
#             'total_stay': total_stay,
#             'INFLATION': INFLATION,
#     }
#         params_adr_plus = {
#             'country': country_code,
#             'FUEL_PRCS':FUEL_PRCS,
#             'lead_time': lead_time,
#             'adr': adr_plus,
#             'arrival_date_month': month,
#             'total_stay': total_stay,
#             'INFLATION': INFLATION,
#     }
#         params_adr_minus = {
#             'country': country_code,
#             'FUEL_PRCS':FUEL_PRCS,
#             'lead_time': lead_time,
#             'adr': adr_minus,
#             'arrival_date_month': month,
#             'total_stay': total_stay,
#             'INFLATION': INFLATION,
#     }
#         params_lead_time_plus = {
#             'country': country_code,
#             'FUEL_PRCS':FUEL_PRCS,
#             'lead_time': lead_time_plus,
#             'adr': adr,
#             'arrival_date_month': month,
#             'total_stay': total_stay,
#             'INFLATION': INFLATION,
#     }
#         params_lead_time_minus = {
#             'country': country_code,
#             'FUEL_PRCS':FUEL_PRCS,
#             'lead_time': lead_time_minus,
#             'adr': adr,
#             'arrival_date_month': month,
#             'total_stay': total_stay,
#             'INFLATION': INFLATION,
#     }
#         #Get api model prediction
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
#                         ######
#                         ''')
#                     average_cancellation = 0.2844
#                     st.markdown('''
#                         ##### Cancellation probability for booking data:
#                         ''')
#                     delta = probability_is_cancelled - average_cancellation
#                     change = 'higher' if delta > 0 else 'lower'
#                     st.metric('', f'{probability_is_cancelled * 100:.0f}  %', f'{(delta) * 100:.0f} % {change} than the average cancellation rate', delta_color="inverse", label_visibility="collapsed")
#                     st.markdown('''
#                         ######
#                         ''')
#                     st.markdown('''
#                         ##### Cancellation probabilities if the booking data were different:
#                         ''')
#                     columns_71 = st.columns(2)
#                     columns_71[0].metric('If the daily rate were 20 $ higher:', f'{probability_is_cancelled_adr_plus * 100:.0f}  %', f'{(probability_is_cancelled_adr_plus - probability_is_cancelled) * 100:.0f} % change', delta_color="inverse")
#                     columns_71[1].metric('If the daily rate were 20 $ lower:', f'{probability_is_cancelled_adr_minus * 100:.0f}  %', f'{(probability_is_cancelled_adr_minus - probability_is_cancelled) * 100:.0f} % change', delta_color="inverse")
#                     columns_71[0].metric('If the customers booked 20 days earlier:', f'{probability_is_cancelled_lead_time_plus * 100:.0f}  %', f'{(probability_is_cancelled_lead_time_plus - probability_is_cancelled) * 100:.0f} % change', delta_color="inverse")
#                     columns_71[1].metric('If the customers booked 20 days later:', f'{probability_is_cancelled_lead_time_minus * 100:.0f}  %', f'{(probability_is_cancelled_lead_time_minus - probability_is_cancelled) * 100:.0f} % change', delta_color="inverse")
#                 else:
#                     st.write('Error in API call')
