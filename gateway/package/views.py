from django.shortcuts import render
from django.views import View
from package.models import Package

class PricingView(View):
    def get_context_data(self):
        packages = Package.objects.filter(is_enable = True)
        return dict(packages = packages)

    def get(self, request, *args, **kwargs):
        template_name = 'package/pricing.html'
        return render(request, template_name, self.get_context_data())
    
        
