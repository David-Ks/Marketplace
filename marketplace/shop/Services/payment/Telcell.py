from marketplace.settings import TELCELL_KEY
from shop.Services.payment.encode import encodeToMd5
from shop.models import CheckOut


def get_secure_code(context):
    encode = TELCELL_KEY + \
             str(context['issuer']) + \
             "֏" + \
             str(context['cart'].total) + \
             str(context['product64']) + \
             str(context['issuer_id']) + "1"
    return encodeToMd5(encode)


class Payment:
    def __init__(self, request):
        self.request = request

    def is_secure(self):
        secure = TELCELL_KEY + \
                 self.request.POST.get('invoice') + \
                 self.request.POST.get('issuer_id') + \
                 self.request.POST.get('payment_id') + \
                 self.request.POST.get('currency') + \
                 self.request.POST.get('sum') + \
                 self.request.POST.get('time') + \
                 self.request.POST.get('status')
        if secure == self.request.POST.get('checksum'):
            return True
        return False

    def is_paied(self):
        if not self.is_secure:
            return 0

        if self.request.POST.get('status') == 'PAID':
            issuer_id = self.request.POST.get('issuer_id')
            checkout = CheckOut.objects.get(id=issuer_id)
            checkout.is_paied = True
            checkout.save()
            return True
        return False
