from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from shop.Services.haysell import cleanProductModel, ProductsModelFiller
from shop.models import CheckOut
from .forms import ReviewForm, ProfileUserForm
from .models import Review


@method_decorator(login_required, "dispatch")
class ProfileView(View):
    def get(self, request):
        context = self.get_context_data()
        return render(request, "user/profile.html", context)

    def post(self, request):
        if request.POST.get('action') == 'refresh':
            ids = request.POST.get('ids')
            if ids:
                ids = ids.split(',')
            checkouts = list(CheckOut.objects.filter(id__in=ids).values('status'))
            return JsonResponse({'response': checkouts})

        form = ProfileUserForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(request.user)

        return redirect('profile')

    def get_context_data(self, *args, **kwargs):
        context = {
            'review': Review.objects.filter(user=self.request.user),
            'form': ProfileUserForm(),
            'checkouts': CheckOut.objects.filter(user=self.request.user, status__lt=4),
            'others': CheckOut.objects.filter(user=self.request.user, status='4'),
        }
        return context


@method_decorator(login_required, "dispatch")
class AddReviewView(View):
    def post(self, request):
        form = ReviewForm(request.POST)

        if form.is_valid():
            """IF USER HAVE REVIEW"""
            review = Review.objects.get_or_create(user_id=request.user.id)[0]
            review.content = form.cleaned_data.get('content')
            review.rate = form.cleaned_data.get('rate')
            review.save()

            # messages.add_message(request, messages.INFO, "Successfully.")
            return redirect('profile')

        # messages.add_message(request, messages.ERROR, "Technical Error.")
        return redirect('profile')


@method_decorator(login_required, "dispatch")
class DelivaryAdminView(View):
    template_name = "delivery/admin.html"

    def get(self, request):
        if not request.user.is_superuser:
            return redirect('home')
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_superuser:
            return redirect('home')
        if request.POST.get('action') and request.user.is_superuser:
            status = 0
            if request.POST.get('action') == 'update_category':
                f = ProductsModelFiller()
                status = f.fillCategory()
            elif request.POST.get('action') == 'update_products':
                f = ProductsModelFiller()
                status = f.fillProduct()
            elif request.POST.get('action') == 'delete_products':
                cleanProductModel()
            if status:
                messages.error(request, "Error with HaySel requests!")
            return redirect('delivery')

        id = request.POST.get('id')
        if id:
            checkout = CheckOut.objects.get(id=id)
            checkout.status = request.POST.get('status')
            checkout.save()
        return redirect('delivery')

    def get_context_data(self):
        context = {
            'checkouts': CheckOut.objects.filter(status__lt=4).order_by('id')
        }
        return context
