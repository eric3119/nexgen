#!/usr/bin/env python
"""
    Main training workflow
"""

import configargparse
import os
import signal
import torch

import onmt.opts as opts

from onmt.bin.train import main


if __name__ == "__main__":
    parser = configargparse.ArgumentParser(
        description='train.py',
        config_file_parser_class=configargparse.YAMLConfigFileParser,
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter)

    # opts.config_opts(parser)
    # opts.add_md_help_argument(parser)
    # opts.model_opts(parser)
    # opts.train_opts(parser)

    opt = parser.parse_args()
    main(opt)