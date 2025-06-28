import sqlite3
import matplotlib

# Arka planda grafik kaydetmek için pencere açılmasını engelle
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs  # Harita projeksiyonları için

class DB_Map:
    def __init__(self, database):
        self.database = database  # Veri tabanı yolunu ayarla
    def create_graph(self, path, cities):
            ax = plt.axes(projection=ccrs.PlateCarree())
            ax.stock_img()
            for city in cities:
                coordinates = self.get_coordinates(city)
                if coordinates:
                    lat, lng = coordinates
                    plt.plot([lng], [lat], color='r', linewidth=1, marker='.', transform=ccrs.Geodetic())
                    plt.text(lng + 3, lat + 12, city, horizontalalignment='left', transform=ccrs.Geodetic())
            plt.savefig(path)
            plt.close()
    def draw_distance(self, city1, city2):
            # İki şehir arasındaki mesafeyi göstermek için bir çizgi çizme
            city1_coords = self.get_coordinates(city1)
            city2_coords = self.get_coordinates(city2)
            fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
            ax.stock_img()
            plt.plot([city1_coords[1], city2_coords[1]], [city1_coords[0], city2_coords[0]], color='red', linewidth=2,
                    marker='o', transform=ccrs.Geodetic())
            plt.text(city1_coords[1] + 3, city1_coords[0] + 12, city1, horizontalalignment='left',
                    transform=ccrs.Geodetic())
            plt.text(city2_coords[1] + 3, city2_coords[0] + 12, city2, horizontalalignment='left',
                    transform=ccrs.Geodetic())
            plt.savefig('distance_map.png')
            plt.close()


if __name__ == "__main__":
    m = DB_Map("database.db")
    m.create_user_table()
