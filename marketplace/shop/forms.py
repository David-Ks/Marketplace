from django import forms

from .models import CheckOut


class CheckOutForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")

        if not str(phone).isdigit():
            msg = "Not Valid phone number."
            self.add_error('phone', msg)

    class Meta:
        model = CheckOut
        fields = ('phone', 'street', 'building', 'apartment', 'floor', 'other')
