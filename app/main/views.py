from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
import requests
import json

# @login_required(login_url='/accounts/login/')
# def home(request):
#     return render(request, 'home.html')

# @login_required(login_url='/accounts/login/')
# def overview(request):
#     return render(request, 'overview.html')

class MyView(View):
    form_class = invoiceForm
    initial = {'key': 'value'}
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        query = """query { 
                    business(id: "QnVzaW5lc3M6NjNiOTVkZGItNWRkOS00MzI0LWEzNGYtMDkxOTJmNjNjNDc0") { 
                        customers { 
                            edges { 
                                node {
                                    id
                                    name
                                    firstName
                                    lastName
                                    internalNotes
                                    createdAt
                                    website
                                    address {
                                        addressLine1
                                    }
                                } 
                            } 
                        }
                    } 
                }"""
        url = 'https://gql.waveapps.com/graphql/public'
        headers = {'Authorization': 'Bearer 8NBKTN3t9pfYUS0GsEoNapjY6ooRbi'}
        r = requests.post(url, json={'query': query}, headers= headers)
        
        return render(request, self.template_name, {'form': form, 'test': r.text })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})
