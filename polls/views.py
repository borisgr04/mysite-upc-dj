from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import  get_object_or_404,render
from django.http import Http404
from .models import Question
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http.response import  JsonResponse
from django.utils import timezone
import json

""" Primera version

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
"""

""" Segunda Version
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([p.question_text for p in latest_question_list])
    return HttpResponse(output)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
"""

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def questions(request):
    s = serializers.serialize('json',Question.objects.all())
    return HttpResponse(s, content_type="application/json")

def get_question(request):
    questions = Question.objects.all()
    all_q = []
    for foreq in questions:
         output = {
                    'question_text': foreq.question_text,
                    'pub_date': foreq.pub_date,
                    'id': foreq.id,
         }
         all_q.append(output)

    return JsonResponse(data=all_q, safe=False)

def questionsdump(request):
    s = serializers.serialize('json',Question.objects.all())
    return HttpResponse(json.dumps(s), content_type="application/json")

def listapreguntas(request):
    return render(request, 'polls/listapreguntas.html')

def add_question(request):
    if request.method == 'POST' and request.is_ajax():
        texto = request.POST.get('question_text')
        q = Question(question_text=texto, pub_date=timezone.now())
        q.save()
        output = {
                    'question_text': q.question_text,
                    'pub_date': q.pub_date,
                    'id': q.id,
        }
    return JsonResponse(data=output, safe=False)