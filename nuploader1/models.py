from django.db import models


class Composite(models.Model):
    name = models.CharField('名前', max_length=255)
    is_dir = models.BooleanField('ディレクトリか', default=True)
    src = models.FileField('ファイルソース', blank=True, null=True)
    parent = models.ForeignKey(
        'self', verbose_name='親ディレクトリ', on_delete=models.CASCADE,
        blank=True, null=True, limit_choices_to={'is_dir': True}
    )
    zip_depth = models.PositiveIntegerField('zipファイルの深さ', default=0)

    class Meta:
        ordering = ('-is_dir', 'name')

    def __str__(self):
        if self.is_dir:
            return f'{self.pk} - {self.name}/'
        else:
            return f'{self.pk} - {self.name}'

    def get_display_name(self):
        if self.is_dir:
            return f'{self.name}/'
        else:
            return f'{self.name}'
