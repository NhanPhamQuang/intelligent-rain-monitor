import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB  = os.getenv("MONGO_DB", "weather_monitor")

APP_NAME = "Intelligent Rain Monitor"
VERSION = "2.0.0"

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "lightgbm_rain_tomorrow_bundle.joblib")
CSV_DATA_PATH = os.path.join(os.path.dirname(__file__), "weatherAUS.csv")

WEATHER_FEATURES = [
    "MinTemp", "MaxTemp", "Rainfall",
    "Humidity3pm", "Pressure3pm",
    "WindSpeed3pm", "Sunshine",
]

ALL_LOCATIONS = [
    "Albury", "BadgerysCreek", "Cobar", "CoffsHarbour", "Moree",
    "Newcastle", "NorahHead", "NorfolkIsland", "Penrith", "Richmond",
    "Sydney", "SydneyAirport", "WaggaWagga", "Williamtown",
    "Wollongong", "Canberra", "Tuggeranong", "MountGinini", "Ballarat",
    "Bendigo", "Sale", "MelbourneAirport", "Melbourne", "Mildura",
    "Nhil", "Portland", "Watsonia", "Dartmoor", "Brisbane", "Cairns",
    "GoldCoast", "Townsville", "Adelaide", "MountGambier", "Nuriootpa",
    "Woomera", "Albany", "Witchcliffe", "PearceRAAF", "PerthAirport",
    "Perth", "SalmonGums", "Walpole", "Hobart", "Launceston",
    "AliceSprings", "Darwin", "Katherine", "Uluru",
]
