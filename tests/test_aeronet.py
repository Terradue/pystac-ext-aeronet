# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import pytest

import pystac
from pystac.extensions.aeronet import AERONET_SCHEMA_URI, AeronetExtension

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.fixture
def item() -> pystac.Item:
    return pystac.Item(
        id="aeronet-site",
        geometry=None,
        bbox=None,
        datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
        properties={"unrelated": "preserved"},
    )


@pytest.mark.parametrize("factory", [AeronetExtension.ext, AeronetExtension.from_item])
def test_missing_extension_requires_explicit_opt_in(
    item: pystac.Item, factory: Callable[..., AeronetExtension]
) -> None:
    with pytest.raises(pystac.ExtensionNotImplemented, match="aeronet"):
        factory(item)
    assert item.stac_extensions == []
    assert item.properties == {"unrelated": "preserved"}


@pytest.mark.parametrize("factory", [AeronetExtension.ext, AeronetExtension.from_item])
def test_attachment_is_idempotent_and_preserves_other_extensions(
    item: pystac.Item, factory: Callable[..., AeronetExtension]
) -> None:
    other_schema = "https://example.com/other/schema.json"
    item.stac_extensions.append(other_schema)
    extension = factory(item, add_if_missing=True)
    factory(item, add_if_missing=True)
    assert extension.item is item
    assert extension.properties is item.properties
    assert item.stac_extensions == [other_schema, AERONET_SCHEMA_URI]
    assert factory(item).item is item
    assert AeronetExtension.has_extension(item)


@pytest.mark.parametrize(
    "schema_uri, expected",
    [
        (AERONET_SCHEMA_URI, True),
        (AERONET_SCHEMA_URI + "/other", False),
        ("https://example.com/schema.json", False),
    ],
)
def test_has_extension_matches_exact_schema_uri(
    item: pystac.Item, schema_uri: str, expected: bool
) -> None:
    item.stac_extensions = [schema_uri]
    assert AeronetExtension.has_extension(item) is expected
    assert AeronetExtension.get_schema_uri() == AERONET_SCHEMA_URI


def test_removing_extension_preserves_properties(item: pystac.Item) -> None:
    extension = AeronetExtension.ext(item, add_if_missing=True)
    extension.site_name = "Rome"
    AeronetExtension.remove_from(item)
    AeronetExtension.remove_from(item)
    assert not AeronetExtension.has_extension(item)
    assert item.properties["aeronet:site_name"] == "Rome"


@pytest.mark.parametrize("add_if_missing", [False, True])
@pytest.mark.parametrize(
    "unsupported",
    [
        pystac.Catalog(id="catalog", description="Unsupported catalog"),
        pystac.Collection(
            id="collection",
            description="Unsupported collection",
            extent=pystac.Extent(
                pystac.SpatialExtent([-180, -90, 180, 90]),
                pystac.TemporalExtent([None, None]),
            ),
        ),
        pystac.Asset(href="https://example.com/data.csv"),
    ],
)
def test_rejects_unsupported_objects(
    unsupported: pystac.Catalog | pystac.Asset, add_if_missing: bool
) -> None:
    original = unsupported.to_dict()
    with pytest.raises(pystac.ExtensionTypeError, match=type(unsupported).__name__):
        # Intentionally violate the typed API to verify the runtime error.
        AeronetExtension.ext(unsupported, add_if_missing=add_if_missing)  # type: ignore[arg-type]
    assert unsupported.to_dict() == original


@pytest.mark.parametrize(
    "property_name, value, replacement",
    [
        ("site_name", "Rome", "Ispra"),
        ("land_use_type", "Urban", "Forest"),
        ("L10", 10, 0),
        ("L15", 15, 0),
        ("L20", 20, 0),
        ("moon_L15", 5, 0),
    ],
)
def test_properties_read_and_update_item_storage(
    item: pystac.Item, property_name: str, value: str | int, replacement: str | int
) -> None:
    extension = AeronetExtension.ext(item, add_if_missing=True)
    property_key = f"aeronet:{property_name}"
    item.properties[property_key] = value
    assert getattr(extension, property_name) == value
    setattr(extension, property_name, replacement)
    assert item.properties[property_key] == replacement
    assert getattr(extension, property_name) == replacement
    assert item.properties["unrelated"] == "preserved"


@pytest.mark.parametrize(
    "property_name", ["site_name", "land_use_type", "L10", "L15", "L20", "moon_L15"]
)
@pytest.mark.parametrize("explicit_null", [False, True])
def test_required_properties_reject_missing_or_null_values(
    item: pystac.Item, property_name: str, explicit_null: bool
) -> None:
    extension = AeronetExtension.ext(item, add_if_missing=True)
    property_key = f"aeronet:{property_name}"
    if explicit_null:
        item.properties[property_key] = None
    with pytest.raises(pystac.RequiredPropertyMissing, match=property_key):
        getattr(extension, property_name)


def test_apply_overwrites_values_and_survives_json_roundtrip(item: pystac.Item) -> None:
    extension = AeronetExtension.ext(item, add_if_missing=True)
    extension.apply("Old site", "Old land use", 1, 1, 1, 1)
    extension.apply(site_name="Rome", land_use_type="Urban", L10=10, L15=8, L20=6, moon_L15=0)
    expected = {
        "unrelated": "preserved",
        "aeronet:site_name": "Rome",
        "aeronet:land_use_type": "Urban",
        "aeronet:L10": 10,
        "aeronet:L15": 8,
        "aeronet:L20": 6,
        "aeronet:moon_L15": 0,
    }
    assert item.properties == expected
    restored = pystac.Item.from_dict(json.loads(json.dumps(item.to_dict())))
    restored_extension = AeronetExtension.from_item(restored)
    assert restored.stac_extensions == [AERONET_SCHEMA_URI]
    for property_name in ("site_name", "land_use_type", "L10", "L15", "L20", "moon_L15"):
        assert getattr(restored_extension, property_name) == expected[f"aeronet:{property_name}"]
    assert restored.properties["unrelated"] == "preserved"
