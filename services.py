def map2range(value, low, high, new_low, new_high):
    """map a value from one range to another"""
    return min(value * 1.0 / (high - low + 1) * (new_high - new_low + 1), new_high)


def get_mock_noise_value(row, calculation_settings) -> int:
    """
    formula for mock noise value
    depending on the cityblocks highway and buildings proximity/abundancy value
    (highway/(buildings/4)) * speed*5 * amount*4
    Traffic noise increases with highway, max_speed and traffic_quota values
    Traffic noise decreases, the higher the building value

    map to end value of 0-7 (int!)
    max values in city_blocks
        - buildings: 15 (edge cases are much higher, but ignored)
        - highways: 15 (edge cases are much higher, but ignored)
    """
    # max values for traffic_quota, speed, city_blocks: highways, building
    mock_value = (
        (min(row["highway"], 15) / (max(1, (row["building"] / 4))))
        * calculation_settings["max_speed"]
        * 5
        * (calculation_settings["traffic_quota"] / 100)
        * 4
    )

    # 75km/h max_speed, max highway val ==15, min building val ==1
    max_mock_value = 75 * 1 * 4 * (15 / 1)
    min_mock_value = 25 * 5 * 0.25 * 4 * 1

    return round(map2range(mock_value, min_mock_value, max_mock_value, 0, 7))


def get_mock_wind_value(row, calculation_settings) -> int:
    """
    formula for mock wind value
    depending on the cityblocks' highway and buildings proximity/abundancy
    Assuming that buildings can block wind, while highways/large streets lead to more wind exposure
    (highway/(buildings/8)) * wind_speed
    Wind-exposure increases with highway and wind_speed values
    Wind-exposure decreases with the buildings value

    map to value of 0-1 (float!)
    max values in city_blocks
        - buildings: 15  (edge cases are much higher, but ignored)
        - highways: 15  (edge cases are much higher, but ignored)
    """
    mock_value = (
        min(row["highway"], 15) / (max(1, (row["building"] / 8)))
    ) * calculation_settings["wind_speed"]

    # 80km/h wind, max highway val, min building val.
    max_mock_value = 80 * (15 / 1)

    return map2range(mock_value, 0, max_mock_value, 0, 1)
