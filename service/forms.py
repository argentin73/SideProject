from django.forms import ModelForm
from service.models import *


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
