from django.contrib import admin
from django.db import transaction
from .models import Product, Contact, Product_mnt, Contact_mnt

@transaction.atomic
def commit_products(modeladmin, request, queryset):
    for product_mnt in queryset:
        product = Product.objects.filter(
            catalog_number=product_mnt.catalog_number).first()
        if product:
            product.style_number = product_mnt.style_number
            product.contact = product_mnt.contact
            product.save()
        else:
            product = Product()
            product.catalog_number = product_mnt.catalog_number
            product.style_number = product_mnt.style_number
            product.contact = product_mnt.contact
            product.save()
        product_mnt.delete()

commit_products.short_description = "Approve updates to database"

@transaction.atomic
def commit_contacts(modeladmin, request, queryset):
    for contact_mnt in queryset:
        contact = Contact.objects.filter(
            name=contact_mnt.name).first()
        if contact:
            contact.phone = contact_mnt.phone
            contact.email = contact_mnt.email
            contact.link = contact_mnt.link
            contact.save()
        else:
            contact = Contact()
            contact.name = contact_mnt.name
            contact.email = contact_mnt.email
            contact.link = contact_mnt.link
            contact.save()
        contact_mnt.delete()

commit_contacts.short_description = "Approve updates to database"

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('catalog_number','style_number',)

class Product_mntAdmin(admin.ModelAdmin):
    search_fields = ('catalog_number','style_number',)
    actions = [commit_products]

class Contact_mntAdmin(admin.ModelAdmin):
    actions = [commit_contacts]

admin.site.register(Product,ProductAdmin)
admin.site.register(Contact)
admin.site.register(Product_mnt, Product_mntAdmin)
admin.site.register(Contact_mnt, Contact_mntAdmin)