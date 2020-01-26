import random
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from .forms import RecruitForm, ResultForm , AnswerForm, SithForm
from .models import TestHandShadow, Recruit, Answer, Result, Sith
from django.shortcuts import render, get_object_or_404

import smtplib
import sys

def authorization(request):
    response = render(request,'authorization.html')
    response.delete_cookie('sith_id')
    response.delete_cookie('recruit_id')

    return response

def recruitRegistration(request):
    if request.method == "POST":
        recruitForm = RecruitForm(request.POST)
        response = redirect('recruitTest')
        if recruitForm.is_valid():
            recruit = recruitForm.save(commit=False)
            recruit.save()
            response.set_cookie('recruit_id', recruit.pk)

        #return redirect('recruitTest', pk = recruit.pk)

        return response

    else:
        recruitForm = RecruitForm()

        return render(request,'recruitRegistration.html',{'recruit': recruitForm})

def recruitTest(request):
    recruit = get_object_or_404(Recruit, pk=request.COOKIES["recruit_id"])
    test = TestHandShadow.objects.all()[random.randrange(0, TestHandShadow.objects.count(), 1)]
    questions = test.question.all()

    if request.method == "POST":
        form = ResultForm(request.POST)
        answers = form['answer'].value()

        newResult = Result(recruit=recruit, test=test)
        newResult.save()

        for answer in answers:
            newAnswer = Answer(answer = answer)
            newAnswer.save()
            newResult.answer.add(newAnswer)

        return redirect('authorization')

    else:
        answerForm = AnswerForm()
        return render(request, 'recruitTest.html', {'questions': questions,'answer': answerForm})


def sithRegistration(request):
    if request.method == "POST":
        if 'sith' in request.POST:
            form = SithForm(request.POST)
            sith_id = form['sith'].value()

            response = redirect('almostSuccessfulRecruits')
            response.set_cookie('sith_id', sith_id)
            return response

        else:
            return redirect('almostSuccessfulRecruits')


    else:

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM barstest_recruit "
                       "INNER JOIN barstest_result on barstest_recruit.id=barstest_result.recruit_id "
                       "WHERE barstest_recruit.rankOfHandShadow = False")

        row = cursor.fetchone()
        print(row)

        sithForm = SithForm()
        return render(request,'sithRegistration.html',{'siths': sithForm})




def almostSuccessfulRecruits(request):
    if request.method == "POST":
        return redirect('recruitResults', pk=request.POST['slist'])
    else:
        s = []
        cursor = connection.cursor()
        cursor.execute("SELECT barstest_recruit.id FROM barstest_recruit "
                       "INNER JOIN barstest_result on barstest_recruit.id=barstest_result.recruit_id "
                       "WHERE barstest_recruit.rankOfHandShadow = False")
        row = cursor.fetchall()

        for recruit_id in row:
            s.append(Recruit.objects.get(pk=recruit_id[0]))

        return render(request, 'almostSuccessfulRecruits.html', {'recruits': s})

def sendEmail(recruit):
        # От кого:
        fromaddr = '<shamiloff.emil@gmail.com>'
        # Кому:
        toaddr = '<'+ recruit.email + '>' #'<shamiloff.emil@yandex.ru>'
        # Тема письма:
        subj = 'Notification from system'
        # Текст сообщения:
        msg_txt = 'Notice:\n\n ' + 'test' + '\n\nBye!'  #
        # Создаем письмо (заголовки и текст)
        msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (fromaddr, toaddr, subj, msg_txt)
        # Логин gmail аккаунта. Пишем только имя ящика.
        # Например, если почтовый ящик someaccount@gmail.com, пишем:
        username = 'shamiloff.emil@gmail.com'
        # Соответственно, пароль от ящика:
        password = 'Bmwm5f10'
        # Инициализируем соединение с сервером gmail по протоколу smtp.
        server = smtplib.SMTP('smtp.gmail.com:587')
        # Выводим на консоль лог работы с сервером (для отладки)
        server.set_debuglevel(1);
        # Переводим соединение в защищенный режим (Transport Layer Security)
        server.starttls()
        # Проводим авторизацию:
        server.login(username, password)
        # Отправляем письмо:
        server.sendmail(fromaddr, toaddr, msg)
        # Закрываем соединение с сервером
        server.quit()

def appointRecruit(recruit,sith):
    recr = get_object_or_404(Recruit, pk=recruit.pk)
    recr.rankOfHandShadow = True
    recr.save()

    sith.countOfHandShadow += 1
    sith.save()


def recruitResults(request,pk):
    recruitRes = Recruit.objects.filter(pk=pk)
    if request.method == "POST":
        acceptEmployee = None
        if 'acceptEmployee' in request.POST:
            acceptEmployee = request.POST['acceptEmployee']
        if acceptEmployee != None:
            sith = Sith.objects.get(id=request.COOKIES["sith_id"])
            if sith.countOfHandShadow <=3:
                #sendEmail(recruitRes[0])
                appointRecruit(recruitRes[0],sith)
        return render(request, 'authorization.html')

    else:
        recriutResults2 = Result.objects.filter(recruit=recruitRes[0])
        return render(request, 'recruitResults.html',
                  {'results': recriutResults2, 'questions': recriutResults2[0].test.question.all(),
                   'answers': recriutResults2[0].answer.all()})

def sithHandShadow(request):
    allSiths = Sith.objects.all()
    print(allSiths)
    return render(request, 'sithHandShadow.html',{'sithHandShadows':allSiths})

def sithHandShadowMore1(request):
    allSiths = Sith.objects.filter(countOfHandShadow__gt = 1)
    print(allSiths)
    return render(request, 'sithHandShadow.html', {'sithHandShadows': allSiths})