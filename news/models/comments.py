from django.db import models

from rayapp import settings


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', blank=True,
                             null=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    publication_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-publication_time',)
        indexes = [
            models.Index(fields=['text']),
        ]
