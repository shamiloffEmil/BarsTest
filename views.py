import random
from django.db import connection
from django.shortcuts import redirect
from .forms import RecruitForm, ResultForm , AnswerForm, SithForm,TestHandShadowForm
from .models import TestHandShadow, Recruit, Answer, Result, Sith
from django.shortcuts import render, get_object_or_404
import smtplib


def authorization(request):
    response = render(request,'authorization.html')
    response.delete_cookie('sith_id')
    response.delete_cookie('recruit_id')
    response.delete_cookie('test_id')

    return response

def recruitRegistration(request):
    if request.method == "POST":
        recruitForm = RecruitForm(request.POST)
        response = redirect('recruitTest')
        if recruitForm.is_valid():
            recruit = recruitForm.save(commit=False)
            recruit.save()
            response.set_cookie('recruit_id', recruit.pk, max_age=24*60*60)
        return response

    else:
        recruitForm = RecruitForm()
        return render(request,'recruitRegistration.html',{'recruit': recruitForm})


def recruitTest(request):
    if request.method == "POST":
        recruit = get_object_or_404(Recruit, pk=request.COOKIES["recruit_id"])
        form = ResultForm(request.POST)
        test = get_object_or_404(TestHandShadow, pk=request.COOKIES["test_id"])

        answers = form['answer'].value()


        newResult = Result(recruit=recruit, test=test)
        newResult.save()

        for answer in answers:
            newAnswer = Answer(answer=answer)
            newAnswer.save()
            newResult.answer.add(newAnswer)

        return redirect('authorization')

    else:
        test = TestHandShadow.objects.all()[random.randrange(0, TestHandShadow.objects.count() - 1, 1)]
        questions = test.question.all()
        answerForm = AnswerForm()

        response = render(request, 'recruitTest.html', {'questions': questions, 'answer': answerForm, 'test': test})

        response.set_cookie('test_id',test.pk)
        return response


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

        sithForm = SithForm()
        return render(request,'sithRegistration.html',{'siths': sithForm})




def almostSuccessfulRecruits(request):
    if request.method == "POST":
        if 'slist' in request.POST:
            return redirect('recruitResults', pk=request.POST['slist'])
        else:
            return redirect('authorization')
    else:
        s = []
        cursor = connection.cursor()
        cursor.execute("SELECT barstest_recruit.id FROM barstest_recruit "
                       "INNER JOIN barstest_result on barstest_recruit.id=barstest_result.recruit_id "
                       "WHERE barstest_recruit.rankOfHandShadow = False")
        row = cursor.fetchall()

        for recruit_id in row:
            if len(recruit_id) != 0:
                s.append(Recruit.objects.get(pk=recruit_id[0]))

        return render(request, 'almostSuccessfulRecruits.html', {'recruits': s})

def sendEmail(recruit):
        # От кого:
        fromaddr = '<emil.shamiloff.test@gmail.com>'
        # Кому:
        toaddr = '<'+ recruit.email + '>' #'<shamiloff.emil@yandex.ru>'
        # Тема письма:
        subj = 'Notification from system'
        # Текст сообщения:
        msg_txt = 'Congratulations!:\n\n ' + 'You are accepted! This letter is your offer!'  #
        # Создаем письмо (заголовки и текст)
        msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (fromaddr, toaddr, subj, msg_txt)
        # Логин gmail аккаунта. Пишем только имя ящика.
        # Например, если почтовый ящик someaccount@gmail.com, пишем:
        username = 'emil.shamiloff.test@gmail.com'
        # Соответственно, пароль от ящика:
        password = 'S1V-36q-2GT-Ud0'
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
    recruitRes = get_object_or_404(Recruit, pk=pk)
    if request.method == "POST":
        acceptEmployee = None
        if 'acceptEmployee' in request.POST:
            acceptEmployee = request.POST['acceptEmployee']
        if acceptEmployee != None:
            sith = get_object_or_404(Sith, pk=request.COOKIES["sith_id"])
            if sith.countOfHandShadow <=3:
                sendEmail(recruitRes)
                appointRecruit(recruitRes,sith)

        return render(request, 'authorization.html')

    else:
        recriutResults2 = Result.objects.filter(recruit=recruitRes)

        if len(recriutResults2) !=0:
            return render(request, 'recruitResults.html',
                  {'results': recriutResults2, 'questions': recriutResults2[0].test.question.all(),
                   'answers': recriutResults2[0].answer.all()})
        else:
            return render(request, 'authorization.html')

def sithHandShadow(request):
    if request.method == "POST":
        return redirect('authorization')
    else:
        allSiths = Sith.objects.all()
        return render(request, 'sithHandShadow.html',{'sithHandShadows':allSiths})

def sithHandShadowMore1(request):
    if request.method == "POST":
        return redirect('authorization')
    else:
        allSiths = Sith.objects.filter(countOfHandShadow__gt = 1)
        return render(request, 'sithHandShadow.html', {'sithHandShadows': allSiths})