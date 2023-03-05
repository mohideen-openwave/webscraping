import scrapy
import re
from scrapy_playwright.page import PageMethod
from datetime import datetime
import math
import json
import requests
 

 

class DrivewaySpider(scrapy.Spider):
    name = "driveway"
    drive_url = f'https://api-gateway.driveway.com/sell/v8/offer?dealershipCode=cdjr-pocatello&saleType=SELL&key=e6c1852eb5124b1890fbd17ad53e870a'
    
        
    def start_requests(self):
        
        payload = {
            "email": "asdfasd@ld.com",
            "phone": "3333333330",
            "firstName": "sdfsadfasd",
            "lastName": "dsafadsf",
            "location": {
                "postalCode": self.zip_code,
                "distanceInMiles": 0,
                "withinMarket": False
            },
            "inspectionPreferences": {
                "contactPreference": "EMAIL"
            },
            "vehicle": {
                "vin": self.vin,
                "year": 2015,
                "make": "Ford",
                "model": "F150",
                "availableTrims": [],
                "selectedTrim": {
                    "vifnum": 10331,
                    "name": "King Ranch Supercrew 4WD",
                    "id": "2015300746"
                },
                "selectedColor": {
                    "vifnum": 10331,
                    "code": "N1",
                    "title": "Blue Jeans Metallic",
                    "simpletitle": "Blue",
                    "rgb1": "092637"
                },
                "options": [
                    {
                        "selected": False,
                        "name": "Navigation System"
                    },
                    {
                        "selected": False,
                        "name": "FX4 Off-Road Package"
                    },
                    {
                        "selected": False,
                        "name": "Chrome Package"
                    },
                    {
                        "selected": False,
                        "name": "20-Inch Wheels"
                    },
                    {
                        "selected": False,
                        "name": "Power Moonroof"
                    },
                    {
                        "selected": True,
                        "name": "3.5L V6 Ecoboost"
                    },
                    {
                        "selected": False,
                        "name": "Roush F-150"
                    },
                    {
                        "selected": False,
                        "name": "Roush F-150 SC"
                    }
                ],
                "availableColors": [
                    {
                        "vifnum": -1,
                        "code": "Black",
                        "title": "Black",
                        "simpletitle": "Black",
                        "rgb1": "2D2926"
                    },
                    {
                        "vifnum": -1,
                        "code": "White",
                        "title": "White",
                        "simpletitle": "White",
                        "rgb1": "FFFFFF"
                    },
                    {
                        "vifnum": -1,
                        "code": "Gray",
                        "title": "Gray",
                        "simpletitle": "Gray",
                        "rgb1": "989898"
                    },
                    {
                        "vifnum": -1,
                        "code": "Silver",
                        "title": "Silver",
                        "simpletitle": "Silver",
                        "rgb1": "DFE0DF"
                    },
                    {
                        "vifnum": -1,
                        "code": "Blue",
                        "title": "Blue",
                        "simpletitle": "Blue",
                        "rgb1": "4173AD"
                    },
                    {
                        "vifnum": -1,
                        "code": "Red",
                        "title": "Red",
                        "simpletitle": "Red",
                        "rgb1": "DA4548"
                    },
                    {
                        "vifnum": -1,
                        "code": "Brown",
                        "title": "Brown",
                        "simpletitle": "Brown",
                        "rgb1": "75523E"
                    },
                    {
                        "vifnum": -1,
                        "code": "Beige",
                        "title": "Beige",
                        "simpletitle": "Beige",
                        "rgb1": "CAB0A2"
                    },
                    {
                        "vifnum": -1,
                        "code": "Gold",
                        "title": "Gold",
                        "simpletitle": "Gold",
                        "rgb1": "C18F55"
                    },
                    {
                        "vifnum": -1,
                        "code": "Green",
                        "title": "Green",
                        "simpletitle": "Green",
                        "rgb1": "74885B"
                    },
                    {
                        "vifnum": -1,
                        "code": "Yellow",
                        "title": "Yellow",
                        "simpletitle": "Yellow",
                        "rgb1": "FDB853"
                    },
                    {
                        "vifnum": -1,
                        "code": "Orange",
                        "title": "Orange",
                        "simpletitle": "Orange",
                        "rgb1": "D87A3F"
                    },
                    {
                        "vifnum": -1,
                        "code": "Pink",
                        "title": "Pink",
                        "simpletitle": "Pink",
                        "rgb1": "F7B7B6"
                    },
                    {
                        "vifnum": -1,
                        "code": "Burgundy",
                        "title": "Burgundy",
                        "simpletitle": "Burgundy",
                        "rgb1": "771A17"
                    },
                    {
                        "vifnum": -1,
                        "code": "Bronze",
                        "title": "Bronze",
                        "simpletitle": "Bronze",
                        "rgb1": "A3492E"
                    },
                    {
                        "vifnum": -1,
                        "code": "Purple",
                        "title": "Purple",
                        "simpletitle": "Purple",
                        "rgb1": "6D4789"
                    },
                    {
                        "vifnum": -1,
                        "code": "Tan",
                        "title": "Tan",
                        "simpletitle": "Tan",
                        "rgb1": "BCB295"
                    },
                    {
                        "vifnum": -1,
                        "code": "Turquoise",
                        "title": "Turquoise",
                        "simpletitle": "Turquoise",
                        "rgb1": "53BBB2"
                    },
                    {
                        "vifnum": -1,
                        "code": "Other",
                        "title": "Other",
                        "simpletitle": "Other",
                        "rgb1": "FFFFFF"
                    }
                ],
                "imageUrl": "https://d2ivfcfbdvj3sm.cloudfront.net/6fd260a869c389e6f8668ba55dfb5f70ed0d4a500b163c8c88cc1df8abcb/color_0640_032_png/MY2015/10331/10331_cc0640_032_N1.png",
                "condition": {
                    "overallCondition": "GREAT",
                    "mileage": self.mileage,
                    "warningLights": True,
                    "accidents": True,
                    "smokedIn": True,
                    "activeFinance": {
                        "type": "LOAN",
                        "estimatedRemaining": 0,
                        "lenderId": "OTX"
                    },
                    "numKeys": "ONE"
                },
                "licensePlate": "JTDKARFU6K3087621",
                "alternatives": []
            }
        }
        headers = {
            'Content-type': 'application/json',
            'User-Agent':"My User Agent 1.0",
            'Accept': '*/*',
            "Postman-Token": "2400114c-e7fc-486d-ad32-b2aee2866452",
            'Host': 'api-gateway.driveway.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Length': '6439',
        }
       
        yield scrapy.Request(
            self.drive_url, 
            callback=self.parse_vin_driveway, 
            method="POST", 
            body=json.dumps(payload), 
            headers=headers
            )
        

    def parse_vin_trim_driveway(self, response):
        #Response from api calls
        json_response = response.json()
        details = {vehicle_property['Variable']: vehicle_property['Value'] for vehicle_property in json_response['Results']}
        self.logger.info('===FullDetails====parse_vin_trim_driveway======Got successful response from {}'.format(json_response))
        partial_result = {
            'vin_number': self.vin,
            'condition': self.condition,
            'mileage': self.mileage,
            'zip_code': self.zip_code,
        }
        self.logger.info("-------patial_result=== {}".format(partial_result))
        # word = input("Enter a word:")
        param = {
            "email": "asdfasd@ld.com",
            "phone": "3333333330",
            "firstName": "sdfsadfasd",
            "lastName": "dsafadsf",
            "location": {
                "postalCode": self.zip_code,
                "distanceInMiles": 0,
                "withinMarket": False
            },
            "inspectionPreferences": {
                "contactPreference": "EMAIL"
            },
            "vehicle": {
                "vin": self.vin,
                "year": 2015,
                "make": "Ford",
                "model": "F150",
                "availableTrims": [],
                "selectedTrim": {
                    "vifnum": 10331,
                    "name": "King Ranch Supercrew 4WD",
                    "id": "2015300746"
                },
                "selectedColor": {
                    "vifnum": 10331,
                    "code": "N1",
                    "title": "Blue Jeans Metallic",
                    "simpletitle": "Blue",
                    "rgb1": "092637"
                },
                "options": [
                    {
                        "selected": False,
                        "name": "Navigation System"
                    },
                    {
                        "selected": False,
                        "name": "FX4 Off-Road Package"
                    },
                    {
                        "selected": False,
                        "name": "Chrome Package"
                    },
                    {
                        "selected": False,
                        "name": "20-Inch Wheels"
                    },
                    {
                        "selected": False,
                        "name": "Power Moonroof"
                    },
                    {
                        "selected": True,
                        "name": "3.5L V6 Ecoboost"
                    },
                    {
                        "selected": False,
                        "name": "Roush F-150"
                    },
                    {
                        "selected": False,
                        "name": "Roush F-150 SC"
                    }
                ],
                "availableColors": [
                    {
                        "vifnum": -1,
                        "code": "Black",
                        "title": "Black",
                        "simpletitle": "Black",
                        "rgb1": "2D2926"
                    },
                    {
                        "vifnum": -1,
                        "code": "White",
                        "title": "White",
                        "simpletitle": "White",
                        "rgb1": "FFFFFF"
                    },
                    {
                        "vifnum": -1,
                        "code": "Gray",
                        "title": "Gray",
                        "simpletitle": "Gray",
                        "rgb1": "989898"
                    },
                    {
                        "vifnum": -1,
                        "code": "Silver",
                        "title": "Silver",
                        "simpletitle": "Silver",
                        "rgb1": "DFE0DF"
                    },
                    {
                        "vifnum": -1,
                        "code": "Blue",
                        "title": "Blue",
                        "simpletitle": "Blue",
                        "rgb1": "4173AD"
                    },
                    {
                        "vifnum": -1,
                        "code": "Red",
                        "title": "Red",
                        "simpletitle": "Red",
                        "rgb1": "DA4548"
                    },
                    {
                        "vifnum": -1,
                        "code": "Brown",
                        "title": "Brown",
                        "simpletitle": "Brown",
                        "rgb1": "75523E"
                    },
                    {
                        "vifnum": -1,
                        "code": "Beige",
                        "title": "Beige",
                        "simpletitle": "Beige",
                        "rgb1": "CAB0A2"
                    },
                    {
                        "vifnum": -1,
                        "code": "Gold",
                        "title": "Gold",
                        "simpletitle": "Gold",
                        "rgb1": "C18F55"
                    },
                    {
                        "vifnum": -1,
                        "code": "Green",
                        "title": "Green",
                        "simpletitle": "Green",
                        "rgb1": "74885B"
                    },
                    {
                        "vifnum": -1,
                        "code": "Yellow",
                        "title": "Yellow",
                        "simpletitle": "Yellow",
                        "rgb1": "FDB853"
                    },
                    {
                        "vifnum": -1,
                        "code": "Orange",
                        "title": "Orange",
                        "simpletitle": "Orange",
                        "rgb1": "D87A3F"
                    },
                    {
                        "vifnum": -1,
                        "code": "Pink",
                        "title": "Pink",
                        "simpletitle": "Pink",
                        "rgb1": "F7B7B6"
                    },
                    {
                        "vifnum": -1,
                        "code": "Burgundy",
                        "title": "Burgundy",
                        "simpletitle": "Burgundy",
                        "rgb1": "771A17"
                    },
                    {
                        "vifnum": -1,
                        "code": "Bronze",
                        "title": "Bronze",
                        "simpletitle": "Bronze",
                        "rgb1": "A3492E"
                    },
                    {
                        "vifnum": -1,
                        "code": "Purple",
                        "title": "Purple",
                        "simpletitle": "Purple",
                        "rgb1": "6D4789"
                    },
                    {
                        "vifnum": -1,
                        "code": "Tan",
                        "title": "Tan",
                        "simpletitle": "Tan",
                        "rgb1": "BCB295"
                    },
                    {
                        "vifnum": -1,
                        "code": "Turquoise",
                        "title": "Turquoise",
                        "simpletitle": "Turquoise",
                        "rgb1": "53BBB2"
                    },
                    {
                        "vifnum": -1,
                        "code": "Other",
                        "title": "Other",
                        "simpletitle": "Other",
                        "rgb1": "FFFFFF"
                    }
                ],
                "imageUrl": "https://d2ivfcfbdvj3sm.cloudfront.net/6fd260a869c389e6f8668ba55dfb5f70ed0d4a500b163c8c88cc1df8abcb/color_0640_032_png/MY2015/10331/10331_cc0640_032_N1.png",
                "condition": {
                    "overallCondition": "GREAT",
                    "mileage": self.mileage,
                    "warningLights": True,
                    "accidents": True,
                    "smokedIn": True,
                    "activeFinance": {
                        "type": "LOAN",
                        "estimatedRemaining": 0,
                        "lenderId": "OTX"
                    },
                    "numKeys": "ONE"
                },
                "licensePlate": "JTDKARFU6K3087621",
                "alternatives": []
            }
        }
        headers = {
            'Content-type': 'application/json',
            'User-Agent':"My User Agent 1.0",
            'Accept': '*/*',
            "Postman-Token": "2400114c-e7fc-486d-ad32-b2aee2866452",
            'Host': 'api-gateway.driveway.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Length': '6439',
        }
        data = requests.post(self.drive_url, data=json.dumps(param), headers=headers)

        try:
            print(data.status_code)
            self.logger.info("---data_json----try--logger==StatusCode= {}".format(data.status_code))
            # data_json = json.loads(data)
            # print(data_json)
            data_json = data.json()
            json_object = json.dumps(data_json)
            # print(data_json)
            self.logger.info("---data_json----try--logger=== {}".format(data_json))
            #Write the out in json file
            with open("driveway.json","w") as outfile:
                outfile.write(json_object)        

        except json.JSONDecodeError:
            print("Empty response")
    
    def parse_vin_driveway(self, response):
        json_response = response.json()
        # details = {vehicle_property['Variable']: vehicle_property['Value'] for vehicle_property in json_response['Results']}
        self.logger.info('=parse_vin_driveway==FullDetails==========Got successful response from {}'.format(json_response))
        partial_result = {
            'vin_number': self.vin,
            'condition': self.condition,
            'mileage': self.mileage,
            'zip_code': self.zip_code,
        }
        # response_2 = requests.post(self.drive_url, data = self.payload)
        # json2_response=response_2.json()
        # self.logger.info("=====response.json()=== {}".format(json2_response))


    def parse_vin_decoded(self, response):
        json_response = response.json()
        details = {vehicle_property['Variable']: vehicle_property['Value'] for vehicle_property in json_response['Results']}
        self.logger.info('===FullDetails==========Got successful response from {}'.format(response))
        partial_result = {
            'vin_number': self.vin,
            'condition': self.condition,
            'mileage': self.mileage,
            'zip_code': self.zip_code,
        }
        # response_2 = requests.post(self.drive_url, data = self.payload)
        # self.logger.info("=====response.json()==="+response_2.json())

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



        
        # mohideen orginal commented
        yield scrapy.http.JsonRequest(
            url= self.drive_url,
            callback=self.parse_driveway_vin_decoded,
            method='POST',
            headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/json',
                'origin':'https://www.driveway.com',
                'referer':'https://www.driveway.com'
            },
            data={
                "email": "asdfasd@ld.com",
                "phone": "3333333330",
                "firstName": "asdfasd",
                "lastName": "dsafasdf",
                "location": {
                    "postalCode": "77831",
                    "distanceInMiles": 0,
                    "withinMarket": True
                },
                "inspectionPreferences": {
                    "location": '',
                    "contactPreference": "EMAIL"
                },
                "vehicle": {
                    "vin": "JTDKARFU6K3087621",
                    "year": 2022,
                    "make": "Acura",
                    "model": "ILX",
                    "availableTrims": [],
                    "selectedTrim": {
                        "vifnum": 15162,
                        "name": "4D Sdn w/Prem&A-SPEC",
                        "id":"2022020104"
                    },
                    "selectedColor": {
                        "vifnum": 15162,
                        "code": "BA",
                        "title": "Apex Blue Pearl",
                        "simpletitle": "Blue",
                        "rgb1": "143CC2"
                    },
                    "options": [],
                    "availableColors": [
                        {
                            "vifnum": -1,
                            "code": "Black",
                            "title": "Black",
                            "simpletitle": "Black",
                            "rgb1": "2D2926"
                        },
                        {
                            "vifnum": -1,
                            "code": "White",
                            "title": "White",
                            "simpletitle": "White",
                            "rgb1": "FFFFFF"
                        },
                        {
                            "vifnum": -1,
                            "code": "Gray",
                            "title": "Gray",
                            "simpletitle": "Gray",
                            "rgb1": "989898"
                        },
                        {
                            "vifnum": -1,
                            "code": "Silver",
                            "title": "Silver",
                            "simpletitle": "Silver",
                            "rgb1": "DFE0DF"
                        },
                        {
                            "vifnum": -1,
                            "code": "Blue",
                            "title": "Blue",
                            "simpletitle": "Blue",
                            "rgb1": "4173AD"
                        },
                        {
                            "vifnum": -1,
                            "code": "Red",
                            "title": "Red",
                            "simpletitle": "Red",
                            "rgb1": "DA4548"
                        },
                        {
                            "vifnum": -1,
                            "code": "Brown",
                            "title": "Brown",
                            "simpletitle": "Brown",
                            "rgb1": "75523E"
                        },
                        {
                            "vifnum": -1,
                            "code": "Beige",
                            "title": "Beige",
                            "simpletitle": "Beige",
                            "rgb1": "CAB0A2"
                        },
                        {
                            "vifnum": -1,
                            "code": "Gold",
                            "title": "Gold",
                            "simpletitle": "Gold",
                            "rgb1": "C18F55"
                        },
                        {
                            "vifnum": -1,
                            "code": "Green",
                            "title": "Green",
                            "simpletitle": "Green",
                            "rgb1": "74885B"
                        },
                        {
                            "vifnum": -1,
                            "code": "Yellow",
                            "title": "Yellow",
                            "simpletitle": "Yellow",
                            "rgb1": "FDB853"
                        },
                        {
                            "vifnum": -1,
                            "code": "Orange",
                            "title": "Orange",
                            "simpletitle": "Orange",
                            "rgb1": "D87A3F"
                        },
                        {
                            "vifnum": -1,
                            "code": "Pink",
                            "title": "Pink",
                            "simpletitle": "Pink",
                            "rgb1": "F7B7B6"
                        },
                        {
                            "vifnum": -1,
                            "code": "Burgundy",
                            "title": "Burgundy",
                            "simpletitle": "Burgundy",
                            "rgb1": "771A17"
                        },
                        {
                            "vifnum": -1,
                            "code": "Bronze",
                            "title": "Bronze",
                            "simpletitle": "Bronze",
                            "rgb1": "A3492E"
                        },
                        {
                            "vifnum": -1,
                            "code": "Purple",
                            "title": "Purple",
                            "simpletitle": "Purple",
                            "rgb1": "6D4789"
                        },
                        {
                            "vifnum": -1,
                            "code": "Tan",
                            "title": "Tan",
                            "simpletitle": "Tan",
                            "rgb1": "BCB295"
                        },
                        {
                            "vifnum": -1,
                            "code": "Turquoise",
                            "title": "Turquoise",
                            "simpletitle": "Turquoise",
                            "rgb1": "53BBB2"
                        },
                        {
                            "vifnum": -1,
                            "code": "Other",
                            "title": "Other",
                            "simpletitle": "Other",
                            "rgb1": "FFFFFF"
                        }
                    ],
                    
                    "condition": {
                        "overallCondition": "GREAT",
                        "mileage": 10000,
                        "warningLights": True,
                        "accidents": True,
                        "smokedIn": True,
                        "activeFinance": {
                            "type": "LEASE",
                            "estimatedRemaining": 3333,
                            "lenderId": ""
                        },
                        "numKeys": "ONE"
                    },
                    "alternatives": []
                }
            },
            
            cb_kwargs={
                'result': '' #partial_result,

            },
        )

    

    def parse_driveway_vin_decoded(self, response, token, token_type, result):
      
        json_response = response.json()
        self.logger.info("===============parse_driveway_vin_decoded %s", json_response)
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

        # yield scrapy.http.JsonRequest(
        #     url=f'https://service.peddle.com/seller/v1/instant-offers',
        #     callback=self.parse_driveway_offer,
        #     headers={
        #         'accept': '*/*',
        #         'accept-language': 'en-US,en;q=0.9',
        #         'authorization': f'{token_type} {token}',
        #         'content-type': 'application/json',
        #     },
        #     data={
        #         'vehicle': {
        #             'year_id': year_id,
        #             'make_id': make_id,
        #             'model_id': model_id,
        #             'body_type_id': body_type_id,
        #             'cab_type_id': cab_type_id,
        #             'door_count': door_count,
        #             'trim_id': trim_id,
        #             'body_style_id': body_style_id,
        #             'fuel_type_id': fuel_type_id,
        #             'vin': self.vin,
        #             'usage': 'unknown',
        #             'location': {
        #                 'zip_code': self.zip_code,
        #             },
        #             'ownership': {
        #                 'type': 'owned',
        #                 'title_type': 'clean',
        #             },
        #             'condition': {
        #                 'mileage': self.mileage,
        #                 'drivetrain_condition': 'drives',
        #                 'key_and_keyfob_available': 'yes',
        #                 'all_tires_inflated': 'yes',
        #                 'flat_tires_location': {
        #                     'driver_side_view': {
        #                         'front': False,
        #                         'rear': False,
        #                     },
        #                     'passenger_side_view': {
        #                         'front': False,
        #                         'rear': False,
        #                     },
        #                 },
        #                 'wheels_removed': 'no',
        #                 'wheels_removed_location': {
        #                     'driver_side_view': {
        #                         'front': False,
        #                         'rear': False,
        #                     },
        #                     'passenger_side_view': {
        #                         'front': False,
        #                         'rear': False,
        #                     },
        #                 },
        #                 'body_panels_intact': 'yes',
        #                 'body_panels_damage_location': {
        #                     'driver_side_view': {
        #                         'front_top': False,
        #                         'front_bottom': False,
        #                         'front_door_top': False,
        #                         'front_door_bottom': False,
        #                         'rear_door_top': False,
        #                         'rear_door_bottom': False,
        #                         'rear_top': False,
        #                         'rear_bottom': False,
        #                     },
        #                     'passenger_side_view': {
        #                         'front_top': False,
        #                         'front_bottom': False,
        #                         'front_door_top': False,
        #                         'front_door_bottom': False,
        #                         'rear_door_top': False,
        #                         'rear_door_bottom': False,
        #                         'rear_top': False,
        #                         'rear_bottom': False,
        #                     },
        #                     'front_view': {
        #                         'driver_side_top': False,
        #                         'driver_side_bottom': False,
        #                         'passenger_side_top': False,
        #                         'passenger_side_bottom': False,
        #                     },
        #                     'rear_view': {
        #                         'driver_side_top': False,
        #                         'driver_side_bottom': False,
        #                         'passenger_side_top': False,
        #                         'passenger_side_bottom': False,
        #                     },
        #                     'top_view': {
        #                         'driver_side_front': False,
        #                         'passenger_side_front': False,
        #                         'driver_side_front_roof': False,
        #                         'passenger_side_front_roof': False,
        #                         'driver_side_rear_roof': False,
        #                         'passenger_side_rear_roof': False,
        #                         'driver_side_rear': False,
        #                         'passenger_side_rear': False,
        #                     },
        #                 },
        #                 'body_damage_free': 'yes',
        #                 'body_damage_location': {
        #                     'driver_side_view': {
        #                         'front_top': False,
        #                         'front_bottom': False,
        #                         'front_door_top': False,
        #                         'front_door_bottom': False,
        #                         'rear_door_top': False,
        #                         'rear_door_bottom': False,
        #                         'rear_top': False,
        #                         'rear_bottom': False,
        #                     },
        #                     'passenger_side_view': {
        #                         'front_top': False,
        #                         'front_bottom': False,
        #                         'front_door_top': False,
        #                         'front_door_bottom': False,
        #                         'rear_door_top': False,
        #                         'rear_door_bottom': False,
        #                         'rear_top': False,
        #                         'rear_bottom': False,
        #                     },
        #                     'front_view': {
        #                         'driver_side_top': False,
        #                         'driver_side_bottom': False,
        #                         'passenger_side_top': False,
        #                         'passenger_side_bottom': False,
        #                     },
        #                     'rear_view': {
        #                         'driver_side_top': False,
        #                         'driver_side_bottom': False,
        #                         'passenger_side_top': False,
        #                         'passenger_side_bottom': False,
        #                     },
        #                     'top_view': {
        #                         'driver_side_front': False,
        #                         'passenger_side_front': False,
        #                         'driver_side_front_roof': False,
        #                         'passenger_side_front_roof': False,
        #                         'driver_side_rear_roof': False,
        #                         'passenger_side_rear_roof': False,
        #                         'driver_side_rear': False,
        #                         'passenger_side_rear': False,
        #                     },
        #                 },
        #                 'mirrors_lights_glass_intact': 'yes',
        #                 'mirrors_lights_glass_damage_location': {
        #                     'driver_side_view': {
        #                         'front_top': False,
        #                         'front_bottom': False,
        #                         'front_door_top': False,
        #                         'front_door_bottom': False,
        #                         'rear_door_top': False,
        #                         'rear_door_bottom': False,
        #                         'rear_top': False,
        #                         'rear_bottom': False,
        #                     },
        #                     'passenger_side_view': {
        #                         'front_top': False,
        #                         'front_bottom': False,
        #                         'front_door_top': False,
        #                         'front_door_bottom': False,
        #                         'rear_door_top': False,
        #                         'rear_door_bottom': False,
        #                         'rear_top': False,
        #                         'rear_bottom': False,
        #                     },
        #                     'front_view': {
        #                         'driver_side_top': False,
        #                         'driver_side_bottom': False,
        #                         'passenger_side_top': False,
        #                         'passenger_side_bottom': False,
        #                     },
        #                     'rear_view': {
        #                         'driver_side_top': False,
        #                         'driver_side_bottom': False,
        #                         'passenger_side_top': False,
        #                         'passenger_side_bottom': False,
        #                     },
        #                     'top_view': {
        #                         'driver_side_front': False,
        #                         'passenger_side_front': False,
        #                         'driver_side_front_roof': False,
        #                         'passenger_side_front_roof': False,
        #                         'driver_side_rear_roof': False,
        #                         'passenger_side_rear_roof': False,
        #                         'driver_side_rear': False,
        #                         'passenger_side_rear': False,
        #                     },
        #                 },
        #                 'interior_intact': 'yes',
        #                 'flood_fire_damage_free': 'yes',
        #                 'engine_transmission_condition': 'intact',
        #             },
        #         },
        #     },
        #     cb_kwargs={
        #         'result': result,
        #     },
        # )

    def parse_driveway_offer(self, response, result):
        json_response = response.json()
        self.logger.info("===============parse_driveway_offer %s", json_response)
        price = json_response['presented_offer_amount']

        result['datetime'] = datetime.utcnow()
        result['source'] = 'Driveway'
        result['price'] = price

        yield result
