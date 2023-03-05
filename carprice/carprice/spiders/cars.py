import scrapy
from Tools.scripts import ifdef
from scrapy.http import request
from scrapy.http.request.form import FormRequest
from scrapy.http import FormRequest
import json
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class CarPricesCarsSpider(scrapy.Spider):
    name = 'car_prices_cars'
    allowed_domains = ['cars.com', 'perseus-api-production.accu-trade.com']
    meta_data = ''

    def start_requests(self):
        form_data = {}
        request_body = json.dumps(form_data)
        # self.logger.info('========start_requests==request_body= {}'.format(request_body))
        site_url = 'https://perseus-api-production.accu-trade.com/api/vehicle/by-vin/{}'.format(self.vin)
        yield scrapy.http.JsonRequest(
            site_url,
            method="GET",
            body=request_body,
            headers={
                'Content-type': 'application/json;charset=UTF-8',
                'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
                'Accept': '*/*',
                'origin': 'https://cashoffer.accu-trade.com',
                'Referer': 'https://cashoffer.accu-trade.com/',
                'authorization': 'Token e5c6f6ea496ed8afac97830b4601539ab0aa79d1',
            },
            callback=self.vehicle_lookup_parse,
            errback=self.errback_httpbin)

    def vehicle_lookup_parse(self, response):
        json_response = response.json()
        # self.logger.info('=======vehicle_lookup_parse===response.headers===csrf-token= {}'.format(json_response))
        result = json_response
        form_data = {
            "custom_questions": {},
            "vehicle_vin": self.vin,
            "vehicle_year": json_response[0]['year'],
            "vehicle_make": json_response[0]['make'],
            "vehicle_model": json_response[0]['model'],
            "vehicle_style": json_response[0]['style'],
            "vehicle_source_id": 305456,
            "vehicle_specialized": False,
            "vehicle_mismatch": False,
            "vehicle_manual_entry": False,
            "vehicle_source": 1,
            "did_agree_to_tos": False,
            "vacs": [],
            "color_adjustment": 0,
            "vehicle_odor_adjustment": 0,
            "media": {
                "vehicle": {
                    "other": []
                }
            },
            "completion": 0.33,
            "lt": "dealer",
            "visitor_uuid": "31dc873b-e454-46c3-b357-528db02c0df9",
            "pricing_type": "gp",
            "lead_source": "leadstart_widget",
            "additional_images": [],
            "status": "draft"
        }
        request_body = json.dumps(form_data)
        yield scrapy.http.JsonRequest('https://perseus-api-production.accu-trade.com/api/offer/',
                                      method="POST",
                                      body=request_body,
                                      headers={
                                          'Content-type': 'application/json;charset=UTF-8',
                                          'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
                                          'Accept': '*/*',
                                          'origin': 'https://cashoffer.accu-trade.com',
                                          'Referer': 'https://cashoffer.accu-trade.com/',
                                          'authorization': 'Token e5c6f6ea496ed8afac97830b4601539ab0aa79d1',
                                      },
                                      callback=self.offer_parse,
                                      errback=self.errback_httpbin,
                                      cb_kwargs={
                                          'result': result
                                      })

    def offer_parse(self, response, result):
        json_response = response.json()
        # self.logger.info('=======offer_parse===response= {}'.format(json_response))
        form_data = {
            "consumer": 11364789,
            "custom_questions": {},
            "vehicle_vin": self.vin,
            "vehicle_year": result[0]['year'],
            "vehicle_make": result[0]['make'],
            "vehicle_model": result[0]['model'],
            "vehicle_style": result[0]['style'],
            "vehicle_source_id": 305456,
            "vehicle_specialized": False,
            "vehicle_mismatch": False,
            "vehicle_manual_entry": False,
            "vehicle_source": 1,
            "did_agree_to_tos": True,
            "vacs": [],
            "vehicle_image": 'null',
            "color_adjustment": 50,
            "vehicle_odor_adjustment": 0,

            "id": 11409089,
            "range_low": 5075,
            "range_high": 7075,
            "needs_dealer_review": False,
            "loan_payoff": 'null',
            "loan_equity": 'null',

            "vehicle_mileage": self.mileage,
            "add_optional_photos": False,
            "key_fobs": "2",
            "vehicle_color": 2,
            "vehicle_interior_color": 2,
            "is_original_owner": True,
            "is_liened": False,
            "has_mechanical_issues": False,
            "has_warning_lights": False,
            "has_modifications": False,
            "has_other_issues": False,
            "hasSignificantIssuesRequired": "",
            "has_accident": False,
            "carfax_has_bad_vhr": True,
            "has_significant_issues": False,
            "expect_transact_months": "0",
            "completion": 1,
            "vehicle_base_price": json_response["vehicle_base_price"],
            "vehicle_trade_price": json_response["vehicle_trade_price"],
            "vehicle_market_price": json_response["vehicle_market_price"],
            "lt": "dealer"
        }
        request_body = json.dumps(form_data)
        yield scrapy.http.JsonRequest('https://perseus-api-production.accu-trade.com/api/offer/guaranteed-price/calculate/1/',
                                      method="POST",
                                      body=request_body,
                                      headers={
                                          'Content-type': 'application/json;charset=UTF-8',
                                          'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
                                          'Accept': '*/*',
                                          'origin': 'https://cashoffer.accu-trade.com',
                                          'Referer': 'https://cashoffer.accu-trade.com/',
                                          'authorization': 'Token e5c6f6ea496ed8afac97830b4601539ab0aa79d1',
                                      },
                                      callback=self.parse,
                                      errback=self.errback_httpbin,
                                      cb_kwargs={
                                          'result': json_response
                                      })

    def parse(self, response, result):
        json_response = response.json()
        # self.logger.info('======parse==response==offer-data= {}'.format(json_response))
        result_param = json.dumps(result)
        # self.logger.info('======parse==result=== {}'.format(result_param))

        # write json out
        result1 = result
        result1['source'] = "cars.com"
        result1['year'] = result["vehicle_year"]
        result1["make"] = result["vehicle_make"]
        result1["model"] = result["vehicle_model"]
        result1["trim"] = self.trim
        result1["private_sale_time"] = result["private_sale_time"]
        result1["style"] = result["vehicle_style"]
        result1["Dealer tax saving"] = result["dealer_tax_savings"]
        result1["dealer_sale_time"] = result["dealer_sale_time"]
        result1["private_expected_depreciation"] = result["private_expected_depreciation"]
        result1["state_tax"] = result["state_tax"]
        result1["untaxed_amount"] = result["untaxed_amount"]
        result1["offer_short_code"] = result["offer_short_code"]
        result1["type"] = result["type"]
        result1["pricing_type"] = result["pricing_type"]
        result1["status"] = result["status"]
        result1["vehicle_includes"] = result["vehicle_includes"]
        result1["vehicle_base_miles"] = result["vehicle_base_miles"]
        result1["vehicle_trade_price"] = result["vehicle_trade_price"]
        result1["vehicle_market_price"] = result["vehicle_market_price"]
        result1["vehicle_base_price"] = result["vehicle_base_price"]
        result1["vehicle_engine_type"] = result["vehicle_engine_type"]
        result1["range_low"] = result["range_low"]
        result1["range_high"] = result["range_high"]
        result1["guaranteed_price"] = result["guaranteed_price"]
        result1["price"] = json_response["value"]
        result1["Minimum Price"] = json_response["range"][0]
        result1["Maximum Price"] = json_response["range"][1]

        # vehical condition
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
        result1["Select your value impacting options"] = "Not Selected"
        result1["How many miles are displayed on your odometer?"] = result["vehicle_base_miles"]
        result1["Upload photos of your car?"] = "No"
        result1["What color is your car?"] = "Black"
        result1["How many keys do you have?"] = "1"
        result1["Are you the original owner?"] = "yes"
        result1["Are you still making payments on your vehicle?"] = "No"
        result1["Was your car ever in an accident?"] = "No"
        result1["Does your vehicle have a clean history report?"] = "yes"
        result1["Does your vehicle have any current issues?"] = "No"

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

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('ErrorHandling===DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('ErrorHandling===TimeoutError on %s', request.url)
