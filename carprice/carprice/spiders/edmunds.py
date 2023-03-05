import scrapy
import re
import math


class CarPricesEdmundsSpider(scrapy.Spider):
    name = "car_prices_edmunds"
    proxy = 'http://dvafvogc:c75babt2ovb6@184.174.58.205:5767'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }


    special_character_except_dash_and_underscore_pattern = re.compile(r'[^a-zA-Z0-9_-]')
    def start_requests(self):
        #Initial data
        yield scrapy.Request(
            url=f'https://www.edmunds.com/gateway/api/vehicle/v3/styles/vins/{self.vin.upper()}',
            callback=self.parse_json_response,
            headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.edmunds.com/appraisal/',
            },
        )

    def parse_json_response(self, response): 
        json_response = response.json()
        self.logger.info('===FullDetails====parse_json_response======Got successful response from {}'.format(json_response))

        vehicle_info = json_response[0]
        # self.logger.info('======process request==={}'.format(vehicle_info['makeName']))
        
        make = vehicle_info['makeName'].lower().replace(' ', '-')
        model = vehicle_info['modelName'].lower().replace(' ', '-')
        year = vehicle_info['year']
        style_id = vehicle_info['styleId']
        result = {
            "make" : make,
            "model" : model,
            "year" : year,
            "style_id" : style_id,
        }
        yield scrapy.FormRequest(
            url=f'https://www.edmunds.com/gateway/api/v2/usedtmv/getalltmvbands',
            method='GET',
            callback=self.parse_json_offer_response,
            headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'referer': f'https://www.edmunds.com/{make}/{model}/{year}/appraisal-value/?vin={self.vin.upper()}&styleIds={style_id}',
                'x-referer': f'https://www.edmunds.com/{make}/{model}/{year}/appraisal-value/',
            },
            formdata={
                'styleid': str(style_id),
                'zipcode': self.zip_code,
                'mileage': self.mileage,
                'typical': 'false',
                'view': 'full',
                'priceband': 'false',
            },
            cb_kwargs={
                'result': result,
            },
        )

    def parse_json_offer_response(self, response, result): 
        vehicle_info = response.json()
        self.logger.info('=====parse_json_offer_response======Got successful response from {}'.format(vehicle_info))
        # vehicle_info = json_response[0]
        make = result['make']
        model = result['model']
        year = result['year']
        style_id = result['style_id']
        #more quests details
        yield scrapy.http.JsonRequest(
            url=f'https://www.edmunds.com/api/partner-offers/v2/quotes',
            method='POST',
            callback=self.parse_json_quotes_response,
            headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'referer': f'https://www.edmunds.com/{make}/{model}/{year}/appraisal-value/?vin={self.vin.upper()}&styleIds={style_id}',
                'x-referer': f'https://www.edmunds.com/{make}/{model}/{year}/appraisal-value/',
            },
            data={
                "vin": "SALVP2RX1JH284344"
            },
            cb_kwargs={
                'result': result,
            },
        )
    
    def parse_json_quotes_response(self, response, result): 
        json_response = response.json()
        self.logger.info('=====parse_json_quotes_response======Got successful response from {}'.format(json_response))
        quotesRw = json_response
        result["isEligible"] = quotesRw["isEligible"]
        result["quoteId"] = quotesRw["lastQuote"]["quoteId"]
        result["visitorId"] = quotesRw["lastQuote"]["visitorId"]
        result["storeId"] = quotesRw["lastQuote"]["ciamId"]
        result["sourceSystem"] = quotesRw["lastQuote"]["sourceSystem"]
        result["code"] = quotesRw["lastQuote"]["code"]
        result["vin"] = quotesRw["lastQuote"]["vin"]
        result["make"] = quotesRw["lastQuote"]["make"]
        result["model"] = quotesRw["lastQuote"]["model"]
        result["year"] = quotesRw["lastQuote"]["year"]
        result["trim"] = quotesRw["lastQuote"]["trim"]
        result["bodyStyle"] = quotesRw["lastQuote"]["bodyStyle"]
        result["mileage"] = quotesRw["lastQuote"]["mileage"]
        result["styleCode"] = quotesRw["lastQuote"]["styleCode"]
        result["transmission"] = quotesRw["lastQuote"]["transmission"]
        result["drive"] = quotesRw["lastQuote"]["drive"]
        result["zipCode"] = quotesRw["lastQuote"]["zipCode"]
        result["valuation"] = quotesRw["lastQuote"]["valuation"]
        result["createdDateUtc"] = quotesRw["lastQuote"]["createdDateUtc"]
        result["expiresDateUtc"] = quotesRw["lastQuote"]["expiresDateUtc"]
        result["expiresDisplayDate"] = quotesRw["lastQuote"]["expiresDisplayDate"]
        result["appointmentUri"] = quotesRw["lastQuote"]["appointmentUri"]
        result["redemptionCertificateUri"] = quotesRw["lastQuote"]["redemptionCertificateUri"]
        result["declineReason"] = quotesRw["lastQuote"]["declineReason"]
        result["isPicsyEligible"] = quotesRw["lastQuote"]["isPicsyEligible"]
     
        print(list(filter(lambda x:x["id"]==410,quotesRw["lastQuote"]["conditionQuestions"])))
        result["Has the vehicle ever been in an accident?"] = "No"
        result["Does the vehicle have any frame damage?"] = "No"
        result["Does the vehicle have any flood damage?"] = "No"
        result["Has this vehicle been smoked in?"] = "No"
        result["Are any interior parts broken or inoperable?"] = "No"
        result["Are there any rips, tears, or stains in the interior?"] = "No"
        result["Are there any mechanical issues or warning lights displayed on the dashboard?"] = "No"
        result["Has the odometer ever been broken or replaced?"] = "No"
        result["Are there any panels in need of paint or body work?"] = "No"
        result["Any major rust and/or hail damage?"] = "No"
        result["Do any tires need to be replaced?"] = "No"
        result["How many keys do you have?"] = "No"
        result["Does the vehicle have any aftermarket modifications?"] = "No"
        result["Are there any other issues with the vehicle?"] = "No"
        result["Vehicle Condition"] = "No"
        result["Add Additional Equipment"] = "No"
        result["Exterior color"] = quotesRw["lastQuote"]["exteriorColorCode"]
        result["Interior color"] = quotesRw["lastQuote"]["metaData"]["interior_color"]
        
        # yield result

    def process_requests(self, result):
        vin_details_response = yield scrapy.Request(
            url=f'https://www.edmunds.com/gateway/api/vehicle/v3/styles/vins/{self.vin.upper()}',
            callback=self.parse_json_response,
            headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.edmunds.com/appraisal/',
            },
        )

        vehicle_info = vin_details_response[0]
        self.logger.info('======process request==={}'.format(vehicle_info))
        make = vehicle_info['makeName'].lower().replace(' ', '-')
        model = vehicle_info['modelName'].lower().replace(' ', '-')
        year = vehicle_info['year']
        style_id = vehicle_info['styleId']

        offer_response = yield scrapy.FormRequest(
            url=f'https://www.edmunds.com/gateway/api/v2/usedtmv/getalltmvbands',
            method='GET',
            callback=self.parse_json_response,
            headers={
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'referer': f'https://www.edmunds.com/{make}/{model}/{year}/appraisal-value/?vin={self.vin.upper()}&styleIds={style_id}',
                'x-referer': f'https://www.edmunds.com/{make}/{model}/{year}/appraisal-value/',
            },
            formdata={
                'styleid': str(style_id),
                'zipcode': self.zip_code,
                'mileage': self.mileage,
                'typical': 'false',
                'view': 'full',
                'priceband': 'false',
            },
        )

        conditions = {
            'bad': 'ROUGH',
            'moderate': 'AVERAGE',
            'good': 'CLEAN',
            'excellent': 'OUTSTANDING',
        }
        condition = conditions[self.condition]

        # result["firstname"] = 
        price = offer_response['tmvconditions'][condition]['Current']['totalWithOptions']['usedTradeIn']

        result['price'] = price

        yield result
