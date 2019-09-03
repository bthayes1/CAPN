from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.db.models import Q
from contacts.models import Product,Product_mnt,Contact,Contact_mnt
import pandas as pd
from django.db import IntegrityError, transaction
from django.shortcuts import render
from contacts.forms import DataUploadForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

class IndexView(TemplateView):
    template_name = 'contacts/index.html'

class Product_mntCreateView(CreateView):
    model = Product_mnt
    fields = ('catalog_number','style_number','contact','note')
    template_name = 'contacts/mnt_create.html'

    def get_initial(self):
        c = self.request.GET.get('c','')
        initial = super(Product_mntCreateView, self).get_initial()
        initial = initial.copy()
        if c:
            prod = Product.objects.get(catalog_number=c)
            initial['pid'] = prod.pk
            initial['catalog_number'] = prod.catalog_number
            initial['style_number'] = prod.style_number
            initial['contact'] = prod.contact
        return initial

class Contact_mntCreateView(CreateView):
    model = Contact_mnt
    fields = ('name','phone','email','link','note')
    template_name = 'contacts/mnt_create.html'

    def get_initial(self):
        c = self.request.GET.get('c','')
        initial = super(Contact_mntCreateView, self).get_initial()
        initial = initial.copy()
        if c:
            cont = Contact.objects.get(name=c)
            initial['pid'] = cont.pk
            initial['name'] = cont.name
            initial['phone'] = cont.phone
            initial['email'] = cont.email
            initial['link'] = cont.link
        return initial

####################
### Part # Query ###
####################
def part_numberQuery(request):
    part_num = request.GET.get('q')
    timestamp = request.GET.get('t')
    product_result = {'t':timestamp,'result':list(Product.objects.filter(
        Q(catalog_number__istartswith=part_num) |
        Q(style_number__istartswith=part_num)).select_related('contact').values(
            'catalog_number',
            'style_number',
            'contact__name',
            'contact__phone',
            'contact__email',
            'contact__link'))[:42]}
    return JsonResponse(product_result, safe=True)

##############################
### Mass Update            ###
##############################

@method_decorator(login_required, name='dispatch')
class DataUploadView(generic.FormView):
    template_name = 'contacts/data_upload.html'
    form_class = DataUploadForm
    success_url = '/contacts/'

    def form_valid(self, form):
        data = ''
        contact_sheet = form.cleaned_data.get('contact_file')
        if contact_sheet:
            cdf = pd.read_excel(contact_sheet)
            headers = set(list(cdf))
            model_fields = set(['name','phone','email','link'])
            if headers != model_fields:
                data += 'Contact headers are not correct<br>'
                return render(self.request,'contacts/data_upload.html',
                    {'data':data})
            else:
                with transaction.atomic():
                    for row in cdf.itertuples():
                        obj, created = Contact.objects.update_or_create(
                            name = row.support,
                            defaults = {
                                'phone':row.phone,
                                'email':row.email,
                                'link':row.link,
                            }
                        )
                data += 'Contact data successfully added<br>'
        else:
            data += 'No contact data<br>'

        product_sheet = form.cleaned_data.get('product_file')
        if product_sheet:
            pdf = pd.read_excel(product_sheet)
            headers = set(list(pdf))
            model_fields = set(['catalog_number','style_number','contact_name'])
            if headers != model_fields:
                data += 'Product headers are not correct<br>'
                return render(self.request,'contacts/data_upload.html',
                    {'data':data})
            else:
                with transaction.atomic():
                    for row in pdf.itertuples():
                        try:
                            contact = Contact.objects.get(name=row.contact_name)
                            obj, created = Product.objects.update_or_create(
                                catalog_number = row.catalog_number,
                                defaults = {
                                    'style_number':row.style_number,
                                    'contact':contact,
                                }
                            )
                        except IntegrityError:
                            continue
                data += 'Product data successfully added<br>'
        else:
            data += 'No product data<br>'

        return render(self.request,'contacts/data_upload.html',
                    {'data':data})
