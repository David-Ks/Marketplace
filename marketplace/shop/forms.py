from django import forms

from .models import CheckOut


class CheckOutForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        pay_method = cleaned_data.get("pay_method")

        if not str(phone).isdigit():
            msg = "Phone is not Valid"
            self.add_error('phone', msg)

        print(pay_method)
        if pay_method not in ['ArCa', 'Telcell', 'IDram']:
            msg = "Pay method is not Valid"
            self.add_error('pay_method', msg)

    class Meta:
        model = CheckOut
        fields = ('phone', 'street', 'building', 'apartment', 'floor', 'other', 'pay_method')
