from django.http import HttpResponseRedirect
from django.shortcuts import render

import board.models as boardmodel
# Create your views here.

def index(request):
    board_no = request.GET.get('no')
    if board_no is not None:
        results = boardmodel.fetchonebyno(board_no)
        data = { 'boarditem': results }
        boardmodel.hit(board_no)
        return render(request, 'board/view.html', data)

    user = request.session.get('userauth')
    if user is None:
        return render(request, 'board/loginrequest.html')

    results = boardmodel.fetchlist()
    data = {'boardlist': results, 'user_no': user['no'] }
    return render(request, 'board/index.html', data)

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
        return HttpResponseRedirect('/board')

    if board['user_no'] == user['no']:
        return render(request, 'board/deleteconfirm.html', {'board_no': board['no']})


def delete(request):
    board_no = request.POST['board_no']
    boardmodel.delete(board_no)

    return HttpResponseRedirect('/board')

def modifyform(request):
    board_no = request.GET['no']
    user = request.session['userauth']

    board = boardmodel.fetchonebyno(board_no)
    if board is None:
        return HttpResponseRedirect('/board')

    if board['user_no'] == user['no']:
        data = { 'board': board }
        return render(request, 'board/modify.html', data)


def modify(request):
    board_no = request.POST['board_no']
    title = request.POST['title']
    content = request.POST['content']

    boardmodel.update(board_no, title, content)

    return HttpResponseRedirect('/board?no={}'.format(board_no))


# no = request.POST['no']
    # password = request.POST['password']
    #
    # result = boardmodel.delete(no, password)
    #
    # if result == 1:
    #     return HttpResponseRedirect('/board')
    # else:
    #     return HttpResponseRedirect('/board/deleteform?no={}&message="sthwrong"'.format(no))
