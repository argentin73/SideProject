import imp
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.forms.fields import URLField
from django.utils.safestring import mark_safe
from .models import Order
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.widgets import DynamicArrayWidget
from django_better_admin_arrayfield.models.fields import DynamicArrayField
from service.api.constant import NOT_READONLY_FIELDS
from django.utils.html import format_html
from admin_interface.models import Theme

# Unregister authentication models
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.unregister(Theme)

admin.site.site_header = "Mein-Nachsenderservice Administrationsbereich"
admin.site.site_title = "Mein-Nachsenderservice Administrationsbereich"
admin.site.index_title = "Order Management"


class URLFieldWidgetWithLink(AdminURLFieldWidget):
    def render(self, name, value, attrs=None):
        widget = super(URLFieldWidgetWithLink, self).render(name, value, attrs)
        return mark_safe(u'<a href="%s" '
                         u'target=_blank > OPEN PDF </a>' % value)


# Register your models here.
class OrdersAdmin(admin.ModelAdmin, DynamicArrayMixin):
    save_on_top = True
    list_display = ("order_id", "full_name", "product_price", "product_name", "delivery_status", "invoice_pdf_link", "created_at")
    list_filter = ("delivery_status", "created_at")
    search_fields = ["order_id", "invoice_id", "full_name", "product_price", "product_name", "other_service"]

    # list_editable = ['delivery_status']
    formfield_overrides = {
        DynamicArrayField: { 'widget': DynamicArrayWidget },
        URLField: { 'widget': URLFieldWidgetWithLink }
    }

    def invoice_pdf_link(self, obj):
        return format_html('<a href="{0}" target=_blank style="color: blue">Rechnung herunterladen</a>', obj.invoice_pdf)

    invoice_pdf_link.short_description = 'PDF-Datei'
    invoice_pdf_link.allow_tags = True

    fieldsets = (
        (
            "Informationen zur Bestellung", {
                "classes": ("extra_wide", ),
                "fields": (("order_id", "status_order"), ("invoice_id", "status_invoice"), "invoice_pdf_link", ("order_reason", "delivery_status"), ("order_time",),
                           ("later_start_time", "deliver_again_date"), ("created_at", "updated_at"))
            }
        ),
        (
            "Informationen zum Dienst", {
                "classes": ("extra_wide", ),
                "fields": (("product_name", "other_service"), ("base_price", "other_price"), ("product_price", "payment_service"))
            }
        ),
        (
            "Kundeninformation", {
                "classes": ("extra_wide", ),
                "fields": ("company_name", ("full_name", "customer_type"), ("email", "phone_number"), ("representative_full_name", "additional_recipients"))
            }
        ),
        (
            "Adresse Informationen", {
                "classes": ("extra_wide", ),
                "fields": ("address", ("address_supplement", "address_additional_pobox"), ("address_additional_zipcode", "address_additional_city"), "new_address", ("new_address_supplement", "new_address_additional_pobox"),
                           ("new_address_additional_zipcode", "new_address_additional_city"))
            }
        ),
        (
            "Other Informationen", {
                "fields": ("notice_of_relocation", "parcel_shipments", "dhl_infopost")
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(OrdersAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [f.name for f in self.model._meta.get_fields() if f.name not in NOT_READONLY_FIELDS]
        self.readonly_fields.append('invoice_pdf_link')

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_form(self, request, obj=None, **kwargs):
        form = super(OrdersAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['other_service'].widget.can_add_related = False
        # form.base_fields['invoice_pdf'].widget.
        return form

    # def get_no_sales(self, obj):
    #     no_of_sales = VehicleSale.objects.filter(owner=obj).count()
    #     return no_of_sales
    # get_no_sales.short_description = "No of Sales"

    class Meta:
        ordering = ("order_id", "full_name")

    class Media:
        css = {
            'all': ('/static/admin_fields.css', )
        }


admin.site.register(Order, OrdersAdmin)
