from django.conf.urls import *
import views

urlpatterns = (
    url(r'^change_email/$', views.change_email, name="change_email"),
)
