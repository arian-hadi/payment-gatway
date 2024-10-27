from django.shortcuts import render
from django.views import View

class PricingView(View):
    def get_context_data(self):
        pass
    
    def get(self, request, *args, **kwargs):
        template_name = 'package/pricing.html'
        return render(request, self.template_name)
