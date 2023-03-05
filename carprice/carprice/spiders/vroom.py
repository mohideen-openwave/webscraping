import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import re
from scrapy_playwright.page import PageMethod
from datetime import datetime
import math
import json
import requests
 

 

class CarPricesVroomSpider(scrapy.Spider):
    name = "car_prices_vroom"
    proxy = 'http://dvafvogc:c75babt2ovb6@184.174.58.205:5767'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    drive_url = f'https://www.vroom.com/appraisal/api/appraisal'
    
        
    def start_requests(self):
        #Initial data
        yield scrapy.http.JsonRequest(
            url=f'https://www.vroom.com/appraisal/api/appraisal',
            callback=self.parse_vin_trim_driveway,
            errback=self.errback_httpbin,
            headers = {
            'Content-type': 'application/json',
            'User-Agent':"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
            'Accept': '*/*',
            'Host': 'api-gateway.driveway.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
              },
        )

    def parse_vin_trim_driveway(self, response):
        #Response from api calls
        json_response = response.json()
        self.logger.info('===FullDetails====parse_vin_trim_driveway======Got successful response from {}'.format(json_response))
        year = json_response['year']
        make = json_response['make']
        model = json_response['model']
        vin = json_response['vin'] 
        tempTrim = json_response['availableTrims']
        self.logger.info('====parse_vin_trim_driveway======tempTrim {}'.format(tempTrim))
        if json_response['selectedTrim']['name']:
            selectedTrim = json_response['selectedTrim']
            self.logger.info('====parse_vin_trim_driveway====if==selectedTrim {}'.format(selectedTrim))
        else:
            tmparray = [x for x in tempTrim if x['name'] == self.trim]
            selectedTrim = tmparray[0]
            self.logger.info('====parse_vin_trim_driveway===else===selectedTrim {}'.format(selectedTrim))
            

        self.logger.info('====parse_vin_trim_driveway======year {}'.format(year))
        
        try:
            result = {
                'firstname' : self.first_name,
                'lastname':self.last_name,
                'email': self.email,
                'phone_number':self.phone_number,
                'zip_code':self.zip_code,
                'mileage':self.mileage,
                'year' : year,
                'make' : make,
                'model' : model,
                'vin': vin,
                'selectedTrim' : selectedTrim
            }
            # Coditions
            if(self.condition=='Excellent'):
                condition = 'GREAT'
            elif(self.condition=='Good'):
                condition = 'GOOD'
            elif(self.condition=='Moderate'):
                condition = 'FAIR'
            else:
                condition = 'POOR'
               
            
            yield scrapy.http.JsonRequest(
                url=f'https://api-gateway.driveway.com/sell/v8/offer?dealershipCode=cdjr-pocatello&saleType=SELL&key=e6c1852eb5124b1890fbd17ad53e870a',
                method='POST',
                callback=self.parse_driveway_offer,
                errback=self.errback_httpbin,
                headers = {
                'Content-type': 'application/json',
                'User-Agent':"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
                'Accept': '*/*',
                'Host': 'api-gateway.driveway.com',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                },
                data={
                    "email": self.email,
                    "phone": self.phone_number,
                    "firstName": self.first_name,
                    "lastName": self.last_name,
                    "location": {
                        "postalCode": self.zip_code,
                        "distanceInMiles": 0,
                        "withinMarket": False
                    },
                    "vehicle": {
                        "vin": self.vin,
                        "year": year,
                        "make": make,
                        "model": model,
                        "selectedTrim": selectedTrim,
                        "condition": {
                            "overallCondition": condition,
                            "mileage": self.mileage,
                            "warningLights": False,
                            "accidents": False,
                            "smokedIn": False,
                            "activeLoans": 'null',
                            "activeFinance": {
                                "type": "NOT_PROVIDED",
                                "estimatedRemaining": 0,
                                "lenderId": ""
                            },
                            "numKeys": "MULTIPLE"
                        },
                        "licensePlate": "JTDKARFU6K3087621",
                        "alternatives": []
                    }
                },
                cb_kwargs={
                'result': result,
                 }
            )
            # with open("driveway.json","w") as outfile:
            #     outfile.write(json_object)        

        except json.JSONDecodeError:
            print("Empty response")
            self.logger.error('===Error {}'.format(json_response))
    
 
    def parse_driveway_offer(self, response, result):
        json_response = response.json()
        self.logger.info("===============parse_driveway_offer %s", json_response)
        lead = json_response['lead']
        self.logger.info("===============parse_driveway_offer price {}".format(lead['offer']['offerAmount']))
        
        result['datetime'] = datetime.utcnow()
        result['source'] = 'Driveway' 
        result['User give condition'] = self.condition       
        result['What is the condition of the car?'] = lead['vehicle']['condition']['overallCondition']
        result['Any active loan or lease on the car?'] = lead['vehicle']['condition']['activeFinance']['type']
        result['Has the car been in an accident?'] = 'No'
        result['Are there active warning lights?'] =  'No'
        result['Has the car been smoked in?'] = 'No'
        result['How many keys are available?'] = 2
        result['price'] = lead['offer']['offerAmount']
        result['carfaxUrl'] = json_response['lead']['carfaxUrl']
       

        


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
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

