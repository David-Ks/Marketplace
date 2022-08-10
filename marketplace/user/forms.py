from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from django import forms
from django.forms.utils import ErrorList

from .models import User, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rate']


class ProfileUserForm(forms.ModelForm):
    """ To change user information in a profile """
    phone = forms.CharField(max_length=8, required=False)

    def __init__(
            self,
            data=None,
            files=None,
            auto_id="id_%s",
            prefix=None,
            initial=None,
            error_class=ErrorList,
            label_suffix=None,
            empty_permitted=False,
            instance=None,
            use_required_attribute=None,
            renderer=None,
            user=None,
    ):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")

        if not str(phone).isdigit():
            msg = "Not Valid phone number."
            self.add_error('phone', msg)

        # If the phone number is already using, or its own number
        if User.objects.filter(phone=phone).exists():
            msg = "This number is already using."
            if self.user is not None:
                userList = User.objects.filter(phone=phone)
                if userList[0].id != self.user.id:
                    self.add_error('phone', msg)
            else:
                self.add_error('phone', msg)

    def save(self, *args, **kwargs):
        if self.user is None:
            return
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.phone = self.cleaned_data['phone']
        self.user.save()

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CustomSignupForm(SignupForm, ProfileUserForm):
    """ Registration form """
    def signup(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user
