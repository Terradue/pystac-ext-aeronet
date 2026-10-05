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

# Python API

```python
from pystac.extensions.aeronet import AeronetExtension
```

| Entry point | Behavior |
| --- | --- |
| `ext(item, add_if_missing=False)` | Wrap an Item; raise `pystac.ExtensionNotImplemented` if its extension declaration is missing. Opt in to adding the declaration with `add_if_missing=True`. |
| `from_item(item, add_if_missing=False)` | Alias for `ext()`. |
| `apply(site_name, land_use_type, L10, L15, L20, moon_L15)` | Write all six required fields. |
| `get_schema_uri()` | Return the schema URL used in extension declarations. |
| `has_extension(item)` | Check for that exact URL in `stac_extensions`. |
| `add_to(item)` | Add the URL if absent; inherited from PySTAC. |
| `remove_from(item)` | Remove the URL, retaining properties; inherited from PySTAC. |

`ext()` rejects objects other than `pystac.Item` with `pystac.ExtensionTypeError`. The package has no Asset wrapper, Collection summary helper, or migration hook. Use the class methods above; the module does not register an `item.ext.aeronet` accessor.

See the [field reference](fields.md) for property access and missing-value behavior.

::: pystac.extensions
    options:
      members:
        - AeronetExtension
        - AERONET_SCHEMA_URI
        - AERONET_PREFIX
        - SITE_NAME_PROP
        - LAND_USE_TYPE_PROP
        - L10_PROP
        - L15_PROP
        - L20_PROP
        - MOON_L15_PROP
      inherited_members: false
      show_root_heading: true
      show_signature_annotations: true
