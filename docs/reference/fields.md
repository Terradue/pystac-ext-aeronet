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

# AERONET fields

`AeronetExtension` exposes the following fields in Item `properties`. All six are required by the [extension schema](https://github.com/Terradue/aeronet-stac-extension/blob/main/json-schema/schema.json). Field meanings follow the [extension specification](https://github.com/Terradue/aeronet-stac-extension#fields).

| STAC field | Python property | Python type | Meaning |
| --- | --- | --- | --- |
| `aeronet:site_name` | `site_name` | `str` | Station name. |
| `aeronet:land_use_type` | `land_use_type` | `str` | Station land use. |
| `aeronet:L10` | `L10` | `int` | Days with Level 1.0 data. |
| `aeronet:L15` | `L15` | `int` | Days with Level 1.5 data. |
| `aeronet:L20` | `L20` | `int` | Days with Level 2.0 data. |
| `aeronet:moon_L15` | `moon_L15` | `int` | Days with lunar Level 1.5 data. |

Names are case-sensitive: use `L10`, `L15`, `L20`, and `moon_L15` exactly as shown.

## Data levels

For Version 3 solar aerosol optical depth, NASA defines Level 1.0 as unscreened, Level 1.5 as cloud-screened and quality-controlled, and Level 2.0 as quality-assured. See the [NASA AERONET overview](https://aeronet.gsfc.nasa.gov/). These fields hold day counts, not optical-depth measurements or level identifiers.

The Python wrapper exposes only the lunar field listed above, even though NASA offers other lunar products.

## Storage and constraints

Getters read the underlying Item properties and raise `pystac.RequiredPropertyMissing` for absent or null values. Setters store their input without coercion or runtime type checking. Zero counts are retained. `apply()` overwrites all six fields and preserves unrelated Item properties.

The schema declares strings and integers, with `int32` formats on the four counts. It defines no land-use enumeration, string length limit, or numeric minimum/maximum. It also rejects unrecognized `aeronet:` fields. The wrapper does not enforce these schema rules; callers must validate before relying on conformance. It does not check relationships between counts or their reporting interval.
