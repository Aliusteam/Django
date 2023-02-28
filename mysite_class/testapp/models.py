from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

class Rubric(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # view_news - мы берем из urls.py - это: name='view_news'
        # news_id - мы берем из urls.py - это: 'news/<int:news_id>/
        # return reverse('view_news', kwargs={'news_id': self.pk})
        return reverse('rubric', kwargs={'pk': self.pk})

    class MPTTMeta:
        order_insertion_by = ['name']


class Article(models.Model):
    name = models.CharField(max_length=50)
    # category = models.ForeignKey(Rubric, on_delete=models.PROTECT)
    category = TreeForeignKey(Rubric, on_delete=models.PROTECT)

    def __str__(self):
        return self.name









