#!/usr/bin/env python3


import asyncio
import builtins
import sys

import rich
import typer
import time

from srcwarnings.api import get_project_warnings, project_has_finished_processing

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
        help="URL of the Watchdog API"
    ),
    api_key: str = typer.Option(..., envvar="WD_API_KEY", help="Watchdog API key"),
):
    asyncio.run(warnings_thread(api_url, api_key, project_id, version_id, period, timeout))


async def warnings_thread(api_url: str, api_key: str, project_id: int, version_id: int, period: int, timeout: int):
    try:
        start_time = time.time()
        analysis_has_finished = await project_has_finished_processing(api_url, api_key, project_id, version_id)
        while time.time() - start_time < timeout and not analysis_has_finished:
            time.sleep(period)
            analysis_has_finished = await project_has_finished_processing(api_url, api_key, project_id, version_id)

        if analysis_has_finished:
            print(await get_project_warnings(api_url, api_key, project_id, version_id))
        else:
            print("Timeout while waiting for project analysis to finish.")
            sys.exit(-1)
    except Exception as e:
        print(f"Could not retrieve information: {e}")
        sys.exit(-1)
