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

# Contributing to the AERONET PySTAC extension

## Development setup

Install Python 3.10 or later, [Hatch](https://hatch.pypa.io/), and [Task](https://taskfile.dev/). From a checkout:

```bash
python -m pip install -e .
task quality:pre-commit:install
```

## Quality gate

Before opening a pull request, run:

```bash
task
```

The default task runs the pre-commit hooks: strict mypy, Ruff formatting and lint checks, Bandit, and pytest across the configured Python 3.10–3.14 matrix. See `AGENTS.md` for the repository's code quality and schema-first rules.

The individual non-mutating checks are:

```bash
hatch run dev:format-check
hatch run dev:lint-check
hatch run dev:typecheck
hatch run dev:security
hatch run test:test
```

## Documentation

Documentation follows Diátaxis: tutorials teach a workflow, how-to guides solve tasks, reference pages describe the API, and explanation pages discuss design and scope.

Follow the [documentation build instructions](docs/how-to/install.md#preview-the-documentation) and run `mkdocs build --strict` before submitting documentation changes. Keep examples consistent with `src/pystac/extensions/aeronet.py` and the upstream [AERONET STAC specification](https://github.com/Terradue/aeronet-stac-extension).
