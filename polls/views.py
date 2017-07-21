# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Page, Choice, Question
from django.views import generic,View
from django.views.generic.base import TemplateView
from .forms import PageForm
from django.http import Http404


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "polls_list"

    @staticmethod
    def get_queryset():
        return Poll.objects.all()


class PageView(View):
    def dispatch(self, request, *args, **kwargs):
        poll_id = kwargs.pop("poll_id")
        print(request.session['pages'])
        if not request.session["pages"]:
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
        return super(PageView, self).dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        poll_id=self.request.session['current_poll']
        process_form(self.request, self.request.session['pages'][0])
        self.request.session['pages'] = self.request.session['pages'][1::]
        if not self.request.session['pages']:
            return redirect('polls:score', poll_id=poll_id)
        return self.get(self.request, poll_id=self.request.session['current_poll'])

    def get(self, *args, **kwargs):
        form = PageForm(page_id=self.request.session['pages'][0])
        context = {'form': form, 'poll': self.request.session['current_poll']}
        return render(self.request, 'polls/details.html', context)


class ResultsView(TemplateView):
    template_name = 'polls/results.html'
    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ResultsView, self).get_context_data(**kwargs)
        context.update({'score': request.session['score'],
                   'max_deltas': [Question.objects.get(pk=x)
                                  for x in request.session['max_deltas']],
                   'poll_score': request.session['poll_score'],
                   'percentage':
                       (request.session['score'] * 100) /
                       request.session['poll_score']})
        return context

def render_page_error(request, page_id):
    form = PageForm(page_id=page_id)
    context = {'form': form,
               'poll': request.session['current_poll'],
               'error': "You must answer all questions"}
    return render(request, 'polls/details.html', context)

def process_form(request, page_id):
    current_score = request.session['score']
    current_page = Page.objects.get(pk=page_id)
    questions = current_page.question_set.all()
    max_delta = 0, -1
    for question in questions:
        question_max_score = question.max_score()
        score = calculate_score(request, question)
        if not score:
            return render_page_error(request,page_id)
        request.session['score'] = current_score + score
        current_delta = question_max_score - score
        max_delta = calculate_delta(current_delta, max_delta, question.pk)
    if max_delta[0] > 0:
        request.session['max_deltas'].append(max_delta[1])

def calculate_score(request, question):
    score = 0
    key = str(question.pk)
    question_answers = request.POST.getlist(key)
    if question_answers:
        for choice in question_answers:
            score += Choice.objects.get(pk=choice).score
    return score if score else None

def calculate_delta(current_delta, max_delta, question):
    if current_delta > max_delta[0]:
        return current_delta, question
    return max_delta
