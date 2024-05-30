import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(
        # page_title="Hello world",
        page_icon="🏩",
        layout="wide",
    )

# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

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


#Title
'''
# HOTEL BOOKING PREDICTOR
'''

#Create second page: https://docs.streamlit.io/develop/api-reference/layout/st.tabs
#Target 'country' X = 'arrival_date_month', 'adr', 'lead_time', 'stays_in_week_nights'

tab1, tab2 = st.tabs(['Cancellation predictor', 'Target country predictor'])

with tab1:
    #Intro
    st.markdown('''
    The cancellation predictor tells you if a hotel booking will be cancelled with an acurate probability. To predict the cancellation probability for an individual booking, please insert the booking parameters of the booking:
                ''')

    #Input
    #adr
        #Range with toggle bar
    adr = st.slider('Average daily rate ($):', 0, 1000, 100)
    #Columns
    columns_1 = st.columns(2)
    #country
    dict_of_countries = {
        'PRT': 'Portugal', 'GBR': 'Great Britain', 'USA': 'United States', 'ESP': 'Spain', 'IRL': 'Ireland',
        'FRA': 'France', 'ROU': 'Romania', 'NOR': 'Norway', 'OMN': 'Oman', 'ARG': 'Argentina', 'POL': 'Poland',
        'DEU': 'Germany', 'BEL': 'Belgium', 'CHE': 'Switzerland', 'CN': 'China', 'GRC': 'Greece', 'ITA': 'Italy',
        'NLD': 'Netherlands', 'DNK': 'Denmark', 'RUS': 'Russia', 'SWE': 'Sweden', 'AUS': 'Australia', 'EST': 'Estonia',
        'CZE': 'Czech Republic', 'BRA': 'Brazil', 'FIN': 'Finland', 'MOZ': 'Mozambique', 'BWA': 'Botswana', 'LUX': 'Luxembourg',
        'SVN': 'Slovenia', 'ALB': 'Albania', 'IND': 'India', 'CHN': 'China', 'MEX': 'Mexico', 'MAR': 'Morocco', 'UKR': 'Ukraine',
        'SMR': 'San Marino', 'LVA': 'Latvia', 'PRI': 'Puerto Rico', 'SRB': 'Serbia', 'CHL': 'Chile', 'AUT': 'Austria', 'BLR': 'Belarus',
        'LTU': 'Lithuania', 'TUR': 'Turkey', 'ZAF': 'South Africa', 'AGO': 'Angola', 'ISR': 'Israel', 'CYM': 'Cayman Islands', 'ZMB': 'Zambia',
        'CPV': 'Cape Verde', 'ZWE': 'Zimbabwe', 'DZA': 'Algeria', 'KOR': 'South Korea', 'CRI': 'Costa Rica', 'HUN': 'Hungary', 'ARE': 'United Arab Emirates',
        'TUN': 'Tunisia', 'JAM': 'Jamaica', 'HRV': 'Croatia', 'HKG': 'Hong Kong', 'IRN': 'Iran', 'GEO': 'Georgia', 'AND': 'Andorra', 'GIB': 'Gibraltar',
        'URY': 'Uruguay', 'JEY': 'Jersey', 'CAF': 'Central African Republic', 'CYP': 'Cyprus', 'COL': 'Colombia', 'GGY': 'Guernsey', 'KWT': 'Kuwait',
        'NGA': 'Nigeria', 'MDV': 'Maldives', 'VEN': 'Venezuela', 'SVK': 'Slovakia', 'FJI': 'Fiji', 'KAZ': 'Kazakhstan', 'PAK': 'Pakistan', 'IDN': 'Indonesia',
        'LBN': 'Lebanon', 'PHL': 'Philippines', 'SEN': 'Senegal', 'SYC': 'Seychelles', 'AZE': 'Azerbaijan', 'BHR': 'Bahrain', 'NZL': 'New Zealand', 'THA': 'Thailand',
        'DOM': 'Dominican Republic', 'MKD': 'North Macedonia', 'MYS': 'Malaysia', 'ARM': 'Armenia', 'JPN': 'Japan', 'LKA': 'Sri Lanka', 'CUB': 'Cuba', 'CMR': 'Cameroon',
        'BIH': 'Bosnia and Herzegovina', 'MUS': 'Mauritius', 'COM': 'Comoros', 'SUR': 'Suriname', 'UGA': 'Uganda', 'BGR': 'Bulgaria', 'CIV': 'Ivory Coast', 'JOR': 'Jordan',
        'SYR': 'Syria', 'SGP': 'Singapore', 'BDI': 'Burundi', 'SAU': 'Saudi Arabia', 'VNM': 'Vietnam', 'PLW': 'Palau', 'QAT': 'Qatar', 'EGY': 'Egypt', 'PER': 'Peru',
        'MLT': 'Malta', 'MWI': 'Malawi', 'ECU': 'Ecuador', 'MDG': 'Madagascar', 'ISL': 'Iceland', 'UZB': 'Uzbekistan', 'NPL': 'Nepal', 'BHS': 'Bahamas', 'MAC': 'Macau',
        'TGO': 'Togo', 'TWN': 'Taiwan', 'DJI': 'Djibouti', 'STP': 'Sao Tome and Principe', 'KNA': 'Saint Kitts and Nevis', 'ETH': 'Ethiopia', 'IRQ': 'Iraq', 'HND': 'Honduras',
        'RWA': 'Rwanda', 'KHM': 'Cambodia', 'MCO': 'Monaco', 'BGD': 'Bangladesh', 'IMN': 'Isle of Man', 'TJK': 'Tajikistan', 'NIC': 'Nicaragua', 'BEN': 'Benin', 'VGB': 'British Virgin Islands',
        'TZA': 'Tanzania', 'GAB': 'Gabon', 'GHA': 'Ghana', 'TMP': 'East Timor', 'GLP': 'Guadeloupe', 'KEN': 'Kenya', 'LIE': 'Liechtenstein', 'GNB': 'Guinea-Bissau', 'MNE': 'Montenegro',
        'UMI': 'United States Minor Outlying Islands', 'MYT': 'Mayotte', 'FRO': 'Faroe Islands', 'MMR': 'Myanmar', 'PAN': 'Panama', 'BFA': 'Burkina Faso', 'LBY': 'Libya', 'MLI': 'Mali',
        'NAM': 'Namibia', 'BOL': 'Bolivia', 'PRY': 'Paraguay', 'BRB': 'Barbados', 'ABW': 'Aruba', 'AIA': 'Anguilla', 'SLV': 'El Salvador', 'DMA': 'Dominica', 'PYF': 'French Polynesia',
        'GUY': 'Guyana', 'LCA': 'Saint Lucia', 'ATA': 'Antarctica', 'GTM': 'Guatemala', 'ASM': 'American Samoa', 'MRT': 'Mauritania', 'NCL': 'New Caledonia', 'KIR': 'Kiribati',
        'SDN': 'Sudan', 'ATF': 'French Southern Territories', 'SLE': 'Sierra Leone', 'LAO': 'Laos'
    }
    country_nationalities = sorted(dict_of_countries.values())
        #Select from drop down
    country_name = columns_1[0].selectbox('Nationality of customer:', country_nationalities)
    country_code = ([key for key, value in dict_of_countries.items() if value == country_name][0])
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


    url = ''

    if url == '':
        #Dummy prediction
        #Prediction needs to be given out as probability_is_cancelled and stored accordingly.
        if st.button('Check cancellation probability (dummy)'):
            if month > 9:
                probability_is_cancelled = 0.8
            elif month > 5:
                probability_is_cancelled = 0.6
            else: probability_is_cancelled = 0.3
            if probability_is_cancelled < 0.5:
                st.success(f'Congrats! The cancellation probability for this booking is {probability_is_cancelled * 100:.0f} %')
            elif probability_is_cancelled < 0.8:
                st.warning(f'Watch out! The cancellation probability for this booking is {probability_is_cancelled * 100:.0f} %')
            else:
                st.error(f'Oh no! The cancellation probability for this booking is {probability_is_cancelled * 100:.0f} %')
    else:
        params = {
            'country': country_code,
            'FUEL_PRCS':FUEL_PRCS,
            'lead_time': lead_time,
            'adr': adr,
            'arrival_date_month': month,
            'stays_in_week_nights': stays_in_week_nights,
            'INFLATION': INFLATION,
    }
        #Get api model prediction
        if st.button('Check cancellation probability'):
            response = requests.get(url, params=params)
            if response.status_code == 200:
                probability_is_cancelled = response.json()['OUTPUT_CANCELLATION']
                if probability_is_cancelled < 0.5:
                    st.success(f'Congrats! The cancellation probability for this booking is {probability_is_cancelled * 100:.0f} %')
                elif probability_is_cancelled < 0.8:
                    st.warning(f'Watch out! The cancellation probability for this booking is {probability_is_cancelled * 100:.0f} %')
                else:
                    st.error(f'Oh no! The cancellation probability for this booking is {probability_is_cancelled * 100:.0f} %')
            else:
                st.write('Error in API call')


