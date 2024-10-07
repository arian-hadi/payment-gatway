# from django.conf import settings
# from suds.client import Client


# def zpal_request_handler(merchant_id, amount, description, user_email,user_mobile, callback):
#     client = Client(settings.ZARINPAL['gateway_request_url'])
#     result = client.service.PaymentRequest(
#         merchant_id, amount, description,
#         user_mobile, user_email,callback,
#     )
#     print(f"ZarinPal Response: Status={result.Status}, Authority={result.Authority}")
#     if result.Status == 100:
#         return 'https://sandbox.zarinpal.com/pg/StartPay/' + result.Authority, result.Authority
#     else:
#         print(f"Error with ZarinPal request: Status={result.Status}")
#         return None, None
    
# def zpal_payment_checker(merchant_id, amount, authority):
#     client = Client(settings.ZARINPAL['gateway_callback_url'])
#     result = client.service.PaymentVerification(merchant_id, authority, amount)
#     is_paid = True if result.status in [100,101] else False
#     return is_paid, result.RefID
    
import requests
from django.conf import settings

def zpal_request_handler(merchant_id, amount, description, user_email, user_mobile, callback):
    data = {
        "merchant_id": merchant_id,
        "amount": amount,
        "description": description,
        "callback_url": callback,
    }

    try:
        response = requests.post(settings.ZARINPAL['gateway_request_url'], json=data)
        response_data = response.json()

        # Debugging the response
        print(f"Zarinpal API Response: {response_data}")  


        if response_data.get('data') and response_data['data'].get('authority'):
            if response_data['data'].get('code') == 100:
                return 'https://sandbox.zarinpal.com/pg/StartPay/' + response_data['data']['authority'], response_data['data']['authority']
            else:
                print(f"Error: Unexpected response code {response_data['data'].get('code')}")
                return None, None
        

        elif response_data.get('errors'):
            error_code = response_data['errors'].get('code', 'Unknown code')
            error_message = response_data['errors'].get('message', 'Unknown error')
            print(f"Error with Zarinpal request: {error_message}, Code: {error_code}")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None, None

def zpal_payment_checker(merchant_id, amount, authority):
    data = {
        "merchant_id": merchant_id,
        "authority": authority,
        "amount": amount
    }

    try:
        response = requests.post(settings.ZARINPAL['gateway_callback_url'], json=data)
        response_data = response.json()

        if response_data['data']['code'] in [100, 101]:  # Successful transaction codes
            return True, response_data['data']['ref_id']
        else:
            return False, None
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return False, None
