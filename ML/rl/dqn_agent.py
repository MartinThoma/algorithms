#!/usr/bin/env python

"""
Deep Q-Learning agent.

This was initially taken from
https://github.com/keon/deep-q-learning/blob/master/dqn.py and
refactored quite a bit.
"""

import logging
import os
import random
import sys
# core modules
from collections import deque

import gym
import numpy as np
# 3rd party modules
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
# local modules
from rl_utils import get_parser, load_cfg, test_agent

np.random.seed(280490)

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
np.set_printoptions(formatter={'float_kind': lambda x: f"{x:>5.2f}"})


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
    print(f"Average reward: {rewards:5.3f}")
    print(f"Trained episodes: {agent.episode}")


class DQNAgent:
    """
    DQN Agent.

    Parameters
    ----------
    cfg : dict
    """

    def __init__(self, cfg, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=cfg['memory']['length'])
        self.gamma = cfg['problem']['gamma']    # discount rate
        self.epsilon = cfg['training']['exploration']['epsilon']
        self.epsilon_min = cfg['training']['exploration']['epsilon_min']
        self.epsilon_decay = cfg['training']['exploration']['epsilon_decay']
        self.learning_rate = cfg['training']['learning_rate']
        self.model = self._build_model()

        self.episode = 0

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(50, input_dim=self.state_size, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        state = self._preprocess_state(state)
        next_state = self._preprocess_state(state)
        self.memory.append((state, action, reward, next_state, done))

    def reset(self):
        """Reset the agent. Call this at the beginning of an episode."""
        self.episode += 1

    def act(self, state, no_exploration=False):
        state = self._preprocess_state(state)
        if not no_exploration and np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def _preprocess_state(self, state):
        state = np.reshape(state, [1, self.state_size])
        return state

    def save(self, name):
        """Serialize an agent."""
        self.model.save_weights(name)
        return self

    def load(self, name):
        """Load an agent."""
        self.model.load_weights(name)
        return self


def load_agent(cfg, env):
    """
    Create (and load) a QTableAgent.

    Parameters
    ----------
    cfg : dict
    env : OpenAI environment
    """
    agent = DQNAgent(cfg, env.observation_space.shape[0], env.action_space.n)
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
        if len(agent.memory) > cfg['training']['batch_size']:
            agent.replay(cfg['training']['batch_size'])
    agent.save(cfg['serialize_path'])
    return agent


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.environment_name, args.agent_cfg_file)
