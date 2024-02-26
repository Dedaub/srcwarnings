#!/usr/bin/env python3

import asyncio
import builtins
import sys

import rich
import time
import typer

from packaging import version

from srcwarnings.api import get_project_warnings, project_has_finished_processing
from srcwarnings.utils import get_latest_app_version, version_callback, __version__

app = typer.Typer()
builtins.print = rich.print  # type: ignore


@app.command()
def single(
    project_id: int = typer.Option('', help="The id of the project for which we want to retrieve warnings"),
    version_id: int = typer.Option('', help="The id of the version for which we want to retrieve warnings"),
    timeout: int = typer.Option(300, help="Max wait period for the project to be analysed"),
    period: int = typer.Option(30, help="Wait period for rechecking if project analysis has concluded"),
    api_url: str = typer.Option(
          "https://api.dedaub.com/api",
        help="URL of the Dedaub API"
    ),
    api_key: str = typer.Option(..., envvar="WD_API_KEY", help="Dedaub API key"),
    app_version: bool = typer.Option(False, '--version', '-v', help="Show the version of the app", is_eager=True, callback=version_callback)
):
    latest_app_version = asyncio.run(get_latest_app_version())
    if not latest_app_version:
        print("Warning: Failed to retrieve the latest available version of the app")

    elif version.parse(__version__) < version.parse(latest_app_version):
        print(f'Notice: A new version is available: {__version__} -> {latest_app_version}\n')
        print(f'Please, update the app to continue:')
        print(f'  For pipx installation run:      pipx upgrade srcwarnings')
        print(f'  For plain pip installation run: pip install --upgrade git+ssh://github.com/Dedaub/srcwarnings#egg=srcwarnings')
        return

    asyncio.run(warnings_thread(api_url, api_key, project_id, version_id, period, timeout))


async def warnings_thread(api_url: str, api_key: str, project_id: int, version_id: int, period: int, timeout: int):
    try:
        start_time = time.time()
        total, failures, analysis_has_finished = await project_has_finished_processing(api_url, api_key, project_id, version_id)
        while time.time() - start_time < timeout and not analysis_has_finished:
            time.sleep(period)
            total, failures, analysis_has_finished = await project_has_finished_processing(api_url, api_key, project_id, version_id)

        print(f"NOTE: {failures} contract(s) out of {total} failed to be analysed")

        if analysis_has_finished:
            print(await get_project_warnings(api_url, api_key, project_id, version_id))
        else:
            print("Timeout while waiting for project analysis to finish.")
            sys.exit(-1)
    except Exception as e:
        print(f"Could not retrieve information: {e}")
        sys.exit(-1)
