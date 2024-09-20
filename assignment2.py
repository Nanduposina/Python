import numpy as np

class WeatherSimulation:
    def __init__(self, transition_probabilities, holding_times):
        # Validate probabilities
        for state, transitions in transition_probabilities.items():
            if not np.isclose(sum(transitions.values()), 1.0):
                raise RuntimeError(f"Transition probabilities for state '{state}' do not sum to 1")
        
        self.transition_probabilities = transition_probabilities
        self.holding_times = holding_times
        self.current_state_name = 'sunny'
        self.remaining_hours = self.holding_times[self.current_state_name]
    
    def get_states(self):
        return list(self.transition_probabilities.keys())
    
    def current_state(self):
        return self.current_state_name
    
    def next_state(self):
        if self.remaining_hours > 1:
            self.remaining_hours -= 1
        else:
            self.remaining_hours = self.holding_times[self.current_state_name]
            states = list(self.transition_probabilities[self.current_state_name].keys())
            probabilities = list(self.transition_probabilities[self.current_state_name].values())
            self.current_state_name = np.random.choice(states, p=probabilities)
    
    def set_state(self, new_state):
        if new_state not in self.transition_probabilities:
            raise ValueError(f"State '{new_state}' is not valid")
        self.current_state_name = new_state
        self.remaining_hours = self.holding_times[new_state]
    
    def current_state_remaining_hours(self):
        return self.remaining_hours
    
    def iterable(self):
        while True:
            yield self.current_state()
            self.next_state()
    
    def simulate(self, hours):
        state_counts = {state: 0 for state in self.transition_probabilities.keys()}
        for _ in range(hours):
            state_counts[self.current_state_name] += 1
            self.next_state()
        
        total = sum(state_counts.values())
        return [state_counts[state] / total * 100 for state in self.get_states()]

