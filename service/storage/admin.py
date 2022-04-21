from django.utils.html import format_html
from django.contrib import admin
from .models import *


class AccessAdmin(admin.ModelAdmin):
    list_display = ['id', 'access', 'secret', 'publish']


class BucketAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'private', 'domain']
    search_fields = ['name', ]


class UploadTokenAdmin(admin.ModelAdmin):
    list_display = ['bucket', 'filename', 'expired', 'copy_token', 'inspect', 'publish']
    list_filter = ['bucket__name', ]
    search_fields = ['filename', ]

    def copy_token(self, obj):
        return format_html(f"""
        <a onclick="document.getElementById('{obj.id}').select();document.execCommand('copy');alert('已复制')"><b>点击复制</b></a>
        <input type="text" id="{obj.id}" value="{obj.token}" style="opacity:0;max-width:1px;">
        """)
    copy_token.short_description = '鉴权值'


class ResourceAdmin(admin.ModelAdmin):
    list_display = ['bucket', 'filename', 'to_url', 'unique', 'publish']
    list_filter = ['bucket__name', ]
    search_fields = ['filename', ]

    def to_url(self, obj):
        return format_html(f"""<a href="{obj.url}"><b>下载文件</b></a>""")
    to_url.short_description = '文件链接'


admin.site.register(Access, AccessAdmin)
admin.site.register(Bucket, BucketAdmin)
admin.site.register(UploadToken, UploadTokenAdmin)
admin.site.register(Resource, ResourceAdmin)
