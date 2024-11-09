from django.shortcuts import render
from django.views import View
from package.models import Package
from purchase.models import Purchase
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CreatePurchaseView(LoginRequiredMixin, View):
    def get(self, request,package_id,*args, **kwargs):
        template_name = "purchase/create.html"
        try:
            package = Package.objects.get(id = package_id)
        except Package.DoesNotExist:
            raise Http404 
        
        purchase = Purchase.create(package, request.user)
        return render(request, template_name, {"purchase": purchase})
        


