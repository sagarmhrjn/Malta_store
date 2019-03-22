from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=850)
    price = models.FloatField()
    description = models.TextField()
    imglink = models.CharField(max_length=1000)

    def __str__(self):
        return ('Id:{},Name:{}, Price:{}, Description:{}, Image_link:{}'.format(self.id, self.name, str(self.price), self.description, self.imglink))


class Order(models.Model):
    first_name = models.CharField(max_length=400)
    last_name = models.CharField(max_length=400)
    address = models.CharField(max_length=600)
    city = models.CharField(max_length=400)
    PAYMENT_METHOD = (
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Paypal', 'Paypal'),
    )
    payment_method = models.CharField(
        max_length=100, choices=PAYMENT_METHOD, default='Credit Card')
    payment_data = models.CharField(max_length=400)
    items = models.TextField()
    fulfilled = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return ('Order by {} {} from {}'.format(self.first_name, self.last_name, self.address))
