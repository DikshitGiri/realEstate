"""
URL configuration for realEstate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from App import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # pages
    path('admin/', admin.site.urls),  
    
    path('broker',views.broker_login_page, name="broker_login_page"),
    path("broker_register_page",views.broker_register_page,name="broker_register_page"),
    path('',views.index, name="index"),
    path('realEstate_dashboard', views.realEstate_dashboard, name='realEstate_dashboard'),
    path('add_property',views.add_property_page, name='add_property_page'),
    path('docs',views.docs_page,name='docs_page'),
    path('broker_dashboard', views.broker_dashboard, name='broker_dashboard'),

    path('property_table', views.property_table_page,name='property_table_page'),
    path ('property_type',views.property_type_page,name="property_type_page"),
    # pages ends
    #login logout begins
    path('owner_login',views.owner_login,name='owner_login'),
    path('broker_login',views.broker_login, name='broker_login'),
    path('broker_register',views.broker_register,name="broker_register"),
    path('log_out',views.log_out,name="log_out"),
    #login logout ends
     
    # insertion process begins
    path ('property_type_db', views.property_type_db,name="property_type_db"),
    path ('property_db', views.property_db,name="property_db"),
   

    # insertion process ends
    # retrival begins
    path('property_search', views.property_search,name='property_search'),
    # retrival ends
    # update and deletion begins
    path('delete_property/<int:id>/', views.delete_property, name='delete_property'),
    path('update_property_page/<int:id>/', views.update_property_page, name='update_property_page'),
    path('update_property/<int:id>/',views.property_update_db,name='update_property_db'),
    # update and deletion ends
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
