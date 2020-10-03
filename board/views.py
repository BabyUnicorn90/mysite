from django.http import HttpResponseRedirect
from django.shortcuts import render

import board.models as boardmodel
# Create your views here.
def index(request):
    return render(request, 'board/loginform.html')

    # user_no = request.session['userauth']['no']
    #
    # if user_no is None:
    #     return render(request, 'board/loginrequest.html')

    # results = boardmodel.fetchlist()
    # data = {'boardlist': results, 'user_no': user_no}
    #
    # return render(request, 'board/indextest2.html', data)


def write(request):
    return render(request, 'board/write.html')

def add(request):
    user_no = request.session['userauth']['no']
    title = request.POST['title']
    content = request.POST['content']

    max_group_dict = boardmodel.get_max_group_no() # 10s

    boardmodel.insert(title, content, max_group_dict['max'], user_no)

    return HttpResponseRedirect('/board')



def deleteform(request):
    no = request.GET['no']
    user = request.session['userauth']

    if user is None:
        return

    board = boardmodel.fetchonebyno(no)
    if board is None:
        return

    if board['user_no'] == user['no']:
        return render(request, 'board/deleteconfirm.html')


def delete(request):
    no = request.POST['no']
    print(no == '')
    # boardmodel.delete(no)

    return HttpResponseRedirect('/board')



# no = request.POST['no']
    # password = request.POST['password']
    #
    # result = boardmodel.delete(no, password)
    #
    # if result == 1:
    #     return HttpResponseRedirect('/board')
    # else:
    #     return HttpResponseRedirect('/board/deleteform?no={}&message="sthwrong"'.format(no))
