import geopandas
import json
import time

from celery.utils.log import get_task_logger
from celery_app import app


from services import create_bbox_matrix, add_result_values


logger = get_task_logger(__name__)


@app.task()
def compute_task_noise(request_json):
    time.sleep(10) # simulate long running task

    result_polygons = create_bbox_matrix(request_json['bbox'], 0.0002)
    gds = geopandas.GeoSeries(result_polygons)
    gdf = geopandas.GeoDataFrame(geometry=gds, crs="EPSG:4326")

    # each polygon set attribute for result
    gdf = add_result_values(gdf, request_json['calculation_settings'], "noise")

    return json.loads(gdf.to_json())


def compute_task_wind(request_json):
    time.sleep(10) # simulate long running task


    result_polygons = create_bbox_matrix(request_json['bbox'], 0.0002)
    gds = geopandas.GeoSeries(result_polygons)
    gdf = geopandas.GeoDataFrame(geometry=gds, crs="EPSG:4326")

    # each polygon set attribute for result
    gdf = add_result_values(gdf, request_json['calculation_settings'], "wind")

    return json.loads(gdf.to_json())

