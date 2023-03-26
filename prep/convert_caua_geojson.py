import json
from pyproj import Proj, transform

source_filename = 'data/Counties_and_Unitary_Authorities_December_2022_UK_BFC_-4504570890330359041.geojson'
target_filename = 'data/Counties_and_Unitary_Authorities_transformed.geojson'

with open(source_filename) as f:
    counties = json.load(f)
    

v84 = Proj(proj="latlong",towgs84="0,0,0",ellps="WGS84")
v36 = Proj(proj="latlong", k=0.9996012717, ellps="airy",
        towgs84="446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894")
vgrid = Proj(init="world:bng")


def ENtoLL84(easting, northing):
    """Returns (longitude, latitude) tuple
    """
    vlon36, vlat36 = vgrid(easting, northing, inverse=True)
    return transform(v36, v84, vlon36, vlat36)

def convert_polygon(polygon):
    for i in range(0, len(polygon)):
        coord1 = polygon[i]
        x1, y1 = coord1[0], coord1[1]
        x2, y2 = ENtoLL84(x1,y1)
        coord2 = [x2, y2]
        polygon[i] = coord2
    return polygon

j = 1
for county in counties['features']:
    print(f"{j} / {len(counties['features'])}")
    j += 1

    print(county['properties']['CTYUA22CD'])
    type = county['geometry']['type']

    if type =='Polygon':
        county['geometry']['coordinates'][0] = convert_polygon(county['geometry']['coordinates'][0])
    elif type == 'MultiPolygon':
        for i in range(0, len(county['geometry']['coordinates'])):
            county['geometry']['coordinates'][i][0] = convert_polygon(county['geometry']['coordinates'][i][0])

    # if j == 10:
    #     break

with open(target_filename, 'w') as f:
    json.dump(counties, f)