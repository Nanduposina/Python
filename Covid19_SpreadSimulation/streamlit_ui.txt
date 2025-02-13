import streamlit as st
import pandas as pd
import os
from datetime import datetime
import assignment2

@st.cache_data
def Load_Countries():
    return pd.read_csv('a2-countries.csv')
class CovidImpactPredictor:
    def __init__(self):
        self.Countries_Data = Load_Countries()

    def Start_Simulation(self, selected_countries, sample_ratio, start_date, end_date):
        assignment2.run(
            countries_csv_name='a2-countries.csv',
            countries=selected_countries,
            sample_ratio=sample_ratio,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        return os.path.exists('a2-covid-simulation.png')

    def Details(self, sample_ratio, start_date, end_date, countries):
        st.write(f"Running with the following settings:")
        st.write(f"Sample Ratio: {sample_ratio:.0f}")
        st.write(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
        st.write(f"End Date: {end_date.strftime('%Y-%m-%d')}")
        st.write(f"Countries: {countries}")

    def run(self):
        st.title("COVID IMPACT PREDICTOR")
        sample_ratio = st.number_input("Sample Ratio", min_value=1e4, max_value=1e7, value=1e6, step=1e5, format="%.0f")
        start_date = st.date_input("Start Date", datetime(2021, 4, 1))
        end_date = st.date_input("End Date", datetime(2022, 4, 30))
        selected_countries = st.multiselect(
            "Select Countries",
            options=self.Countries_Data['country'].tolist(),
            default=['Afghanistan', 'Sweden', 'Japan']
        )
        if st.button("Run"):
            if selected_countries:
                with st.spinner('Running simulation...'):
                    Result = self.Start_Simulation(selected_countries, sample_ratio, start_date, end_date)
                self.Details(sample_ratio, start_date, end_date, selected_countries)
                if Result:
                    st.image('a2-covid-simulation.png')
                else:
                    st.error("The simulation image was not generated. Please check the logs for errors.")
            else:
                st.error("Please select at least one country before running the simulation.")
                
if __name__ == "__main__":
    app = CovidImpactPredictor()
    app.run()
