import requests

from datetime import datetime, timedelta
from django.utils import timezone
from marketplace import settings
from shop.models import Category, Product, Update


def cleanProductModel():
    Product.objects.all().delete()


def cleanCategoryModel():
    Category.objects.all().delete()


class TimeToUpdateModelsData:
    def __init__(self):
        lastUpdateTime = Update.objects.get_or_create(id=1)
        if (timezone.now() - lastUpdateTime[0].updated_at) > timedelta(minutes=settings.DATAS_REFRESH_TIME):
            fill = ProductsModelFiller()
            fill.fillProduct()
            lastUpdateTime[0].save()


class ProductsModelFiller:
    """Fills the models with received data"""
    url = settings.HAYSELL_URL
    token = settings.TOKEN
    profile_id = settings.PROFILE_ID

    def __init__(self):
        self.payload = {
            "token": self.token,
            "profile_id": self.profile_id,
            "action": "get_balance"
        }

        try:
            self.response = requests.get(self.url, json=self.payload)
            self.response.raise_for_status()
        except:
            self.response = None

    def fillCategory(self):
        if not self.response:
            return 1

        cleanCategoryModel()
        jsonData = self.response.json()
        cats = set()
        for product in jsonData:
            if 'balance' in product:
                cats.add(product.get('category'))

        for cat in cats:
            Category.objects.create(title=cat)
        return 0

    def fillProduct(self):
        if not self.response:
            return 1

        jsonData = self.response.json()
        for product in jsonData:
            if ('balance' in product) and ('barcode' in product):
                pr = Product.objects.get_or_create(barcode=product.get('barcode'))
                pr[0].balance = sum(map(lambda x: float(x.replace(',', '')), product.get('balance').values()))
                pr[0].price = product.get('price')["3"]
                pr[0].item_name = product.get('item_name')
                cat = Category.objects.get(title=product.get('category'))
                pr[0].category = cat
                pr[0].save()
        return 0
