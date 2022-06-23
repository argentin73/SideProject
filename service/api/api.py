import stripe
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from service.api.constant import PAYMENT_SERVICE_STRIPE_LABEL
from django.conf import settings
# DATA PROCESSING FUNC
from service.api.handler_postgre import insert_order_data, update_order_status_by_pk, update_order_status_order_id
from service.api.handler_stripe import stripe_handle_prepare_order, stripe_finalize_invoice
from service.api.handler_paypal import paypal_generate_client_token, paypal_handle_prepare_order, paypal_finalize_invoice


def init_paypal(request):
    if request.method == 'GET':
        client_id = settings.PAYPAL_CLIENT_ID
        print('init paypal')
        client_token = paypal_generate_client_token()
        print(client_token)
        return JsonResponse({ "client_id": client_id, "client_token": client_token }, status=200)


@ensure_csrf_cookie
@api_view(['POST'])
def create_order(request):
    message = None
    explanation = None
    status_code = 200
    data = request.data

    if request.method == 'POST':
        print('data ', data)
        # STRIPE #
        if data['payment_service'] == PAYMENT_SERVICE_STRIPE_LABEL.lower():
            customer, invoice, order = stripe_handle_prepare_order(data)
            # POSTGRESQL #
            if 'client_secret' in order and 'id' in invoice:
                data['order_id'] = order['id']
                data['invoice_id'] = invoice['id']
                data['customer_id'] = customer['id']
                # Insert Data to DB
                tbl_order = insert_order_data(data=data)
                print("tbl_order::: ", tbl_order)
                if tbl_order:
                    # Update Invoice with order id
                    invoice = stripe.Invoice.modify(invoice['id'],
                                                    metadata={"tbl_order_id": tbl_order})
                    # Response to Client Side
                    return JsonResponse({
                        'clientSecret': order['client_secret'],
                        'invoiceId': invoice['id']
                    }, status=200)
                else:
                    status_code = 500
                    message = "Order creation failed - postgre"
            else:
                # NO ORDER CREATED
                status_code = 500
                message = "Order creation failed - stripe"

        # PAYPAL #
        else:
            order, invoice = paypal_handle_prepare_order(data)
            if 'id' in order and 'id' in invoice:
                data['order_id'] = order['id']
                data['invoice_id'] = invoice['id']
                data['customer_id'] = data['full_name']

                # Insert Data to DB
                tbl_order = insert_order_data(data=data)
                print("tbl_order::: ", tbl_order)
                if tbl_order:
                    # Response to Client Side
                    return JsonResponse(order, status=200)
                else:
                    status_code = 500
                    message = "Order creation failed - postgre"
            else:
                # NO ORDER CREATED
                status_code = 500
                message = "Order creation failed - paypal"
    else:
        status_code = 400
        message = 'The request method is not valid'
    return JsonResponse({'message': message, 'explanation': explanation}, status=status_code)


@ensure_csrf_cookie
@api_view(['POST'])
def finalize_invoice(request):
    message = None
    explanation = None
    status_code = 200
    data = request.data

    print("Finalize Invoice")

    if request.method == 'POST':
        
        if data['service'] == PAYMENT_SERVICE_STRIPE_LABEL.lower():
            invoice = stripe_finalize_invoice(data)
            tbl_order_id = invoice["metadata"]["tbl_order_id"]
            if 'id' in invoice:
                update_order_status_by_pk(tbl_order_id, invoice)
                # Response to Client Side
                return JsonResponse(invoice, status=200)
        else:
            tbl_order_id, invoice = paypal_finalize_invoice(data)
            if 'id' in invoice:
                update_order_status_order_id(tbl_order_id, invoice)
                # Response to Client Side
                return JsonResponse(invoice, status=200)
        # NO INVOICE FINALIZED
        status_code = 500
        message = "Invoice finalization failed"
    else:
        status_code = 400
        message = 'The request method is not valid'
    return JsonResponse({'message': message, 'explanation': explanation}, status=status_code)


def stripe_webhook(request):
    if request.method == 'POST':
        print('WEBHOOK ___ ', request)
        # payload = request.data
        # headers = {}
        #
        # for (key, value) in request.headers:
        #     headers[key.upper().replace('-', '_')] = request.headers.get(key)
        #
        # sig_header = headers.get('STRIPE_SIGNATURE', '')
        # event = None
        #
        # try:
        #     event = stripe.Webhook.construct_event(
        #         payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_KEY
        #     )
        # except ValueError as e:
        #     # Invalid payload
        #     print("Invalid payload")
        #     return HttpResponse(status=400)
        # except stripe.error.SignatureVerificationError as e:
        #     # Invalid signature
        #     print("Invalid signature")
        #     return HttpResponse(status=400)
        #
        # print('receive event type {}'.format(event['type']))
        return HttpResponse(status=200)
