from auth import AuthFedex
import pandas as pd
import requests
import json
from config import Config
from table_processing import TableProcessing
from decorators import renew_access_token


class CalculationParcels:
    @classmethod
    @renew_access_token
    def getting_price(cls):
        config = Config.auth_conf()
        parcels_sizes = TableProcessing.getting_table()
        url = "https://apis-sandbox.fedex.com/rate/v1/rates/quotes"
        list_price = []
        for size in parcels_sizes:
            print(size)
            rates_payload = {
                "accountNumber": {
                    "value": config["account"]
                },
                "requestedShipment": {
                    "shipper": {
                        "address": {
                            "postalCode": 78731,  # need valid postal codes
                            "countryCode": "US"
                        }
                    },
                    "recipient": {
                        "address": {
                            "postalCode": 90210,
                            "countryCode": "US",
                            "residential": "true"
                        }
                    },
                    "pickupType": "CONTACT_FEDEX_TO_SCHEDULE",
                    "serviceType": "GROUND_HOME_DELIVERY",
                    "preferredCurrency": "USD",
                    "rateRequestType": [
                        "ACCOUNT"
                    ],
                    "requestedPackageLineItems": [
                        {
                            "weight": {
                                "units": "LB",
                                "value": size.lbs
                            },
                            "dimensions": {
                                "length": size.length,
                                "width": size.width,  # data from tables
                                "height": size.height,
                                "units": "IN"
                            }
                        }
                    ]
                }
            }
            headers = {
                'Content-Type': "application/json",
                'X-locale': "en_US",
                'Authorization': f"Bearer {config['access_token']}"
            }

            response = requests.request("POST", url, data=json.dumps(rates_payload), headers=headers)
            price_dict = cls.cut_price(response, size.id)
            list_price.append(price_dict)
        return cls.add_price_to_table(list_price)

    @classmethod
    def add_price_to_table(cls, list_price):
        df_excel = pd.read_excel('test_table.xlsx')
        df_prices = pd.DataFrame(list_price)
        result = pd.merge(df_excel, df_prices, left_index=True, right_index=True)
        return result.to_excel('test_table.xlsx', index=False)

    @classmethod
    def cut_price(cls, response, parcels_id):
        info_parcels = response.json()
        rate_replay_details = info_parcels['output']['rateReplyDetails']

        price_dict = {
            'id': parcels_id,
            'totalBaseCharge': rate_replay_details[0]['ratedShipmentDetails'][0]['totalBaseCharge'],
            'totalNetCharge': rate_replay_details[0]['ratedShipmentDetails'][0]['totalNetCharge'],
            'ratedShipmentDetails': rate_replay_details[0]['ratedShipmentDetails'][0]['totalNetFedExCharge']}
        return price_dict


print(CalculationParcels.getting_price())
