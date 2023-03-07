from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class HomeMenu(MPTTModel):
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT,  null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_id', kwargs={'pk': self.pk})

    class MPTTMeta:
        order_insertion_by = ['name']


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)
    items = models.ManyToManyField(HomeMenu)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name
