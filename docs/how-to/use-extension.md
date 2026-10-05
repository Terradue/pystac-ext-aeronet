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

# Work with AERONET metadata

These examples continue from the Item created in the [tutorial](../tutorials/first-steps.md).

## Update one field

```python
aeronet = AeronetExtension.ext(item)
aeronet.L20 = 19
assert item.properties["aeronet:L20"] == 19
assert aeronet.site_name == "Example_Station"
```

Individual setters preserve other properties. To replace all six fields, call `apply()` with all six arguments, as in the tutorial. There are no default values in `apply()`.

## Open an existing Item

`AeronetExtension.from_item(item)` is an alias for `AeronetExtension.ext(item)`. Both require the extension URL to be declared, unless you pass `add_if_missing=True`.

```python
if AeronetExtension.has_extension(restored_item):
    existing = AeronetExtension.from_item(restored_item)
    assert existing.site_name == "Example_Station"
```

Accessing a missing or JSON-null AERONET field raises `pystac.RequiredPropertyMissing`. Attaching the extension alone does not populate those fields. Supply all required values before publishing the Item.

## Manage extension membership

```python
AeronetExtension.remove_from(item)
assert not AeronetExtension.has_extension(item)
assert item.properties["aeronet:site_name"] == "Example_Station"

AeronetExtension.add_to(item)
AeronetExtension.add_to(item)
assert item.stac_extensions.count(AeronetExtension.get_schema_uri()) == 1
```

Removal changes the extension declaration only; stored fields remain. Assigning `None` is outside the setter type contract and does not remove a field. If you intentionally remove AERONET metadata, remove its properties explicitly as well as its declaration.

## Validate a complete Item

Install PySTAC's validation dependencies:

```bash
python -m pip install "pystac[validation]>=1,<2"
```

Then, with all required values populated:

```python
item.validate()
```

Validation may fetch STAC and extension schemas over the network. For offline use, configure a PySTAC validator with locally available schemas. `apply()` and `to_dict()` do not invoke validation. See the [validation boundaries](../explanation/architecture.md#validation-boundaries) for the checks performed by this wrapper.
