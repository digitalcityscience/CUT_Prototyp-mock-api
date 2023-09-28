import geopandas
import pandas as pd
from shapely.geometry import Polygon
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

    bbox_pol = Polygon(request_json["bbox"])
    input_gdf = city_blocks_gdf.clip(bbox_pol)

    input_gdf["value"] = input_gdf.apply(
        lambda row: get_mock_noise_value(row, request_json["calculation_settings"]),
        axis=1,
    )

    return json.loads(input_gdf.to_json())


@app.task()
def compute_task_wind(request_json):
    time.sleep(10)  # simulate long running task

    bbox_pol = Polygon(request_json["bbox"])
    input_gdf = city_blocks_gdf.clip(bbox_pol)

    input_gdf["value"] = input_gdf.apply(
        lambda row: get_mock_wind_value(row, request_json["calculation_settings"]),
        axis=1,
    )

    # sort values into bins of [0, 0.2, 0.4, 0.6, 0.8, 1]
    input_gdf["value"] = pd.cut(
        input_gdf["value"], [0, 0.2, 0.4, 0.6, 0.8, 1], labels=[0.2, 0.4, 0.6, 0.8, 1]
    )
    input_gdf["value"] = input_gdf["value"].astype("float")
    input_gdf["value"] = input_gdf["value"].fillna(0)

    return json.loads(input_gdf.to_json())
