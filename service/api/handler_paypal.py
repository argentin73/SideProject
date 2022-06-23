from email.quoprimime import body_check
from urllib import response
from django.conf import settings
from datetime import datetime
import base64
import requests
import json

CLIENT_ID = settings.PAYPAL_CLIENT_ID
APP_SECRET = settings.PAYPAL_APP_SECRET
BASE_URL = settings.PAYPAL_BASE_URL


def paypal_handle_prepare_order(data):
    print("Paypal Prepare Order --- ", data)
    
    try:
        invoice = paypal_create_invoice(data)
        print("Next to order")
        order = paypal_create_order(data, invoice)
        return order, invoice
    except Exception as e:
        return e, 400


def paypal_create_order(data, invoice):
    print("Paypal Create Order --- ")
    access_token = paypal_generate_access_token()
    product_price = data['product_price']
    product_description = ", ".join(data['other_service'])

    url = '%s/v2/checkout/orders' % BASE_URL
    response = requests.post(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": 'Bearer %s' % access_token
        },
        data=json.dumps({
            "intent": "CAPTURE",
            # "payer": {},
            "purchase_units": [
                {
                    'amount': {
                        "currency_code": "EUR",
                        'value': product_price
                    },
                    "description": product_description,
                    "invoice_id": invoice['id']
                },
            ]
        })
    )
    data = response.json()
    print(data)
    return data


def paypal_create_invoice(data):
    print("Paypal Create Invoice --- ")
    access_token = paypal_generate_access_token()
    email = data['email']
    city = data['newAddressCity']
    postal_code = data['newAddressZipCode']
    country = data['new_countryCode']
    line1 = '%s %s' % (data['newAddressStreet'], data['newAddressHouse'])
    product_name = data['product_name']
    product_price = data['product_price']
    product_id = '%s %s' % (data['product_name'], product_price)
    product_id = product_id.lower().replace(" ", "_")
    product_description = ", ".join(data['other_service'])

    # Generate Invoice Number
    url = '%s/v2/invoicing/generate-next-invoice-number' % BASE_URL
    response = requests.post(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": 'Bearer %s' % access_token
        },)
    numberData = response.json()

    # Create Invoice
    url = '%s/v2/invoicing/invoices' % BASE_URL
    response = requests.post(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": 'Bearer %s' % access_token
        },
        data=json.dumps({
            "status": "SENT",
            "detail": {
                "invoice_number": numberData['invoice_number'],
                # "reference": "deal-ref",
                "invoice_date": datetime.now().strftime("%Y-%m-%d"),
                "currency_code": "EUR",
                "note": "PLease Write down your own note here...",
                "term": "No refunds after 30 days.(Write your own term on here)",
                "memo": "This is a long contract(Write your own memo on here....)",
                # "payment_term": {
                #     "term_type": "NET_10",
                #     "due_date": datetime.now().strftime("%Y-%m-%d")
                # }
            },
            # "invoicer": {
            #     "name": {
            #         "given_name": "David",
            #         "surname": "Larusso"
            #     },
                # "address": {
                #     "address_line_1": "1234 First Street",
                #     "address_line_2": "337673 Hillside Court",
                #     "admin_area_2": "Anytown",
                #     "admin_area_1": "DE",
                #     "postal_code": "98765",
                #     "country_code": "DE"
                # },
                # "email_address": "merchant@example.com",
                # "phones": [
                #     {
                #         "country_code": "001",
                #         "national_number": "4085551234",
                #         "phone_type": "MOBILE"
                #     }
                # ],
                # "website": "www.test.com",
                # "tax_id": "ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy- Jb5SeuGj185MNNw6g",
                # "logo_url": "https://example.com/logo.PNG",
                # "additional_notes": "2-4"
            # },
            "primary_recipients": [
                {
                "billing_info": {
                    "name": {
                        "given_name": data["nameFirst"],
                        "surname": data["nameLast"]
                    },
                    "address": {
                        "address_line_1": line1,
                        "admin_area_2": city,
                        "admin_area_1": "DE",
                        "postal_code": postal_code,
                        "country_code": country
                    },
                    "email_address": email,
                    # "phones": [
                    # {
                    #     "country_code": "001",
                    #     "national_number": "4884551234",
                    #     "phone_type": "HOME"
                    # }
                    # ],
                    # "additional_info_value": "add-info"
                },
                # "shipping_info": {
                #     "name": {
                #     "given_name": "Stephanie",
                #     "surname": "Meyers"
                #     },
                #     "address": {
                #     "address_line_1": "1234 Main Street",
                #     "admin_area_2": "Anytown",
                #     "admin_area_1": "CA",
                #     "postal_code": "98765",
                #     "country_code": "US"
                #     }
                # }
                }
            ],
            "items": [
                {
                    "name": product_name,
                    "description": product_description,
                    "quantity": "1",
                    "unit_amount": {
                        "currency_code": "EUR",
                        "value": product_price
                    },
                    # "tax": {
                    #     "name": "Sales Tax",
                    #     "percent": "7.25"
                    # },
                    # "discount": {
                    #     "percent": "5"
                    # },
                    "unit_of_measure": "QUANTITY"
                },
            ],
            "configuration": {
                # "partial_payment": {
                #     "allow_partial_payment": True,
                #     "minimum_amount_due": {
                #         "currency_code": "USD",
                #         "value": "20.00"
                #     }
                # },
                "allow_tip": True,
                # "tax_calculated_after_discount": True,
                # "tax_inclusive": False,
                # "template_id": "TEMP-19V05281TU309413B"
            },
            # "amount": {
            #     "breakdown": {
            #         "custom": {
            #             "label": "Packing Charges",
            #             "amount": {
            #             "currency_code": "USD",
            #             "value": "10.00"
            #             }
            #         },
            #         "shipping": {
            #             "amount": {
            #             "currency_code": "USD",
            #             "value": "10.00"
            #             },
            #             "tax": {
            #             "name": "Sales Tax",
            #             "percent": "7.25"
            #             }
            #         },
            #         "discount": {
            #             "invoice_discount": {
            #             "percent": "5"
            #             }
            #         }
            #     }
            # }
        })
    )
    data = response.json()
    
    # Get Invoice
    response = requests.get(
        url=data['href'],
        headers={
            
            "Content-Type": "application/json",
            "Authorization": 'Bearer %s' % access_token
        })
    data = response.json()
    print('invoice response ', data)
    return data


