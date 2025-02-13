from assignment2 import WeatherSimulation
import numpy as np
import sys
import pylint as pl

# print(dir(assignment2))

print('\n*****************************')
print('Testing Assignment 2, DV1614')
print('*****************************')



#Check Python version
if sys.version_info < (3,7,0):
    print('\nYour python version info is:',sys.version_info )
    sys.exit("Python version should be equal or bigger than 3.7.0")
else:
    print(f'\nYour python version is correct ({sys.version_info})')


def check_formalities(transitions, holding_time):

    ITERATING_ROUNDS = 100

    # Check creating WeatherSimulation
    try:
        weather_sim = WeatherSimulation(transitions, holding_time)
    except:
        print('ERROR! Error in create WeatherSimulation object.')
        sys.exit('NOK!')


    # Check methods
    # set_holding_time_in_state', 'current_state', 'current_state_staying_hours', 'current_state_remaining_hours', 'next_state', 'iterable', 'simulate']
    methods = ['get_states', 'set_state', 'current_state',  'current_state_remaining_hours', 'next_state', 'iterable', 'simulate']
    if not all(map(lambda x: hasattr(weather_sim, x) and callable(getattr(weather_sim, x)), methods)):
        print('ERROR! Not all methods has been implemented.')
        sys.exit('NOK!')

    # Check iterables
    print(f'\nTesting iterating (for {ITERATING_ROUNDS} rounds):')
    try:
        sim_iter = weather_sim.iterable()
        for i in range(ITERATING_ROUNDS):
            print(next(sim_iter))
    except:
        print('ERROR! Problem in iterating!')
        sys.exit('NOK!')


    # Check Pylint score
    # Decision: not at this stage

def check_exception(wrong_transitions, holding_time):

    print(f'\nCheck exception handling')

    try:
        weather_sim = WeatherSimulation(wrong_transitions, holding_time)
    except RuntimeError as err:
        print(f'Exception raised (correctly) with details: {err}')
        result = True
    except :
        print(f'Exception raised but not with RuntimeError object')
        result = False
    else:
        result = False
    
    return result

def check_holding_times(transitions, holding_time):

    print(f'\nCheck holding times')

    NUM_CHANGES = 20

    weather_sim = WeatherSimulation(transitions, holding_time)

    for i in range(NUM_CHANGES):
        last_state = weather_sim.current_state()
        hd = holding_time[last_state]
        for j in range(hd):
            if weather_sim.current_state() != last_state:
                print(f'Error: State {last_state} changed before holding time {hd} to {weather_sim.current_state()}!')
                return False
            weather_sim.next_state()
    return True

 
def run_test(transitions, holding_time, avg, tolerance):



    STATES = ['sunny', 'cloudy', 'rainy', 'snowy']
    HOURS = 10000


    weather_sim = WeatherSimulation(transitions, holding_time)


    # Test simulation
    print(f'\nTesting simulation function for {HOURS} hours:')
    freq = weather_sim.simulate(HOURS)
    print(f'Simulation resulted in {list(zip(STATES,freq))}')

    # Check if the percentages adds up to 100
    if round(np.sum(freq)) != 100:
        sys.exit('ERROR! Summarization percentages do not add up to 100.')

    diff = list(map(lambda x: round(abs(x[0]-x[1]),2), zip(freq,avg)))
    if any(list(map(lambda x: x[0]>x[1] , zip(diff,tolerance)))):
        print(f'Some of your results are out of the acceptable range.')
        print(f'Higher range: {list(map(lambda x: round(x[0]+x[1],2), zip(avg,tolerance)))}')
        print(f'Your result: {freq}')        
        print(f'Lower range: {list(map(lambda x: round(x[0]-x[1],2), zip(avg,tolerance)))}')
    else:
        print(f'Results are in the acceptable range.')
        print(f'Higher range: {list(map(lambda x: round(x[0]+x[1],2), zip(avg,tolerance)))}')
        print(f'Your result: {freq}')        
        print(f'Lower range: {list(map(lambda x: round(x[0]-x[1],2), zip(avg,tolerance)))}')
        return True




transitions = {
'sunny':{'sunny':0.7, 'cloudy':0.3, 'rainy':0, 'snowy':0}, 
'cloudy':{'sunny':0.5, 'cloudy': 0.3, 'rainy':0.15, 'snowy':0.05}, 
'rainy':{'sunny':0.6, 'cloudy':0.2, 'rainy':0.15, 'snowy':0.05}, 
'snowy':{'sunny':0.7, 'cloudy':0.1, 'rainy':0.05, 'snowy':0.15} 
}

wrong_transitions = {
'sunny':{'sunny':0.7, 'cloudy':0.3, 'rainy':0.1, 'snowy':0}, 
'cloudy':{'sunny':0.5, 'cloudy': 0.3, 'rainy':0.15, 'snowy':0.05}, 
'rainy':{'sunny':0.6, 'cloudy':0.2, 'rainy':0.15, 'snowy':0.05}, 
'snowy':{'sunny':0.7, 'cloudy':0.1, 'rainy':0.05, 'snowy':0.15} 
}

holding_time = {'sunny':1, 'cloudy':2, 'rainy':2, 'snowy':1}


# No holding time
# avg = [63.5335, 29.1455,  5.284,   2.037 ]
# tolerance = [2.05, 1.75, 0.79, 0.45]


avg = [47.4975, 43.332,   7.697,   1.4735]
tolerance = [3.14, 2.38, 1.18, 0.47]

check_formalities(transitions, holding_time)

if not check_exception(wrong_transitions, holding_time):
    print("Exception handling did not work as instructed.")
    sys.exit('NOK!')

if not check_holding_times(transitions, holding_time):
    print("Probably a problem with holding times")
    sys.exit('NOK!')
else:
    print("Correct holding times")


if run_test(transitions, holding_time, avg, tolerance):
    print("\nAll tests passed")
    exit('OK!')
else:
    sys.exit('NOK!')



