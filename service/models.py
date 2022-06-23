from pyexpat import model
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from service.api.constant import DELIVERY_CHOICES, CUSTOMER_CHOICES, ORDER_REASON_CHOICES, \
    PAYMENT_SERVICE_CHOICES, DELIVERY_OPEN_LABEL, CUSTOMER_PRIVATE_LABEL, ORDER_REASON_MOVE_LABEL, \
    PAYMENT_SERVICE_PAYPAL_LABEL


# Create your models here.
class Order(models.Model):
    order_id = models.CharField('Order ID', max_length=60, default='ORders', blank=True)
    customer_id = models.CharField('Customer ID', max_length=60, default='Customer', blank=True)
    invoice_id = models.CharField('Invoice ID', max_length=60, default='INvoice', blank=True)
    delivery_status = models.CharField(
        'Delivery Status',
        max_length=20,
        choices=DELIVERY_CHOICES,
        default=DELIVERY_OPEN_LABEL,
    )
    customer_type = models.CharField(
        'Nachsende-Typ',
        max_length=20,
        choices=CUSTOMER_CHOICES,
        default=CUSTOMER_PRIVATE_LABEL,
    )
    order_reason = models.CharField(
        'Nachsendegrund',
        max_length=40,
        choices=ORDER_REASON_CHOICES,
        default=ORDER_REASON_MOVE_LABEL,
    )
    order_time = models.CharField('Order Time', max_length=60, null=True, blank=True)
    later_start_time = models.DateField('Nachsende-Start', null=True, blank=True)
    deliver_again_date = models.DateField('Wieder zustellen ab', null=True, blank=True)
    # base_price = MoneyField('', max_digits=14, decimal_places=2, default_currency=DEFAULT_CURRENCY, null=True)
    base_price = models.CharField('Grundpreis', max_length=60, null=True, blank=True)
    product_price = models.CharField('Produktpreis', max_length=60, null=True, blank=True)
    other_price = models.CharField('Preis der Dienstleistung', max_length=60, null=True, blank=True)
    product_name = models.CharField('Produktname', max_length=60, null=True, blank=True)
    company_name = models.CharField('Firma', max_length=60, null=True, blank=True)
    full_name = models.CharField('voller Name', max_length=60, null=True, blank=True)
    email = models.EmailField('E-Mail', max_length=254, null=True, blank=True)
    phone_number = models.CharField('Telefon', max_length=60, null=True, blank=True)
    representative_full_name = models.CharField('Bevollmächtigter', max_length=60, null=True, blank=True)
    notice_of_relocation = models.BooleanField('Umzugsmitteilung', default=False, blank=True)
    parcel_shipments = models.BooleanField('Päckchen und Pakete', default=False, blank=True)
    dhl_infopost = models.BooleanField('DHL INFOPOST', default=False, blank=True)
    status_order = models.BooleanField('Status der Bestellung', default=False, blank=True)
    status_invoice = models.BooleanField('Status der Rechnung', default=False, blank=True)
    other_service = ArrayField(models.CharField('Weitere Versanddienstleister', max_length=200), blank=True, null=True)
    additional_recipients = ArrayField(models.CharField('Weitere Person', max_length=200), blank=True, null=True)
    address = models.CharField('Adresse', max_length=60, null=True, blank=True)
    address_supplement = models.CharField('Adresszusatz', max_length=60, null=True, blank=True)
    address_additional_pobox = models.CharField('Postfach-Nr.', max_length=60, null=True, blank=True)
    address_additional_zipcode = models.CharField('PLZ', max_length=60, null=True, blank=True)
    address_additional_city = models.CharField('Stadt', max_length=60, null=True, blank=True)
    new_address = models.CharField('neue Adresse', max_length=60, null=True, blank=True)
    new_address_supplement = models.CharField('neue Adresse Adresszusatz', max_length=60, null=True, blank=True)
    new_address_additional_pobox = models.CharField('neue Adresse Postfach-Nr.', max_length=60, null=True, blank=True)
    new_address_additional_zipcode = models.CharField('neue Adresse PLZ', max_length=60, null=True, blank=True)
    new_address_additional_city = models.CharField('neue Adresse Stadt', max_length=60, null=True, blank=True)
    invoice_pdf = models.URLField('Rechnungsstellung PDF-Datei', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField('erstellt am', auto_now_add=True)
    updated_at = models.DateTimeField('aktualisiert am', auto_now=True)
    payment_service = models.CharField(
        'Zahlungsart wählen',
        max_length=40,
        choices=PAYMENT_SERVICE_CHOICES,
        default=PAYMENT_SERVICE_PAYPAL_LABEL
    )

    def __str__(self):
        return self.order_id
