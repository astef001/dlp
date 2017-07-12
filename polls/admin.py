# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *


class QuestionInline(admin.StackedInline):
    model = Question
    fields = ('question_text', '_link')
    readonly_fields = ('_link',)

    def _link(self, obj):
        if obj.id:
            link_pattern = u'<a ' \
                           u'href="/admin/polls/question/{0}/change">' \
                           u'{1}' \
                           u'</a>'
            return link_pattern.format(obj.pk, obj.question_text)
        return None

    _link.allow_tags = True


class PageInline(admin.options.TabularInline):
    model = Page
    fields = ('page_name', '_link')
    readonly_fields = ('_link', )

    def _link(self, obj):
        if obj.id:
            link_pattern = u'<a ' \
                           u'href="/admin/polls/page/{0}/change">' \
                           u'{1}' \
                           u'</a>'
            return link_pattern.format(obj.pk, obj.page_name)
        return None
    _link.allow_tags = True


class ChoiceInline(admin.options.TabularInline):
    model = Choice
    fields = ('choice_text', 'score', '_link')
    readonly_fields = ('_link', )

    def _link(self, obj):
        if obj.id:
            link_pattern = u'<a ' \
                           u'href="/admin/polls/choice/{0}/change">' \
                           u'{1}' \
                           u'</a>'
            return link_pattern.format(obj.pk, obj.choice_text)
        return None
    _link.allow_tags = True


class PollAdmin(admin.ModelAdmin):
    inlines = [PageInline]


class PageAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Poll, PollAdmin)
admin.site.register(Page, PageAdmin)
