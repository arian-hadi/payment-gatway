from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from finance.utils.zarinpal import zpal_request_handler, zpal_payment_checker
from .forms import ChargeWalletForm
from .models import Payment,GateWay
from django.http import Http404

class ChargeWalletView(View):
    template_name = 'finance/charge_wallet.html'
    form_class = ChargeWalletForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            payment_link, authority =zpal_request_handler(settings.ZARINPAL['merchant_id'], form.cleaned_data['amount'],
            "wallet_charge", "arianhadi2003@gmail.com", None, settings.ZARINPAL['gateway_callback_url'],        
            )
            if payment_link is not None:
                return redirect (payment_link)
        
        return render(request, self.template_name, {'form': form})
    

class VerifyView(View):
    template_name = 'finance/callback.html'

    def post(self, request, *args, **kwargs):
        authority = request.POST.get('Authority')
        try:
            payment = Payment.objects.get(authority = authority)       
        
        except Payment.DoesNotExist:
            raise Http404 
        data = dict(merchant_id = payment.gateway.auth_data,payment = payment.amount, autority = payment.authority)
        payment.verify(data)

        return render(request,self.template_name, {"payment":payment})
    

class PaymentView(View):
    def get(self, request, invoice_number, *arga, **kwargs):
        template_name = "finance/payment_datail.html"
        try:
            payment = Payment.objects.get(invoice_number = invoice_number)       
        
        except Payment.DoesNotExist:
            raise Http404

        gateways = GateWay.objects.filter(is_enable = True)

        return render(request, template_name, {"payment": payment, "gateways": gateways})


class PaymentGatewayView(View):
    def get(self, request, invoice_number, gateway_code, *arag, **kwargs): 
        
        try:
            payment = Payment.objects.get(invoice_number = invoice_number)       
        
        except Payment.DoesNotExist:
            raise Http404 


        try:
            gateway = GateWay.objects.get(gateway_code = gateway_code)       
        
        except GateWay.DoesNotExist:
            raise Http404
        
        payment.gateway = gateway
        payment.save()
        payment_link = payment.bank_page
        if payment_link:
            return redirect(payment_link)
        
        gateways = GateWay.objects.filter(is_enable = True)
        return render(request, 'finance/payment_datail.html', {"payment": payment, "gateways": gateways})
        
