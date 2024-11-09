import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
# from django.utils.translation import ugettext_lazy
import json

from finance.utils.zarinpal import zpal_request_handler, zpal_payment_checker



class GateWay(models.Model):
    
    FUNCTION_SAMAN = 'saman'
    FUNCTION_ZARIN = 'zarin'
    FUNCTION_PASARSIAN = 'parsian'
    FUNCTION_SHAPARAK = 'shaparak'

    GATEWAY_FUNCTIONS = (
        (FUNCTION_PASARSIAN, ('parsian')),
        (FUNCTION_SAMAN, ('saman')),
        (FUNCTION_SHAPARAK, ('shaparak')),
        (FUNCTION_ZARIN, ('zarin'))
    )
    
    title = models.CharField(max_length=100, verbose_name=('title'), null = True)
    gatway_url_request = models.CharField(max_length=150, verbose_name=('gateway url request'), null=True, blank=True)
    gateway_verify_url = models.CharField(max_length=150, verbose_name=('gateway urlverification'), null=True, blank=True)
    gateway_code = models.CharField(max_length=150, verbose_name=('gateway code'), choices= GATEWAY_FUNCTIONS)
    is_enable = models.BooleanField(verbose_name=('is enabled'),default=True)
    auth_data = models.CharField(verbose_name=('data authentication'),null = True, blank = True)

    class Meta:
        verbose_name = ('Gateway')
        verbose_name_plural = ('Gateways')

    def __str__(self):
        return self.title   
    

    def get_request_handler(self):
        handlers = {
            self.FUNCTION_PASARSIAN : None,
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_ZARIN: zpal_request_handler,
            self.FUNCTION_SHAPARAK: None,
        }
        
        return handlers[self.gateway_code]
    
    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_PASARSIAN : None,
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_ZARIN: zpal_payment_checker,
            self.FUNCTION_SHAPARAK: None,
        }
        return handlers[self.gateway_code]
    
    @property
    def cridentials(self):
        return json.loads(self.auth_data)

class Payment(models.Model):
    invoice_number = models.UUIDField(verbose_name=('invoice number'), unique=True, default=uuid.uuid4)
    amount = models.PositiveIntegerField(verbose_name=('payment amount'),editable=True)
    gateway =models.ForeignKey(GateWay,verbose_name=('payments'),null = True, blank = True, on_delete= models.SET_NULL)
    is_paid = models.BooleanField(verbose_name=('is paid'),default=False)
    payment_log = models.TextField(verbose_name=('payment log'), blank= True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=('user'), null = True, on_delete=models.SET_NULL)
    authority = models.CharField(max_length=64, verbose_name=('authority'), blank = True)


    class Meta:
        verbose_name = ('Payment')
        verbose_name_plural = ('Payments')

    def __str__(self):
        return self.invoice_number.hex
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_paid = self.is_paid
    

    def get_handler_data(self):
        return dict(merchant_id = settings.ZARINPAL['merchant_id'], amount = self.amount , description = self.title,
                    user_email = self.user.email ,user_mobile = getattr(self.user,'phone_number',None), 
                    callback = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
                    )

    
    @property
    def bank_page(self):
        handler = self.gateway.get_request_handler()
        if handler is not None:
            data = self.get_handler_data()
            link, authority = handler(**data)
            if authority is not None:
                self.authority = authority
                self.save()
            return link
        
    @property
    def title(self):
        return 'Instant payment'

    def status_changed(self):
        return self.is_paid != self._b_is_paid

    def verify(self, data):
        handler = self.gateway.get_verify_handler()
        if not self.is_paid and handler is not None:
            handler(**data)
        return self.is_paid
        
    def get_gateway(self):
        gateway  =GateWay.objects.filter(is_enable = True).first()
        return gateway.gateway_code
    
    def save_log(self, data, scope = 'Request Handler', save = True):
        generated_log = "[{}][{}] {} \n".format(timezone.now(), scope, data)
        if self.payment_log != '':
            self.payment_log += generated_log
        else:
            self.payment_log = generated_log
        if save:
            self.save()
