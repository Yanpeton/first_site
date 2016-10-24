"""ten_mins URL Configuration

The `urlpatterns` listing routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from blog.views import listing, article_detail, index_login, index_register, \
     complete, profile, profile_post, pwd_change, collection_list
from django.contrib.auth.views import logout
from first_site import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^articles/$', listing, name='article_list'),
    url(r'^articles/(?P<tag>[a-z]+)/$', listing, name='article_category_list'),
    url(r'^articles/(?P<tag>[a-z]+)/(?P<sort>[a-z]+)/$', listing,
        name='article_category_sort_list'),
    url(r'^articles/(?P<article_id>\d+)/$', article_detail,
        name='article_detail'),
    url(r'^login/$', index_login, name='login'),
    url(r'^register/$', index_register, name='register'),
    url(r'^logout/$', logout, {'next_page': '/login'}, name='logout'),
    url(r'^complete/$', complete, name='complete'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^profile_post/$', profile_post, name='profile_post'),
    url(r'^profile/pwd_change/$', pwd_change, name='pwd_change'),
    url(r'^profile/collection/$', collection_list, name='collection_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
