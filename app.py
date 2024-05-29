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
#lead_time
    #Range with toggle bar
st.slider('Delta between booking and arrival:', 1, 100, 3)

#adr
    #Range with toggle bar
#arrival_date_month
    #Select from drop down
#stays_in_weeknights
    #Tange with toggle bar
#FUEL_PRCS
    #Range with toggle bar
#INFLATION
    #Range with toggle bar


#Get prediction

if st.button('Check cancellation probability'):
    st.write(f'The cancellation probability for this booking is {dummy_data * 100:.0f} %')
