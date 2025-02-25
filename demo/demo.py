import json

import requests

local = True

local_url = 'http://127.0.0.1:8000'
remote_url = 'http://ec2-54-171-174-135.eu-west-1.compute.amazonaws.com:8000'

if local:
    url = local_url
else:
    url = remote_url


def test_create_event():
    event = {
        "device_name": "Temperature",
        "description": "Temperature above 25C"
    }
    response = requests.post(f'{url}/event', json=event)
    print('Event 1:', response.json())

    event = {
        "device_name": "Humidity",
        "description": "Humidity above 50%"
    }
    response = requests.post(f'{url}/event', json=event)
    print('Event 2:', response.json())

    event = {
        "device_name": "Distance",
        "description": "Distance below 10cm"
    }
    response = requests.post(f'{url}/event', json=event)
    print('Event 3:', response.json())

    event = {
        "device_name": "CO2",
        "description": "CO2 above 1000ppm"
    }
    response = requests.post(f'{url}/event', json=event)
    print('Event 4:', response.json())

    event = {
        "device_name": "Pump",
        "description": "Pump on"
    }
    response = requests.post(f'{url}/event', json=event)
    print('Event 5:', response.json())

    event = {
        "device_name": "Alarm",
        "description": "Alarm on"
    }
    response = requests.post(f'{url}/event', json=event)
    print('Event 6:', response.json())

    event = {
        "device_name": "Light",
        "description": "Light on"
    }
    response = requests.post(f'{url}/event', json=event)
    print('Event 7:', response.json())

    event = {
        "device_name": "Window",
        "description": "Window open"
    }
    response = requests.post(f'{url}/event', json=event)
    print('Event 8:', response.json())

    event = {
        "device_name": "Fan",
        "description": "Fan on"
    }
    response = requests.post(f'{url}/event', json=event)
    print('Event 9:', response.json())

    return


def test_get_event():
    response = requests.get(f'{url}/event')
    print('Events:', response.json())
    return


def test_create_sensor_data():
    sensor_data = {
        "sensor": "Temperature",
        "value": 25.0
    }
    response = requests.post(f'{url}/sensor-data', json=sensor_data)
    print('Sensor Data 1:', response.json())

    sensor_data = {
        "sensor": "Humidity",
        "value": 50.0
    }
    response = requests.post(f'{url}/sensor-data', json=sensor_data)
    print('Sensor Data 2:', response.json())

    sensor_data = {
        "sensor": "Distance",
        "value": 10.0
    }
    response = requests.post(f'{url}/sensor-data', json=sensor_data)
    print('Sensor Data 3:', response.json())

    sensor_data = {
        "sensor": "CO2",
        "value": 1000.0
    }
    response = requests.post(f'{url}/sensor-data', json=sensor_data)
    print('Sensor Data 4:', response.json())

    return


def test_get_sensor_data():
    response = requests.get(f'{url}/sensor-data/Temperature')
    print('Temperature:', response.json())
    return


print('Testing create event')
test_create_event()

print('Testing get event')
test_get_event()

print('Testing create sensor data')
test_create_sensor_data()

print('Testing get sensor data')
test_get_sensor_data()
