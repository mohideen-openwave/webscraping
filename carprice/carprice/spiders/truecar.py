import scrapy
from scrapy.http import request
from scrapy.http.request.form import FormRequest
from scrapy.http import FormRequest
import json
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class CarPricesTrueCarSpider(scrapy.Spider):
    name = 'car_prices_truecar'
    allowed_domains = ['truecar.com']
    meta_data = ''
    def start_requests(self): 
        form_data = {
            "first_name": "moh",
            "last_name": "khad",
            "email": "mohide@dl.com",
            "phone_number": "(939) 939-3333",
            "zip_code": self.zip_code
        }
        request_body = json.dumps(form_data)
        # self.logger.info('========start_requests==request_body= {}'.format(request_body))
        yield scrapy.Request('https://cars.allcars.com/sell-your-car',
                            method="GET",
                            body=request_body,
                            headers={
                                'Content-type': 'application/json',
                                'User-Agent':"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
                                'Accept': '*/*',
                                'Host':"cars.allcars.com",
                                'x-csrf-token':'Mfwb1D5w50JStGh8uDWrvmcBcYz8mZdkoUEC5ao6',
                                'x-xsrf-token': 'eyJpdiI6InM1cWhlQkRwbXIxdU5vKzlFZWVRVXc9PSIsInZhbHVlIjoiUXlCM21hTXlxRE9nRTVNMS9ROHNxQ1p4K1RPUEFEWVd6K09JdnhVSWdrdTdGaWdOVHhjbnNZUGJraGVhR3R2SFhEbHJUQmJHSkt2UEdjMUFISVNzTDlNMmgvQjBUQWZxZ0RTalYzakFtSU1ubDhBZis1bHROTEpRK0pqc0Z3MXUiLCJtYWMiOiI5NjI3YTIyZmE4ZmM3YjY3MTAxZTE2MGFiMDljYzk4NzU3ZTVhYTE5OWEwYTVhMTJiMGU5NGFiMjgyN2RmODY3IiwidGFnIjoiIn0='
                                },
                            callback=self.vehicle_lookup_parse,
                            errback=self.errback_httpbin )
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
            "trim": 'null',
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
                                'USER_AGENT':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
                                'referer':'https://cars.allcars.com/sell-your-car',
                                'x-csrf-token':meta[1],
                                'x-xsrf-token': 'eyJpdiI6InM1cWhlQkRwbXIxdU5vKzlFZWVRVXc9PSIsInZhbHVlIjoiUXlCM21hTXlxRE9nRTVNMS9ROHNxQ1p4K1RPUEFEWVd6K09JdnhVSWdrdTdGaWdOVHhjbnNZUGJraGVhR3R2SFhEbHJUQmJHSkt2UEdjMUFISVNzTDlNMmgvQjBUQWZxZ0RTalYzakFtSU1ubDhBZis1bHROTEpRK0pqc0Z3MXUiLCJtYWMiOiI5NjI3YTIyZmE4ZmM3YjY3MTAxZTE2MGFiMDljYzk4NzU3ZTVhYTE5OWEwYTVhMTJiMGU5NGFiMjgyN2RmODY3IiwidGFnIjoiIn0='
                                },
                            callback=self.offer_parse,
                            errback=self.errback_httpbin,
                             )
            

    def offer_parse(self, response):
        res = response.json()
        # meta = response.css('meta::attr(content)').extract()
        self.logger.info('=======offer_parse===response.headers===csrf-token= {}'.format(res))
        content = response.body
        paramresult = {
            'year' : res["vin_data"]["attributes"]["year"],
            "make" : res["vin_data"]["attributes"]["make"],
            "model" : res["vin_data"]["attributes"]["model"],
            "trim" : res["vin_data"]["attributes"]["trim"],
            "type" : res["vin_data"]["attributes"]["type"],
            "size" : res["vin_data"]["attributes"]["size"],
            "category" : res["vin_data"]["attributes"]["category"],
            "made_in" : res["vin_data"]["attributes"]["made_in"],
            "made_in_city" : res["vin_data"]["attributes"]["made_in_city"],
            "doors" : res["vin_data"]["attributes"]["doors"],
            "fuel_type" : res["vin_data"]["attributes"]["fuel_type"],
            "fuel_capacity" : res["vin_data"]["attributes"]["fuel_capacity"],           

        }
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
            "trim": 'null',
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
                    "manufacturer_suggested_retail_price": res["vin_data"]["attributes"]["manufacturer_suggested_retail_price"],
                    "color": "Black",
                    "mileage": self.mileage,
                    "zip_code": self.zip_code,
                    "conditions": {
                        "vehicle_condition": "Needs Lots Of Love",
                        "vehicle_accident": "2+ Accident",
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
                "colors":res["vin_data"]["colors"],
                "recalls": res["vin_data"]["recalls"],
                "photos": res["vin_data"]["photos"],
                "success": True,
                "error": ""
            }
        }
        request_body = json.dumps(form_data)
        result = request_body
        yield scrapy.http.JsonRequest('https://cars.allcars.com/sell-your-car/drivably/additional_info/56922/execute-node-offer-scraper',
                            method="POST",
                            body=request_body,
                            headers={
                                'Content-Type': 'application/json;charset=UTF-8', 
                                'USER_AGENT':'carprice (+https://cars.allcars.com)',
                                'referer':'https://cars.allcars.com/sell-your-car',
                                'x-csrf-token':self.meta_data,
                                'x-xsrf-token': 'eyJpdiI6InM1cWhlQkRwbXIxdU5vKzlFZWVRVXc9PSIsInZhbHVlIjoiUXlCM21hTXlxRE9nRTVNMS9ROHNxQ1p4K1RPUEFEWVd6K09JdnhVSWdrdTdGaWdOVHhjbnNZUGJraGVhR3R2SFhEbHJUQmJHSkt2UEdjMUFISVNzTDlNMmgvQjBUQWZxZ0RTalYzakFtSU1ubDhBZis1bHROTEpRK0pqc0Z3MXUiLCJtYWMiOiI5NjI3YTIyZmE4ZmM3YjY3MTAxZTE2MGFiMDljYzk4NzU3ZTVhYTE5OWEwYTVhMTJiMGU5NGFiMjgyN2RmODY3IiwidGFnIjoiIn0='
                                },
                            callback=self.parse,
                            errback=self.errback_httpbin,
                            cb_kwargs={
                                'result': res,
                            })
        

    def parse(self, response, result):
        offerdata = response.json()
        self.logger.info('======parse==response==offerdata= {}'.format(offerdata))
        resultParam = json.dumps(result)
        self.logger.info('======parse==result=== {}'.format(resultParam))
        attributes = result["vin_data"]["attributes"]
        result['year']=attributes["year"]
        result["make"]=attributes["make"]
        result["model"]=attributes["model"]
        result["trim"]=attributes["trim"]
        result["type"]=attributes["type"]
        result["size"]=attributes["size"]
        result["category"]=attributes["category"]
        result["made_in"]=attributes["made_in"]
        result["made_in_city"]=attributes["made_in_city"]
        result["doors"]=attributes["doors"]
        result["fuel_type"]=attributes["fuel_type"]
        result["fuel_capacity"]=attributes["fuel_capacity"]
        result["city_mileage"]=attributes["city_mileage"]
        result["highway_mileage"]=attributes["highway_mileage"]
        result["engine"]=attributes["engine"]
        result["engine_size"]=attributes["engine_size"]
        result["engine_cylinders"]=attributes["engine_cylinders"]
        result["transmission"]=attributes["transmission"]
        result["transmission_type"]=attributes["transmission_type"]
        result["transmission_speeds"]=attributes["transmission_speeds"]
        result["drivetrain"]=attributes["drivetrain"]
        result["anti_brake_system"]=attributes["anti_brake_system"]
        result["steering_type"]=attributes["steering_type"]
        result["gross_vehicle_weight_rating"]=attributes["gross_vehicle_weight_rating"]
        result["overall_height"]=attributes["overall_height"]
        result["overall_length"]=attributes["overall_length"]
        result["overall_width"]=attributes["overall_width"]
        result["wheelbase_length"]=attributes["wheelbase_length"]
        result["standard_seating"]=attributes["standard_seating"]
        result["offer_price"]=attributes["manufacturer_suggested_retail_price"]  
        
        #conditions 
        try:            
            conditions = attributes["conditions"]
            self.logger.info('======conditions= {}'.format(conditions))
            result["What is the condition of the vehicle?"]=conditions["vehicle_condition"]
            result["Has the vehicle been in an accident?"]=conditions["vehicle_accident"]
            result["Optional Equipment"]=conditions["optional_equipment"][0]
            result["Title Present"]=conditions["title_present"]
            result["Title Issues"]=conditions["title_issues"]
            result["Frame Damage"]=conditions["frame_damage"]
            result["Glass Damage"]=conditions["glass_damage"]
            result["Rust Damage"]=conditions["rust_damage"]
            result["Body Damage"]=conditions["body_damage"]
            result["Engine Issues"]=conditions["engine_issues"]
            result["Interior Issues"]=conditions["interior_issues"]
            result["Mechanical Issues"]=conditions["mechanical_issues"]
            result["Warning Lights"]=conditions["warning_lights"]
            result["Modifications"]=conditions["modifications"]
            result["Tire Issues"]=conditions["tire_issues"]
            result["Tire Tread"]=conditions["tire_tread"]
            result["Transmission"]=conditions["transmission"]
        except:
            print("An exception occurred")
            result["What is the condition of the vehicle?"]="No"
            result["Has the vehicle been in an accident?"]="No"
            result["Optional Equipment"]="No"
            result["Title Present"]="No"
            result["Title Issues"]="No"
            result["Frame Damage"]="No"
            result["Glass Damage"]="No"
            result["Rust Damage"]="No"
            result["Body Damage"]="No"
            result["Engine Issues"]="No"
            result["Interior Issues"]="No"
            result["Mechanical Issues"]="No"
            result["Warning Lights"]="No"
            result["Modifications"]="No"
            result["Tire Issues"]="No"
            result["Tire Tread"]="No"
            result["Transmission"]="No"

        result['firstname']= self.first_name
        result['lastname']=self.last_name
        result['email']= self.email
        result['phone_number']=self.phone_number
        result['zip_code']=self.zip_code
        result['mileage']=self.mileage
        self.logger.info('===final===parse==result=== {}'.format(result))
        yield result
    
        #Error Handling
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

