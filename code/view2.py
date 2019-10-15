import plotly.graph_objects as go
import numpy as np

class Utils:
    @staticmethod
    def deg_to_rad(deg):
        return deg/180*np.pi

    @staticmethod
    def rad_to_deg(rad):
        return rad/np.pi*180

    @staticmethod
    def mid_point(pt0, pt1):
        x = (pt0.x + pt1.x)/2
        y = (pt0.y + pt1.y)/2
        z = (pt0.z + pt1.z)/2
        return Point3D(x, y, z)

    @staticmethod
    def surface_mid_point(pt0, pt1):
        mid_point = Utils.mid_point(pt0, pt1)
        avg_radius = (pt0.radius() + pt1.radius()) / 2
        scale_ratio = avg_radius / mid_point.radius()
        mid_point.scale(scale_ratio)
        return mid_point
    
    @staticmethod
    def latlon_to_xyz(latlon, r):
        lat = latlon[0]
        lon = latlon[1]
        hori_dist = r * np.cos(Utils.deg_to_rad(lat))
        
        x = hori_dist * np.cos(Utils.deg_to_rad(lon))
        y = hori_dist * np.sin(Utils.deg_to_rad(lon))
        z = r * np.sin(Utils.deg_to_rad(lat))
        return [x, y, z]

class GeodesicGrid:
    @staticmethod
    def get_init_regions(r):
        init_latlons = [
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

        point_xyz_list = [Utils.latlon_to_xyz(latlon, r) for latlon in init_latlons]
        pts = [Point3D(point[0], point[1], point[2]) for point in point_xyz_list]
        top, bot = pts[0], pts[1]

        r0 = DiamondRegion([top, pts[2], pts[11], pts[6]], '0')
        r1 = DiamondRegion([top, pts[3], pts[7], pts[2]], '1')
        r2 = DiamondRegion([top, pts[4], pts[8], pts[3]], '2')
        r3 = DiamondRegion([top, pts[5], pts[9], pts[4]], '3')
        r4 = DiamondRegion([top, pts[6], pts[10], pts[5]], '4')
        r5 = DiamondRegion([pts[2], pts[7], bot, pts[11]], '5')
        r6 = DiamondRegion([pts[3], pts[8], bot, pts[7]], '6')
        r7 = DiamondRegion([pts[4], pts[9], bot, pts[8]], '7')
        r8 = DiamondRegion([pts[5], pts[10], bot, pts[9]], '8')
        r9 = DiamondRegion([pts[6], pts[11], bot, pts[10]], '9')

        return [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9]

    @staticmethod
    def get_grid(order, r):
        regions = GeodesicGrid.get_init_regions(r)
        while order > 0:
            next_regions = []
            for region in regions:
                next_regions += region.sub_regions()
            regions = next_regions
            order -= 1

        return [region.centroid() for region in regions]

class DiamondRegion:
    def __init__(self, vertices, encoding):
        '''
            vertices follow this ordering:
                0
              3   1
                2
        '''
        self.vertices = vertices
        self.encoding = encoding

    def centroid(self):
        return Utils.surface_mid_point(self.vertices[1], self.vertices[3])

    def sub_regions(self):
        '''
            sub-DiamondRegions follow this layout:
                  v0
              
               *  r0  *
            
            v3 r3 *  r1 v1
            
               *  r2  *
            
                  v2

            encoding mapping:
            r0: self.encoding + '0'
            r1: self.encoding + '1'
            r2: self.encoding + '2'
            r3: self.encoding + '3'
        '''

        v = self.vertices
        top_right = Utils.surface_mid_point(v[0], v[1])
        bot_right = Utils.surface_mid_point(v[1], v[2])
        bot_left = Utils.surface_mid_point(v[2], v[3])
        top_left = Utils.surface_mid_point(v[3], v[0])

        center = self.centroid()
        r0 = DiamondRegion([v[0], top_right, center, top_left], self.encoding + '0')
        r1 = DiamondRegion([top_right, v[1], bot_right, center], self.encoding + '1')
        r2 = DiamondRegion([center, bot_right, v[2], bot_left], self.encoding + '2')
        r3 = DiamondRegion([top_left, center, bot_left, v[3]], self.encoding + '3')

        return [r0, r1, r2, r3]

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def radius(self):
        return self.distance(Point3D(0, 0, 0))
    
    def distance(self, pt1):
        return (abs(self.x-pt1.x)**2 + abs(self.y-pt1.y)**2 + abs(self.z-pt1.z)**2)**0.5

    def latlon(pt):
        r = pt.radius()
        x = pt[0]
        y = pt[1]
        z = pt[2]
        lat = Utils.rad_to_deg(np.arcsin(z/r))
        lon = Utils.rad_to_deg(np.arctan(y/x))
        if x < 0:
            if y > 0:
                lon += 180
            if y <= 0:
                lon -= 180
        return lat, lon

    def scale(self, factor):
        self.x *= factor
        self.y *= factor
        self.z *= factor

def draw_graph(pts):
    x = [pt.x for pt in pts]
    y = [pt.y for pt in pts]
    z = [pt.z for pt in pts]
    color = [1 for i in range(len(pts))]
    size = [3 for i in range(len(pts))]

    marker = dict(size=size, color=color, opacity=0.8)
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=marker)])
    fig.show()

def main():
    points = GeodesicGrid.get_grid(4, 1)
    draw_graph(points)

if __name__ == "__main__":
    main()