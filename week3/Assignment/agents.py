from bandits import Bandit
import random
import math
import numpy as np

class Agent:
    def __init__(self, bandit: Bandit) -> None:
        self.bandit = bandit
        self.num_actions = bandit.getN()

        self.total_reward = 0
        self.iterations = 0
    
    def choose_action(self) -> int:
        '''This method should be overridden to define the action selection strategy.'''
        raise NotImplementedError()

    def update_policy(self, action: int, reward: int) -> None:
        '''This method should be overridden to define the policy update after receiving a reward.'''
        raise NotImplementedError()

    def act(self) -> int:
        action = self.choose_action()
        reward = self.bandit.choose(action)

        self.total_reward += reward
        self.iterations += 1

        self.update_policy(action, reward)
        return reward

class GreedyAgent(Agent):
    def __init__(self, bandit: Bandit, initial_value: float) -> None:
        super().__init__(bandit)
        self.q_estimates = [initial_value] * self.num_actions
        self.action_count = [0] * self.num_actions

    def choose_action(self) -> int:
        return np.argmax(self.q_estimates)

    def update_policy(self, action: int, reward: int) -> None:
        self.action_count[action] += 1
        self.q_estimates[action] += (reward - self.q_estimates[action]) / self.action_count[action]

class EpsilonGreedyAgent(Agent):
    def __init__(self, bandit: Bandit, epsilon: float) -> None:
        super().__init__(bandit)
        self.epsilon = epsilon
        self.q_estimates = [0.0] * self.num_actions
        self.action_count = [0] * self.num_actions
    
    def choose_action(self) -> int:
        if random.random() < self.epsilon:
            return random.randint(0, self.num_actions - 1)
        else:
            return np.argmax(self.q_estimates)

    def update_policy(self, action: int, reward: int) -> None:
        self.action_count[action] += 1
        self.q_estimates[action] += (reward - self.q_estimates[action]) / self.action_count[action]

class UCBAgent(Agent):
    def __init__(self, bandit: Bandit, exploration_param: float) -> None:
        super().__init__(bandit)
        self.c = exploration_param
        self.q_estimates = [0.0] * self.num_actions
        self.action_count = [0] * self.num_actions

    def choose_action(self) -> int:
        for i in range(self.num_actions):
            if self.action_count[i] == 0:
                return i
        ucb_values = [self.q_estimates[i] + self.c * math.sqrt(math.log(self.iterations + 1) / self.action_count[i]) for i in range(self.num_actions)]
        return np.argmax(ucb_values)

    def update_policy(self, action: int, reward: int) -> None:
        self.action_count[action] += 1
        self.q_estimates[action] += (reward - self.q_estimates[action]) / self.action_count[action]

class GradientBanditAgent(Agent):
    def __init__(self, bandit: Bandit, learning_rate: float) -> None:
        super().__init__(bandit)
        self.alpha = learning_rate
        self.preferences = [0.0] * self.num_actions
        self.avg_reward = 0.0

    def choose_action(self) -> int:
        exp_preferences = np.exp(self.preferences)
        action_probabilities = exp_preferences / np.sum(exp_preferences)
        return np.random.choice(range(self.num_actions), p=action_probabilities)

    def update_policy(self, action: int, reward: int) -> None:
        self.avg_reward += (reward - self.avg_reward) / (self.iterations + 1)
        exp_preferences = np.exp(self.preferences)
        action_probabilities = exp_preferences / np.sum(exp_preferences)
        for i in range(self.num_actions):
            if i == action:
                self.preferences[i] += self.alpha * (reward - self.avg_reward) * (1 - action_probabilities[i])
            else:
                self.preferences[i] -= self.alpha * (reward - self.avg_reward) * action_probabilities[i]

class ThompsonSamplingAgent(Agent):
    def __init__(self, bandit: Bandit) -> None:
        super().__init__(bandit)
        self.successes = [1] * self.num_actions
        self.failures = [1] * self.num_actions

    def choose_action(self) -> int:
        sampled_theta = [np.random.beta(self.successes[i], self.failures[i]) for i in range(self.num_actions)]
        return np.argmax(sampled_theta)

    def update_policy(self, action: int, reward: int) -> None:
        if reward > 0:
            self.successes[action] += 1
        else:
            self.failures[action] += 1
