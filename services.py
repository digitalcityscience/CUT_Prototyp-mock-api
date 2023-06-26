from typing import List
import math
from shapely.geometry import box, Polygon
import random

# creates a matrix of bboxes covering the project area polygon
def create_bbox_matrix(bbox_coords, bbox_length) -> List[box]:
    polygon = Polygon(bbox_coords)
    bbox_matrix = []
    polygon_envelop = polygon.exterior.envelope

    envelop_minX = min(polygon_envelop.exterior.xy[0])
    envelop_maxX = max(polygon_envelop.exterior.xy[0])
    envelop_minY = min(polygon_envelop.exterior.xy[1])
    envelop_maxY = max(polygon_envelop.exterior.xy[1])

    # number of rows and cols of bbox matrix
    max_cols = math.floor((envelop_maxX - envelop_minX) / bbox_length) + 1
    max_rows = math.floor((envelop_maxY - envelop_minY) / bbox_length) + 1

    for row in range(0, max_rows):
        minY = envelop_minY + bbox_length * row
        maxY = minY + bbox_length
        for col in range(0, max_cols):
            minX = envelop_minX + bbox_length * col
            maxX = minX + bbox_length

            # minX, minY, maxX, maxY
            bbox = box(minX, minY, maxX, maxY)
            if polygon.intersection(bbox):
                # only add bbox to matrix, if actually intersecting with the project area polygon
                bbox_matrix.append(bbox)

    return bbox_matrix


def add_result_values(gdf, calculation_settings, simulation):

    
    def get_random_wind_value(wind_speed):
        possible_values = [0, 0.2, 0.4]
        if wind_speed >= 15:
            possible_values.append(0.6)
        if wind_speed >= 30:
            possible_values.append(0.8)
            possible_values.pop(0)
        if wind_speed >= 45:
            possible_values.append(1)
            possible_values.pop(0)
        
        print("possible wind values", possible_values)
        return random.choice(possible_values)
    
    def get_random_noise_value(max_speed):
        possible_values = [0, 1, 2, 3]
        if max_speed >= 15:
            possible_values.append(4)
        if max_speed > 30:
            possible_values.append(5)
            possible_values.pop(0)
        if max_speed > 50:
            possible_values.append(6)
            possible_values.pop(0)
        if max_speed > 60:
            possible_values.append(7)
            possible_values.pop(0)
        
        return random.choice(possible_values)
    
    # add random result values to each feature
    if simulation == "noise":
        gdf["value"] = gdf.apply(lambda row: get_random_noise_value(calculation_settings['max_speed']), axis=1)
    if simulation == "wind":
        gdf["value"] = gdf.apply(lambda row: get_random_wind_value(calculation_settings['wind_speed']), axis=1)

    return gdf
    



if __name__ == "__main__":
    request_data = {
        "simulation": "noise",
        "bbox": [
            [
              10.010449058044909,
              53.533773119496075
            ],
            [
              10.011056083791818,
              53.533773119496075
            ],
            [
              10.011056083791818,
              53.53398760073027
            ],
            [
              10.010449058044909,
              53.53398760073027
            ],
            [
              10.010449058044909,
              53.533773119496075
            ]
          ],
        "calculation_settings": {
            "max_speed": 70,
            "wind_direction": 15
        }
    }
