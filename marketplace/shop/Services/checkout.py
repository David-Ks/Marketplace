from shop.models import Item, Product
from shop.models import CheckOut as chkout


class CheckOut:
    def __init__(self, request, model):
        self.request = request
        self.model = model
        self.total = 0

    def save_items(self):
        barCodes = self.request.POST.getlist('barcode')
        counts = self.request.POST.getlist('count')

        if len(barCodes) == len(counts):
            for i in range(len(barCodes)):
                if len(str(float(counts[i]) / 25)) > 4:
                    counts[i] = int(float(counts[i]) / 0.25) * 0.25
                product = Product.objects.get(barcode=barCodes[i])
                self.total += product.price * float(counts[i])
                item = Item.objects.create(barcode=product, count=counts[i])
                self.model.items.add(item)
            return True
        return False

    def save(self):
        foo = self.save_items()
        if not foo:
            return False
        if self.total < 10000:
            self.total += 500
        self.model.total = self.total
        if self.request.user.is_authenticated:
            self.model.user = self.request.user
        else:
            self.request.session['checkout_id'] = self.model.id
        self.model.status = '1'
        self.model.save()
        return True

    def clearAll(self):
        Item.objects.all().delete()
        chkout.objects.all().delete()
