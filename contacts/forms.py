from django import forms

class DataUploadForm(forms.Form):
    contact_file = forms.FileField(help_text='File must have these exact four columns: name, phone, email, link', required=False)
    product_file = forms.FileField(help_text='File must have these exact three columns: catalog_number, style_number, contact_name', required=False)
