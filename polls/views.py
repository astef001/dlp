# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Question, Poll
from django.views import generic
from .forms import PageForm


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "polls_list"

    @staticmethod
    def get_queryset():
        """Return the last five published questions."""
        return Poll.objects.all()[:5]

def page(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if len(request.POST) > 1:
        var_dict = dict(request.POST.iterlists())
        questions = Question.objects.all()
        for question in questions:
            if var_dict.get(str(question.id)):
                for choice in question.choice_set.all():
                    if str(choice.id) in var_dict.get(str(question.id)):
                        try:
                            request.session['score'] = request.session['score'] + choice.score
                        except KeyError:
                            request.session['score'] = 0
    try:
        del request.session['pages'][0]
        page = request.session['pages'][0]
    except KeyError:
        request.session['pages'] = []
        for x in poll.page_set.all():
            request.session["pages"].append(x.id)
        page = request.session['pages'][0]
    except IndexError:
        score = request.session['score']
        del request.session['pages'], request.session['score']
        return render(request, 'polls/results.html', {'score': score})
    form = PageForm(poll=poll_id, page=page)
    return render(request, 'polls/details.html', {'form': form})


def vote(request):
    pass