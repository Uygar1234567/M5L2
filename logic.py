import sqlite3
import matplotlib
matplotlib.use('Agg')  # Pencere açılmasını engelle
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from geopy.geocoders import Nominatim

class DB_Map:
    def __init__(self, database):
        self.database = database
        self.geolocator = Nominatim(user_agent="city_bot")
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_cities (
                    user_id TEXT,
                    city TEXT
                )
            ''')
            conn.commit()

    def get_coordinates(self, city_name):
        try:
            location = self.geolocator.geocode(city_name)
            if location:
                return (location.latitude, location.longitude)
        except Exception as e:
            print(f"Koordinat alınamadı: {e}")
        return None

    def add_city(self, user_id, city_name):
        coords = self.get_coordinates(city_name)
        if coords is None:
            return False

        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_cities (user_id, city) VALUES (?, ?)", (str(user_id), city_name))
            conn.commit()
        return True

    def select_cities(self, user_id):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT city FROM user_cities WHERE user_id = ?", (str(user_id),))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
                                                      #alttaki rengi degistir
    def create_graph(self, path, cities, marker_color="purple"):
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()

        ax.add_feature(cfeature.LAND, facecolor='lightgreen')
        ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.RIVERS, edgecolor='blue')
        ax.add_feature(cfeature.LAKES, facecolor='lightblue')

    
        for city in cities:
            coordinates = self.get_coordinates(city)
            if coordinates:
                lat, lng = coordinates
                plt.plot([lng], [lat], color=marker_color, linewidth=1, marker='o', transform=ccrs.Geodetic())
                plt.text(lng + 3, lat + 5, city, horizontalalignment='left', transform=ccrs.Geodetic())

        plt.savefig(path)
        plt.close()

    def draw_distance(self, city1, city2):
        city1_coords = self.get_coordinates(city1)
        city2_coords = self.get_coordinates(city2)
        if not city1_coords or not city2_coords:
            print("Şehir koordinatları bulunamadı.")
            return

        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        ax.set_global()


        plt.plot(
            [city1_coords[1], city2_coords[1]],
            [city1_coords[0], city2_coords[0]],
            color='red', linewidth=2, marker='o', transform=ccrs.Geodetic()
        )
        plt.text(city1_coords[1] + 3, city1_coords[0] + 5, city1, transform=ccrs.Geodetic())
        plt.text(city2_coords[1] + 3, city2_coords[0] + 5, city2, transform=ccrs.Geodetic())

        plt.savefig('distance_map.png')
        plt.close()


if __name__ == "__main__":
    m = DB_Map("database.db")

