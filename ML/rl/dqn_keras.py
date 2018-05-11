#!/usr/bin/env python

import numpy as np
import gym
import gym_banana

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.memory import EpisodeParameterMemory


def main(env_name, nb_steps):
    # Get the environment and extract the number of actions.
    env = gym.make(env_name)
    np.random.seed(123)
    env.seed(123)

    nb_actions = env.action_space.n
    input_shape = (1,) + env.observation_space.shape
    model = create_nn_model(input_shape, nb_actions)

    # Finally, we configure and compile our agent.
    memory = EpisodeParameterMemory(limit=10000, window_length=1)

    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1.,
                                  value_min=.1, value_test=.05,
                                  nb_steps=1000000)
    agent = DQNAgent(model=model, nb_actions=nb_actions, policy=policy,
                     memory=memory, nb_steps_warmup=1000000,
                     gamma=.99, target_model_update=1000,
                     train_interval=4, delta_clip=1.)
    agent.compile(Adam(lr=.00025), metrics=['mae'])
    agent.fit(env, nb_steps=nb_steps, visualize=False, verbose=1)

    # After training is done, we save the best weights.
    agent.save_weights('dqn_{}_params.h5f'.format(env_name), overwrite=True)

    # Finally, evaluate the agent
    history = agent.test(env, nb_episodes=100, visualize=False)
    rewards = np.array(history.history['episode_reward'])
    print(("Test rewards (#episodes={}): mean={:>5.2f}, std={:>5.2f}, "
           "min={:>5.2f}, max={:>5.2f}")
          .format(len(rewards),
                  rewards.mean(),
                  rewards.std(),
                  rewards.min(),
                  rewards.max()))


def create_nn_model(input_shape, nb_actions):
    """
    Create a neural network model which maps the input to actions.

    Parameters
    ----------
    input_shape : tuple of int
    nb_actoins : int

    Returns
    -------
    model : keras Model object
    """
    model = Sequential()
    if len(input_shape) == 3:
        model.add(Flatten(input_shape=input_shape))
        model.add(Dense(32))
    else:
        model.add(Dense(32, input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    print(model.summary())
    return model


def get_parser():
    """Get parser object."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--env",
                        dest="environment",
                        help="OpenAI Gym environment",
                        metavar="ENVIRONMENT",
                        default="CartPole-v0")
    parser.add_argument("--steps",
                        dest="steps",
                        default=10000,
                        type=int,
                        help="how steps are trained?")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.environment, args.steps)
