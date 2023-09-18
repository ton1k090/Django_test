from django.db import models
from django.urls import reverse


class News(models.Model):
    """Модель для статей новостей"""
    title = models.CharField('Название', max_length=150)
    content = models.TextField('Контент', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обнавлено', auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.PROTECT,
                                 verbose_name='Категория',
                                 )
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        """Метод для создания ссылок"""
        return reverse('view_news', kwargs={'pk': self.pk})

    def __str__(self):
        """Метод возвращает строку"""
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Category(models.Model):
    """Модель категорий"""
    title = models.CharField('Название категории', max_length=150, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']