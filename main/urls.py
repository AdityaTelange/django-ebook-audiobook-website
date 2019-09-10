from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView, RedirectView

import main.forms
import main.views

urlpatterns = [
                  url(r"about-us/",
                      TemplateView.as_view(template_name="about_us.html"),
                      name='about_us'),
                  path("",
                       TemplateView.as_view(template_name="home.html"),
                       name="home"),
                  path("contact-us/",
                       main.views.ContactUs.as_view(),
                       name="contact_us"),
                  path("accounts/", RedirectView.as_view(url='login', permanent=True, )),
                  path('accounts/signup/',
                       main.views.SignupView.as_view(),
                       name="signup"),
                  path("accounts/login/",
                       auth_views.LoginView.as_view(template_name="account/login.html",
                                                    form_class=main.forms.AuthenticationForm,
                                                    redirect_authenticated_user=True),
                       name="login",
                       kwargs={'redirect_authenticated_user': True}),
                  path("accounts/logout/",
                       auth_views.LogoutView.as_view(),
                       name="logout"),
                  path("accounts/profile/",
                       main.views.ProfileView.as_view(),
                       name="profile", ),
                  # path("authed/", RedirectView.as_view(url='home', permanent=False)),
                  path(
                      "address/",
                      main.views.AddressListView.as_view(),
                      name="address_list",
                  ),
                  path(
                      "address/create/",
                      main.views.AddressCreateView.as_view(),
                      name="address_create",
                  ),
                  path(
                      "address/<int:pk>/",
                      main.views.AddressUpdateView.as_view(),
                      name="address_update",
                  ),
                  path(
                      "address/<int:pk>/delete/",
                      main.views.AddressDeleteView.as_view(),
                      name="address_delete",
                  ),
                  path(
                      "add_to_basket/",
                      main.views.add_to_basket,
                      name="add_to_basket",
                  ),
                  path('basket/',
                       main.views.manage_basket,
                       name="basket"),
                  path(
                      "order/done/",
                      TemplateView.as_view(template_name="main/done_order.html"),
                      name="checkout_done",
                  ),
                  path(
                      "order/address_select/",
                      main.views.AddressSelectionView.as_view(),
                      name="address_select",
                  ),
                  # path(
                  #     "order_dashboard/",
                  #     main.views.OrderView.as_view(),
                  #     name="order_dashboard",
                  # ),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
