from django.utils.html import format_html
from django.contrib import admin
from .models import *


class AccessAdmin(admin.ModelAdmin):
    list_display = ['id', 'access', 'secret', 'publish']


class BucketAdmin(admin.ModelAdmin):
    list_display = ['name', 'private', 'domain']
    search_fields = ['name', ]


class TokenAdmin(admin.ModelAdmin):
    list_display = ['bucket', 'filename', 'expired', 'copy_token', 'inspect', 'publish']
    list_filter = ['bucket__name', ]
    search_fields = ['bucket', 'filename']

    def copy_token(self, obj):
        return format_html(f"""
        <a onclick="document.getElementById('{obj.id}').select();document.execCommand('copy');alert('已复制')"><b>点击复制</b></a>
        <input type="text" id="{obj.id}" value="{obj.token}" style="opacity:0;max-width:1px;">
        """)
    copy_token.short_description = '鉴权值'


admin.site.register(Access, AccessAdmin)
admin.site.register(Bucket, BucketAdmin)
admin.site.register(Token, TokenAdmin)
