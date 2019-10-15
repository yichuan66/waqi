from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

earth_radius = 6371

def distance(pt0, pt1):
    return (abs(pt0[0]-pt1[0])**2 + abs(pt0[1]-pt1[1])**2 + abs(pt0[2]-pt1[2])**2)**0.5

def deg_to_rad(deg):
    return deg/180*np.pi

def rad_to_deg(rad):
    return rad/np.pi*180

def witin_err(num0, num1, err):
    return abs(num0 - num1) < err

def latlon_to_xyz(latlon):
    lat = latlon[0]
    lon = latlon[1]
    hori_dist = earth_radius * np.cos(deg_to_rad(lat))
    
    x = hori_dist * np.cos(deg_to_rad(lon))
    y = hori_dist * np.sin(deg_to_rad(lon))
    z = earth_radius * np.sin(deg_to_rad(lat))
    return [x, y, z]

def xyz_to_latlon(pt):
    x = pt[0]
    y = pt[1]
    z = pt[2]
    lat = rad_to_deg(np.arcsin(z/earth_radius))
    lon = rad_to_deg(np.arctan(y/x))
    return lat, lon

def mid_point(pt0, pt1):
    x = (pt0[0] + pt1[0])/2
    y = (pt0[1] + pt1[1])/2
    z = (pt0[2] + pt1[2])/2
    return [x, y, z]

def get_init_latlons():
    return [
        (90, 0),
        (-90, 0),
        (26.5650512, 0),
        (26.5650512, 72),
        (26.5650512, 144),
        (26.5650512, -144),
        (26.5650512, -72),
        (-26.5650512, 36),
        (-26.5650512, 108),
        (-26.5650512, 180),
        (-26.5650512, -108),
        (-26.5650512, -36),
    ]

def get_new_latlons():
    init_latlons = get_init_latlons()
    init_dist = 6698.9
    err = 1

    latlons = []
    for i in range(len(init_latlons)):
        for j in range(i+1, len(init_latlons)):
            pt0 = latlon_to_xyz(init_latlons[i])
            pt1 = latlon_to_xyz(init_latlons[j])
            dist = distance(pt0, pt1)
            if witin_err(dist, init_dist, err):
                mid_latlon = xyz_to_latlon(mid_point(pt0, pt1))
                print(pt0, pt1, mid_point(pt0, pt1), init_latlons[i], init_latlons[j], mid_latlon)
                latlons.append(mid_latlon)
    print(len(latlons))
    return latlons

def draw_earth_with_points():
    map = Basemap(projection='ortho', 
                lat_0=0, lon_0=0)
    map.bluemarble()

    lats, lons = [], []
    for latlon in get_init_latlons():
        lats.append(latlon[0])
        lons.append(latlon[1])
    x,y = map(lons, lats)
    map.scatter(x, y, marker='o', color='r', s=100)

    lats, lons = [], []
    for latlon in get_new_latlons():
        lats.append(latlon[0])
        lons.append(latlon[1])
    x,y = map(lons, lats)
    map.scatter(x, y, marker='o', color='g', s=10)

    print(get_new_latlons())
    print('\n\n\n')
    print(get_init_latlons())

    plt.show()

def main():
    draw_earth_with_points()    

if __name__ == "__main__":
    main()