# Map scales and geographic context

The brass half-dial starts at **District**, with useful stops **Country → Region → County → District → Close**. Minus steps outward, plus inward; the dial/wheel interpolate between scales. Local/reset returns to the selected district. Pan the wider view by dragging. Map projection and coastlines give geographic context; county and region are scale descriptions, not precise administrative-boundary overlays. This is not a navigation map.

## What is real and what is illustrative

Country coastlines come from Natural Earth; place labels use approximate representative coordinates. The local street/park/river drawing, six public profiles and their decorative positions remain fictional. Wide views group those current results around their selected district; they never scatter fake patrons across Britain. Clicking the group returns to the district. Mood filters update the grouped count.

GU2/GU1/SW1A are the current example district centres. Public searches for other districts keep the fictional profiles and explicitly label wider geography as an example near GU2, rather than pretending to geocode the input. The member lounge uses the centre from its three-district local fixture index. Zoom changes the view, not the radius or result set returned by the backend. Nationwide discovery still needs a production district index, viewport queries/explicit search scope and privacy-preserving aggregation.

## Data and privacy

Bundled `map-geography.js` contains a clipped/rounded SVG-path subset of Natural Earth 1:50m admin-0 country geometry: United Kingdom, Ireland and nearby European land. An equirectangular display with a fixed 52° latitude reference is used for this context preview; it is not survey precision. Labels are not administrative polygons.

- Source: [Natural Earth vector repository, ne_50m_admin_0_countries.geojson](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_admin_0_countries.geojson), retrieved 23 October 2026.
- Licence: [Natural Earth public-domain terms](https://www.naturalearthdata.com/about/terms-of-use/).
- The browser loads these files from the same website. No third-party map tiles, geocoder, map API key or external map tracking request is introduced. Existing hosting/font privacy disclosures still apply.

Controls keep portraits readable locally. At broader scales the grouped badge is used instead of overlapping individual pins. The map retains fictional/approximate location notices and offers keyboard controls through the slider, +/− and reset.
