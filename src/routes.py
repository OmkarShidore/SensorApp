import os
from flask_cors import CORS
from flask import Flask, request, jsonify
from src.models import Task
from src.utils import logger

app = Flask(__name__)

CORS(app)

#Addition endpoint
@app.route('/add', methods=['GET'])
def add_numbers():
    """
    test route
    """
    num1 = request.args.get('num1')
    num2 = request.args.get('num2')
    result = Task().add(num1, num2)
    return result

# API to insert a new devices
@app.route('/add_device', methods=['POST'])
def add_device():
    """
    organization_id: uuid of the organization record
    device_name: name of the device
    """
    logger(f"Running route add_device")
    organization_id = request.args.get('organization_id')
    device_name = request.args.get('device_name')
    response = Task().add_device(organization_id, device_name, add_default_sensors=True)
    return response

@app.route('/<device_id>/update_device', methods=['POST'])
def update_device(device_id):
    """
    device_id: uuid of the device record
    """
    # Check if the device ID already exists.
    device_exists = Task().device_exists(device_id)
    if not device_exists:
        response = {
                "error": f"The device with ID {device_id} does not exist."
                }
        return jsonify(response), 404
    else:
        new_device_name = request.args.get('new_device_name')
        response = Task().update_device(device_id=device_id, new_device_name=new_device_name)
        return response

@app.route('/get_devices', methods=['GET'])
def get_devices():
    """
    organization_id: uuid of the organization
    device_name: name of the device
    """
    organization_id = request.args.get('organization_id')
    response = Task().get_devices(organization_id)
    return response
    
@app.route('/<device_id>/add_sensor', methods=['POST'])
def add_sensor(device_id):
    """
    Used to add sensor to sensors table.
    device_id: uuid of the device record
    sensor_type: type of the sensor -> pressure/temprature/flow/depth
    """
    # Check if the device ID already exists.
    exists = Task().device_exists(device_id)
    if not exists:
        response = {
                "error": f"The device with ID {device_id} does not exist."
                }
        return jsonify(response), 404
    else:
        sensor_type = request.args.get('sensor_type')
        response = Task().add_sensor(sensor_type=sensor_type, device_id=device_id)
        return response

@app.route('/<device_id>/get_sensors', methods=['GET'])
def get_sensors(device_id):
    """
    Used to add sensor to sensors table.
    device_id: uuid of the device record
    sensor_type: type of the sensor -> pressure/temprature/flow/depth
    """
    # Check if the device ID already exists.
    exists = Task().device_exists(device_id)
    if not exists:
        response = {
                "error": f"The device with ID {device_id} does not exist."
                }
        return jsonify(response), 404
    else:
        response = Task().get_sensors(device_id=device_id)
        return response

@app.route('/<device_id>/<sensor_id>/send_sensor_data', methods=['POST'])
def send_sensor_data(device_id, sensor_id):
    """
    Used to add a sensors data to sensor_data table.
    device_id: uuid of the device record.
    sensor_id: uuid of the device record.
    sensor_type: type of the sensor -> pressure/temprature/flow/depth
    """

    # Check if the device ID already exists.
    sensor_exists = Task().sensor_exists(device_id, sensor_id)
    if not sensor_exists:
        response = {
                "error": f"The device_id: {device_id} or sensor_id: {sensor_id}does not exist."
                }
        return jsonify(response), 404
    else:
        value = request.args.get('value')
        response = Task().add_sensor_data(sensor_id=sensor_id, value=value)
        return response
    
@app.route('/<device_id>/<sensor_id>/get_sensor_data', methods=['GET'])
def get_sensor_data(device_id, sensor_id):
    """
    Used to get sensors data from sensor_data table
    device_id: uuid of the device record.
    sensor_id: uuid of the device record.
    start_date: queryable parameter on created_date of sensors_data 
    end_date: queryable parameter on created_date of sensors_data 
    """
    sensor_exists = Task().sensor_exists(device_id, sensor_id)
    if not sensor_exists:
        response = {
                "error": f"The device_id: {device_id} or sensor_id: {sensor_id}does not exist."
                }
        return jsonify(response), 404
    else:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        response = Task().get_sensor_data(sensor_id, start_date, end_date)
        return response

if __name__ == '__main__':
    if "LOCAL_RUN" in os.environ and os.environ["LOCAL_RUN"] == "True":
        app.run()