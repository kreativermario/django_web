from django import forms


class StockSearchForm(forms.Form):
    stock_ticker = forms.CharField(
        label="Stock Ticker",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
