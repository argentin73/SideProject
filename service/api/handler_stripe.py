import stripe
from service.api.constant import DEFAULT_CURRENCY_LOWER
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY
stripe.api_version = "2020-08-27; orders_beta=v3;"


def stripe_handle_prepare_order(data):
    print("Stripe Prepare Order --- ", data)

    try:
        customer = stripe_create_customer(data)
        order = stripe_create_order(data, customer)
        invoice = stripe_create_invoice(data, customer, order)
        return customer, invoice, order
    except Exception as e:
        return e, 400


def stripe_create_order(data, customer):
    print("Stripe Create Order --- ")

    # Variables
    email = data['email']
    name = data['full_name']
    city = data['newAddressCity']
    postal_code = data['newAddressZipCode']
    country = data['new_countryCode']
    line1 = '%s %s' % (data['newAddressStreet'], data['newAddressHouse'])
    product_name = data['product_name']
    product_price = int(data['product_price'] * 100)
    product_id = '%s %s' % (data['product_name'], product_price)
    product_id = product_id.lower().replace(" ", "_")
    product_description = ", ".join(data['other_service'])

    order = stripe.Order.create(
        currency=DEFAULT_CURRENCY_LOWER,
        line_items=[
            {
                "product_data": {
                    "name": product_name,
                    "id": product_id,
                    "description": product_description,
                },
                "price_data": {
                    "unit_amount": product_price,
                    "tax_behavior": "exclusive"
                },
                "quantity": 1,
            },
        ],
        payment={
            'settings': {
                'payment_method_types': ['card'],
            },
        },
        # Replace this with checkout form input from the request
        shipping_details={
            'name': name,
            'address': {
                'line1': line1,
                'city': city,
                'postal_code': postal_code,
                'country': country
            },
        },
        # automatic_tax={'enabled': True},
        customer=customer['id'],
        expand=['line_items'],
        metadata={
            "customer email": email
        },
    )
    return order


def stripe_create_invoice(data, customer, order):
    print("Stripe Create Invoice --- ")

    name = data['full_name']
    product_id = order["line_items"]["data"][0]["price"]["product"]
    product_name = data['product_name']
    product_price = int(data['product_price'] * 100)
    product_description = ", ".join(data['other_service'])
    product_description = "%s %s - %s" % (name, product_name, product_description)
    stripe.InvoiceItem.create(
        customer=customer['id'],
        description=product_description,
        price_data={
            "currency": DEFAULT_CURRENCY_LOWER,
            "product": product_id,
            "unit_amount": product_price,
        }
    )
    invoice = stripe.Invoice.create(
        customer=customer['id'],
        collection_method='send_invoice',
        days_until_due=1,
        auto_advance=False,
    )
    return invoice


def stripe_create_customer(data):
    print("Stripe Create Customer --- ", data)

    # Variables
    email = data['email']
    name = data['full_name']
    city = data['newAddressCity']
    postal_code = data['newAddressZipCode']
    country = data['new_countryCode']
    line1 = '%s %s' % (data['newAddressStreet'], data['newAddressHouse'])
    customer_description = '%s %s' % (data['customer_type'], data.get('company_name', ''))

    print("step1")
    # Create Customer
    exist_customers = stripe.Customer.list(email=email)['data']

    print("step2")
    if len(exist_customers) > 0:
        customer = stripe.Customer.modify(
            exist_customers[0]['id'],
            email=email,
            name=name,
            address={
                'line1': line1,
                'city': city,
                'postal_code': postal_code,
                'country': country
            },
            description=customer_description,
            preferred_locales=[
                "de"
            ]
        )
    else:
        customer = stripe.Customer.create(
            email=email,
            name=name,
            address={
                'line1': line1,
                'state': city,
                'postal_code': postal_code,
                'country': country
            },
            description=customer_description,
            preferred_locales=[
                "de"
            ]
        )

    print("step3")
    return customer


def stripe_finalize_invoice(data):
    invoice_id = data['invoiceId']

    invoice = stripe.Invoice.finalize_invoice(invoice_id)
    stripe.Invoice.pay(invoice_id, paid_out_of_band=True)
    invoice = stripe.Invoice.retrieve(invoice_id)
    print("after finalize ", invoice)
    stripe.Invoice.send_invoice(invoice_id)

    return invoice
