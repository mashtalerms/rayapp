from django.db import models

from rayapp import settings


class News(models.Model):
    sources = (
        ('mediametrics', 'mediametrics'),
        ('vk', 'vk'),
        ('users', 'users'),
    )
    publication_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Дата публикации')
    title = models.TextField(blank=True, verbose_name='Текст новости')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', blank=True,
                             null=True)
    url = models.TextField(verbose_name='Ссылка', blank=True)
    source = models.CharField(choices=sources, max_length=50, verbose_name='Источник', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-publication_time',)
        indexes = [
            models.Index(fields=['publication_time']),
            models.Index(fields=['user']),
            models.Index(fields=['title']),
            models.Index(fields=['url']),
            models.Index(fields=['source']),
        ]
