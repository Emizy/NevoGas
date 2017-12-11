import hashlib
from django.db import models


# Create your models here.
class Contact(models.Model):
    subject = models.CharField(max_length=40)
    Email = models.EmailField(null=True, blank=True, max_length=254)
    message = models.TextField()

    def __str__(self):
        return self.subject


# class Product(models.Model):
#     price = models.IntegerField()
#     product_name = models.CharField(max_length=300)
#     types = (
#         ('Provisions', 'Provisions'),
#         ('Raw Food', 'Raw Food'),
#         ('Snacks', 'Snacks'),
#         ('Cooked Food', 'Cooked Food'),
#         ('Soup ingredient', 'Soup ingredient'),
#     )
#     category = models.CharField(choices=types, max_length=20, blank=True, null=True)
#     type_choices = {
#         ('Men', 'Men'),
#         ('Women', 'Women'),
#         ('Children', 'Children'),
#     }
#     section = models.CharField(choices=type_choices, max_length=20, blank=True, null=True)
#     image = models.FileField(null=True, blank=True)
#     supplier = models.CharField(max_length=200)
#     date = models.DateTimeField(auto_now_add=True)
#
#     # class Meta:
#     #     verbose_name_plural = "Products"
#
#     def __str__(self):
#         return "%s - %s" % (self.category, self.product_name)


class Location(models.Model):
    name = models.CharField(max_length=100)
    charge = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.charge)


class Gas(models.Model):
    price = models.IntegerField()
    product_name = models.CharField(max_length=300)
    types = (
        ('gas_acc', 'gas_acc'),
        ('gas_refill', 'gas_refill'),
    )
    Accessories = models.CharField(choices=types, max_length=20, blank=True, null=True)
    image = models.FileField(null=True, blank=True)
    supplier = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     verbose_name_plural = "Products"

    def __str__(self):
        return "%s - %s" % (self.product_name, self.price)


class GasRepair(models.Model):
    fname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(null=True, blank=True, max_length=254)
    phone = models.CharField(max_length=11)
    location = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    cooker = models.CharField(max_length=200, blank=True, null=True)
    descrip = models.TextField(blank=True)
    image1 = models.FileField(null=True, blank=True)
    image2 = models.FileField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.fname, self.phone)


class Order(models.Model):
    Name = models.CharField(max_length=90)
    Email = models.EmailField(null=True, blank=True, max_length=254)
    Phone = models.CharField(max_length=11)
    address = models.TextField(blank=True)
    loc = models.CharField(max_length=100)
    del_charge = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()
    sumtotal = models.IntegerField()
    confirm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.Name, self.sumtotal)


class OrderingDetails(models.Model):
    item = models.ForeignKey(Gas, on_delete=models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    qty = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s - %s - %s - %s" % (
            self.order.Name, self.order.Phone, self.order.Phone, self.item.product_name,
            self.order.sumtotal)


class adminreg(models.Model):
    Username = models.CharField(max_length=15, unique=True)
    Password = models.TextField()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.Password = createHash(self.Password)
        super(adminreg, self).save(*args, **kwargs)


# hashing of password using SHA256
def createHash(value):
    hash = hashlib.sha256()
    hash.update(str(value).encode(encoding='UTF-8'))
    return hash.hexdigest()
