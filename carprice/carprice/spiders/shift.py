import scrapy
from Tools.scripts import ifdef
from scrapy.http import request
from scrapy.http.request.form import FormRequest
from scrapy.http import FormRequest
import json
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import time
from http.cookies import SimpleCookie

class CarPricesCarsSpider(scrapy.Spider):
    name = 'car_prices_shift'
    allowed_domains = ['shift.com']
    meta_data = ''
    proxy = 'http://dvafvogc:c75babt2ovb6@45.158.187.187:7196'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }
    global_cookies = ''
    def start_requests(self):
        captcha_solving_task_creation_response = yield scrapy.http.JsonRequest(
            url='https://api.capsolver.com/createTask',
            headers={
                'Accept': '*/*',
                'Content-Type': 'application/json',
            },
            data={
                'clientKey': 'CAI-B4FFF136581A0240260C4C4B8B4C0381',
                'task': {
                    'type': 'DatadomeSliderTask',
                    'websiteURL': f'https://shift.com/api/consumer/v1/lp_vin_details?vin={self.vin.upper()}',
                    'captchaUrl': 'https://geo.captcha-delivery.com/captcha/?initialCid=AHrlqAAAAAMA_VBUvSlCUysAerIrfQ==&cid=0DZsUI2lEkciy39BZTqiNbAtljNlIlgQ066xTSonkwSgU-9s7QTX_02IxtxvtDsB1_MZKO7BCyuEvRe6JksxnDM9LwUF~XTAV4dp9hdcUs3VzXPxWyswNdlWi5CHEuEY&referer=http%3A%2F%2Fshift.com%2Fapi%2Fconsumer%2Fv1%2Flp_vin_details%3Fvin%3DSALVP2RX1JH284344&hash=2065822642B818FC6FB69F4B5EA4A4&t=fe&s=36395&e=15cbc0399ea4e863ce84e328b241df8ab14a892c38efc33f50ca5ea064a5d681',
                    "proxy": "socks5:185.102.50.102:7185:dvafvogc:c75babt2ovb6",
                    "userAgent": "'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"

                },
            },
            callback=self.parse_json_response1,
        )
        self.logger.info('=======captcha_solving_task_creation_response= {}'
                         .format(captcha_solving_task_creation_response))

    def parse_json_response1(self, response):
        json_response = response.json()
        captcha_solving_task_creation_response = json_response
        self.logger.info('=======parse_json_response= {}'.format(json_response))
        captcha_solving_task_id = captcha_solving_task_creation_response['taskId']
        self.logger.info('=======captcha_solving_task_id= {}'.format(captcha_solving_task_id))
        captcha_solution_token = None
        while (captcha_solution_token is None):
            time.sleep(20)
            captcha_solving_task_status_response = yield scrapy.http.JsonRequest(
                method="POST",
                url='https://api.capsolver.com/getTaskResult',
                headers={
                    'Accept': '*/*',
                    'Content-Type': 'application/json',
                },
                data={
                    'clientKey': 'CAI-B4FFF136581A0240260C4C4B8B4C0381',
                    'taskId': captcha_solving_task_id,
                },
                callback=self.capsolver_final_response,
                dont_filter=True,
            )

            self.logger.info('====IsSideWhileLoop===captcha_solving_task_status_response= {}'
                             .format(captcha_solving_task_status_response))
            # if captcha_solving_task_status_response['errorId'] > 0:
            #     raise RuntimeError(captcha_solving_task_status_response['errorDescription'])

            if captcha_solving_task_status_response['status'] == 'ready':
                captcha_solution_token = captcha_solving_task_status_response
        #
        # self.logger.info('====captcha_solution_token= {}'.format(captcha_solution_token))

    def capsolver_final_response(self, response):
        json_response = response.json()
        captcha_solving_task_creation_response = json_response
        self.logger.info('====jsonresponse===capsolver_final_response= {}'.format(json_response))

        cookie_entries = json_response['solution']['cookie'].split('; ')

        def cookie_entry_to_key_value_pair(entry):
            pair = entry.split('=')
            return pair if len(pair) == 2 else [pair[0], '']

        cookie_pairs = [cookie_entry_to_key_value_pair(entry) for entry in cookie_entries]
        cookie_dict = {k: v for k, v in cookie_pairs}
        self.logger.debug(cookie_dict)
        self.global_cookies = cookie_dict
        vin_request = scrapy.http.JsonRequest(
            url=f'https://shift.com/api/consumer/v1/lp_vin_details?vin={self.vin.upper()}',
            method='GET',
            headers={
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'text/json',
                "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
            },
            cookies=self.global_cookies,
            callback=self.offer_actual_data_response,
            errback=self.errback_httpbin,
        )
        self.logger.info("=======vin_request====before yield {}".format(vin_request))
        yield vin_request

    def offer_actual_data_response(self, response):
        json_response = response.json()
        self.logger.info('=======actual_data_response= {}'.format(json_response))
        request_para = {
                          "analytics_info": {
                            "context": {
                              "campaign": {
                                "content": '',
                                "medium": '',
                                "name": '',
                                "source": '',
                                "term": ''
                              },
                              "page": {
                                "path": "/sell-my-car/estimate/pet1.ck1pt.Yo83Krrtc4rT_tb5t60HCk3L44P-FawxyEIO_yYlzO7e3XEv7LlJZu4RICc-0LEp04qJ28zgMJ74rN3RZWLwLheEJSPlcj8cMclf3EiZm38Ljpqq_FcHWoAdcp_sKN7p8ymy-qdY-rhiMzutRaxgl0k9..1",
                                "referrer": f"https://shift.com/quote-flow/condition?vin={self.vin.upper()}",
                                "search": "",
                                "title": "Dashboard | Shift",
                                "url": "https://shift.com/sell-my-car/estimate/pet1.ck1pt.Yo83Krrtc4rT_tb5t60HCk3L44P-FawxyEIO_yYlzO7e3XEv7LlJZu4RICc-0LEp04qJ28zgMJ74rN3RZWLwLheEJSPlcj8cMclf3EiZm38Ljpqq_FcHWoAdcp_sKN7p8ymy-qdY-rhiMzutRaxgl0k9..1"
                              }
                            },
                            "google_click_identifier": ''
                          },
                          "app_info": {
                            "app_identifier": "ConsumerWeb",
                            "app_version": "1.0.2",
                            "build": "2023-02-23T00:32:35Z_bk-gae-29879"
                          },
                          "auth_info": {
                            "csrf_token": "",
                            "user_account_csrf_token": ""
                          },
                          "client_info": {
                            "locale": "en-US",
                            "os_name": "Win32",
                            "os_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                            "timestamp": "2023-02-23T04:24:40.758Z"
                          },
                          "request": {
                            "token": "pet1.ck1pt.Yo83Krrtc4rT_tb5t60HCk3L44P-FawxyEIO_yYlzO7e3XEv7LlJZu4RICc-0LEp04qJ28zgMJ74rN3RZWLwLheEJSPlcj8cMclf3EiZm38Ljpqq_FcHWoAdcp_sKN7p8ymy-qdY-rhiMzutRaxgl0k9..1"
                          },
                          "request_id": "itst3JssNoc"
                        }

        yield scrapy.http.JsonRequest(
            url=f'https://shift.com/clientapi/consumer/seller/get_price_info_by_pricing_event_token_2',
            method='POST',
            headers={
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/json; charset=UTF-8',
                "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
            },
            data=request_para,
            cookies=self.global_cookies,
            callback=self.final_result,
            errback=self.errback_httpbin,
            cb_kwargs={
                'result': json_response
            }
        )

    def final_result(self, response, result):
        json_response = response.json()
        self.logger.info('=======final_result= {}'.format(json_response))
        result = result
        details = json_response["result"]["content"]["details"]
        instant_cash = details["quote"]["instant_cash"]
        vehicle_details = details["vehicle_details"]
        car_details = details["deal"]["car"]
        result['source'] = "shift.com"
        result['firstname'] = self.first_name
        result['lastname'] = self.last_name
        result['email'] = self.email
        result['phone_number'] = self.phone_number
        result['zip_code'] = self.zip_code
        result['mileage'] = self.mileage
        result["trim"] = details["trim"]
        result['year'] = car_details["year"]
        result["make"] = car_details["make"]
        result["model"] = car_details["model"]
        result["Exterior Color"] = "Black"
        result["Body Style"] = vehicle_details["features"][0]["description"]
        result["Transmission"] = vehicle_details["transmission"]
        result["DriveTrain"] = vehicle_details["drivetrain"]
        result["Engine"] = vehicle_details["engine"]
        result["Select any additional features in your car"] = vehicle_details["features"]
        result["Does your car have any issues that prevent it from starting or driving?"] = "No"
        result["Does your car have any mechanical issues or persistent dashboard warning lights?"] = "No"
        result["Does your car have any aftermarket modifications?"] = "No"
        result[" Does your car have any persistent odors?"] = "No"
        result["Do you have a loan or lease on this vehicle?"] = "No"
        result["Do any of your vehicle’s exterior panels have damage?"] = "No"
        result["Has your vehicle been in an accident?"] = "No"
        result["Does your vehicle have hail damage (or multiple ding/dents on horizontal panels)"] = "No"
        result["Do any of your interior panels have significant damage or missing parts"] = "No"
        result["Does the vehicle have front and back plates?"] = "Yes"
        result["price"] = instant_cash["rounded_amount_usd"]

        self.logger.info('===final===parse==result=== {}'.format(result))

        yield result

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
