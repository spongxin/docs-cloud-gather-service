from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save
from django.contrib.admin import display
from django.utils import timezone
from django.db import models
from qiniu import Auth


class Access(models.Model):
    access = models.CharField(max_length=128, unique=True, verbose_name="名称")
    secret = models.CharField(max_length=128, verbose_name="密钥")
    publish = models.DateTimeField(auto_now=True, verbose_name="提交时间")

    def __str__(self):
        return '密钥%d' % self.id

    class Meta:
        verbose_name_plural = "密钥列表"
        verbose_name = "密钥"
        ordering = ['id']


class Bucket(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="名称")
    private = models.BooleanField(default=False, verbose_name="私有仓库")
    domain = models.CharField(max_length=128, blank=True, null=True, verbose_name="源站域名")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "存储列表"
        verbose_name = "存储空间"


class Token(models.Model):
    access = models.ForeignKey(Access, on_delete=models.CASCADE, verbose_name="密钥")
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, verbose_name="存储空间")
    filename = models.CharField(max_length=128, verbose_name="文件名")
    expired = models.IntegerField(default=3600, verbose_name="过期时间")
    token = models.CharField(max_length=256, editable=False, null=True, blank=True, verbose_name="鉴权值")
    publish = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    @display(description="有效", )
    def inspect(self):
        return (timezone.localtime() - self.publish).seconds < self.expired

    class Meta:
        verbose_name_plural = "鉴权列表"
        verbose_name = "鉴权对象"


@receiver(pre_save, sender=Token)
def generate(instance, *_args, **_kwargs):
    instance.token = Auth(
        instance.access.access,
        instance.access.secret
    ).upload_token(instance.bucket.name, instance.filename, instance.expired)