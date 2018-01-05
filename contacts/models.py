from django.db import models

class Product(models.Model):
    catalog_number = models.CharField(max_length=20, unique=True)
    style_number = models.CharField(max_length=20, blank=True, unique=True)
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE)

    def __str__(self):
        return self.catalog_number

class Contact(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=500, blank=True)
    email = models.EmailField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name
