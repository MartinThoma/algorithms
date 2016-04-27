#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A chat client."""

import logging
import sys
import Pyro.core

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(server, name):
    """Run the chat."""
    chat_server = Pyro.core.getProxyForURI(server)
    last_msg_id = 0
    print("*"*80)
    print("* Chat started. You are called '{name}'.".format(name=name))
    print("*"*80)
    while True:
        msg = raw_input()
        new_msgs, last_msg_id = chat_server.receive(name, msg, last_msg_id)
        for sender, msg in new_msgs:
            print("[{sender}] {msg}".format(sender=sender, msg=msg))


def get_parser():
    """Get parser object for chat_client.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--server",
                        dest="server",
                        required=True,
                        help="starts with PYRO://")
    parser.add_argument("--name",
                        required=True,
                        help="what others see")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.server, args.name)
