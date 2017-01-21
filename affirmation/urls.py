from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from affirmation import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^account/$', views.account, name='account'),
    url(r'^data/$', views.data, name='data'),
    url(r'^pastdata/$', views.pastData, name='pastdata'),
    url(r'^treatment/$', views.treatment, name='treatment'),
    url(r'^resources/$', views.resources, name='resources'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
