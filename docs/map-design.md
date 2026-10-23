# Map scales and geographic context

The brass half-dial starts at **District**, with useful stops **Country → Region → County → District → Close**. Minus steps outward, plus inward; the dial/wheel interpolate between scales. Local/reset returns to the selected district. Pan the wider view by dragging. Map projection and coastlines give geographic context; county and region are scale descriptions, not precise administrative-boundary overlays. This is not a navigation map.

## What is real and what is illustrative

Country coastlines come from Natural Earth; place labels use approximate representative coordinates. The local street/park/river drawing and profile pin layout remain illustrative. The nationwide atlas contains 5,988 openly labelled fictional adult characters: two at each of 2,988 approximate postcode-district centres, two at each of three additional coverage areas, plus the six original GU2 characters. All demo cards, pins and clusters are blue and explicitly labelled. Red is reserved for real members, of which none are live. Gold/sparkles are optional decoration, not status.

The public search uses a bundled GeoNames outward-code index. It returns up to twelve nearby demo characters within 30 great-circle miles of the selected district centre. Wider views cluster the fictional atlas geographically; clicking a cluster moves towards that area. Zoom alone changes the view, not the local list. The member lounge still has its separate three-district development fixture index and does not import these characters as accounts. See [the atlas and coverage method](demo-atlas.md).

## Data and privacy

Bundled `map-geography.js` contains a clipped/rounded SVG-path subset of Natural Earth 1:50m admin-0 country geometry: United Kingdom, Ireland and nearby European land. An equirectangular display with a fixed 52° latitude reference is used for this context preview; it is not survey precision. Labels are not administrative polygons.

- Source: [Natural Earth vector repository, ne_50m_admin_0_countries.geojson](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_admin_0_countries.geojson), retrieved 23 October 2026.
- Licence: [Natural Earth public-domain terms](https://www.naturalearthdata.com/about/terms-of-use/).
- The browser loads these files from the same website. No third-party map tiles, geocoder, map API key or external map tracking request is introduced. Existing hosting/font privacy disclosures still apply.

Controls keep portraits readable locally. At broader scales the grouped badge is used instead of overlapping individual pins. The map retains fictional/approximate location notices and offers keyboard controls through the slider, +/− and reset.
