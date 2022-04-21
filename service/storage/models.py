from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.contrib.admin import display
from qiniu import Auth, BucketManager
from django.utils import timezone
from django.db import models
from uuid import uuid4


class Access(models.Model):
    access = models.CharField(max_length=128, unique=True, verbose_name="名称")
    secret = models.CharField(max_length=128, verbose_name="密钥")
    publish = models.DateTimeField(auto_now=True, verbose_name="提交时间")

    @property
    def auth(self):
        self._auth = Auth(self.access, self.secret)
        return self._auth

    def __str__(self):
        return '密钥%d' % self.id

    class Meta:
        verbose_name_plural = "密钥列表"
        verbose_name = "密钥"
        ordering = ['id']


class Bucket(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="名称")
    private = models.BooleanField(default=False, verbose_name="私有仓库")
    domain = models.CharField(max_length=128, verbose_name="源站域名")
    access = models.ForeignKey(Access, on_delete=models.CASCADE, verbose_name="归属密钥")

    @property
    def manager(self):
        self._manager = BucketManager(self.access.auth)
        return self._manager

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "存储仓库"
        verbose_name = "存储空间"


class UploadToken(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, verbose_name="存储空间")
    filename = models.CharField(max_length=128, verbose_name="文件名")
    expired = models.IntegerField(default=3600, verbose_name="过期时间")
    token = models.CharField(max_length=256, editable=False, null=True, blank=True, verbose_name="鉴权值")
    publish = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    @display(description="有效状态", )
    def inspect(self):
        return (timezone.localtime() - self.publish).seconds < self.expired

    def __str__(self):
        return "鉴权%d(%s)" % (self.id, self.inspect().__str__())

    class Meta:
        verbose_name_plural = "上传鉴权"
        verbose_name = "上传鉴权"


class Resource(models.Model):
    unique = models.UUIDField(default=uuid4, db_index=True, editable=False, verbose_name="文件标识码")
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, verbose_name="存储空间")
    filename = models.CharField(max_length=128, verbose_name="文件名")
    publish = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")

    @property
    def url(self):
        return f"{self.bucket.domain}/{self.filename}"

    def __str__(self):
        return f"{self.bucket.name}:{self.filename}"

    class Meta:
        verbose_name_plural = "文件列表"
        verbose_name = "云端文件"


@receiver(pre_save, sender=UploadToken)
def generate(instance, *_args, **_kwargs):
    instance.token = instance.bucket.access.auth.upload_token(instance.bucket.name, instance.filename, instance.expired)


@receiver(pre_delete, sender=Resource)
def delete(instance, *_args, **_kwargs):
    instance.bucket.manager.delete(instance.bucket.name, instance.filename)
