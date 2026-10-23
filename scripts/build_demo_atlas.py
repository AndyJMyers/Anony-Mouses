"""Build a fictional UK atlas from GeoNames outward codes and Natural Earth land.

Usage: python scripts/build_demo_atlas.py GB.txt countries.geojson
Inputs are public geographic data, never patron records. See docs/demo-atlas.md.
"""
import collections, hashlib, json, math, sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parents[1]
R=6371.0088

def xyz(lat,lon):
    a=np.radians(lat);b=np.radians(lon)
    return np.column_stack((np.cos(a)*np.cos(b),np.cos(a)*np.sin(b),np.sin(a)))

def build(postal_path,countries_path):
    groups=collections.defaultdict(list)
    for line in Path(postal_path).read_text().splitlines():
        r=line.split('\t')
        try:lat,lon=float(r[9]),float(r[10])
        except (ValueError,IndexError):continue
        if r[0]=='GB' and 49.8<=lat<=61.2 and -8.5<=lon<=2.3:groups[r[1]].append((lat,lon,r[2]))
    districts=[]
    for code,rows in sorted(groups.items()):
        districts.append([code,collections.Counter(r[2] for r in rows).most_common(1)[0][0],round(sum(r[0] for r in rows)/len(rows),5),round(sum(r[1] for r in rows)/len(rows),5)])
    data=json.loads(Path(countries_path).read_text())
    uk=next(f for f in data['features'] if f['properties'].get('ADMIN',f['properties'].get('name'))=='United Kingdom')
    polygons=uk['geometry']['coordinates']
    if uk['geometry']['type']=='Polygon':polygons=[polygons]
    polygons=[p for p in polygons if any(49.5<=y<=61.5 and -9<=x<=3 for x,y in p[0])]
    # Scanline sampling: interior grid plus coastline vertices, including small islands.
    samples=[]
    for polygon in polygons:
        outer=polygon[0]
        samples.extend((y,x) for x,y in outer)
        low=min(y for x,y in outer);high=max(y for x,y in outer)
        for lat in np.arange(low+.0125,high,.025):
            crossings=[]
            for ring in polygon:
                for (x1,y1),(x2,y2) in zip(ring,ring[1:]):
                    if (y1>lat)!=(y2>lat):crossings.append(x1+(lat-y1)*(x2-x1)/(y2-y1))
            crossings.sort()
            for left,right in zip(crossings[::2],crossings[1::2]):
                samples.extend((float(lat),float(lon)) for lon in np.arange(left+.0125,right,.025))
    points=np.array(samples);sphere=xyz(points[:,0],points[:,1]);coords=np.array([[r[2],r[3]] for r in districts])
    base=xyz(coords[:,0],coords[:,1]);tree=cKDTree(base)
    chord,_=tree.query(sphere);distance=2*R*np.arcsin(np.minimum(1,chord/2));extra=[]
    while distance.max()>35:
        i=int(distance.argmax());lat,lon=points[i];nearest=tree.query(sphere[i])[1];near=districts[nearest]
        extra.append([f'DEMO-{len(extra)+1:03}',f'Near {near[0]} · illustrative area',round(float(lat),5),round(float(lon),5)])
        new=xyz(np.array([lat]),np.array([lon]))[0]
        distance=np.minimum(distance,2*R*np.arcsin(np.minimum(1,np.linalg.norm(sphere-new,axis=1)/2)))
    report={'districts':len(districts),'extra_areas':len(extra),'fictional_profiles':2*(len(districts)+len(extra)),'land_samples':len(samples),'sample_spacing_degrees':.025,'furthest_sample_miles':round(float(distance.max())/1.609344,2),'target_miles':30,'distance':'great-circle, not road or ferry distance','scope':'Natural Earth UK land sample and coastline vertices; approximate coverage, not a population/address guarantee','geonames_sha256':hashlib.sha256(Path(postal_path).read_bytes()).hexdigest()}
    payload={'districts':districts,'extraAreas':extra,'coverage':report}
    (ROOT/'demo-atlas-data.js').write_text("'use strict';\n// Derived GeoNames CC BY 4.0 district centres; see docs/demo-atlas.md. All profiles fictional.\nglobalThis.AnonyDemoAtlasData="+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n')
    (ROOT/'docs/demo-coverage.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':build(*sys.argv[1:])
