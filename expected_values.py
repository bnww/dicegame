"""Expected values policy"""
import time
import copy
import statistics

class Expected_Values(DiceGameAgent):
    def __init__(self, game):
        # this calls the superclass constructor (does self.game = game)
        super().__init__(game)
        #print(f"Dice: {self.game._dice}, Sides:{self.game._sides}, Values:{self.game._values}, Bias:{self.game._bias}, Penalty:{self.game._penalty}")

        self.reset()
        
    def reset(self):
        self.hold_all = tuple(_ for _ in range(self.game._dice))
        self.number_actions = 0
        self.action_expectation = {}
            
    def find_expected_value(self, state, action):
        rolls, game_over, self.rewards, probabilities = self.game.get_next_states(action, (state))
        
        possible_scores = []
        for roll in rolls:
            possible_scores.append(float(self.game.final_scores[roll] + (self.rewards * self.number_actions)))
                                       
        return sum(score * probability for score, probability in zip(possible_scores, probabilities))
        
    def play(self, state):
        self.number_actions += 1
        for action in self.game.actions:
            # if expectation value for rolling all dice has already been calculated,
            # instead of running it again, just add on the reward
            if action == () and action in self.action_expectation.keys():
                self.action_expectation[action] += self.rewards
                continue
            if action == self.hold_all:
                # skip when action is to hold all dice
                continue
            expected_value = self.find_expected_value(state, action)
            self.action_expectation[action] = expected_value
        
        current_score = self.game.final_score(state) + (self.rewards * (self.number_actions - 1))
        
        self.action_expectation[self.hold_all] = current_score

        best_action = max(self.action_expectation, key = self.action_expectation.get)
        
        if best_action == self.hold_all:
            self.reset()
            
        return best_action