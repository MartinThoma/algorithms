#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Agent playing random actions."""

# core modules
import logging
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


class RandomAgent:
    """
    Random Agent.

    Parameters
    ----------
    cfg : dict
    """

    def __init__(self, cfg, state_size, action_size):
        self.env = cfg['env']
        self.episode = 0

    def remember(self, state, action, reward, next_state, done):
        pass  # Dummy method

    def reset(self):
        """Reset the agent. Call this at the beginning of an episode."""
        self.episode += 1

    def act(self, state, no_exploration=False):
        return self.env.action_space.sample()

    def save(self, name):
        """Serialize an agent."""
        return self

    def load(self, name):
        """Load an agent."""
        return self


def load_agent(cfg, env):
    """
    Create (and load) a QTableAgent.

    Parameters
    ----------
    cfg : dict
    env : OpenAI environment
    """
    agent = RandomAgent(cfg,
                        env.observation_space.shape[0],
                        env.action_space.n)
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
