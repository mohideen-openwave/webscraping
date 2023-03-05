import scrapy
from Tools.scripts import ifdef
from scrapy.http import request
from scrapy.http.request.form import FormRequest
from scrapy.http import FormRequest
import json
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class CarPricesAllCarSpider(scrapy.Spider):
    name = 'car_prices_allcars'
    allowed_domains = ['allcars.com']
    meta_data = ''
    proxy = 'http://dvafvogc:c75babt2ovb6@45.158.187.187:7196'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):
        form_data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "zip_code": self.zip_code
        }
        request_body = json.dumps(form_data)
        # self.logger.info('========start_requests==request_body= {}'.format(request_body))
        yield scrapy.Request('https://cars.allcars.com/sell-your-car',
                             method="GET",
                             body=request_body,
                             headers={
                                 'Content-type': 'application/json',
                                 'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
                                 'Accept': '*/*',
                                 'Host': "cars.allcars.com",
                                 'x-csrf-token': 'Mfwb1D5w50JStGh8uDWrvmcBcYz8mZdkoUEC5ao6',
                                 'x-xsrf-token': 'eyJpdiI6InM1cWhlQkRwbXIxdU5vKzlFZWVRVXc9PSIsInZhbHVlIjoiUXlCM21hTXlxRE9nRTVNMS9ROHNxQ1p4K1RPUEFEWVd6K09JdnhVSWdrdTdGaWdOVHhjbnNZUGJraGVhR3R2SFhEbHJUQmJHSkt2UEdjMUFISVNzTDlNMmgvQjBUQWZxZ0RTalYzakFtSU1ubDhBZis1bHROTEpRK0pqc0Z3MXUiLCJtYWMiOiI5NjI3YTIyZmE4ZmM3YjY3MTAxZTE2MGFiMDljYzk4NzU3ZTVhYTE5OWEwYTVhMTJiMGU5NGFiMjgyN2RmODY3IiwidGFnIjoiIn0='
                             },
                             callback=self.vehicle_lookup_parse,
                             meta={
                                 'proxy': self.proxy,
                             },
                             errback=self.errback_httpbin)

    def vehicle_lookup_parse(self, response):
        res = response
        meta = response.css('meta::attr(content)').extract()
        self.meta_data = meta[1]
        self.logger.info('=======vehicle_lookup_parse===response.headers===csrf-token= {}'.format(self.meta_data))
        content = response.body
        # for item in response.css('meta'):
        #     self.logger.info('=======meta::attr(name=)= {}'.format(item.css('meta::attr(name)').get()))
        #     self.logger.info('=======meta::attr(content)= {}'.format(item.css('meta::attr(content)').get()))
        form_data = {
            "vin": self.vin,
            "is_new": True,
            "plate": 'null',
            "plateState": 'null',
            "year": 'null',
            "make": 'null',
            "model": 'null',
            "trim": self.trim,
            "uvc": 'null',
            "style_list": 'null',
            "type": "sCVin"
        }
        request_body = json.dumps(form_data)
        yield scrapy.http.JsonRequest('https://cars.allcars.com/sell-your-car/vehicle_lookup/57360',
                                      method="PATCH",
                                      body=request_body,
                                      headers={
                                          'Content-Type': 'application/json;charset=UTF-8',
                                          'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
                                          'referer': 'https://cars.allcars.com/sell-your-car',
                                          'x-csrf-token': meta[1],
                                          'x-xsrf-token': 'eyJpdiI6InM1cWhlQkRwbXIxdU5vKzlFZWVRVXc9PSIsInZhbHVlIjoiUXlCM21hTXlxRE9nRTVNMS9ROHNxQ1p4K1RPUEFEWVd6K09JdnhVSWdrdTdGaWdOVHhjbnNZUGJraGVhR3R2SFhEbHJUQmJHSkt2UEdjMUFISVNzTDlNMmgvQjBUQWZxZ0RTalYzakFtSU1ubDhBZis1bHROTEpRK0pqc0Z3MXUiLCJtYWMiOiI5NjI3YTIyZmE4ZmM3YjY3MTAxZTE2MGFiMDljYzk4NzU3ZTVhYTE5OWEwYTVhMTJiMGU5NGFiMjgyN2RmODY3IiwidGFnIjoiIn0='
                                      },
                                      callback=self.offer_parse,
                                      meta={
                                          'proxy': self.proxy,
                                      },
                                      errback=self.errback_httpbin,
                                      cb_kwargs={
                                          'result': res,
                                      }
                                      )

    def offer_parse(self, response, result):
        res = response.json()
        # meta = response.css('meta::attr(content)').extract()
        self.logger.info('=======offer_parse===response.headers===csrf-token= {}'.format(res))
        content = response.body

        condition = ""
        if self.condition == 'excellent' or self.condition == 'Excellent':
            condition = "Needs Lots Of Love"
        elif self.condition == 'good' or self.condition == 'Good':
            condition = "Seen Better Days"
        else:
            condition = "Used Modestly"

        form_data = {
            "vin": self.vin,
            "is_new": True,
            "plate": 'null',
            "plateState": 'null',
            "year": 'null',
            "make": 'null',
            "model": 'null',
            "trim": self.trim,
            "uvc": "2018495127",
            "style_list": 'null',
            "type": res['type'],
            "vin_data": {
                "input": {
                    "key": "JMQZG9RUDXN1G2O",
                    "vin": self.vin,
                    "format": "json",
                    "include": "attributes,equipments,colors,recalls,warranties,photos"
                },
                "attributes": {
                    "year": res["vin_data"]["attributes"]["year"],
                    "make": res["vin_data"]["attributes"]["make"],
                    "model": res["vin_data"]["attributes"]["model"],
                    "trim": res["vin_data"]["attributes"]["trim"],
                    "style": res["vin_data"]["attributes"]["style"],
                    "type": res["vin_data"]["attributes"]["type"],
                    "size": res["vin_data"]["attributes"]["size"],
                    "category": res["vin_data"]["attributes"]["category"],
                    "made_in": res["vin_data"]["attributes"]["made_in"],
                    "made_in_city": res["vin_data"]["attributes"]["made_in_city"],
                    "doors": res["vin_data"]["attributes"]["doors"],
                    "fuel_type": res["vin_data"]["attributes"]["fuel_type"],
                    "fuel_capacity": res["vin_data"]["attributes"]["fuel_capacity"],
                    "city_mileage": res["vin_data"]["attributes"]["city_mileage"],
                    "highway_mileage": res["vin_data"]["attributes"]["highway_mileage"],
                    "engine": res["vin_data"]["attributes"]["engine"],
                    "engine_size": res["vin_data"]["attributes"]["engine_size"],
                    "engine_cylinders": res["vin_data"]["attributes"]["engine_cylinders"],
                    "transmission": res["vin_data"]["attributes"]["transmission"],
                    "transmission_type": res["vin_data"]["attributes"]["transmission_type"],
                    "transmission_speeds": res["vin_data"]["attributes"]["transmission_speeds"],
                    "drivetrain": res["vin_data"]["attributes"]["drivetrain"],
                    "anti_brake_system": res["vin_data"]["attributes"]["anti_brake_system"],
                    "steering_type": res["vin_data"]["attributes"]["steering_type"],
                    "curb_weight": "",
                    "gross_vehicle_weight_rating": res["vin_data"]["attributes"]["gross_vehicle_weight_rating"],
                    "overall_height": res["vin_data"]["attributes"]["overall_height"],
                    "overall_length": res["vin_data"]["attributes"]["overall_length"],
                    "overall_width": res["vin_data"]["attributes"]["overall_width"],
                    "wheelbase_length": res["vin_data"]["attributes"]["wheelbase_length"],
                    "standard_seating": res["vin_data"]["attributes"]["standard_seating"],
                    "invoice_price": res["vin_data"]["attributes"]["invoice_price"],
                    "delivery_charges": res["vin_data"]["attributes"]["delivery_charges"],
                    "manufacturer_suggested_retail_price": res["vin_data"]["attributes"][
                        "manufacturer_suggested_retail_price"],
                    "color": "Black",
                    "mileage": self.mileage,
                    "zip_code": self.zip_code,
                    "conditions": {
                        "vehicle_condition": condition,
                        "vehicle_accident": "No Accidents",
                        "optional_equipment": [
                            "Sunroof"
                        ],
                        "title_present": "No",
                        "title_issues": "No",
                        "frame_damage": "No",
                        "glass_damage": "No",
                        "rust_damage": "No",
                        "rust_damage_true": [],
                        "body_damage": "No",
                        "body_damage_true": [],
                        "engine_issues": "No",
                        "engine_issues_true": [],
                        "interior_issues": "No",
                        "interior_issues_true": [],
                        "mechanical_issues": "No",
                        "mechanical_issues_true": [],
                        "warning_lights": "No",
                        "warning_lights_true": [],
                        "modifications": "No",
                        "modifications_true": [],
                        "tire_issues": "No",
                        "tire_issues_true": [],
                        "tire_tread": "Good",
                        "transmission": "Manual"
                    }
                },
                "equipments": res["vin_data"]["equipments"],
                "warranties": res["vin_data"]["warranties"],
                "colors": res["vin_data"]["colors"],
                "recalls": res["vin_data"]["recalls"],
                "photos": res["vin_data"]["photos"],
                "success": True,
                "error": ""
            }
        }
        static_data = {
                      "vin": "SALVP2RX1JH284344",
                      "is_new": True,
                      "plate": '',
                      "plateState": '',
                      "year": '',
                      "make": '',
                      "model": '',
                      "trim": '',
                      "uvc": "2018495127",
                      "style_list": '',
                      "type": "sCVin",
                      "vin_data": {
                        "input": {
                          "key": "JMQZG9RUDXN1G2O",
                          "vin": "SALVP2RX1JH284344",
                          "format": "json",
                          "include": "attributes,equipments,colors,recalls,warranties,photos"
                        },
                        "attributes": {
                          "year": "2018",
                          "make": "Land Rover",
                          "model": "Range Rover Evoque",
                          "trim": "SE",
                          "style": "4D SAV",
                          "type": "Sport Utility Vehicle",
                          "size": "Compact",
                          "category": "Small Sport Utility Vehicle",
                          "made_in": "United Kingdom",
                          "made_in_city": "HALEWOOD",
                          "doors": "4-Door",
                          "fuel_type": "Regular",
                          "fuel_capacity": "18.00 gallons",
                          "city_mileage": "22 miles/gallon",
                          "highway_mileage": "29 miles/gallon",
                          "engine": "2.0-L L-4 DOHC 24V Turbo",
                          "engine_size": "2",
                          "engine_cylinders": "4",
                          "transmission": "9-Speed Automatic",
                          "transmission_type": "Automatic",
                          "transmission_speeds": "9-Speed",
                          "drivetrain": "Four-Wheel Drive",
                          "anti_brake_system": "4-Wheel ABS",
                          "steering_type": "Rack & Pinion",
                          "curb_weight": "",
                          "gross_vehicle_weight_rating": "6000 pounds",
                          "overall_height": "64.40 inches",
                          "overall_length": "172.00 inches",
                          "overall_width": "78.10 inches",
                          "wheelbase_length": "104.70 inches",
                          "standard_seating": "5",
                          "invoice_price": "$39,292",
                          "delivery_charges": "$995",
                          "manufacturer_suggested_retail_price": "$41,800",
                          "color": "Black",
                          "mileage": "19,000",
                          "zip_code": "60194",
                          "conditions": {
                            "vehicle_condition": "Needs Lots Of Love",
                            "vehicle_accident": "No Accidents",
                            "optional_equipment": [
                              "Sunroof"
                            ],
                            "title_present": "No",
                            "title_issues": "No",
                            "frame_damage": "No",
                            "glass_damage": "No",
                            "rust_damage": "No",
                            "rust_damage_true": [],
                            "body_damage": "No",
                            "body_damage_true": [],
                            "engine_issues": "No",
                            "engine_issues_true": [],
                            "interior_issues": "No",
                            "interior_issues_true": [],
                            "mechanical_issues": "No",
                            "mechanical_issues_true": [],
                            "warning_lights": "No",
                            "warning_lights_true": [],
                            "modifications": "No",
                            "modifications_true": [],
                            "tire_issues": "No",
                            "tire_issues_true": [],
                            "tire_tread": "Good",
                            "transmission": "Manual"
                          }
                        },
                        "equipments": [
                          {
                            "group": "Anti-Theft & Locks",
                            "name": "Child Safety Door Locks",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Anti-Theft & Locks",
                            "name": "Vehicle Anti-Theft",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Braking & Traction",
                            "name": "ABS Brakes",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Safety",
                            "name": "Driver Airbag",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Safety",
                            "name": "Front Side Airbag",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Safety",
                            "name": "Passenger Airbag",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Safety",
                            "name": "Side Head Curtain Airbag",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Interior Features",
                            "name": "Cruise Control",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Interior Features",
                            "name": "Telescopic Steering Column",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Seat",
                            "name": "Driver Multi-Adjustable Power Seat",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Seat",
                            "name": "Front Power Lumbar Support",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Seat",
                            "name": "Passenger Multi-Adjustable Power Seat",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Tires & Wheels",
                            "name": "Alloy Wheels",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Tires & Wheels",
                            "name": "Run Flat Tires",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Mirrors & Windows & Wipers",
                            "name": "Power Windows",
                            "value": "",
                            "availability": "Standard"
                          },
                          {
                            "group": "Chassis",
                            "name": "Anti-Brake System",
                            "value": "4-Wheel ABS",
                            "availability": ""
                          },
                          {
                            "group": "Chassis",
                            "name": "Steering Type",
                            "value": "R&P",
                            "availability": ""
                          },
                          {
                            "group": "Chassis",
                            "name": "Front Brake Type",
                            "value": "Disc",
                            "availability": ""
                          },
                          {
                            "group": "Chassis",
                            "name": "Rear Brake Type",
                            "value": "Disc",
                            "availability": ""
                          },
                          {
                            "group": "Chassis",
                            "name": "Front Suspension",
                            "value": "IND",
                            "availability": ""
                          },
                          {
                            "group": "Chassis",
                            "name": "Rear Suspension",
                            "value": "IND",
                            "availability": ""
                          },
                          {
                            "group": "Chassis",
                            "name": "Front Spring Type",
                            "value": "Coil",
                            "availability": ""
                          },
                          {
                            "group": "Chassis",
                            "name": "Rear Spring Type",
                            "value": "Coil",
                            "availability": ""
                          },
                          {
                            "group": "Chassis",
                            "name": "Run Flat Tires",
                            "value": "Std.",
                            "availability": ""
                          },
                          {
                            "group": "Interior Dimensions",
                            "name": "Front Headroom",
                            "value": "38.90 In.",
                            "availability": ""
                          },
                          {
                            "group": "Interior Dimensions",
                            "name": "Rear Headroom",
                            "value": "38.00 In.",
                            "availability": ""
                          },
                          {
                            "group": "Exterior Dimensions & Weight",
                            "name": "Overall Length",
                            "value": "172.00 In.",
                            "availability": ""
                          },
                          {
                            "group": "Exterior Dimensions & Weight",
                            "name": "Overall Width",
                            "value": "78.10 In.",
                            "availability": ""
                          },
                          {
                            "group": "Exterior Dimensions & Weight",
                            "name": "Overall Height",
                            "value": "64.40 In.",
                            "availability": ""
                          },
                          {
                            "group": "Exterior Dimensions & Weight",
                            "name": "Wheelbase",
                            "value": "104.70 In.",
                            "availability": ""
                          },
                          {
                            "group": "Exterior Dimensions & Weight",
                            "name": "Ground Clearance",
                            "value": "8.30 In.",
                            "availability": ""
                          },
                          {
                            "group": "Cargo Bed Dimensions",
                            "name": "Overall Length",
                            "value": "172.00 In.",
                            "availability": ""
                          },
                          {
                            "group": "Capacities",
                            "name": "Standard Seating",
                            "value": "5",
                            "availability": ""
                          }
                        ],
                        "warranties": [
                          {
                            "type": "Basic",
                            "months": "48 Months",
                            "miles": "50,000 miles"
                          },
                          {
                            "type": "Powertrain",
                            "months": "48 Months",
                            "miles": "50,000 miles"
                          },
                          {
                            "type": "Rust",
                            "months": "72 Months",
                            "miles": "unlimited miles"
                          }
                        ],
                        "colors": [
                          {
                            "category": "Interior",
                            "name": "Almond/Espresso"
                          },
                          {
                            "category": "Interior",
                            "name": "Cirrus/Lunar"
                          },
                          {
                            "category": "Interior",
                            "name": "Ebony"
                          },
                          {
                            "category": "Exterior",
                            "name": "Carpathian Grey Premium Metallic"
                          },
                          {
                            "category": "Exterior",
                            "name": "Silicon Silver Premium Metallic"
                          },
                          {
                            "category": "Exterior",
                            "name": "Fuji White"
                          },
                          {
                            "category": "Exterior",
                            "name": "Narvik Black"
                          },
                          {
                            "category": "Exterior",
                            "name": "Corris Grey Metallic"
                          },
                          {
                            "category": "Exterior",
                            "name": "Loire Blue Metallic"
                          },
                          {
                            "category": "Exterior",
                            "name": "Firenze Red Metallic"
                          },
                          {
                            "category": "Exterior",
                            "name": "Santorini Black Metallic"
                          },
                          {
                            "category": "Exterior",
                            "name": "Yulong White Metallic"
                          },
                          {
                            "category": "Exterior",
                            "name": "Kaikoura Stone Metallic"
                          },
                          {
                            "category": "Exterior",
                            "name": "Indus Silver Metallic"
                          },
                          {
                            "category": "Roof",
                            "name": "Santorini Black Metallic Contrast Roof"
                          },
                          {
                            "category": "Roof",
                            "name": "Corris Grey Metallic Contrast Roof"
                          },
                          {
                            "category": "Interior Trim",
                            "name": "Textured Aluminum"
                          },
                          {
                            "category": "Interior Trim",
                            "name": "Dark Sport Textured"
                          }
                        ],
                        "recalls": [
                          {
                            "source": "NHTSA",
                            "campaign": "18v087000",
                            "date": "20180201",
                            "components": "Fuel System, Gasoline:fuel Injection System:fuel Rail",
                            "summary": "Jaguar Land Rover North America, LLC (Land Rover) IS Recalling Certain 2018 Land Rover Range Rover Evoque, Range Rover Velar, and Land Rover Discover Sport Vehicles Equipped With A 2.0l Gasoline Engine.  THE Fuel Rail END Caps MAY Leak, Possibly Resulting IN Fuel Vapor or Liquid Fuel Leaking Into THE Engine Bay.",
                            "consequence": "A Fuel Leak IN THE Presence OF AN Ignition Source Such AS HOT Engine or Exhaust Components CAN Increase THE Risk OF A Fire.",
                            "remedy": "Land Rover Will Notify Owners, and Dealers Will Replace THE Fuel Rail, Free OF Charge.  THE Recall Began ON March 8, 2018.  Owners MAY Contact Land Rover Customer Service AT 1-800-637-6837.  Land Rover's Number FOR This Recall IS N138.",
                            "notes": "Owners MAY Also Contact THE National Highway Traffic Safety Administration Vehicle Safety Hotline AT 1-888-327-4236 (Tty 1-800-424-9153), or GO TO Www.safercar.gov."
                          },
                          {
                            "source": "NHTSA",
                            "campaign": "18v088000",
                            "date": "20180201",
                            "components": "Tires:pressure Monitoring and Regulating Systems",
                            "summary": "Jaguar Land Rover North America, LLC (Land Rover) IS Recalling Certain 2018 Land Rover Range Rover Evoque Convertible Vehicles Equipped With 20-Inch Wheels.  THE Tire Pressure Monitoring System (Tpms) MAY BE Incorrectly SET and Thus MAY NOT Illuminate THE Warning ON THE Instrument Panel When A Tire's Pressure IS 25% Below THE Recommended Cold Inflation Pressure.   AS Such, These Vehicles Fail TO Comply With THE Requirements OF Federal Motor Vehicle Safety Standard (fmvss) Number 138, \"tire Pressure Monitoring Systems.\"",
                            "consequence": "IF THE Vehicle Fails TO Warn THE Driver OF Low Tire Pressure, Driving THE Vehicle MAY Result IN Tire Tread Separation, Increasing THE Risk OF A Crash.",
                            "remedy": "Land Rover Will Notify Owners, and Dealers Will Update THE Tpms Setting TO Correct THE Illumination Setting, Free OF Charge.  THE Recall Began ON March 9, 2018.  Owners MAY Contact Land Rover Customer Service AT 1-800-637-6837.  Land Rover's Number FOR This Recall IS N164.",
                            "notes": "Owners MAY Also Contact THE National Highway Traffic Safety Administration Vehicle Safety Hotline AT 1-888-327-4236 (Tty 1-800-424-9153), or GO TO Www.safercar.gov."
                          }
                        ],
                        "photos": [
                          {
                            "url": "https://imgset.info/a/SALVP2RX2JH286569_20190205_0-31859jpg?size=medium"
                          },
                          {
                            "url": "https://imgset.info/a/SALVR2RX0JH323760_20190205_0-55599jpg?size=medium"
                          },
                          {
                            "url": "https://imgset.info/a/SALVR2RX2JH277073_20190205_0-46229jpg?size=medium"
                          },
                          {
                            "url": "https://imgset.info/a/SALVR2RX4JH323146_20190205_0-54679jpg?size=medium"
                          },
                          {
                            "url": "https://imgset.info/a/SALVR2RX9JH324065_20190205_0-48487jpg?size=medium"
                          }
                        ],
                        "success": True,
                        "error": ""
                      }
                    }
        request_body = json.dumps(form_data)
        result = request_body
        yield scrapy.http.JsonRequest(
            'https://cars.allcars.com/sell-your-car/drivably/additional_info/58726/execute-node-offer-scraper',
            method="POST",
            body=request_body,
            headers={
                'Content-Type': 'application/json;charset=UTF-8',
                'USER_AGENT': 'carprice (+https://cars.allcars.com)',
                'referer': 'https://cars.allcars.com/sell-your-car',
                'x-csrf-token': self.meta_data,
                'x-xsrf-token': 'eyJpdiI6InM1cWhlQkRwbXIxdU5vKzlFZWVRVXc9PSIsInZhbHVlIjoiUXlCM21hTXlxRE9nRTVNMS9ROHNxQ1p4K1RPUEFEWVd6K09JdnhVSWdrdTdGaWdOVHhjbnNZUGJraGVhR3R2SFhEbHJUQmJHSkt2UEdjMUFISVNzTDlNMmgvQjBUQWZxZ0RTalYzakFtSU1ubDhBZis1bHROTEpRK0pqc0Z3MXUiLCJtYWMiOiI5NjI3YTIyZmE4ZmM3YjY3MTAxZTE2MGFiMDljYzk4NzU3ZTVhYTE5OWEwYTVhMTJiMGU5NGFiMjgyN2RmODY3IiwidGFnIjoiIn0='
            },
            callback=self.parse,
            meta={
                'proxy': self.proxy,
            },
            errback=self.errback_httpbin,
            dont_filter=False,
            cb_kwargs={
                'result': res,
            })

    def parse(self, response, result):
        offerdata = response.json()
        self.logger.info('======parse==response==offer-data= {}'.format(offerdata))
        result_param = json.dumps(result)
        self.logger.info('======parse==result=== {}'.format(result_param))

        attributes = result["vin_data"]["attributes"]
        result1 = result["vin_data"]["attributes"]
        result1['source'] = "allcars.com"
        result1['year'] = attributes["year"]
        result1["make"] = attributes["make"]
        result1["model"] = attributes["model"]
        result1["trim"] = self.trim
        result1["type"] = attributes["type"]
        result1["size"] = attributes["size"]
        result1["category"] = attributes["category"]
        result1["made_in"] = attributes["made_in"]
        result1["made_in_city"] = attributes["made_in_city"]
        result1["doors"] = attributes["doors"]
        result1["fuel_type"] = attributes["fuel_type"]
        result1["fuel_capacity"] = attributes["fuel_capacity"]
        result1["city_mileage"] = attributes["city_mileage"]
        result1["highway_mileage"] = attributes["highway_mileage"]
        result1["engine"] = attributes["engine"]
        result1["engine_size"] = attributes["engine_size"]
        result1["engine_cylinders"] = attributes["engine_cylinders"]
        result1["transmission"] = attributes["transmission"]
        result1["transmission_type"] = attributes["transmission_type"]
        result1["transmission_speeds"] = attributes["transmission_speeds"]
        result1["drivetrain"] = attributes["drivetrain"]
        result1["anti_brake_system"] = attributes["anti_brake_system"]
        result1["steering_type"] = attributes["steering_type"]
        result1["gross_vehicle_weight_rating"] = attributes["gross_vehicle_weight_rating"]
        result1["overall_height"] = attributes["overall_height"]
        result1["overall_length"] = attributes["overall_length"]
        result1["overall_width"] = attributes["overall_width"]
        result1["wheelbase_length"] = attributes["wheelbase_length"]
        result1["standard_seating"] = attributes["standard_seating"]
        result1["price"] = attributes["manufacturer_suggested_retail_price"]

        # conditions
        try:
            conditions = attributes["conditions"]
            self.logger.info('======conditions= {}'.format(conditions))
            result1["What is the condition of the vehicle?"] = conditions["vehicle_condition"]
            result1["Has the vehicle been in an accident?"] = conditions["vehicle_accident"]
            result1["Optional Equipment"] = conditions["optional_equipment"][0]
            result1["Title Present"] = conditions["title_present"]
            result1["Title Issues"] = conditions["title_issues"]
            result1["Frame Damage"] = conditions["frame_damage"]
            result1["Glass Damage"] = conditions["glass_damage"]
            result1["Rust Damage"] = conditions["rust_damage"]
            result1["Body Damage"] = conditions["body_damage"]
            result1["Engine Issues"] = conditions["engine_issues"]
            result1["Interior Issues"] = conditions["interior_issues"]
            result1["Mechanical Issues"] = conditions["mechanical_issues"]
            result1["Warning Lights"] = conditions["warning_lights"]
            result1["Modifications"] = conditions["modifications"]
            result1["Tire Issues"] = conditions["tire_issues"]
            result1["Tire Tread"] = conditions["tire_tread"]
            result1["Transmission"] = conditions["transmission"]
        except:
            # print("An exception occurred")
            result1["What is the condition of the vehicle?"] = "No"
            result1["Has the vehicle been in an accident?"] = "No"
            result1["Optional Equipment"] = "No"
            result1["Title Present"] = "No"
            result1["Title Issues"] = "No"
            result1["Frame Damage"] = "No"
            result1["Glass Damage"] = "No"
            result1["Rust Damage"] = "No"
            result1["Body Damage"] = "No"
            result1["Engine Issues"] = "No"
            result1["Interior Issues"] = "No"
            result1["Mechanical Issues"] = "No"
            result1["Warning Lights"] = "No"
            result1["Modifications"] = "No"
            result1["Tire Issues"] = "No"
            result1["Tire Tread"] = "No"
            result1["Transmission"] = "No"

        result1['firstname'] = self.first_name
        result1['lastname'] = self.last_name
        result1['email'] = self.email
        result1['phone_number'] = self.phone_number
        result1['zip_code'] = self.zip_code
        result1['mileage'] = self.mileage
        self.logger.info('===final===parse==result=== {}'.format(result1))
        yield result1

        # Error Handling

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('ErrorHandling===HttpError on %s', response.url)
            self.logger.error('ErrorHandling===HttpError on Headers %s', response.headers)
            self.logger.error('ErrorHandling===HttpError on Body %s', response.body)
            # convert into variable
            # hxs = HtmlXPathSelector(response)
            # sample = response.body.selector.xpath("//meta[@name='csrf-token']/p[1]").get()
            # parser = MyHTMLParser(strict=False)
            # offerdata = json.loads(response.body)
            # self.logger.info("=====Resone Meta== {}".format(offerdata))
            # body = HTMLParser

            # sample = body.xpath('//meta/@content').getall()
            # self.logger.info("=====Resone Meta== {}".format(sample))

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('ErrorHandling===DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('ErrorHandling===TimeoutError on %s', request.url)
