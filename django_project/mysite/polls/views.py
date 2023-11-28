from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from polls.models import Question, Choice
from django.urls import reverse
from django.http import HttpResponseRedirect
from polls.forms import NameForm
import logging

logger = logging.getLogger(__name__)
# Create your views here.

class IndexView(ListView):
    template_name = 'polls/index.html'
    model = Question

class DetailView(DetailView):
    template_name = 'polls/detail.html'
    model = Question

class ResultsView(DetailView):
    template_name = 'polls/results.html'
    model = Question

def vote(request, question_id):
    logger.debug(f"vote().question_id: {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoseNotExist):
        return render(request, 'polls/detail.html',{'question': question,
                                                    'error_message': "You didn't select a choice",})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


def name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            new_name = form.cleaned_data['name']
            return HttpResponseRedirect('')
    else:
        form = NameForm()
    return render(request, 'polls/name.html', {'form': form})
