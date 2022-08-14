from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, TemplateView

from marketplace import settings
from user.models import Review
from .Services.cart import UserCart, UserSavedCard
from .Services.checkout import CheckOut
from .Services.haysell import TimeToUpdateModelsData
from .Services.client import send_msg_AdminMail
from .Services.payment import Telcell, IDram
from .Services.payment.encode import encodeToBase64
from .forms import CheckOutForm
from .models import Product
from .models import CheckOut as CheckOutModel


class HomeView(TimeToUpdateModelsData, View):
    template_name = 'shop/home.html'

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        if request.POST.get('action') == 'send_mail':
            username = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('msg')
            message += "\n" + "\n" + username + "\n" + email
            send_msg_AdminMail(message)
        return redirect('home')

    def get_context_data(self, *args, **kwargs):
        context = {
            'reviews': Review.objects.filter(for_view=True),
        }

        checkout = self.request.session.get('checkout_id')

        try:
            checkout = CheckOutModel.objects.get(id=int(checkout))
        except:
            checkout = None
        if checkout and int(checkout.status) != 4:
            if int(checkout.status) != 4:
                context['checkout'] = checkout
            else:
                del self.request.session['checkout']

        products = Product.objects.select_related('category').filter(balance__gt=0)
        context['products1'] = products.filter(category__title='Ալկոհոլային խմիչք')
        context['products2'] = products.filter(category__title='Կաթնամթերք և հավկիթ')
        return context


class ProductsView(TimeToUpdateModelsData, ListView):
    template_name = "shop/products.html"
    paginate_by = 12

    def get_queryset(self):
        cats = self.request.GET.getlist('cats')
        if cats:
            products = Product.objects.filter(
                category_id__in=cats,
                balance__gt=0)
        else:
            products = Product.objects.all()

        search = self.request.GET.get('search')
        if search:
            products = products.filter(item_name__icontains=search)

        minPrice = self.request.GET.get('min')
        maxPrice = self.request.GET.get('max')
        if minPrice and int(minPrice) > 1:
            products = products.filter(price__gt=minPrice)
        if maxPrice and int(minPrice) > 1:
            products = products.filter(price__lt=maxPrice)

        return products

    def post(self, request):
        response = JsonResponse({'data': 'Ok'}, status=200)

        if request.POST.get('action') == 'add_to_cart':
            userCart = UserCart(request)
            cart = userCart.add_to_cart({
                'barcode': request.POST.get('barcode'),
                'count': request.POST.get('count')
            })
            response.set_cookie('cart', cart)

        elif request.POST.get('action') == 'add_to_saves':
            userSaves = UserSavedCard(request)
            saves = userSaves.add_to_saves(request.POST.get('barcode'))
            response.set_cookie('saves', saves)

        elif request.POST.get('action') == 'remove_saves_item':
            userSaves = UserSavedCard(request)
            saves = userSaves.remove_saves_item(request.POST.get('barcode'))
            response.set_cookie('saves', saves)

        return response

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        cards = UserSavedCard(self.request)
        context['saves'] = cards.get_saves()

        return context


class BusketView(TimeToUpdateModelsData, TemplateView):
    template_name = "shop/busket.html"

    def post(self, request):
        response = JsonResponse({"data": "Ok"}, status=200)

        if request.POST.get('action') == 'delete':
            userCart = UserCart(request)
            cart = userCart.remove_cart_item(request.POST.get('barcode'))
            response.set_cookie('cart', cart)

        return response

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        userCart = UserCart(self.request)
        cartItems = userCart.get_cart()

        barCodes = []
        counts = []
        for item in cartItems:
            barCodes.append(item['barcode'])
            counts.append(item['count'])

        context['products'] = Product.objects.filter(barcode__in=barCodes)
        context['counts'] = counts
        context['barcodes'] = barCodes
        context['range'] = list(range(len(barCodes)))

        return context


class CheckOutView(View):
    template_name = 'shop/checkout.html'

    def get(self, request):
        context = self.get_context_data()
        if len(request.GET.getlist('barcode')) == 0:
            return redirect('home')
        return render(request, self.template_name, context)

    def post(self, request):
        form = CheckOutForm(request.POST)
        response = redirect('pay')
        if form.is_valid():
            print("mb")
            model = form.save()
            checkout = CheckOut(request, model)
            save = checkout.save()
            if save:
                response.delete_cookie('cart')
                return response

        return redirect('home')  # Return some error!!!

    def get_context_data(self, *args, **kwargs):
        barCodes = self.request.GET.getlist('barcode')
        counts = self.request.GET.getlist('count')
        barCodes = list(map(int, barCodes))

        for i in range(len(counts)):
            if len(str(float(counts[i]) / 25)) > 4:
                counts[i] = int(float(counts[i]) / 0.25) * 0.25

        context = {
            'products': Product.objects.filter(barcode__in=barCodes),
            'counts': counts,
            'barcodes': barCodes,
            'range': list(range(len(barCodes)))
        }

        return context


class SavesView(TimeToUpdateModelsData, ListView):
    template_name = 'shop/saves.html'
    paginate_by = 8

    def get_queryset(self):
        cards = UserSavedCard(self.request)
        cards = cards.get_saves()

        return Product.objects.filter(barcode__in=cards)


class InfoView(TemplateView):
    template_name = 'shop/info.html'


class PayView(TemplateView):
    template_name = 'shop/pay.html'

    def get_context_data(self, **kwargs):
        context = super(PayView, self).get_context_data(**kwargs)
        cartId = self.request.session.get('cartId')

        context['cart'] = get_object_or_404(CheckOutModel, id=cartId)
        context['payMethod'] = self.request.session.get('pay_method')

        if context['payMethod'] == 'Telcell':
            context['issuer'] = settings.ISSUER
            context['product64'] = encodeToBase64("Order:" + str(cartId))
            context['issuer_id'] = encodeToBase64(cartId)
            context['secure'] = Telcell.get_secure_code(context)
        elif context['payMethod'] == 'IDram':
            context['account'] = settings.IDRAM_ACCOUNT
            context['description'] = "Invoice:" + str(cartId)
            context['bill_no'] = str(cartId)

        return context


class IdramPayView(View):
    def get(self, request):
        checkIDrma = IDram.payment(request)
        if checkIDrma.is_valid():
            return HttpResponse('OK')
        return HttpResponse('NOT KO')