from marketplace import settings
from shop.Services.payment.encode import encodeToMd5
from shop.models import CheckOut


class Payment:
    def __init__(self, request):
        self.request = request

    def get_bill_no(self):
        try:
            checkoutID = self.request.GET.get('EDP_BILL_NO')
            checkout = CheckOut.objects.get(id=checkoutID, is_paied=False)
            return checkout
        except:
            return False

    def is_valid(self):
        if self.request.GET.get('EDP_PRECHECK') != 'YES':
            return False

        checkout = self.get_bill_no()
        if not checkout:
            return False

        if self.request.GET.get('EDP_REC_ACCOUNT') != settings.IDRAM_ACCOUNT:
            return False

        if int(self.request.GET.get('EDP_AMOUNT')) != int(checkout.total):
            return False

        return True

    def is_secure(self):
        checkout = self.get_bill_no()
        amount = self.request.GET.get('EDP_AMOUNT')
        checkSum = self.request.GET.get('EDP_CHECKSUM')

        if not checkout or int(amount) != int(checkout.total):
            return False

        check = settings.IDRAM_ACCOUNT + ":" + \
            amount + ":" + \
            settings.IDRAM_SECRET_KEY + ":" + \
            checkout.id + ":" + \
            self.request.GET.get('EDP_PAYER_ACCOUNT') + ":" + \
            self.request.GET.get('EDP_TRANS_ID') + ":" + \
            self.request.GET.get('EDP_TRANS_DATE')
        if encodeToMd5(check) == checkSum:
            return True
        return False


