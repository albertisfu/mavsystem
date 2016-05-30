from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'mavalpa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('almacen.urls')),


]


from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



