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

# Scope, architecture, and validation

## Station metadata and observations

[NASA AERONET](https://aeronet.gsfc.nasa.gov/) distributes aerosol observations and derived products. The [Terradue STAC extension](https://github.com/Terradue/aeronet-stac-extension) provides station metadata for discovery. This Python package stores that metadata; it does not retrieve measurements, perform cloud screening, calculate aerosol optical depth, or count available days.

## Package structure

The distribution is `pystac-ext-aeronet`; its API lives in `pystac.extensions.aeronet`. The wheel excludes the shared `pystac.extensions` initializer owned by PySTAC.

`AeronetExtension` combines PySTAC's `PropertiesExtension` and `ExtensionManagementMixin`. It holds a reference to the Item's properties dictionary. Updates through either the Item or wrapper are therefore visible to the other, and ordinary PySTAC serialization preserves the fields.

Only Items are supported. Assets, Catalogs, Collections, and item asset definitions cannot be wrapped. No Collection summary aggregation or automatic extension registration is provided.

## Schema identity

The code uses this exact URL in `stac_extensions`:

```text
https://raw.githubusercontent.com/Terradue/aeronet-stac-extension/refs/heads/main/json-schema/schema.json
```

`has_extension()` checks exact membership, rather than accepting alternate URLs or versions. The URL tracks the upstream `main` branch; the Python package version does not pin a schema revision.

At the time of this documentation update, the upstream README lists proposal maturity and retains a template identifier. The schema also retains a template `$id` and title, but its `stac_extensions` constraint requires the raw GitHub URL above. Use `get_schema_uri()` rather than copying the README's template identifier. The schema's Item structure and this implementation determine the supported scope, despite broader template text in the upstream README.

Source: [upstream JSON Schema](https://github.com/Terradue/aeronet-stac-extension/blob/main/json-schema/schema.json).

## Validation boundaries

Python annotations describe the accepted types, but setters do not enforce them at runtime. Getters require non-null values; they do not verify the type of an existing value. Extension membership checks also do not validate field contents.

`apply()` assigns all six fields in sequence. It does not compute values, validate consistency, or provide a transactional update. `to_dict()` serializes without validating. Use PySTAC's `item.validate()` separately for schema validation, as described in the [how-to guide](../how-to/use-extension.md#validate-a-complete-item).

The [field reference](../reference/fields.md) distinguishes schema constraints from wrapper behavior. Scientific interpretation and the relationship between availability counts and an Item's temporal extent remain the data producer's responsibility.
