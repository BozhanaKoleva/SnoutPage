from django.conf.urls import url,include
from SnoutPage import views

urlpatterns =[
    url(r'^$', views.index, name = 'index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^logout/$', views.user_logout, name ='logout'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        views.add_page, name='add_page'),
    url(r'^login/$', views.user_login, name = 'index'),
    url(r'^register/$',views.register, name = 'register'),
    url(r'^search/$',views.search, name = 'search'),
   # url(r'^connect/(?P<parameter>.+)/(?P<pk>\d+)/$',views.update_friends, name= 'update_friends')
]
