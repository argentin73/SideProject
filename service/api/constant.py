DEFAULT_CURRENCY = 'EUR'
DEFAULT_CURRENCY_LOWER = 'eur'

DELIVERY_OPEN_LABEL = 'offen'
DELIVERY_IN_PROGRESS_LABEL = 'Bearbeitung'
DELIVERY_FINALIZED_LABEL = 'abgeschlossen'

CUSTOMER_PRIVATE_LABEL = 'Privat'
CUSTOMER_BUSINESS_LABEL = 'Gewerbe'

ORDER_REASON_MOVE_LABEL = 'Umzug'
ORDER_REASON_ABSENCE_VACATION_LABEL = 'Abwesenheit / Urlaub'
ORDER_REASON_CARE_CASE_LABEL = 'Betreuungsfall'
ORDER_REASON_DEATH_LABEL = 'Sterbefall'
ORDER_REASON_INSOLVENCY_LABEL = 'Insolvenz'

PAYMENT_SERVICE_PAYPAL_LABEL = 'PAYPAL'
PAYMENT_SERVICE_STRIPE_LABEL = 'STRIPE'

DELIVERY_CHOICES = [
    (DELIVERY_OPEN_LABEL, DELIVERY_OPEN_LABEL),
    (DELIVERY_IN_PROGRESS_LABEL, DELIVERY_IN_PROGRESS_LABEL),
    (DELIVERY_FINALIZED_LABEL, DELIVERY_FINALIZED_LABEL),
]

CUSTOMER_CHOICES = [
    (CUSTOMER_PRIVATE_LABEL, CUSTOMER_PRIVATE_LABEL),
    (CUSTOMER_BUSINESS_LABEL, CUSTOMER_BUSINESS_LABEL),
]

ORDER_REASON_CHOICES = [
    (ORDER_REASON_MOVE_LABEL, ORDER_REASON_MOVE_LABEL),
    (ORDER_REASON_ABSENCE_VACATION_LABEL, ORDER_REASON_ABSENCE_VACATION_LABEL),
    (ORDER_REASON_CARE_CASE_LABEL, ORDER_REASON_CARE_CASE_LABEL),
    (ORDER_REASON_DEATH_LABEL, ORDER_REASON_DEATH_LABEL),
    (ORDER_REASON_INSOLVENCY_LABEL, ORDER_REASON_INSOLVENCY_LABEL),
]

PAYMENT_SERVICE_CHOICES = [
    (PAYMENT_SERVICE_PAYPAL_LABEL, PAYMENT_SERVICE_PAYPAL_LABEL),
    (PAYMENT_SERVICE_STRIPE_LABEL, PAYMENT_SERVICE_STRIPE_LABEL),
]

NOT_READONLY_FIELDS = [
    'delivery_status', 'other_service', 'additional_recipients'
]