from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.db.models import Q
from contacts.models import Product,Product_mnt,Contact,Contact_mnt

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
