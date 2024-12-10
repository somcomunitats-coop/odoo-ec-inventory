# import json
import requests
import time
# import os

PYPI_URL = "https://pypi.org/pypi/{}/json"
PYPI_SLEEP = 0.2


def _get_version_line(line):
    return line.split("==")[1]

def _get_upgraded_line(line):
    module_name = line.split("==")[0].replace("odoo14", "odoo")
    available_versions = {
        version
        for version in requests.get(PYPI_URL.format(module_name))
        .json()
        .get("releases", {})
        .keys()
    }
    upgraded_line_list = list(filter(lambda x: x.startswith("16"), available_versions))
    upgraded_line_list.sort()
    prefix = ""
    try:
        module_version = upgraded_line_list[-1]
    except Exception:
        prefix = "#"
        module_version = "undefined"
    return "{prefix}{module_name}=={module_version}".format(
        prefix=prefix, module_name=module_name, module_version=module_version
    )


with open("files/requirements.txt") as req_file:
    new_req = open("files/_analysis.txt", "a")
    for line in req_file:
        if line.startswith("odoo"):
            original_line_version = _get_version_line(line)
            upgraded_line = _get_upgraded_line(line)
            upgraded_line_version = _get_version_line(upgraded_line)
            time.sleep(PYPI_SLEEP)
            if str(original_line_version).strip() != str(upgraded_line_version).strip():
                print(upgraded_line)
                new_req.write("{}\n".format(upgraded_line))
        # else:
        #     print(line)
        #     new_req.write("{}\n".format(line))
    new_req.close()
