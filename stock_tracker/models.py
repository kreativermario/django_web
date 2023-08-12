from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    country = models.CharField(max_length=50, default=None)
    city = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=50, default=None)
    address = models.CharField(max_length=50, default=None)
    website = models.CharField(max_length=50, default=None)
    industry = models.CharField(max_length=50, default=None)
    sector = models.CharField(max_length=50, default=None)
    business_summary = models.CharField(max_length=250, default=None)


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)  # Ticker symbol
    name = models.CharField(max_length=100, default=None)  # Stock name
    currency = models.CharField(max_length=5, default='')  # Currency
    exchange = models.CharField(max_length=15, default=None)  # Market exchange
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                default=-1.0)  # Current price
    company = models.OneToOneField(Company, models.CASCADE, default=None)
    overall_risk = models.CharField(max_length=15, default=None)
    previous_close_price = models.DecimalField(max_digits=6, decimal_places=2,
                                default=-1.0)  # Previous close price
    open_price = models.DecimalField(max_digits=6, decimal_places=2,
                                default=-1.0)  # Open price
    bid_price = models.DecimalField(max_digits=6, decimal_places=2,
                                default=-1.0)  # Bid price
    ask_price = models.DecimalField(max_digits=6, decimal_places=2,
                                default=-1.0)  # Ask price
    # TODO add price, ISIN, and other relevant fields

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stocks = models.ManyToManyField(Stock, through='PortfolioStock')

    def __str__(self):
        return self.name


class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Transaction(models.Model):
    BUY = 'Buy'
    SELL = 'Sell'
    TRANSACTION_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.stock} - {self.quantity} shares"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #TODO Add additional user profile fields
