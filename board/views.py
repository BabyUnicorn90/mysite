import math
from django.http import HttpResponseRedirect
from django.shortcuts import render

import board.models as boardmodel
# Create your views here.

def index(request):
    page_no = request.GET.get('page')
    board_no = request.GET.get('no')
    limit = 10

    if page_no is None:
        page_no = 1
    else:
        page_no = int(page_no)

    if page_no < 1:
        page_no = 1

    if board_no is not None:
        results = boardmodel.fetchonebyno(board_no)
        data = { 'boarditem': results }
        boardmodel.hit(board_no)
        return render(request, 'board/view.html', data)

    user = request.session.get('userauth')
    if user is None:
        return HttpResponseRedirect('/user/loginform')


    results = boardmodel.fetchlist(limit, page_no)

    if len(results) == 0:
        return HttpResponseRedirect('/board')

    topcnt = results[0]['topcnt']
    max_page = math.ceil(topcnt/limit)

    page_range = range(1, 6)
    if page_no > 2:
        page_range = range(page_no - 2, page_no + 3)

    data = {
        'boardlist': results,
        'user_no': user['no'],
        'max_page': max_page,
        'page_range': page_range,
        'page': page_no
    }
    print(data)
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