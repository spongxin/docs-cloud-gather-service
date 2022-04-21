from django.contrib.auth.models import User
from django.contrib.admin import display
from django.utils import timezone
from django.db import models
from uuid import uuid4


class Package(models.Model):
    unique = models.UUIDField(default=uuid4, db_index=True, editable=False, verbose_name="仓库标识码")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, verbose_name="发布人")
    title = models.CharField(max_length=20, verbose_name="标题", help_text="文档仓库显示的名称，将作为打包文件的默认名称")
    description = models.CharField(max_length=128, null=True, blank=True, verbose_name="描述(选填)", help_text="文档收集仓库的描述")
    items = models.JSONField(null=True, blank=True, editable=False, verbose_name="用户填写信息")
    formats = models.CharField(max_length=64, null=True, blank=True, verbose_name="重命名格式", help_text="将根据该格式重命名已收集文件，用户填写的信息将替换对应标签")
    deadline = models.BooleanField(default=False, verbose_name="设置截止时间", help_text="将在截止时间自动锁定仓库")
    date = models.DateField(null=True, blank=True, verbose_name="截止日期", help_text="选择`设置截止时间`后生效")
    time = models.TimeField(null=True, blank=True, verbose_name="截止时间", help_text="选择`设置截止时间`后生效")
    filesize = models.BooleanField(default=True, verbose_name="限制文件大小", help_text="限制单次提交文件的大小")
    size = models.IntegerField(default=64, verbose_name="最大文件大小", help_text="选择`限制文件大小`后生效")
    public = models.BooleanField(default=True, verbose_name="公开已提交信息", help_text="公开已收集到的信息清单(不包含文件下载权限)")
    locked = models.BooleanField(default=False, verbose_name="锁定状态", help_text="将禁止提交至该仓库")
    publish = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    @display(description="有效状态", )
    def inspect(self):
        if not self.locked and self.deadline and self.date and self.time:
            return (timezone.localdate() - self.date).seconds + (timezone.localtime().time() - self.time).seconds < 0
        return not self.locked

    class Meta:
        verbose_name_plural = "收集仓库列表"
        verbose_name = "收集仓库"
