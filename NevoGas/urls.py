
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from Gas import views

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', views.index, name="index"),
                  url(r'^contact/', views.contact, name="contact"),
                  url(r'^cart/(?P<url_name>\w+)/$', views.cart),
                  url(r'^checkout/', views.checkout, name="checkout"),
                  url(r'^search/', views.search, name="search"),
                  url(r'^adminpage/', views.adminpage, name="adminpage"),
                  url(r'^add_product/', views.add_product, name="add_product"),
                  url(r'^change/', views.change, name="change"),
                  url(r'^gas_acc/', views.gas_repair, name="gas_acc"),
                  url(r'^gas_repair/', views.gas_repair, name="gas_repair"),
                  # url(r'^edit/(?P<edit_id>[0-9]+)/$', views.edit, name='edit'),
                  # url(r'^prod_del/(?P<del_id>[0-9]+)/$', views.prod_del, name='prod_del'),
                  url(r'^show_order/', views.show_order, name="show_order"),
                  url(r'^comment/', views.comment, name="comment"),
                  url(r'^Adminreg/', views.Adminreg, name="Adminreg"),
                  url(r'^Adminlog/', views.Adminlog, name="Adminlog"),
                  url(r'^Adminlogout/', views.Adminlogout, name="Adminlogout"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

