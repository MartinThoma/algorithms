#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Q-Table Reinforcement Learning agent."""

# core modules
import logging
import os
import pickle
import sys
import yaml

# 3rd party modules
import gym
import numpy as np

np.random.seed(280490)

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


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
    print("Trained epochs: {}".format(agent.epoch))


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
        self.epoch = 0

    def reset(self):
        self.epoch += 1

    def act(self, observation, no_exploration=False):
        """
        Decide which action to execute.

        Parameters
        ----------
        observation : int
        no_exploration : bool, optional (default: False)
        """
        assert self.epoch >= 1, "Reset before you run an episode."
        if no_exploration:
            noise = np.zeros((1, self.nb_act))
        else:
            f = self.epoch // 2 + 1
            noise = np.random.randn(1, self.nb_act) * (1.0 / f)
        action = np.argmax(self.Q[observation, :] + noise)
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
        gradient = (
            reward + self.gamma * np.max(self.Q[state, :]) -
            self.Q[prev_state, action]
        )
        self.Q[prev_state, action] += self.lr * gradient
        return self

    def save(self, path):
        """Serialize an agent."""
        data = {'Q': self.Q,
                'epoch': self.epoch}
        with open(path, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return self

    def load(self, path):
        """Load an agent."""
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
            self.Q = data['Q']
            self.epoch = data['epoch']
        return self


def load_agent(cfg, env):
    """Create (and load) a QTableAgent."""
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
    cum_rewards = 0.0
    for episode in range(cfg['training']['nb_epochs']):
        agent.reset()
        observation_previous = env.reset()
        is_done = False
        while not is_done:
            action = agent.act(observation_previous)
            observation, reward, is_done, _ = env.step(action)
            cum_rewards += reward
            agent.remember(observation_previous, action, reward, observation,
                           is_done)
            observation_previous = observation
        agent.save(cfg['serialize_path'])
        if episode % cfg['training']['print_score'] == 0 and episode > 0:
            print("Average score: {:>5.2f}"
                  .format(cum_rewards / (episode + 1)))
    agent.save(cfg['serialize_path'])
    return agent


def test_agent(cfg, env, agent):
    """Calculate average reward."""
    cum_reward = 0.0
    for epoch in range(cfg['testing']['nb_epochs']):
        agent.reset()
        observation_previous = env.reset()
        while True:
            action = agent.act(observation_previous, no_exploration=True)
            observation, reward, is_done, _ = env.step(action)
            cum_reward += reward
            observation_previous = observation
            if is_done:
                env.close()
                break
    return cum_reward / cfg['testing']['nb_epochs']


# General code for loading ML configuration files
def load_cfg(yaml_filepath):
    """
    Load a YAML configuration file.

    Parameters
    ----------
    yaml_filepath : str

    Returns
    -------
    cfg : dict
    """
    # Read YAML experiment definition file
    with open(yaml_filepath, 'r') as stream:
        cfg = yaml.load(stream)
    cfg = make_paths_absolute(os.path.dirname(yaml_filepath), cfg)
    return cfg


def make_paths_absolute(dir_, cfg):
    """
    Make all values for keys ending with `_path` absolute to dir_.

    Parameters
    ----------
    dir_ : str
    cfg : dict

    Returns
    -------
    cfg : dict
    """
    for key in cfg.keys():
        if key.endswith("_path"):
            cfg[key] = os.path.join(dir_, cfg[key])
            cfg[key] = os.path.abspath(cfg[key])
            if not os.path.isfile(cfg[key]):
                logging.error("%s does not exist.", cfg[key])
        if type(cfg[key]) is dict:
            cfg[key] = make_paths_absolute(dir_, cfg[key])
    return cfg


def get_parser():
    """Get parser object."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--env",
                        dest="environment_name",
                        help="OpenAI Gym environment",
                        metavar="ENVIRONMENT",
                        default="FrozenLake-v0")
    parser.add_argument("--agent",
                        dest="agent_cfg_file",
                        required=True,
                        metavar="AGENT_YAML",
                        help="Configuration file for the agent")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.environment_name, args.agent_cfg_file)
