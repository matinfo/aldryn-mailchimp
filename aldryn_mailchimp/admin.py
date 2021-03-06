# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _

from adminsortable.admin import SortableAdmin, SortableTabularInline

from .models import Campaign, Category, Keyword


class KeywordInline(SortableTabularInline):
    model = Keyword
    extra = 0


class CategoryAdmin(SortableAdmin):
    inlines = (KeywordInline, )


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('mc_title', 'display_name', 'list_name',
                    'list_id', 'send_time', 'hidden', 'category')
    search_fields = ('cid', 'subject', 'mc_title', 'list_name',
                     'list_id', 'display_name')
    list_filter = ('hidden', 'category')
    list_editable = ('hidden', )
    readonly_fields = ('cid', 'mc_title', 'subject', 'send_time',
                       'content_html', 'content_text', 'slug',
                       'list_name', 'list_id',)
    actions = ['fetch_campaigns']

    _fieldsets = (
        (_('MailChimp Info'), {
            'fields': (
                'cid', 'mc_title', 'subject',
                'send_time',
                ('list_name', 'list_id'),
            )}),
        (_('Visibility & Classification'), {
            'fields': (
                ('display_name', 'category'),
                'hidden',
            )}),
        (_('Content'), {
            'classes': ('collapse', ),
            'fields': (
                'content_text', 'content_html',
            )}),
    )

    def get_fieldsets(self, request, obj=None):
        return self._fieldsets

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def fetch_campaigns(self, request, queryset):
        call_command('fetch_campaigns')
    fetch_campaigns.short_description = "Fetch campaigns from Mailchimp"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Campaign, CampaignAdmin)