with tab2:
    #Intro
    st.markdown('''The target country predictor tells you which countries you can target for underutilized time periods. To predict the target country (e.g., for marketing campagins) for a potential booking type, please insert the booking parameters for your aspired booking type:
    ''')

    #Input
    #Columns
    columns_5 = st.columns(2)
    #adr
        #Range with toggle bar
    adr_c = columns_5[0].slider('Potential average daily rate ($):', 0, 1000, 100)
    #Month
    months_c = [1,2,3,4,5,6,7,8,9,10,11,12]
    month_c = columns_5[1].selectbox('Potential month of arrival:', months_c)
        #Columns
    columns_6 = st.columns(2)
    #lead_time
        #Range with toggle bar
    lead_time_c = columns_6[0].slider('Days until potential arrival:', 1, 100, 30)
    #stays_in_week_nights
        #range with toggle bar
    stays_in_week_nights_c = columns_6[1].slider('Potential number of weekday nights:', 0, 50, 3)

    dict_of_countries_c = {
        'PRT': 'Portugal', 'GBR': 'Great Britain', 'USA': 'United States', 'ESP': 'Spain', 'IRL': 'Ireland',
        'FRA': 'France', 'ROU': 'Romania', 'NOR': 'Norway', 'OMN': 'Oman', 'ARG': 'Argentina', 'POL': 'Poland',
        'DEU': 'Germany', 'BEL': 'Belgium', 'CHE': 'Switzerland', 'CN': 'China', 'GRC': 'Greece', 'ITA': 'Italy',
        'NLD': 'Netherlands', 'DNK': 'Denmark', 'RUS': 'Russia', 'SWE': 'Sweden', 'AUS': 'Australia', 'EST': 'Estonia',
        'CZE': 'Czech Republic', 'BRA': 'Brazil', 'FIN': 'Finland', 'MOZ': 'Mozambique', 'BWA': 'Botswana', 'LUX': 'Luxembourg',
        'SVN': 'Slovenia', 'ALB': 'Albania', 'IND': 'India', 'CHN': 'China', 'MEX': 'Mexico', 'MAR': 'Morocco', 'UKR': 'Ukraine',
        'SMR': 'San Marino', 'LVA': 'Latvia', 'PRI': 'Puerto Rico', 'SRB': 'Serbia', 'CHL': 'Chile', 'AUT': 'Austria', 'BLR': 'Belarus',
        'LTU': 'Lithuania', 'TUR': 'Turkey', 'ZAF': 'South Africa', 'AGO': 'Angola', 'ISR': 'Israel', 'CYM': 'Cayman Islands', 'ZMB': 'Zambia',
        'CPV': 'Cape Verde', 'ZWE': 'Zimbabwe', 'DZA': 'Algeria', 'KOR': 'South Korea', 'CRI': 'Costa Rica', 'HUN': 'Hungary', 'ARE': 'United Arab Emirates',
        'TUN': 'Tunisia', 'JAM': 'Jamaica', 'HRV': 'Croatia', 'HKG': 'Hong Kong', 'IRN': 'Iran', 'GEO': 'Georgia', 'AND': 'Andorra', 'GIB': 'Gibraltar',
        'URY': 'Uruguay', 'JEY': 'Jersey', 'CAF': 'Central African Republic', 'CYP': 'Cyprus', 'COL': 'Colombia', 'GGY': 'Guernsey', 'KWT': 'Kuwait',
        'NGA': 'Nigeria', 'MDV': 'Maldives', 'VEN': 'Venezuela', 'SVK': 'Slovakia', 'FJI': 'Fiji', 'KAZ': 'Kazakhstan', 'PAK': 'Pakistan', 'IDN': 'Indonesia',
        'LBN': 'Lebanon', 'PHL': 'Philippines', 'SEN': 'Senegal', 'SYC': 'Seychelles', 'AZE': 'Azerbaijan', 'BHR': 'Bahrain', 'NZL': 'New Zealand', 'THA': 'Thailand',
        'DOM': 'Dominican Republic', 'MKD': 'North Macedonia', 'MYS': 'Malaysia', 'ARM': 'Armenia', 'JPN': 'Japan', 'LKA': 'Sri Lanka', 'CUB': 'Cuba', 'CMR': 'Cameroon',
        'BIH': 'Bosnia and Herzegovina', 'MUS': 'Mauritius', 'COM': 'Comoros', 'SUR': 'Suriname', 'UGA': 'Uganda', 'BGR': 'Bulgaria', 'CIV': 'Ivory Coast', 'JOR': 'Jordan',
        'SYR': 'Syria', 'SGP': 'Singapore', 'BDI': 'Burundi', 'SAU': 'Saudi Arabia', 'VNM': 'Vietnam', 'PLW': 'Palau', 'QAT': 'Qatar', 'EGY': 'Egypt', 'PER': 'Peru',
        'MLT': 'Malta', 'MWI': 'Malawi', 'ECU': 'Ecuador', 'MDG': 'Madagascar', 'ISL': 'Iceland', 'UZB': 'Uzbekistan', 'NPL': 'Nepal', 'BHS': 'Bahamas', 'MAC': 'Macau',
        'TGO': 'Togo', 'TWN': 'Taiwan', 'DJI': 'Djibouti', 'STP': 'Sao Tome and Principe', 'KNA': 'Saint Kitts and Nevis', 'ETH': 'Ethiopia', 'IRQ': 'Iraq', 'HND': 'Honduras',
        'RWA': 'Rwanda', 'KHM': 'Cambodia', 'MCO': 'Monaco', 'BGD': 'Bangladesh', 'IMN': 'Isle of Man', 'TJK': 'Tajikistan', 'NIC': 'Nicaragua', 'BEN': 'Benin', 'VGB': 'British Virgin Islands',
        'TZA': 'Tanzania', 'GAB': 'Gabon', 'GHA': 'Ghana', 'TMP': 'East Timor', 'GLP': 'Guadeloupe', 'KEN': 'Kenya', 'LIE': 'Liechtenstein', 'GNB': 'Guinea-Bissau', 'MNE': 'Montenegro',
        'UMI': 'United States Minor Outlying Islands', 'MYT': 'Mayotte', 'FRO': 'Faroe Islands', 'MMR': 'Myanmar', 'PAN': 'Panama', 'BFA': 'Burkina Faso', 'LBY': 'Libya', 'MLI': 'Mali',
        'NAM': 'Namibia', 'BOL': 'Bolivia', 'PRY': 'Paraguay', 'BRB': 'Barbados', 'ABW': 'Aruba', 'AIA': 'Anguilla', 'SLV': 'El Salvador', 'DMA': 'Dominica', 'PYF': 'French Polynesia',
        'GUY': 'Guyana', 'LCA': 'Saint Lucia', 'ATA': 'Antarctica', 'GTM': 'Guatemala', 'ASM': 'American Samoa', 'MRT': 'Mauritania', 'NCL': 'New Caledonia', 'KIR': 'Kiribati',
        'SDN': 'Sudan', 'ATF': 'French Southern Territories', 'SLE': 'Sierra Leone', 'LAO': 'Laos'
    }

    url = ''

    if url == '':
        #Dummy prediction
        #Prediction needs to give out country_code_c and that will be stored as country_code.
        if st.button('Check target country (dummy)'):
            if month_c > 9:
                country_code_c = 'PRT'
            elif month_c > 5:
                country_code_c = 'KNA'
            else: country_code_c = 'GHA'
            #Get dummy prediction
            country_pred = dict_of_countries_c[country_code_c]
            st.write(f'Your potential bookings will most likely be done by people from {country_pred}.')
    else:
        params = {
            'adr': adr_c,
            'arrival_date_month': month_c,
            'lead_time': lead_time_c,
            'stays_in_week_nights': stays_in_week_nights_c,
        }

        #Get api model prediction

        if st.button('Check target country'):
            response = requests.get(url, params=params)
            if response.status_code == 200:
                country_code_c = response.json()['OUTPUT']
                country_pred = dict_of_countries_c[country_code_c]
                st.write(f'Your potential bookings will most likely be done by people from {country_pred}.')
            else:
                st.write('Error in API call')
