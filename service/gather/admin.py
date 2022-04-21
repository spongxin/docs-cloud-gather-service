from django.contrib import admin
from .models import *


class PackageAdmin(admin.ModelAdmin):
    list_display = ['unique', 'owner', 'title', 'description', 'deadline', 'inspect', 'publish']
    list_filter = ['owner__username', 'locked']
    search_fields = ['title', ]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


admin.site.site_header = '系统控制台'
admin.site.site_title = '中控服务管理系统'
admin.site.register(Package, PackageAdmin)
