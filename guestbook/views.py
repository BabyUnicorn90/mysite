from django.http import HttpResponseRedirect
from django.shortcuts import render

import guestbook.models as guestbookmodel


def index(request):
    # return HttpResponse('<h1>Hello World</h1>', content_type='text/html')
    results = guestbookmodel.fetchlist()
    data = {'guestbooklist': results}
    return render(request, 'guestbook/index.html', data)


def add(request):
    name = request.POST['name']
    password = request.POST['password']
    message = request.POST['message']

    guestbookmodel.insert(name, password, message)

    return HttpResponseRedirect('/guestbook')


def deleteform(request):
    no = request.GET['no']
    msg = request.GET.get('message')
    data = {'no': no, 'message': msg}
    return render(request, 'guestbook/deleteform.html', data)


def delete(request):
    no = request.POST['no']
    password = request.POST['password']

    result = guestbookmodel.delete(no, password)

    if result == 1:
        return HttpResponseRedirect('/guestbook')
    else:
        return HttpResponseRedirect('/guestbook/deleteform?message="sthwrong"')