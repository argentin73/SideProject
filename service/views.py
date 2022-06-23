from django.views.generic import TemplateView

# Create your views here.
frontend = TemplateView.as_view(template_name='index.html')