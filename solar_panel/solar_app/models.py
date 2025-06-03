from django.db import models
from datetime import date

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key="true")
    name = models.CharField(max_length=30)
    email =  models.CharField(max_length=50)
    phone_number = models.BigIntegerField(max_length=10, default="9090909090")  # Changed to CharField for phone numbers
    password = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=15, default='')  # Provided default value for city
    address = models.CharField(max_length=100, default='')
    is_admin = models.BooleanField(default=False)
    
class Category(models.Model):
    owner_id = models.IntegerField(default=0)
    id = models.AutoField(primary_key="true")
    pimg = models.ImageField(upload_to='media/')
    price = models.BigIntegerField(default=0)
    wattage = models.CharField(max_length=50, blank=True)
    voltage = models.CharField(max_length=50, blank=True)
    warrenty = models.CharField(max_length=250,blank=True)
    title = models.CharField(max_length=250,blank=True)
    description1 = models.TextField(default='No description provided.')
    solar_panel = models.BooleanField(default=False)
    solar_heater = models.BooleanField(default=False)
    inverter = models.BooleanField(default=False)
    solar_cooker = models.BooleanField(default=False)
    luminous = models.BooleanField(default=False)
    loom = models.BooleanField(default=False)
    hi_mo = models.BooleanField(default=False)
    discount_10 = models.BooleanField(default=False)
    discount_20 = models.BooleanField(default=False)
    discount_30 = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, blank=True)  # Allow blank for optional field
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)  # Allow blank for optional field
    phone = models.CharField(max_length=15, blank=True)
    description = models.TextField(default='No description provided.')
    cart=models.IntegerField(default=0)
    buy=models.IntegerField(default=0)
    arrival_time=models.DateField(default=None,null=True)
    status=models.CharField(blank=True)

  
class Contact(models.Model):
    id = models.AutoField(primary_key="true")
    name = models.CharField(max_length=30)
    email =  models.CharField(max_length=50)
    phone_number = models.BigIntegerField(max_length=10, default="9090909090")  # Changed to CharField for phone numbers
    city = models.CharField(max_length=15, default='')  # Provided default value for city
    description1 = models.TextField(default='No description provided.')

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    time = models.TimeField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    address = models.TextField()

    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    discount_10 = models.BooleanField(default=False)
    discount_20 = models.BooleanField(default=False)
    discount_30 = models.BooleanField(default=False)

    gstin = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    arrival_time = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.invoice_id
