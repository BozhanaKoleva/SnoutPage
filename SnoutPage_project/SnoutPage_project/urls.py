"""SnoutPage_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from SnoutPage import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name = 'index'),
    url(r'^index/', views.index, name = 'index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^logout/$', views.user_logout, name ='logout'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        views.add_page, name='add_page'),
    url(r'^login/$', views.user_login, name = 'index'),
    url(r'^register/$',views.register, name = 'register'),
    url(r'^search/$',views.search, name = 'search'),
    url(r'^user_page/$',views.user_page, name= 'user_page'),
    url(r'^pet/$',views.pet, name='pet'),
    url(r'^edit_pet/$', views.edit_pet, name='edit_pet'),
    url(r'^category_list/$', views.category_list, name='category_list'),
    url(r'^add_pet/$', views.add_page, name ='add_pet'),
    url(r'^edit_user/$',views.edit_user, name='edit_user'),
    url(r'^password/$',views.change_password, name='change_password'),
   # url(r'^connect/(?P<parameter>.+)/(?P<pk>\d+)/$',views.update_friends, name= 'update_friends')
]
