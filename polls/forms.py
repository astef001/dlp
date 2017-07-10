from django import forms
from .models import Page


class PageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        page = kwargs.pop('page_id')
        super(forms.Form, self).__init__(*args, **kwargs)
        page = Page.objects.get(pk=page)
        questions = page.question_set.all()

        for question in questions:
            choice_list = []
            choices = question.choice_set.all()
            for choice in choices:
                choice_list.append((choice.id, choice.choice_text))
            self.fields['%s' % question.pk] = forms.MultipleChoiceField(label=question.question_text,
                                                                        choices=choice_list,
                                                                        widget=forms.CheckboxSelectMultiple)


