from django.contrib import admin

from .models import Product, Contact, Product_mnt, Contact_mnt

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Product_mnt)
admin.site.register(Contact_mnt)