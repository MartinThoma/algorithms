#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility functions for Reinforcement Learning."""

# core modules
import logging
import os

# 3rd party modules
import yaml


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


def test_agent(cfg, env, agent):
    """Calculate average reward."""
    cum_reward = 0.0
    for episode in range(cfg['testing']['nb_epochs']):
        agent.reset()
        observation_previous = env.reset()
        is_done = False
        while not is_done:
            action = agent.act(observation_previous, no_exploration=True)
            observation, reward, is_done, _ = env.step(action)
            cum_reward += reward
            observation_previous = observation
    return cum_reward / cfg['testing']['nb_epochs']


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
