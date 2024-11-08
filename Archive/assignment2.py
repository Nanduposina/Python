import pandas as pd
import random
from datetime import datetime, timedelta
from sim_parameters import TRANSITION_PROBS, HOLDING_TIMES
from helper import create_plot

def Get_Country_Details(countries_csv_name: str):
    try:
        df = pd.read_csv(countries_csv_name)
        print(f"Reading data from the file {countries_csv_name} is successfully completed")
        yield df
    except FileNotFoundError:
        print(f"File named {countries_csv_name} not found.Recheck the spelling")
        raise
    except pd.errors.EmptyDataError:
        print(f"File named {countries_csv_name} does not contains any elements with in it")
        raise
def Load_Ctry_Data(countries_csv_name: str) -> pd.DataFrame:
    return next(Get_Country_Details(countries_csv_name))

def AgeGroup_Sampler(person_id, country, age_group, group_sample_size):
    return [{'person_id': person_id + i, 'country': country, 'age_group_name': age_group} 
            for i in range(group_sample_size)]

def PopulationSample_creator(Countries_Data, selected_countries, sample_ratio):
    _Samples_ = []
    P_id = 0
    for Ctry in selected_countries:
        Ctry_data = Countries_Data[Countries_Data['country'] == Ctry].iloc[0]
        Tot_Popu = Ctry_data['population']
        Sample_Size = Tot_Popu // sample_ratio
        AgeGroups_ = {
            'less_5': Ctry_data['less_5'],
            '5_to_14': Ctry_data['5_to_14'],
            '15_to_24': Ctry_data['15_to_24'],
            '25_to_64': Ctry_data['25_to_64'],
            'over_65': Ctry_data['over_65']
        }
        for Age_Group_, Percentage in AgeGroups_.items():
            GrupSample_Size = round(Sample_Size * Percentage / 100)
            _Samples_.extend(AgeGroup_Sampler(P_id, Ctry, Age_Group_, GrupSample_Size))
            P_id += GrupSample_Size
    return _Samples_

def Transition_Simulation(current_state, age_group, days_in_state):
    if days_in_state < HOLDING_TIMES[age_group][current_state]:
        return current_state, days_in_state + 1
    Probs = TRANSITION_PROBS[age_group][current_state]
    Rand = random.random()
    Cumm_Probs = []
    CumM_Prob = 0
    for Prob_ in Probs.values():
        CumM_Prob += Prob_
        Cumm_Probs.append(CumM_Prob)
    for Nxt_St, cum_prob in zip(Probs.keys(), Cumm_Probs):
        if Rand <= cum_prob:
            return Nxt_St, 0
    return current_state, days_in_state + 1

def Daily_State(person, current_state, days_in_state, current_date):
    Nxt_St_, Nxt_Days_ = Transition_Simulation(current_state, person['age_group_name'], days_in_state)
    return {
        'person_id': person['person_id'],
        'age_group_name': person['age_group_name'],
        'country': person['country'],
        'date': current_date.strftime('%Y-%m-%d'),
        'state': current_state,
        'staying_days': days_in_state,
        'prev_state': current_state  
    }, Nxt_St_, Nxt_Days_

def Infection_Spread(Population__Samples_, start_date, end_date):
    Start_ = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    days = (end - Start_).days + 1
    Sim_Result = []
    for person in Population__Samples_:
        current_state = 'H'  
        days_in_state = 0
        for day in range(days):
            current_date = Start_ + timedelta(days=day)
            Daily_Result, current_state, days_in_state = Daily_State(person, current_state, days_in_state, current_date)
            Sim_Result.append(Daily_Result)
    return Sim_Result

def Summary(Simulation_Results):
    Df = pd.DataFrame(Simulation_Results)
    Summary_ = Df.groupby(['date', 'country'])['state'].value_counts().unstack(fill_value=0)
    Summary = Summary_.reindex(columns=['H', 'I', 'S', 'M', 'D'], fill_value=0)
    _SUMMARY_ = Summary.reset_index()
    return _SUMMARY_[['date', 'country', 'D', 'H', 'I', 'M', 'S']]

def run(countries_csv_name, countries, sample_ratio, start_date, end_date):
    Countries_Data = Load_Ctry_Data(countries_csv_name)
    Population__Samples_ = PopulationSample_creator(Countries_Data, countries, sample_ratio)
    Simulation_Results = Infection_Spread(Population__Samples_, start_date, end_date)
    pd.DataFrame(Simulation_Results).to_csv('a2-covid-simulated-timeseries.csv', index=False)
    Summary_df = Summary(Simulation_Results)
    Summary_df.to_csv('a2-covid-summary-timeseries.csv', index=False)
    create_plot('a2-covid-summary-timeseries.csv', countries)
