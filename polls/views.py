# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Poll, Page, Choice, Question
from django.views import generic
from .forms import PageForm
from django.http import Http404


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "polls_list"

    @staticmethod
    def get_queryset():
        """Return the last five published questions."""
        return Poll.objects.all()


def poll(request, poll_id):
    if request.session.get('current_poll', None) != poll_id:
        request.session.flush()
        current_poll = get_object_or_404(Poll, pk=poll_id)
        request.session['pages'] = [x.pk for x in current_poll.page_set.all()]
        if not request.session['pages']:
            raise Http404
        request.session['score'] = 0
        request.session['current_poll'] = poll_id
        request.session['max_deltas'] = []
        request.session['poll_score'] = sum([x.score
                                             for y
                                             in current_poll.page_set.all()
                                             for z
                                             in y.question_set.all()
                                             for x
                                             in z.choice_set.all()
                                             if x.score > 0])
    return page(request)


def page(request):
    page_list = request.session['pages']
    if request.method == 'POST':
        process_form(request, page_list[0])
        request.session['pages'] = page_list[1::]
    if not request.session['pages']:
        return calculate_score(request)
    else:
        form = PageForm(page_id=request.session['pages'][0])
        context = {'form': form, 'poll': poll}
        return render(request, 'polls/details.html', context)


def process_form(request, page_id):
    current_score = request.session['score']
    current_page = Page.objects.get(pk=page_id)
    questions = current_page.question_set.all()
    max_delta = 0, -1
    score = 0
    for question in questions:
        question_max_score = question.max_score()
        key = str(question.pk)
        question_answers = request.POST.getlist(key)
        if question_answers:
            for choice in question_answers:
                score += Choice.objects.get(pk=choice).score
        else:
            form = PageForm(page_id=page_id)
            context = {'form': form,
                       'poll': poll,
                       'error': "You must answer all questions"}
            return render(request, 'polls/details.html', context)

        request.session['score'] = current_score + score
        current_delta = question_max_score - score
        if current_delta > max_delta[0]:
            max_delta = current_delta, question.pk
        if max_delta[0] > 0:
            request.session['max_deltas'].append(max_delta[1])


def calculate_score(request):
    q_list = []
    for question in request.session['max_deltas']:
        q_list.append(Question.objects.get(pk=question))
    context = {'score': request.session['score'],
               'max_deltas': q_list,
               'poll_score': request.session['poll_score'],
               'percentage':
                   (request.session['score']*100) /
                   request.session['poll_score']}

    return render(request, 'polls/results.html', context)
