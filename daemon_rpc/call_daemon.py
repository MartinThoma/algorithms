#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Talk with the daemon."""

import logging
import sys
import Pyro.core

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(up):
    """Do something with bartimaeus - who lives in another realm."""
    # you have to change the URI below to match your own host/port.
    logging.info("Send up: %i", up)
    bartimaeus = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/bartid")
    print(bartimaeus.count(up))


def get_parser():
    """Get parser object for call_demon.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n",
                        dest="up",
                        default=1,
                        type=int,
                        help="count up")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.up)
