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
