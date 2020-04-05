from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import *
from .utils import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
# from django.contrib.messages import constants as messages

import requests
import json

# MESSAGE_TAGS = {
#     messages.INFO: 'danger',
#     50: 'critical',
# }

class CustomerTable(ListView):
    initial = {'key': 'value'}
    template_name = 'customers.html'

    def get(self, request, *args, **kwargs):
        page = request.GET.get('page') or 1
        pageSize = 10

        query = """query($page: Int!, $pageSize: Int!) { 
                    business(id: "QnVzaW5lc3M6NjNiOTVkZGItNWRkOS00MzI0LWEzNGYtMDkxOTJmNjNjNDc0") { 
                        customers(page: $page, pageSize: $pageSize) {
                            pageInfo {
                                currentPage
                                totalPages
                                totalCount
                            }
                            edges { 
                                node {
                                    id
                                    name
                                    email
                                    phone
                                    firstName
                                } 
                            } 
                        }
                    } 
                    }"""
        variables = {
                    "page": int(page),
                    "pageSize": int(pageSize)
                }

        url = 'https://gql.waveapps.com/graphql/public'
        headers = {'Authorization': 'Bearer 8NBKTN3t9pfYUS0GsEoNapjY6ooRbi'}

        try:
            r = requests.post(url, json={'query': query, 'variables': variables}, headers= headers)
            response = json.loads( r.text )
            resp = response['data']['business']['customers']
            return render(request, self.template_name, { 'page': resp, 'test': request.GET.get('page') })
        except:
            return render(request, self.template_name, { 'test': request.GET.get('page') })

# class CustomerTable(ListView):
#     # This class reads from the Customers database records and displays the returned data in a table.

#     model = Customers
#     template_name = 'customers.html'
#     context_object_name = 'pages'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = self.model._meta.object_name
#         context['metas'] = self.model._meta.fields
#         context['form'] = CustomersForm(self.request.POST)
#         return context

#     def get_paginate_by(self, queryset):
#         items_per_page = self.request.GET.get('results') or 10
#         return items_per_page

#     def get_queryset(self):
#         return self.model.objects.all().values_list()

class CustomerCreate(SuccessMessageMixin, CreateView):
    # This class creates a Customers and CustomersPrice database record(s) when the form is submitted.

    template_name = 'customers/add.html'
    form_class = CustomersPriceForm
    success_message = "%(name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super(CustomerCreate, self).get_context_data(**kwargs)
        customerprice = ServiceModelFormset(queryset=CustomersPrice.objects.none())
        context['formset'] = customerprice
        context['customer_form'] = CustomerForm()
        return context

    def post(self, request, *args, **kwargs):
        formset = ServiceModelFormset(request.POST)
        if formset.is_valid():
            query = """mutation ($input: CustomerCreateInput!) {
                        customerCreate(input: $input) {
                            didSucceed
                            inputErrors {
                                code
                                message
                                path
                            }
                            customer {
                                id
                                name
                                email
                                phone
                                firstName
                            }
                        }
                    }"""
            variables = {
                "input": {
                    "businessId": "QnVzaW5lc3M6NjNiOTVkZGItNWRkOS00MzI0LWEzNGYtMDkxOTJmNjNjNDc0",
                        "name": request.POST.get('name'),
                        "email": request.POST.get('email'),
                        "phone": request.POST.get('phone'),
                        "firstName": request.POST.get('contact'),
                        
                    }
            }

            url = 'https://gql.waveapps.com/graphql/public'
            headers = {'Authorization': 'Bearer 8NBKTN3t9pfYUS0GsEoNapjY6ooRbi'}

            try:
                r = requests.post(url, json={'query': query, 'variables': variables}, headers= headers)
                response = json.loads( r.text )
                resp = response['data']['customerCreate']['customer']
            
                return self.form_valid(resp, formset)
            except:
                return HttpResponseRedirect(reverse('customers:customers'))

    def form_valid(self, resp, formset):
        for item in formset.save(commit=False):
            item.customer_id = resp['id']
            item.save()
        
        return HttpResponseRedirect(reverse('customers:customer_update', kwargs={'id': resp['id']}))

class CustomerUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'customers/add.html'
    form_class = CustomersPriceForm
    success_message = "%(name)s was created successfully"

    def get(self, request, *args, **kwargs):
        customerId = self.kwargs['id']

        query = """query ($businessId: ID!, $customerId: ID!) {
                    business(id: $businessId) {
                        id
                        customer(id: $customerId) {
                            id
                            name
                            email
                            phone
                            firstName
                        }
                    }
                }"""
        variables = {
                    "businessId": "QnVzaW5lc3M6NjNiOTVkZGItNWRkOS00MzI0LWEzNGYtMDkxOTJmNjNjNDc0",
                    "customerId": customerId
                }

        url = 'https://gql.waveapps.com/graphql/public'
        headers = {'Authorization': 'Bearer 8NBKTN3t9pfYUS0GsEoNapjY6ooRbi'}

        # try:
        r = requests.post(url, json={'query': query, 'variables': variables}, headers= headers)
        response = json.loads( r.text )
        resp = response['data']['business']['customer']
        customer_form = CustomerForm(data={
            'name': resp['name'],
            'email': resp['email'],
            'phone': resp['phone'],
            'contact': resp['firstName'],
        })
        formset = ServiceModelFormset(queryset=CustomersPrice.objects.filter(customer_id=resp['id']))
        return render(request, self.template_name, { 'page': resp, 'customer_form': customer_form, 'formset': formset })
        # except:
            # return render(request, self.template_name, { 'test': response })

    # def post():


# def customerupdate(request, pk):
#     # Read and Update individual Customer records in a form

#     if request.method == 'GET':
#         customerform = CustomersForm(instance=Customers.objects.get(pk=pk))
#         formset = ServiceModelFormset(queryset=CustomersPrice.objects.filter(customer_id=pk))
#     elif request.method == 'POST':
#         customerform = CustomersForm(request.POST or None, instance=Customers.objects.get(pk=pk))
#         formset = ServiceModelFormset(request.POST)

#         if formset.is_valid() and customerform.is_valid():
#             obj= customerform.save(commit= False)
#             obj.save()

#             itemlist = []
#             for item in formset.save(commit=False):    
#                 itemlist.append(item.services_id)
#                 item.customer_id = pk
            
#             if len(itemlist) != len(set(itemlist)):
#                 messages.success(request, "Duplicate service prices are not allowed", extra_tags="danger")
#             else:
#                 messages.success(request, "Customer was updated successfully")
#                 formset.save()
            
#             return redirect('customers:customer_update', pk=pk)
#     return render(request, 'customers/add.html', {
#         'formset': formset,
#         'customer_form': customerform,
#         })

class CustomerDelete(DeleteView):
    # Delete individual Customer records in a modal

    model = Customers

    def get(self, request, **kwargs):
        query = """mutation ($input: CustomerCreateInput!) {
                        customerDelete(input: $input) {
                            didSucceed
                            inputErrors {
                                code
                                message
                                path
                            }
                            customer {
                                id
                                name
                                email
                                phone
                                firstName
                            }
                        }
                    }"""
        variables = {
            "input": {
                "businessId": "QnVzaW5lc3M6NjNiOTVkZGItNWRkOS00MzI0LWEzNGYtMDkxOTJmNjNjNDc0",
                    "id": request.POST.get('id'),
                }
        }
        url = 'https://gql.waveapps.com/graphql/public'
        headers = {'Authorization': 'Bearer 8NBKTN3t9pfYUS0GsEoNapjY6ooRbi'}
        r = requests.post(url, json={'query': query, 'variables': variables}, headers= headers)

        return self.post(request, **kwargs)
    
    def get_success_url(self):
        # CustomersPrice.objects.filter(customer_id=self.object.pk).delete()
        return reverse_lazy('customers:customers')

class CustomerPriceDelete(DeleteView):
    # Delete individual Customer Price records in the repeater field

    model = CustomersPrice

    def get(self, request, **kwargs):
        return self.post(request, **kwargs)

    def get_success_url(self):
        return reverse_lazy('customers:customer_update', kwargs={'pk': self.object.customer_id})