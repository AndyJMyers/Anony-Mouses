"""Import the bundled approximate GeoNames outward-district centres for staging.

This is not a claim that the dated source is maintained production geography.
No full postcodes, addresses or person locations are imported.
"""
import json
from pathlib import Path

def bundled_districts(path=None):
    path=Path(path) if path else Path(__file__).resolve().parent.parent/'demo-atlas-data.js'
    source=path.read_text();marker='globalThis.AnonyDemoAtlasData='
    if source.count(marker)!=1:raise ValueError('Unrecognised bundled district format')
    data=json.loads(source.split(marker,1)[1].strip().removesuffix(';'))
    return [(code,float(lat),float(lon)) for code,place,lat,lon in data['districts']]
