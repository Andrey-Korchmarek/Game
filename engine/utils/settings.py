class StateManager:
    def __init__(self):
        self.states = {}  # Словарь состояний
        self.current_state = None

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def change_state(self, state_name):
        if self.current_state:
            self.current_state.exit()

        self.current_state = self.states[state_name]
        self.current_state.enter()

    def update(self, delta_time):
        if self.current_state:
            self.current_state.update(delta_time)

    def render(self):
        if self.current_state:
            self.current_state.render()