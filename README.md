# CUT_Prototyp-mock-api
mocking wind and noise services

### Trigger mock WIND task
post to /noise/trigger_calculation to create new noise task. 
post a json payload like this 
```
{
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
            "traffic_quota": 0.5
        }
```


### Trigger mock WIND task
post to /wind/trigger_calculation to create new noise task. 
post a json payload like this 
```
{
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
            "wind_speed": 70,
            "wind_direction": 0.5
        }
```


The api will return a {"taskId": "SOME_TASK_ID" } reponse. 

## Task status
Use the task id to ask the the tasks status via a GET request to "/tasks/<task_id>/status" 
will return one of these options

```
    *PENDING*
        The task is waiting for execution. 
        OR TASK doesnt exist (long story, ..google it)
    *STARTED*
        The task has been started.
    *RETRY*
        The task is to be retried, possibly because of failure.
    *FAILURE*
        The task raised an exception, or has exceeded the retry limit.
        The :attr:`result` attribute then contains the
        exception raised by the task.
    *SUCCESS*
        The task executed successfully.  The :attr:`result` attribute
        then contains the tasks return value.
```


## TASK RESULT
use the task id to get task result via GET request to "/tasks/<task_id>"
will return an object like
```
{
        'taskId': async_result.id,
        'taskState': async_result.state,
        'result': YOUR_RESULT_AS_GEOJSON
}
```
