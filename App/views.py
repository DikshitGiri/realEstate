from django.shortcuts import render

# Create your views here.
def realEstate_dashboard(request):
    return render(request, 'components/overview.html')
def add_property_page(request):
    return render(request, 'components/add_property.html') 
def docs_page(request):
    return render (request,'components/docs.html')
def property_table_page(request):
    return render (request,'components/property_table.html')