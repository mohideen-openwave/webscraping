import scrapy
import re
from scrapy_playwright.page import PageMethod
from datetime import datetime
import math


class PeddleSpider(scrapy.Spider):
    name = "peddle"
    
    def start_requests(self):
        yield scrapy.FormRequest(
            url=f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{self.vin}',
            method='GET',
            callback=self.parse_vin_decoded,
            formdata={
                'format': 'json',
            },
        )

    def parse_vin_decoded(self, response):
        json_response = response.json()
        details = {vehicle_property['Variable']: vehicle_property['Value'] for vehicle_property in json_response['Results']}

        partial_result = {
            'vin_number': self.vin,
            'condition': self.condition,
            'mileage': self.mileage,
            'zip_code': self.zip_code,
        }

        if 'Make' in details:
            partial_result['make'] = details['Make']

        if 'Model' in details:
            partial_result['model'] = details['Model']

        if 'Model Year' in details:
            partial_result['year'] = details['Model Year']

        if 'Trim' in details:
            partial_result['trim'] = details['Trim']

        if 'Body Class' in details:
            partial_result['body_type'] = details['Body Class']

        if 'Transmission Style' in details:
            partial_result['transmission'] = details['Transmission Style']

        if 'Engine Model' in details:
            partial_result['engine'] = details['Engine Model']



        yield scrapy.Request(
            url='https://sell.peddle.com/api/anonymous-token',
            method='POST',
            callback=self.parse_peddle_token,
            headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
            },
            cb_kwargs={
                'result': partial_result,
            },
        )
 


    def parse_peddle_token(self, response, result):
        json_response = response.json()

        token = json_response['access_token']
        token_type = json_response['token_type']

        yield scrapy.Request(
            url=f'https://service.peddle.com/universal/v2/vins/{self.vin}',
            callback=self.parse_peddle_vin_decoded,
            headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': f'{token_type} {token}',
            },
            cb_kwargs={
                'token': token,
                'token_type': token_type,
                'result': result,
            },
        )

    def parse_peddle_vin_decoded(self, response, token, token_type, result):
        json_response = response.json()

        year_id = json_response['year']['id'] if 'year' in json_response else ''
        make_id = json_response['make']['id'] if 'make' in json_response else ''

        model_id = json_response['model']['id'] if 'model' in json_response else ''
        model_info = json_response['model'] if 'model' in json_response else {}

        body_type_id = model_info['body_type']['id'] if 'body_type' in model_info else ''
        cab_type_id = model_info['cab_type']['id'] if 'cab_type' in model_info else ''
        door_count = model_info['door_count'] if 'door_count' in model_info else ''

        trim_id = json_response['trim']['id'] if 'trim' in json_response else ''
        trim_info = json_response['trim'] if 'trim' in json_response else {}

        body_style_id = trim_info['body_style']['id'] if 'body_style' in trim_info else ''
        fuel_type_id = trim_info['fuel_type']['id'] if 'fuel_type' in trim_info else ''

        yield scrapy.http.JsonRequest(
            url=f'https://service.peddle.com/seller/v1/instant-offers',
            callback=self.parse_peddle_offer,
            headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': f'{token_type} {token}',
                'content-type': 'application/json',
            },
            data={
                'vehicle': {
                    'year_id': year_id,
                    'make_id': make_id,
                    'model_id': model_id,
                    'body_type_id': body_type_id,
                    'cab_type_id': cab_type_id,
                    'door_count': door_count,
                    'trim_id': trim_id,
                    'body_style_id': body_style_id,
                    'fuel_type_id': fuel_type_id,
                    'vin': self.vin,
                    'usage': 'unknown',
                    'location': {
                        'zip_code': self.zip_code,
                    },
                    'ownership': {
                        'type': 'owned',
                        'title_type': 'clean',
                    },
                    'condition': {
                        'mileage': self.mileage,
                        'drivetrain_condition': 'drives',
                        'key_and_keyfob_available': 'yes',
                        'all_tires_inflated': 'yes',
                        'flat_tires_location': {
                            'driver_side_view': {
                                'front': False,
                                'rear': False,
                            },
                            'passenger_side_view': {
                                'front': False,
                                'rear': False,
                            },
                        },
                        'wheels_removed': 'no',
                        'wheels_removed_location': {
                            'driver_side_view': {
                                'front': False,
                                'rear': False,
                            },
                            'passenger_side_view': {
                                'front': False,
                                'rear': False,
                            },
                        },
                        'body_panels_intact': 'yes',
                        'body_panels_damage_location': {
                            'driver_side_view': {
                                'front_top': False,
                                'front_bottom': False,
                                'front_door_top': False,
                                'front_door_bottom': False,
                                'rear_door_top': False,
                                'rear_door_bottom': False,
                                'rear_top': False,
                                'rear_bottom': False,
                            },
                            'passenger_side_view': {
                                'front_top': False,
                                'front_bottom': False,
                                'front_door_top': False,
                                'front_door_bottom': False,
                                'rear_door_top': False,
                                'rear_door_bottom': False,
                                'rear_top': False,
                                'rear_bottom': False,
                            },
                            'front_view': {
                                'driver_side_top': False,
                                'driver_side_bottom': False,
                                'passenger_side_top': False,
                                'passenger_side_bottom': False,
                            },
                            'rear_view': {
                                'driver_side_top': False,
                                'driver_side_bottom': False,
                                'passenger_side_top': False,
                                'passenger_side_bottom': False,
                            },
                            'top_view': {
                                'driver_side_front': False,
                                'passenger_side_front': False,
                                'driver_side_front_roof': False,
                                'passenger_side_front_roof': False,
                                'driver_side_rear_roof': False,
                                'passenger_side_rear_roof': False,
                                'driver_side_rear': False,
                                'passenger_side_rear': False,
                            },
                        },
                        'body_damage_free': 'yes',
                        'body_damage_location': {
                            'driver_side_view': {
                                'front_top': False,
                                'front_bottom': False,
                                'front_door_top': False,
                                'front_door_bottom': False,
                                'rear_door_top': False,
                                'rear_door_bottom': False,
                                'rear_top': False,
                                'rear_bottom': False,
                            },
                            'passenger_side_view': {
                                'front_top': False,
                                'front_bottom': False,
                                'front_door_top': False,
                                'front_door_bottom': False,
                                'rear_door_top': False,
                                'rear_door_bottom': False,
                                'rear_top': False,
                                'rear_bottom': False,
                            },
                            'front_view': {
                                'driver_side_top': False,
                                'driver_side_bottom': False,
                                'passenger_side_top': False,
                                'passenger_side_bottom': False,
                            },
                            'rear_view': {
                                'driver_side_top': False,
                                'driver_side_bottom': False,
                                'passenger_side_top': False,
                                'passenger_side_bottom': False,
                            },
                            'top_view': {
                                'driver_side_front': False,
                                'passenger_side_front': False,
                                'driver_side_front_roof': False,
                                'passenger_side_front_roof': False,
                                'driver_side_rear_roof': False,
                                'passenger_side_rear_roof': False,
                                'driver_side_rear': False,
                                'passenger_side_rear': False,
                            },
                        },
                        'mirrors_lights_glass_intact': 'yes',
                        'mirrors_lights_glass_damage_location': {
                            'driver_side_view': {
                                'front_top': False,
                                'front_bottom': False,
                                'front_door_top': False,
                                'front_door_bottom': False,
                                'rear_door_top': False,
                                'rear_door_bottom': False,
                                'rear_top': False,
                                'rear_bottom': False,
                            },
                            'passenger_side_view': {
                                'front_top': False,
                                'front_bottom': False,
                                'front_door_top': False,
                                'front_door_bottom': False,
                                'rear_door_top': False,
                                'rear_door_bottom': False,
                                'rear_top': False,
                                'rear_bottom': False,
                            },
                            'front_view': {
                                'driver_side_top': False,
                                'driver_side_bottom': False,
                                'passenger_side_top': False,
                                'passenger_side_bottom': False,
                            },
                            'rear_view': {
                                'driver_side_top': False,
                                'driver_side_bottom': False,
                                'passenger_side_top': False,
                                'passenger_side_bottom': False,
                            },
                            'top_view': {
                                'driver_side_front': False,
                                'passenger_side_front': False,
                                'driver_side_front_roof': False,
                                'passenger_side_front_roof': False,
                                'driver_side_rear_roof': False,
                                'passenger_side_rear_roof': False,
                                'driver_side_rear': False,
                                'passenger_side_rear': False,
                            },
                        },
                        'interior_intact': 'yes',
                        'flood_fire_damage_free': 'yes',
                        'engine_transmission_condition': 'intact',
                    },
                },
            },
            cb_kwargs={
                'result': result,
            },
        )

    def parse_peddle_offer(self, response, result):
        json_response = response.json()

        price = json_response['presented_offer_amount']

        result['datetime'] = datetime.utcnow()
        result['source'] = 'Peddle'
        result['price'] = price

        yield result
