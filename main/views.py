import logging

# import django_filters
from django import forms as django_forms
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    # UserPassesTestMixin,
)
# from django.db import models as django_models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.list import ListView

import ebook.models
import main.models
from main import forms

# from django_filters.views import FilterView

logger = logging.getLogger(__name__)


class ContactUs(FormView):
    template_name = 'main/contact_form.html'
    form_class = forms.ContactForm
    success_url = "/"

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.send_mail()
        messages.info(self.request, "Message Sent successfully.")
        return response


class SignupView(FormView):
    template_name = "account/signup.html"
    form_class = forms.UserCreationForm

    success_url = "/"

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info("New signup for email=%s through SignupView", email)
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(self.request, "You signed up successfully.")
        return response


class AddressListView(LoginRequiredMixin, ListView):
    model = main.models.Address

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = main.models.Address
    fields = [
        "name",
        "address1",
        "address2",
        "zip_code",
        "city",
        "country",
    ]
    success_url = reverse_lazy("address_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = main.models.Address
    fields = [
        "name",
        "address1",
        "address2",
        "zip_code",
        "city",
        "country",
    ]
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = main.models.Address
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ProfileView(LoginRequiredMixin, ListView):
    template_name = "account/profile.html"
    model = main.models.Address

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def add_to_basket(request):
    product = get_object_or_404(
        ebook.models.Ebook, pk=request.GET.get("ebook_id")
    )
    basket = request.basket
    if not request.basket:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        basket = main.models.Basket.objects.create(user=user)
        request.session["basket_id"] = basket.id

    basketline, created = main.models.BasketLine.objects.get_or_create(
        basket=basket, product=product
    )
    if not created:
        basketline.quantity += 1
        basketline.save()
    return HttpResponseRedirect(
        reverse("ebook", args=(product.slug,))
    )


def manage_basket(request):
    if not request.basket:
        return render(request, "main/basket.html", {"formset": None})
    if request.method == "POST":
        formset = forms.BasketLineFormSet(
            request.POST, instance=request.basket
        )
        if formset.is_valid():
            formset.save()
    else:
        formset = forms.BasketLineFormSet(
            instance=request.basket
        )
    if request.basket.is_empty():
        return render(request, "main/basket.html", {"formset": None})
    return render(request, "main/basket.html", {"formset": formset})


class AddressSelectionView(LoginRequiredMixin, FormView):
    template_name = "main/address_select.html"
    form_class = forms.AddressSelectionForm
    success_url = reverse_lazy('checkout_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        del self.request.session['basket_id']
        basket = self.request.basket
        basket.create_order(
            form.cleaned_data['billing_address'],
            form.cleaned_data['shipping_address']
        )
        return super().form_valid(form)


class DateInput(django_forms.DateInput):
    input_type = "date"

# class OrderFilter(django_filters.FilterSet):
#     class Meta:
#         model = main.models.Order
#         fields = {
#             "user__email": ["icontains"],
#             "status": ["exact"],
#             "date_updated": ["gt", "lt"],
#             "date_added": ["gt", "lt"],
#         }
#         filter_overrides = {
#             django_models.DateTimeField: {
#                 "filter_class": django_filters.DateFilter,
#                 "extra": lambda f: {"widget": DateInput},
#             }
#         }


# class OrderView(UserPassesTestMixin, FilterView):
#     filterset_class = OrderFilter
#     login_url = reverse_lazy("login")
#
#     def test_func(self):
#         return self.request.user.is_staff is True


# def room(request, order_id):
#     return render(
#         request,
#         "chat_room.html",
#         {"room_name_json": str(order_id)},
#     )
