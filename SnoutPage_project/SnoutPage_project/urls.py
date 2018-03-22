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
from django.conf import settings
from django.conf.urls.static import static
from SnoutPage import views

app_name = 'SnoutPage'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name = 'index'),
    url(r'^index/', views.index, name = 'index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^logout/$', views.user_logout, name ='logout'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        views.add_page, name='add_page'),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^register/$',views.register, name = 'register'),
    url(r'^search/$',views.search, name = 'search'),
    url(r'^show_user_page/$',views.show_user_page, name= 'show_user_page'),
    # url(r'^show_user_page/(P<pk>\d+)/$',views.show_user_page, name= 'show_user_page_with_pk'),
    url(r'^show_user_page/(?P<username>[\w\-]+)/$', views.show_user_page, name='show_user_page'),
    #url(r'^pet/$',views.pet, name='pet'),
##    url(r'SnoutPage/(?P<pet_name_slug>[\w\-]+)/$',
##        views.pet, name='pet'),
    url(r'^edit_pet/$', views.edit_pet, name='edit_pet'),
    url(r'^category_list/$', views.category_list, name='category_list'),
    url(r'^add_pet/$', views.add_pet, name ='add_pet'),
    url(r'^edit_user/$',views.edit_user, name='edit_user'),
    url(r'^password/$',views.change_password, name='change_password'),
    url(r'^add_info/$', views.add_info, name = 'add_info'),
    url(r'^add_post/(?P<pet_name_slug>[\w\-]+)/$', views.add_post, name = 'add_post'),
    url(r'^add_comment/(?P<post_title_slu>[\w\-]+)/$', views.add_comment, name = 'add_comment'),
    url(r'SnoutPage/pet/(?P<pet_name_slug>[\w\-]+)/$', views.pet, name='pet'),
    url(r'SnoutPage/post/(?P<post_title_slug>[\w\-]+)/$', views.post, name='post'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   # url(r'^connect/(?P<parameter>.+)/(?P<pk>\d+)/$',views.update_friends, name= 'update_friends')
