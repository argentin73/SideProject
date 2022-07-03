from service.forms import OrderForm
from django.http import JsonResponse
from service.models import Order


def insert_order_data(data):
    try:
        print('Posgresql -- insert : ', data)
        # data['product_price'] = locale.currency(data['product_price'], grouping=True)
        data['base_price'] = str(data['base_price']).join("\xa0€")
        data['other_price'] = str(data['other_price']).join("\xa0€")
        data['product_price'] = str(data['product_price']).join("\xa0€")
        print('step1')

        data['payment_service'] = str(data['payment_service']).upper()
        print('step2')

        form = OrderForm(data)
        print(form.errors)
        if form.is_valid():
            order = form.save()
            message = "Order has been created"
            explanation = ""
            return form.instance.id
        else:
            message = "The form has errors"
            explanation = form.errors.as_data()
            status_code = 400
    except Exception as e:
        print(e)
        status_code = 400
        message = "Exception has occured"
        explanation = e
    return JsonResponse({'message': message, 'explanation': explanation}, status=status_code)


def update_order_status_by_pk(id, invoice):
    Order.objects.filter(pk=id).update(status_order=True, status_invoice=True, invoice_pdf=invoice['invoice_pdf'])


def update_order_status_order_id(id, invoice):
    Order.objects.filter(order_id=id).update(status_order=True, status_invoice=True, invoice_pdf=invoice['detail']['metadata']['recipient_view_url'])