from django.conf.urls import url

from contents import views

urlpatterns = [
    url(r'^index/$',views.ContentsView.as_view(),name='index')
]
