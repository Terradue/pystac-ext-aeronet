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

# Create an AERONET Item

[Install the package](../how-to/install.md), then run this complete example. The station, coordinates, reporting interval, and availability counts are synthetic; they are not NASA observations.

```python
import json
from datetime import datetime, timezone

import pystac
from pystac.extensions.aeronet import AeronetExtension

item = pystac.Item(
    id="example-aeronet-station",
    geometry={"type": "Point", "coordinates": [12.5, 41.9]},
    bbox=[12.5, 41.9, 12.5, 41.9],
    datetime=None,
    start_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    end_datetime=datetime(2026, 1, 31, 23, 59, 59, tzinfo=timezone.utc),
    properties={"title": "Synthetic AERONET station"},
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

serialized = item.to_dict()
assert AeronetExtension.get_schema_uri() in serialized["stac_extensions"]
assert serialized["properties"]["aeronet:L20"] == 18

restored_item = pystac.Item.from_dict(json.loads(json.dumps(serialized)))
restored = AeronetExtension.from_item(restored_item)
assert restored.site_name == "Example_Station"
assert restored.L20 == 18
assert restored.moon_L15 == 0
```

`add_if_missing=True` adds the schema URL to `item.stac_extensions`. `apply()` requires all six arguments and writes them directly into `item.properties`. The four integer fields describe days of data availability; zero is a valid stored value.

This example uses an Item interval to describe its reporting period. The wrapper neither chooses the Item's temporal extent nor derives counts from it. Supply a period and counts appropriate to your source data.

Serialization preserves the metadata but does not validate it against JSON Schema. Continue with [updates and validation](../how-to/use-extension.md).
