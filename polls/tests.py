# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from polls.models import Poll, Question, Page, Choice
from django.core.urlresolvers import reverse
from polls.forms import PageForm
# Create your tests here.


class SimpleTest(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(name='test',
                            description='test_description')
        self.page = Page.objects.create(page_name='first_test_page',
                                        poll=self.poll)
        self.Question = Question.objects.create(question_text="First test question?",
                                                page=self.page)
        self.Choice1 = Choice.objects.create(choice_text="First Choice", score=1,
                                             question=self.Question)
        self.Choice2 = Choice.objects.create(choice_text="Second Choice", score=1,
                                             question=self.Question)

    def test_index(self):
        url = reverse('polls:index')
        response = self.client.get(url)
        poll_list = list(response.context['polls_list'])
        self.assertEqual([self.poll],poll_list)

    def test_page(self):
        url = reverse('polls:page', kwargs={'poll_id': self.poll.pk, })
        response = self.client.get(url)
        form = response.context['form']
        page_form = PageForm(page_id=self.page.pk)
        self.assertEqual(form.as_table(),page_form.as_table())