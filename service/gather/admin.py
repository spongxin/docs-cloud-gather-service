from django.contrib import admin
# from django.utils.html import format_html
from .models import *


class PackageAdmin(admin.ModelAdmin):
    list_display = ['unique', 'owner', 'title', 'description', 'deadline', 'locked', 'publish']
    list_filter = ['owner', 'locked']
    search_fields = ['owner', 'title']

    def has_add_permission(self, *args, **kwargs):
        return False


admin.site.site_header = '文档收集服务'
admin.site.site_title = '文档收集服务管理'
admin.site.register(Package, PackageAdmin)
