# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from FSA.models import Terminal
from django.template.defaultfilters import linebreaksbr

# Create your views here.


class Home(View):

    def get(self,request):
        return render(request, 'main/index.html')

    def post(self,request):
        yourInstance = Terminal()
        commandInput = request.POST["command"]
        if commandInput:
            response = yourInstance.command(commandInput)
            response = linebreaksbr(response)
        else:
            response = ""
        return render(request, 'main/index.html',{"message":response})
