import numpy as np
import matplotlib.pyplot as plt
from bandits import Bandit
from agents import *

def evaluate_agents(agents, bandit, steps=1000):
    reward_history = np.zeros((len(agents), steps))
    regret_history = np.zeros((len(agents), steps))
    
    for idx, agent in enumerate(agents):
        cumulative_reward = 0
        for t in range(steps):
            reward = agent.act()
            cumulative_reward += reward
            reward_history[idx, t] = reward
            regret_history[idx, t] = bandit.get_regret()
        bandit.reset_regret()  # Reset the bandit's regret for the next agent

    return reward_history, regret_history

def plot_agent_performance(reward_history, regret_history, agent_names):
    # Plotting reward per step
    plt.figure(figsize=(12, 6))
    for i, agent_name in enumerate(agent_names):
        plt.plot(reward_history[i], label=agent_name)
    plt.xlabel('Steps')
    plt.ylabel('Reward per Step')
    plt.title('Comparison of Rewards per Step Across Agents')
    plt.legend()
    plt.savefig("reward_comparison.png")
    plt.show()

    # Plotting accumulated regret
    plt.figure(figsize=(12, 6))
    for i, agent_name in enumerate(agent_names):
        plt.plot(regret_history[i], label=agent_name)
    plt.xlabel('Steps')
    plt.ylabel('Cumulative Regret')
    plt.title('Comparison of Cumulative Regret Across Agents')
    plt.legend()
    plt.savefig("regret_comparison.png")
    plt.show()

# Test setup
num_bandits = 10
bandit = Bandit(num_bandits, "Bernoulli")

# Instantiate agents
greedy_agent = GreedyAgent(bandit, initial_value=1.0)
epsilon_greedy_agent = EpsilonGreedyAgent(bandit, epsilon=0.1)
ucb_agent = UCBAgent(bandit, exploration_param=2)
gradient_agent = GradientBanditAgent(bandit, learning_rate=0.1)
thompson_agent = ThompsonSamplingAgent(bandit)

# Collect agents into a list
agents = [greedy_agent, epsilon_greedy_agent, ucb_agent, gradient_agent, thompson_agent]
agent_names = [type(agent).__name__ for agent in agents]

# Evaluate and plot results
reward_history, regret_history = evaluate_agents(agents, bandit, steps=1000)
plot_agent_performance(reward_history, regret_history, agent_names)
