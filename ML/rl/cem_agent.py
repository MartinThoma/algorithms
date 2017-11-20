#!/usr/bin/env python

import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten

from rl.agents.cem import CEMAgent
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
    memory = EpisodeParameterMemory(limit=450, window_length=1)

    agent = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
                     batch_size=50, nb_steps_warmup=2000, train_interval=50,
                     elite_frac=0.05)
    agent.compile()
    agent.fit(env, nb_steps=nb_steps, visualize=False, verbose=1)

    # After training is done, we save the best weights.
    agent.save_weights('cem_{}_params.h5f'.format(env_name), overwrite=True)

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
        model.add(Dense(16))
    else:
        model.add(Dense(16, input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('softmax'))
    print(model.summary())
    return model


def get_parser():
    """Get parser object for script xy.py."""
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
