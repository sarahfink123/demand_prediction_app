import streamlit as st
import os

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
# Hotel booking predictor
'''

#Create second page: https://docs.streamlit.io/develop/api-reference/layout/st.tabs
#Target 'country' X = 'arrival_date_month', 'adr', 'lead_time', 'stays_in_week_nights'

tab1, tab2 = st.tabs(['Cancellation predictor', 'Target country predictor'])

with tab1:
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

with tab2:
    #Intro
    st.markdown('''Predict the target country for marketing campaigns for certain booking types:
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

    #Dummy data
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
    #Dummy prediction
    if month_c > 9:
        country_code = 'PRT'
    elif month > 5:
        country_code = 'KNA'
    else: country_code = 'GHA'

    country_pred = dict_of_countries[country_code]

    #Get prediction
    if st.button('Check target country'):
        st.write(f'Your potential bookings will most likely be done by people from {country_pred}.')
