from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import json

from .models import Questions,Choice

def index(request):
    latest_question_list = Questions.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_question_list}

    return render(request, 'polls/index.html',context)

def detail(request,question_id):
    try:
        question = Questions.objects.get(pk=question_id)
    except Questions.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html',{'question':question})

def result(request,question_id):
    question = get_object_or_404(Questions, pk=question_id)
    # question1 = question_id
    data = question.choice_set.all()
    votedata = {} 
    for vote in data:
        votedata.update({vote.choice_text:vote.votes})
    jsonData = json.dumps(votedata)
    print(jsonData)
    return render(request,'polls/results.html', {'question':question,'votedata':jsonData})


def vote(request,question_id):
    print(request.POST['choice'])
    question = get_object_or_404(Questions,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message': "You don't select choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result',args=(question.id,)))