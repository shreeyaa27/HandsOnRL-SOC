from bandits import Bandit
# Import libraries if you need them

class Agent:
    def __init__(self, bandit: Bandit) -> None:
        self.bandit = bandit
        self.banditN = bandit.getN()

        self.rewards = 0
        self.numiters = 0
    

    def action(self) -> int:
        '''This function returns which action is to be taken. It must be implemented in the subclasses.'''
        raise NotImplementedError()

    def update(self, choice : int, reward : int) -> None:
        '''This function updates all member variables you may require. It must be implemented in the subclasses.'''
        raise NotImplementedError()

    # dont edit this function
    def act(self) -> int:
        choice = self.action()
        reward = self.bandit.choose(choice)

        self.rewards += reward
        self.numiters += 1

        self.update(choice,reward)
        return reward
class GreedyAgent(Agent):
    def __init__(self, bandits: Bandit, initialQ: float) -> None:
        super().__init__(bandits)
        self.q_values = np.full(self.banditN, initialQ)  # Initialize Q values
        self.action_counts = np.zeros(self.banditN)  # Track counts of each action

    def action(self) -> int:
        return np.argmax(self.q_values)

    def update(self, choice: int, reward: int) -> None:
        self.action_counts[choice] += 1
        alpha = 1.0 / self.action_counts[choice]
        self.q_values[choice] += alpha * (reward - self.q_values[choice])

# class GreedyAgent(Agent):
#     def __init__(self, bandits: Bandit, initialQ : float) -> None:
#         super().__init__(bandits)
#         # add any member variables you may require
        
#     # implement
#     def action(self) -> int:
#         pass

#     # implement
#     def update(self, choice: int, reward: int) -> None:
#         pass
class epsGreedyAgent(Agent):
    def __init__(self, bandits: Bandit, epsilon: float) -> None:
        super().__init__(bandits)
        self.epsilon = epsilon
        self.q_values = np.zeros(self.banditN)
        self.action_counts = np.zeros(self.banditN)

    def action(self) -> int:
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.banditN)
        else:
            return np.argmax(self.q_values)

    def update(self, choice: int, reward: int) -> None:
        self.action_counts[choice] += 1
        alpha = 1.0 / self.action_counts[choice]
        self.q_values[choice] += alpha * (reward - self.q_values[choice])

# class epsGreedyAgent(Agent):
#     def __init__(self, bandits: Bandit, epsilon : float) -> None:
#         super().__init__(bandits)
#         self.epsilon = epsilon
#         # add any member variables you may require
    
#     # implement
#     def action(self) -> int:
#         pass

#     # implement
#     def update(self, choice: int, reward: int) -> None:
#         pass
class UCBAAgent(Agent):
    def __init__(self, bandits: Bandit, c: float) -> None:
        super().__init__(bandits)
        self.c = c
        self.q_values = np.zeros(self.banditN)
        self.action_counts = np.zeros(self.banditN)

    def action(self) -> int:
        total_counts = np.sum(self.action_counts)
        if total_counts < self.banditN:
            return np.argmin(self.action_counts)
        ucb_values = self.q_values + self.c * np.sqrt(np.log(total_counts) / (self.action_counts + 1))
        return np.argmax(ucb_values)

    def update(self, choice: int, reward: int) -> None:
        self.action_counts[choice] += 1
        alpha = 1.0 / self.action_counts[choice]
        self.q_values[choice] += alpha * (reward - self.q_values[choice])

# class UCBAAgent(Agent):
#     def __init__(self, bandits: Bandit, c: float) -> None:
#         super().__init__(bandits)
#         self.c = c
#         # add any member variables you may require

#     # implement
#     def action(self) -> int:
#         pass

#     # implement
#     def update(self, choice: int, reward: int) -> None:
#         pass
class GradientBanditAgent(Agent):
    def __init__(self, bandits: Bandit, alpha: float) -> None:
        super().__init__(bandits)
        self.alpha = alpha
        self.preferences = np.zeros(self.banditN)
        self.avg_reward = 0

    def action(self) -> int:
        exp_preferences = np.exp(self.preferences - np.max(self.preferences))
        self.action_probabilities = exp_preferences / np.sum(exp_preferences)
        return np.random.choice(self.banditN, p=self.action_probabilities)

    def update(self, choice: int, reward: int) -> None:
        self.avg_reward += (reward - self.avg_reward) / self.numiters
        self.preferences[choice] += self.alpha * (reward - self.avg_reward) * (1 - self.action_probabilities[choice])
        for i in range(self.banditN):
            if i != choice:
                self.preferences[i] -= self.alpha * (reward - self.avg_reward) * self.action_probabilities[i]

# class GradientBanditAgent(Agent):
#     def __init__(self, bandits: Bandit, alpha : float) -> None:
#         super().__init__(bandits)
#         self.alpha = alpha
#         # add any member variables you may require

#     # implement
#     def action(self) -> int:
#         pass

#     # implement
#     def update(self, choice: int, reward: int) -> None:
#         pass
class ThompsonSamplerAgent(Agent):
    def __init__(self, bandits: Bandit) -> None:
        super().__init__(bandits)
        self.successes = np.zeros(self.banditN)
        self.failures = np.zeros(self.banditN)

    def action(self) -> int:
        sampled_values = np.random.beta(1 + self.successes, 1 + self.failures)
        return np.argmax(sampled_values)

    def update(self, choice: int, reward: int) -> None:
        if reward == 1:
            self.successes[choice] += 1
        else:
            self.failures[choice] += 1

# class ThompsonSamplerAgent(Agent):
#     def __init__(self, bandits: Bandit) -> None:
#         super().__init__(bandits)
#         # add any member variables you may require

#     # implement
#     def action(self) -> int:
#         pass

#     # implement
#     def update(self, choice: int, reward: int) -> None:
#         pass

# Implement other subclasses if you want to try other strategies