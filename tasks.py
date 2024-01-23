import geopandas
import pandas as pd
from shapely.geometry import box
import json
import time

from celery.utils.log import get_task_logger
from celery_app import app

from services import get_mock_noise_value, get_mock_wind_value


logger = get_task_logger(__name__)
city_blocks_gdf = geopandas.read_file("./data/hamburg_city_blocks.gpkg")


@app.task()
def compute_task_noise(request_json):
    time.sleep(10)  # simulate long running task

    bbox_pol = box(*geopandas.GeoDataFrame.from_features(request_json["buildings"]["features"]).total_bounds)
    input_gdf = city_blocks_gdf.clip(bbox_pol)

    roads_gdf = geopandas.GeoDataFrame.from_features(request_json["roads"]["features"])

    max_speed = roads_gdf["max_speed"].mean(),
    traffic_quota = 100

    if request_json.get("max_speed", None) is not None:
        max_speed = request_json["max_speed"]

    if request_json.get("traffic_quota", None) is not None:
        traffic_quota = request_json["traffic_quota"]

    calculation_settings = {
        "max_speed": max_speed,
        "traffic_quota": traffic_quota
    }

    input_gdf["value"] = input_gdf.apply(
        lambda row: get_mock_noise_value(row, calculation_settings),
        axis=1,
    )

    return json.loads(input_gdf.to_json())


@app.task()
def compute_task_wind(request_json):
    time.sleep(10)  # simulate long running task

    bbox_pol = box(*geopandas.GeoDataFrame.from_features(request_json["buildings"]["features"]).total_bounds)
    input_gdf = city_blocks_gdf.clip(bbox_pol)

    calculation_settings = {
        "wind_speed": request_json["wind_speed"],
        "wind_direction": request_json["wind_direction"]
    }

    input_gdf["value"] = input_gdf.apply(
        lambda row: get_mock_wind_value(row, calculation_settings),
        axis=1,
    )

    # sort values into bins of [0, 0.2, 0.4, 0.6, 0.8, 1]
    input_gdf["value"] = pd.cut(
        input_gdf["value"], [0, 0.2, 0.4, 0.6, 0.8, 1], labels=[0.2, 0.4, 0.6, 0.8, 1]
    )
    input_gdf["value"] = input_gdf["value"].astype("float")
    input_gdf["value"] = input_gdf["value"].fillna(0)

    return json.loads(input_gdf.to_json())
