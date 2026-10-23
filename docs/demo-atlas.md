# Nationwide fictional demo atlas

The public preview contains **5,988 fictional adult characters**: two per approximate postcode-district centre (2,988 centres), two at each of three extra coverage areas, plus the original six GU2 characters. Names, biographies, intentions, replies and style choices are fictional combinations, not scraped dating profiles. All characters are adults in their 30s–60s. The copy invites flirtation and clearly negotiated adult connection without graphic content. No real person, meeting or availability is represented.

## Visible separation

- **Blue = DEMO.** Pins, cards, profile details and geographic clusters use blue styling and written labels. Chats are explicitly scripted.
- **Red = real members**, reserved for future server-classified patrons. No real patrons are live. Local development accounts are explicitly returned as `profile_kind: demo` by the server; a client field cannot promote them.
- **Gold trim and sparkles** are optional avatar controls. They cannot change a profile's status. Colour alone is never the disclosure.

## The 30-mile target

The target is a nearby fictional introduction across UK land, not a guarantee about real people. We check great-circle distance, **not driving, walking or ferry distance**. We do not infer anyone's precise location: public search starts from a postcode-district centre.

The reproducible generator samples the Natural Earth UK land polygons on a 0.025° grid and includes coastline vertices/small islands. Starting from the district centres, it adds a fictional area where the furthest sample exceeds 35 km. The current run checks **53,962 samples**, adds **three areas**, and finds a maximum sample-to-demo distance of **20.19 miles**, within the 30-mile target. See [machine-readable results](demo-coverage.json). This is an approximate, sampled geographic check, not proof for every UK address or a guarantee of a route under 30 miles. Boundary and centroid accuracy, unsampled places, travel across water, postcode changes and the chosen mood filter can affect the experience. No GPS or population file is involved.

Public results show up to twelve characters within 30 miles of the selected centre, sorted by approximate distance. The all-moods view is the coverage target; a specific mood may return fewer or none. Country/region/county views cluster the atlas; the nearest demo list remains tied to the chosen area until a new area is selected. An unknown district is reported as unavailable in this approximate index, rather than silently geocoded to Guildford.

## Geographic sources and reuse

- Approximate outward postcode centres/place labels derived by averaging GeoNames GB postal rows per district. [GeoNames download](https://download.geonames.org/export/zip/GB.zip), retrieved 23 October 2026. The downloaded archive's readme specifies [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); attribution: [GeoNames](https://www.geonames.org/). Data is supplied without accuracy, timeliness or completeness warranty. This is a district index, not the full-postcode/address database. Source hash is in the coverage report.
- Land/coastline sampling uses [Natural Earth 1:50m countries](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_admin_0_countries.geojson), [public domain](https://www.naturalearthdata.com/about/terms-of-use/).
- Changes: aggregated/rounded district centres, a clipped country subset, generated fictional locations, and newly authored fictional personas. No source supplies patron identities or preferences. All data is bundled and served by the website; no geocoder, tile tracker or external map service request is introduced.

Rebuild with `python scripts/build_demo_atlas.py GB.txt countries.geojson` after downloading those geographic inputs. The build uses NumPy/SciPy for the nearest-point coverage check; the browser needs neither. `demo-atlas-data.js` holds centres and coverage metadata; `demo-atlas.js` generates characters deterministically. Do not silently convert demo characters, messages, keepsakes or preview payment steps into live customers or paid activity. The local backend remains development-only and the atlas is not seeded into its patron tables.
