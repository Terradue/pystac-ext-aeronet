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

`pystac-ext-aeronet` reads and writes AERONET station metadata on `pystac.Item` objects. Import `AeronetExtension` from `pystac.extensions.aeronet`.

[AERONET (AErosol RObotic NETwork)](https://aeronet.gsfc.nasa.gov/) is an international network of ground-based aerosol observations. Its measurements support aerosol research and satellite retrieval validation.

The [Terradue AERONET STAC extension](https://github.com/Terradue/aeronet-stac-extension) describes stations through their site name, land use, and days of data availability. This package supplies Python accessors for those fields. It does not download observations or calculate availability counts.

```bash
python -m pip install pystac-ext-aeronet
```

- [Create an AERONET Item](tutorials/first-steps.md) and round-trip its metadata.
- [Update station metadata](how-to/use-extension.md) and manage extension membership.
- [Look up fields](reference/fields.md), types, and required-property behavior.
- [Browse the Python API](reference/api.md).
- [Understand scope and validation](explanation/architecture.md).
