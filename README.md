# Watchdog srcwarnings

`srcwarnings` is Dedaub's utility CLI for retrieving a summary of your warnings from a project you previously uploaded
using `srcup` (see https://github.com/Dedaub/srcup).

## Installation

**NOTE**: While `pipx` is not required, it's highly recommended to use it instead of `pip` to ensure our
CLI tool is run in an isolated/clean environment.

1. [Optional] [Install pipx](https://pypa.github.io/pipx/). This is **recommended**.
2. Install the CLI tool: `pipx install git+ssh://github.com/Dedaub/srcwarnings#egg=srcwarnings`
3. Test the installation: `srcwarnings --help`
4. [Optional] Install the CLI completions: `srcwarnings --install-completion`


## Upgrading

### For pipx installation
```bash
pipx upgrade srcwarnings
```

### For plain pip installation
```bash
pip install --upgrade git+ssh://github.com/Dedaub/srcwarnings#egg=srcwarnings
```

## Usage

The following steps assumes you've acquired/generated a Watchdog API key. This can be done from your Watchdog
profile page (top right corner of the UI, top right button in the header of that page).

To upload the sources of a project:
1. Run `srcwarnings --api-key <api_key> --project-id <project-id> --version-id <version-id>` where `<project-id>`
and `<version-id>` are the values returned by `srcup`

2. You can also define two optional parameters: `--timeout <timeout>` and `--period <period>` where `timeout`
is the maximum time in seconds to wait for analysis to finish and `period` is the polling period to check whether analysis has fniished.

## Storing the API key

It is possible to store the API key in a file to make future `srcwarnings` invocations simpler. The API key can be stored
in the following places:
- As a standard environment variable in your shell's RC file.
- In `~/.config/dedaub/credentials`

In both cases, the environment variable defintion should be `WD_API_KEY=<api_key>`.