def paypal_generate_access_token():
    auth = base64.b64encode(str(CLIENT_ID + ':' + APP_SECRET).encode('ascii')).decode('ascii')
    print('auth ', auth)
    print('url ', '%s/v1/oauth2/token' % BASE_URL)
    response = requests.post(
        '%s/v1/oauth2/token' % BASE_URL,
        data="grant_type=client_credentials",
        headers={
            "Authorization": 'Basic %s' % auth,
        },
    )
    data = response.json()
    print(data)
    return data['access_token']


def paypal_generate_client_token():
    print('start')
    access_token = paypal_generate_access_token()
    print('access_token ', access_token)
    response = requests.post(
        '%s/v1/identity/generate-token' % BASE_URL,
        headers={
            "Authorization": 'Bearer %s' % access_token,
            "Accept-Langugage": "de_DE",
            "Content-Type": "application/json",
        },
    )
    data = response.json()
    print('response ', data)
    return data['client_token']


def paypal_finalize_invoice(data):
    print('finalize invoice ', data)
    access_token = paypal_generate_access_token()
    tbl_order_id = data['invoiceId']
    
    # Get Invoice id from order
    url = '%s/v2/checkout/orders/%s' % (BASE_URL, tbl_order_id)
    response = requests.get(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": 'Bearer %s' % access_token
        },)
    order = response.json()
    invoice_id = order['purchase_units'][0]['invoice_id']
    
    # Retreive Invoice
    url = '%s/v2/invoicing/invoices/%s' % (BASE_URL, invoice_id)
    print('url ', url)
    response = requests.get(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": 'Bearer %s' % access_token
        },)
    invoice = response.json()
    print('retreive invoice ', invoice)
    invoice["status"] = "MARKED_AS_PAID"
    # Update Invoice
    response = requests.put(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": 'Bearer %s' % access_token
        },
        data=json.dumps(invoice)
    )
    print('update resopne: ', response, response.json())
    # Again retrieve
    url = '%s/v2/invoicing/invoices/%s' % (BASE_URL, invoice_id)
    print('url ', url)
    response = requests.get(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": 'Bearer %s' % access_token
        },)
    invoice = response.json()
    print('retreive invoice2 ', invoice)
    # Send Invoice
    url = '%s/v2/invoicing/invoices/%s/send' % (BASE_URL, invoice_id)
    requests.post(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": 'Bearer %s' % access_token
        },
        data=json.dumps({
            "send_to_recipient": "true"
        })
    )
    print('invoice sent')
    return tbl_order_id, invoice
