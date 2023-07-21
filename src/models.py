import os
import json
from src.utils import get_uuid4
from datetime import datetime
from src.resource_clients import PSQLClient
from flask import jsonify
from src.utils import logger

class Task():
    def __init__(self) -> None:
        #Query's
        self.insert_device_query = "INSERT INTO devices (device_id, device_name, organization_id) VALUES (%s, %s, %s);"
        self.insert_sensor_query = "INSERT INTO sensors (sensor_id, sensor_type, device_id) VALUES (%s, %s, %s);"
        self.device_exists_query = "SELECT EXISTS (SELECT 1 FROM devices WHERE device_id = %(device_id)s)"
        self.device_update_query = "UPDATE devices SET device_name = %s, modified_date = %s WHERE device_id = %s;"
        self.sensor_exists_query = "SELECT EXISTS (SELECT 1 FROM sensors WHERE sensor_id = %(sensor_id)s)"
        self.insert_sensor_data_query = "INSERT INTO sensor_data (sensor_id, value) VALUES (%s, %s);"
        self.select_sensor_data_query = "SELECT * FROM sensor_data WHERE sensor_id = %s"
        self.select_devices_data_query = "SELECT * FROM devices;"
        self.select_sensors_query = "SELECT * FROM sensors WHERE device_id = %s;"
        #Custom PSQL Client
        self.psql_client = PSQLClient()

    def add(self, num1, num2):
        """
        Test route method
        Return addition of num1 & num2
        """
        addition = int(num1) + int(num2)
        result = {
            'num1': num1,
            'num2': num2,
            'result': addition
        }
        return jsonify(result), 201
    
    def add_sensor(self, sensor_type, device_id, jsonify_response=True):
        """
        Method to add sensor to sensors table
        Return sensor properties like it's uuid and type
        """
        sensor_id = get_uuid4()
        values = (sensor_id, sensor_type, device_id)
        self.psql_client.run_query(sql=self.insert_sensor_query, values=values)
        response = {
                    "sensor":{
                    "sensor_id": sensor_id,
                    "sensor_type": sensor_type
                    }
                }
        if jsonify_response:
            return jsonify(response), 201
        else:
            return response
    
    def add_sensor_data(self, sensor_id, value):
        """
        Method to add sensor data to sensors_data table
        Return sensor id and the value inserted
        """
        values = (sensor_id, value)
        self.psql_client.run_query(sql=self.insert_sensor_data_query, values=values)
        response = {
                    "sensor_data":{
                    "sensor_id": sensor_id,
                    "value": value
                    }
                }
        return jsonify(response), 201
        
        

    def add_device(self, organization_id, device_name, add_default_sensors=True):
        """
        Method to add device to devices table
        organization_id: organization_id (uuid) from organizations table
        device_name: name of the device
        add_default_sensors=True: add temrature and pressure sensor if set True
        """
        logger(f"Running Task add_device ")
        

        #Add Device
        device_id = get_uuid4()

        values = (device_id, device_name, organization_id)
        self.psql_client.run_query(sql=self.insert_device_query, values=values)
        
        response = {
                    "device": {
                        "device_id": device_id,
                        "device_name": device_name
                    }
                }
        #Add Sensor
        if add_default_sensors:
            resp1 = self.add_sensor(sensor_type="temprature", device_id=device_id, jsonify_response=False)
            resp2 = self.add_sensor(sensor_type="pressure", device_id=device_id, jsonify_response=False)

            response["device"]["sensors"] = [resp1, resp2]
            
        return jsonify(response), 201
    
    def device_exists(self, device_id):
        """
        Method to check if device_id (uuid) exists in devices table
        Return boolean True or False
        """
        values = {'device_id': device_id}
        exists = self.psql_client.data_exists(sql=self.device_exists_query, values=values)
        return exists
    
    def sensor_exists(self, device_id, sensor_id):
        """
        Method to check if sensor (uuid) exists in sensors table
        Return boolean True or False
        """
        exists = False
        device_exists = self.device_exists(device_id)
        if device_exists:
            values = {'sensor_id': sensor_id}
            sensor_exists = self.psql_client.data_exists(sql=self.sensor_exists_query, values=values)
            if sensor_exists:
                exists = True
        return exists
    
    def update_device(self, device_id, new_device_name):
        """
        Method to update poperties of device in devices table
        device_id: existing device_id (uuid) in devices table
        new_device_name: replace the current device_name with new_device_name in the record.
        """
        current_datetime = datetime.now()
        values = (new_device_name, current_datetime, device_id)
        self.psql_client.run_query(sql=self.device_update_query, values=values)
        response = {
                    "device": {
                        "device_id": device_id,
                        "device_name": new_device_name
                    }
                }
        return jsonify(response), 201
    

    def get_sensor_data(self, sensor_id, start_date, end_date):
        """
        Method to update poperties of device in devices table.
        device_id: uuid of the device record.
        sensor_id: uuid of the device record.
        start_date: queryable parameter on created_date of sensors_data 
        end_date: queryable parameter on created_date of sensors_data 
        """
        values = (sensor_id,)
        select_query = self.select_sensor_data_query

        if start_date or end_date:
            select_query = select_query+ " AND"
        if start_date:
            select_query = select_query + " created_date >= %s"
            values = (sensor_id, start_date,)
        if start_date and end_date:
            select_query = select_query + " AND created_date <= %s"
            values = (sensor_id, start_date, end_date)
        if not start_date and end_date:
            select_query = select_query + " created_date <= %s"
            values = (sensor_id, end_date,)
        select_query = select_query + ";"
        response = self.psql_client.select_query(sql=select_query, values=values)
        return jsonify(response), 201

    def get_devices(self, organization_id):
        """
        Method to retrive all devices of an organization
        organization_id: uuid of an organization in organizations table
        """
        values = (organization_id,)
        select_query = self.select_devices_data_query[:-1] + " WHERE organization_id = %s;"
        response = self.psql_client.select_query(sql=select_query, values=values)
        return jsonify(response), 201
    
    def get_sensors(self, device_id):
        """
        Method to retrive all devices of an organization
        organization_id: uuid of an organization in organizations table
        """
        values = (device_id,)
        response = self.psql_client.select_query(sql=self.select_sensors_query, values=values)
        return jsonify(response), 201



        


