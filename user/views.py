from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import user.models as usermodels

def loginform(request):
    return render(request, "user/loginform.html")

def login(request):
    email = request.POST['email']
    password = request.POST['password']

    result = usermodels.get_one_user(email, password)
    if result is None:
        return HttpResponseRedirect('/user/loginform?result=fail')

    request.session['userauth'] = result

    # 로그인 처리
    return HttpResponseRedirect('/')

def joinform(request):
    return render(request, "user/joinform.html")

def joinsuccess(request):
    return render(request, "user/joinsuccess.html")

def join(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    gender = request.POST['gender']

    print(name, email, password, gender)

    usermodels.insert(name, email, password, gender)
    return HttpResponseRedirect('/user/joinsuccess')

def updateform(request):
    no = request.session['userauth']['no']
    result = usermodels.fetchonebyno(no)

    if result['gender'] == 'female':
        result['isFemale'] = True
    else:
        result['isFemale'] = False

    data = {'user': result}
    return render(request, 'user/updateform.html', data)

def update(request):
    no = request.session['userauth']['no']
    name = request.POST['name']
    password = request.POST['password']
    gender = request.POST['gender']
    # request.POST['email']

    print(name, password, gender)

    usermodels.update(no, name, password, gender)
    return HttpResponseRedirect('/user/updatesuccess')

def updatesuccess(request):
    return render(request, "user/updatesuccess.html")

def logout(request):
    del request.session['userauth']
    return HttpResponseRedirect('/')

