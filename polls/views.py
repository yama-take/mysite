"""
    Django polls application views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):  # pylint:disable=too-many-ancestors
    """"
    Class IndexView will use generic ListView in index.html file
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView): # pylint:disable=too-many-ancestors
    """
    Class DetailView will use generic DetailView in detail.html
    """
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView): # pylint:disable=too-many-ancestors
    """
    Class ResultView will use generic DetailView in results.html
    """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """
    Vote method increments the value of votes for the respective choice
    :param request:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html',
                      {'question': question, 'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after the voting
        # This prevents data to be posted twice if user presses Back
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
