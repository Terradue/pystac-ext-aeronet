<!--
Copyright 2026 Terradue

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# AERONET PySTAC extension

[![PyPI - Version](https://img.shields.io/pypi/v/pystac-ext-aeronet.svg)](https://pypi.org/project/pystac-ext-aeronet)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pystac-ext-aeronet.svg)](https://pypi.org/project/pystac-ext-aeronet)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/terradue/pystac-ext-aeronet/package.yaml?branch=develop&event=push&label=build&logo=githubactions)](https://github.com/terradue/pystac-ext-aeronet/actions/workflows/package.yaml?query=branch%3Adevelop)
[![Code coverage](https://img.shields.io/codecov/c/github/terradue/pystac-ext-aeronet/develop?logo=codecov)](https://app.codecov.io/gh/terradue/pystac-ext-aeronet/tree/develop)

PySTAC implementation of the [Terradue AERONET STAC extension](https://github.com/Terradue/aeronet-stac-extension), for describing stations from the [NASA AERONET network](https://aeronet.gsfc.nasa.gov/).

The package reads and writes six required Item properties: site name, land use, and day counts for solar Levels 1.0, 1.5, 2.0 and lunar Level 1.5. It manages metadata; it does not download observations or compute counts.

## Install and use

Requires Python 3.10 or later and PySTAC `>=1,<2`.

```bash
python -m pip install pystac-ext-aeronet
```

```python
from datetime import datetime, timezone

import pystac
from pystac.extensions.aeronet import AeronetExtension

# Synthetic metadata snapshot; replace with your station's metadata.
item = pystac.Item(
    id="example-station",
    geometry=None,
    bbox=None,
    datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    properties={},
)
aeronet = AeronetExtension.ext(item, add_if_missing=True)
aeronet.apply(
    site_name="Example_Station",
    land_use_type="Urban",
    L10=25,
    L15=20,
    L20=18,
    moon_L15=0,
)
assert item.to_dict()["properties"]["aeronet:L20"] == 18
```

The wrapper supports Items. All six `apply()` arguments are required, and reading an absent or null field raises `pystac.RequiredPropertyMissing`. Setters do not perform runtime type or schema validation; use `item.validate()` with PySTAC's validation dependencies when needed.

## Documentation

Read the [project documentation](https://terradue.github.io/pystac-ext-aeronet/) for Python examples, the field reference, and API documentation.

To preview it locally:

```bash
python -m pip install . "mkdocs<2" mkdocs-material "mkdocstrings[python]"
mkdocs serve
```

## Contribute

Submit a [GitHub issue](https://github.com/Terradue/pystac-ext-aeronet/issues) if you have comments or suggestions.

### Local quality checks

Install [Hatch](https://hatch.pypa.io/) and [Taskfiles](https://taskfile.dev/docs/guide) then install the Git hook:

```console
task quality:pre-commit:install
```

Every commit runs Ruff (including the configured McCabe complexity limit),
Ruff formatting, strict mypy checks, Bandit, and the pytest suite.

Run the complete hook explicitly with:

```console
task
```

## License

[![Apache License, Version 2.0](https://img.shields.io/badge/license-Apache%20License%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)
