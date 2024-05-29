import streamlit as st
#Title
'''
# Hotel booking predictor
'''
#Intro
st.markdown('''
Predict cancellations
            ''')

dummy_data = 0.7

#Input

#country
    #Select from drop down
st.selectbox('Nationality of customer:', 'German', 'France', 'Italian')
#lead_time
    #Range with toggle bar
st.slider('Days between time of booking and arrival:', 1, 100, 30)
#adr
    #Range with toggle bar
st.slider('Average daily rate ($):', 0, 1000, 100)
#arrival_date_month
    #Select from drop down
st.selectbox('Month of arrival:', 1,2,3,4,5,6,7,8,9,10,11,12)
#stays_in_week_nights
    #range with toggle bar
st.slider('Booked weekday nights:', 0, 50, 3)
#FUEL_PRCS
    #Range with toggle bar
st.slider('Current fuel price:', 113, 204, 150)
#INFLATION
    #Range with toggle bar
st.slider('Current inflation:', 1.6, 2.3, 2.0)

#Get prediction

if st.button('Check cancellation probability'):
    st.write(f'The cancellation probability for this booking is {dummy_data * 100:.0f} %')
