#!/usr/bin/env python3

from srcwarnings.cli import app
from srcwarnings.utils import create_config_dir, load_envfile


def main():
    create_config_dir()
    load_envfile()
    app()


if __name__ == "__main__":
    main()
