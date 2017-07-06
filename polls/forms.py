from django import forms
from .models import Poll, Page, Choice
class PageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        page = kwargs.pop('page')
        poll = kwargs.pop('poll')
        super(forms.Form, self).__init__(*args, **kwargs)
        poll=Poll.objects.get(pk=poll)
        page=poll.page_set.get(pk=page)
        questions=page.question_set.all()
        choice_list=[]
        for question in questions:
            choices = question.choice_set.all()
            for choice in choices:
                choice_list.append((choice.pk, choice.choice_text))
            self.fields['%s' % question.pk] = forms.MultipleChoiceField(label=question.question_text, choices=choice_list, widget=forms.CheckboxSelectMultiple)