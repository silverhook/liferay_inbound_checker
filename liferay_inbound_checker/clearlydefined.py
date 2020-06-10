# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import json
from typing import Dict, Set

import requests
from requests.compat import urljoin

from .dependencies import Dependency


def definitions_from_clearlydefined(dependency: Dependency) -> Dict:
    """
    :raises requests.RequestException: if the request could not be made.
    """
    url = urljoin(
        "https://api.clearlydefined.io/definitions/maven/mavencentral/",
        f"{dependency.groupid}/{dependency.artifactid}/{dependency.version}",
    )
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    raise requests.RequestException("Status code was not 200")


class ClearlyDefinedDefinitions:
    def __init__(self, json_dict: Dict):
        self._json_dict = json_dict

    @property
    def discovered_license_expressions(self) -> Set[str]:
        result = {self._json_dict["licensed"]["declared"]}
        for _, facet in self._json_dict["licensed"]["facets"].items():
            result = result.union(set(facet["discovered"]["expressions"]))
        return result

    @property
    def score(self) -> int:
        return self._json_dict["scores"]["effective"]
