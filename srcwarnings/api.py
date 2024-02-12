#!/usr/bin/env python3
import aiohttp

from srcwarnings.models import Confidence, Severity

HEADER = "You have {} warnings in your project.\n"
REPORT_TEMPLATE = "* {} {} warning(s). ({} with MEDIUM PLUS or higher confidence and MEDIUM or higher severity)"
FOOTER = "\nSee https://app.dedaub.com/projects/{}_{} for detailed information"


async def project_has_finished_processing(
        watchdog_api: str,
        api_key: str,
        project_id: int,
        version_id: int
) -> bool:
    async with aiohttp.ClientSession(
            headers={"x-api-key": api_key}, json_serialize=lambda x: x.json()
    ) as session:

        url = f"{watchdog_api}/project/{project_id}/version/{version_id}/stats"

        req = await session.get(
            url=url)

        if req.status == 200:
            stats = await req.json()
            return not list(filter(lambda x: x['stage'] != 'COMPLETED' or x['success'] is False, stats))
        else:
            error = await req.text()
            raise Exception(error)


async def get_project_warnings(
        watchdog_api: str,
        api_key: str,
        project_id: int,
        version_id: int
) -> str:
    async with aiohttp.ClientSession(
            headers={"x-api-key": api_key}, json_serialize=lambda x: x.json()
    ) as session:

        url = f"{watchdog_api}/project/{project_id}/version/{version_id}/warnings"

        req = await session.get(
            url=url)

        if req.status == 200:
            warnings = await req.json()
            return await generate_warning_report(warnings, project_id, version_id)
        else:
            error = await req.text()
            raise Exception(error)


async def generate_warning_report(warnings, project_id, version_id):

    warning_kinds = set(map(lambda x: x['kind'], warnings))

    report = []
    for kind in warning_kinds:
        warnings_per_kind = len(list(filter(lambda x: x['kind'] == kind, warnings)))
        serious_warnings_per_kind = len(
            list(filter(lambda x: x['kind'] == kind
                        and Confidence[x['confidence'].replace(" ", "_")] >= Confidence.MEDIUM_PLUS
                        and Severity[x['severity'].replace(" ", "_")] >= Severity.MEDIUM,
                        warnings)))
        report.append([warnings_per_kind, kind if kind is not None else 'Unclassified type', serious_warnings_per_kind])

    return (HEADER.format(len(warnings))
            + '\n'.join([REPORT_TEMPLATE.format(*entry) for entry in report])
            + FOOTER.format(project_id, version_id))

