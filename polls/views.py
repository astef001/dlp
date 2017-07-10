# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Poll, Page, Choice, Question
from django.views import generic
from .forms import PageForm


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "polls_list"

    @staticmethod
    def get_queryset():
        """Return the last five published questions."""
        return Poll.objects.all()


def page(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        page_list = request.session['pages']
        current_score = request.session['score']
    except KeyError:
        page_list = []
        for x in poll.page_set.all():
            page_list.append(x.pk)
        current_score = 0
    print(page_list)
    current_page = Page.objects.get(pk=page_list[0])
    questions = current_page.question_set.all()
    max_delta = 0, -1

    if request.method == 'POST':
        for question in questions:
            score = 0
            question_max_score = question.max_score()
            key = str(question.pk)
            question_answers = request.POST.getlist(key)
            try:
                for choice in question_answers:
                    score += Choice.objects.get(pk=choice).score
            except TypeError:
                form = PageForm(page_id=page_list[0])
                return render(request, 'polls/details.html', {'form': form, 'poll': poll, 'error': "You must answer all questions"})
            current_score += score
            current_delta = question_max_score - score
            if current_delta > max_delta[0]:
                max_delta = current_delta, question.pk

        try:
            if max_delta[0] > 0:
                request.session['max_deltas'].append(max_delta[1])
        except KeyError:
            request.session['max_deltas'] = [max_delta[1]]

        request.session['score'] = current_score
        del page_list[0]
        request.session['pages'] = page_list
    if not page_list:
        q_list = []
        try:
            for question in request.session['max_deltas']:
                q_list.append(Question.objects.get(pk=question))
        except KeyError:
            pass
        request.session.flush()
        return render(request, 'polls/results.html', {'score': current_score, 'max_deltas': q_list})
        pass
    else:
        form = PageForm(page_id=page_list[0])
    return render(request, 'polls/details.html', {'form': form, 'poll': poll})


def vote(request):
    pass