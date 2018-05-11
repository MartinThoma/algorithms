#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Q-Table Reinforcement Learning agent."""

# core modules
import logging
import os
import pickle
import sys

# 3rd party modules
import gym
import numpy as np

# local modules
from rl_utils import get_parser, load_cfg, test_agent

np.random.seed(280490)

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
np.set_printoptions(formatter={'float_kind': lambda x: "{:>5.2f}".format(x)})


def main(environment_name, agent_cfg_file):
    """
    Load, train and evaluate a Reinforcment Learning agent.

    Parameters
    ----------
    environment_name : str
    agent_cfg_file : str
    """
    cfg = load_cfg(agent_cfg_file)

    # Set up environment and agent
    env = gym.make(environment_name)
    cfg['env'] = env
    cfg['serialize_path'] = ('artifacts/{}-{}.pickle'
                             .format(cfg['model_name'], environment_name))
    agent = load_agent(cfg, env)

    agent = train_agent(cfg, env, agent)
    rewards = test_agent(cfg, env, agent)
    print("Average reward: {:5.3f}".format(rewards))
    print("Trained episodes: {}".format(agent.episode))


class QTableAgent:
    """
    Q-Table Agent.

    Parameters
    ----------
    cfg : dict
    """

    def __init__(self, agent_cfg, nb_observations, nb_actions):
        self.nb_obs = nb_observations
        self.nb_act = nb_actions
        self.Q = np.zeros([nb_observations, nb_actions])
        self.lr = agent_cfg['training']['learning_rate']
        self.gamma = agent_cfg['problem']['gamma']  # discount
        self.episode = 0
        self.exploration = agent_cfg['training']['exploration']

    def reset(self):
        """Reset the agent. Call this at the beginning of an episode."""
        self.episode += 1

    def act(self, observation, no_exploration=False):
        """
        Decide which action to execute.

        Parameters
        ----------
        observation : int
        no_exploration : bool, optional (default: False)

        Returns
        -------
        action : int
        """
        assert self.episode >= 1, "Reset before you run an episode."
        action = np.argmax(self.Q[observation, :])
        if not no_exploration:
            if self.exploration['name'] == 'epsilon-greedy':
                if np.random.uniform() < self.exploration['epsilon']:
                    action = np.random.random_integers(0, self.nb_act - 1)
            elif self.exploration['name'] == 'Boltzmann':
                T = 1
                clip = self.exploration['clip']
                q_values = self.Q[observation, :].astype('float64')
                q_values = np.clip(q_values / T, clip[0], clip[1])
                exp_values = np.exp(q_values)
                probs = exp_values / np.sum(exp_values)
                action = np.random.choice(range(self.nb_act), p=probs)
            else:
                raise NotImplemented(self.exploration['name'])
        return action

    def remember(self, prev_state, action, reward, state, is_done):
        """
        Store data in the Q-Table. Here, the learning happens.

        Parameters
        ----------
        prev_state : int
        action : int
        reward : float
        state : int
        """
        delta = reward - self.Q[prev_state, action]
        if not is_done:
            delta += self.gamma * np.max(self.Q[state, :])
        self.Q[prev_state, action] += self.lr * delta
        return self

    def save(self, path):
        """Serialize an agent."""
        data = {'Q': self.Q,
                'episode': self.episode}
        with open(path, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return self

    def load(self, path):
        """Load an agent."""
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
            self.Q = data['Q']
            self.episode = data['episode']
        return self


def load_agent(cfg, env):
    """
    Create (and load) a QTableAgent.

    Parameters
    ----------
    cfg : dict
    env : OpenAI environment
    """
    agent = QTableAgent(cfg, env.observation_space.n, env.action_space.n)
    if os.path.isfile(cfg['serialize_path']):
        agent.load(cfg['serialize_path'])
    return agent


# General training and testing code
def train_agent(cfg, env, agent):
    """
    Train an agent in environment.

    Parameters
    ----------
    cfg : dict
    env : OpenAI environment
    agent : object

    Return
    ------
    agent : object
    """
    rewards = []
    window_size = cfg['training']['print_window_size']
    max_episode_length = cfg['training']['max_episode_length']
    for episode in range(cfg['training']['nb_episodes']):
        agent.reset()
        observation_previous = env.reset()
        is_done = False
        time = 0
        while not (time >= max_episode_length) and not is_done:
            action = agent.act(observation_previous)
            observation, reward, is_done, _ = env.step(action)
            rewards.append(reward)
            agent.remember(observation_previous, action, reward, observation,
                           is_done)
            observation_previous = observation
            time += 1
        if episode % cfg['training']['print_score'] == 0 and episode > 0:
            agent.save(cfg['serialize_path'])
            print("Average score: {:>5.2f}"
                  .format(sum(rewards[-window_size:]) / window_size))
    agent.save(cfg['serialize_path'])
    return agent


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.environment_name, args.agent_cfg_file)
