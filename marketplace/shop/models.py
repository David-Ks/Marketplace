from django.db import models

from user.models import User


class Category(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Product(models.Model):
    item_name = models.CharField(max_length=300, verbose_name="product title", null=True)
    balance = models.CharField(max_length=10, verbose_name="count", null=True, default=0)
    price = models.PositiveIntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True)
    barcode = models.PositiveBigIntegerField(unique=True, db_index=True)

    def __str__(self):
        return self.item_name

    def get_img_url(self):
        code = str(self.barcode)
        while len(code) < 5:
            code = "0" + code
        return "https://new.haysell.com/images/upload/items_images/thumb/2909/480/" + code + ".jpg"

    class Meta:
        ordering = ['-id']


class Update(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.updated_at)


class Item(models.Model):
    barcode = models.ForeignKey(Product, to_field="barcode", db_column="barcode", null=True, on_delete=models.CASCADE)
    count = models.CharField(max_length=10, verbose_name="count", null=True, default=0)

    def __str__(self):
        return self.barcode.item_name + " | " + str(self.count)


class CheckOut(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=8)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255, blank=True, null=True)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, related_name='checkouts', on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(Item, blank=True, null=True)
    total = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=False)
    is_paied = models.BooleanField(default=False)
