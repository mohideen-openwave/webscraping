import json
import requests


def main():
    URL = "https://api-gateway.driveway.com/sell/v8/offer?dealershipCode=cdjr-pocatello&saleType=SELL&key=e6c1852eb5124b1890fbd17ad53e870a"
    # word = input("Enter a word:")
    param = {
        "email": "asdfasd@ld.com",
        "phone": "3333333330",
        "firstName": "sdfsadfasd",
        "lastName": "dsafadsf",
        "location": {
            "postalCode": "84542",
            "distanceInMiles": 0,
            "withinMarket": False
        },
        "inspectionPreferences": {
            "contactPreference": "EMAIL"
        },
        "vehicle": {
            "vin": "1FTEW1EG0FFA25695",
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
                "mileage": 103000,
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
    data = requests.post(URL, data=json.dumps(param), headers=headers)

    try:
        print(data.status_code)
        # data_json = json.loads(data)
        # print(data_json)
        data_json = data.json()
        json_object = json.dumps(data_json)
        print(data_json)
        #Write the out in json file
        with open("driveway.json","w") as outfile:
            outfile.write(json_object)        

    except json.JSONDecodeError:
        print("Empty response")

# def main():
#     URL = "http://httpbin.org/post"
#     # word = input("Enter a word:")
#     param = {"key": "value"}

#     data = requests.post(URL, param)

#     try:
#         data.status_code
#         print(data.json())
#         # data_json = json.loads(data)
#         # print(data_json)
#     except json.JSONDecodeError:
#         print("Empty response")


if __name__ == "__main__":
    main()
