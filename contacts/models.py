from django.db import models
from django.urls import reverse

class Product(models.Model):
    catalog_number = models.CharField(max_length=20, unique=True)
    style_number = models.CharField(max_length=20, blank=True, unique=True)
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE)

    def __str__(self):
        return self.catalog_number

class Contact(models.Model):
    name = models.CharField(max_length=200,unique=True)
    phone = models.CharField(max_length=500, blank=True)
    email = models.EmailField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Product_mnt(models.Model):
    pid = models.IntegerField(blank=True,null=True)
    catalog_number = models.CharField(max_length=20, unique=True)
    style_number = models.CharField(max_length=20, blank=True, unique=True)
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE)
    note = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.catalog_number

    def get_absolute_url(self):
        return reverse('contacts:index')

class Contact_mnt(models.Model):
    pid = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=200,unique=True)
    phone = models.CharField(max_length=500, blank=True)
    email = models.EmailField(blank=True)
    link = models.URLField(blank=True)
    note = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contacts:index')