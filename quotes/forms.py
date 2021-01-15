from django import forms
from .models import Stock

class StockForms(forms.ModelForm):
    
    class Meta:
        model = Stock
        fields = ["ticker"]