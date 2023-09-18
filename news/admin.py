from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import News, Category
from django import forms


class NewsAdminForm(forms.ModelForm):
    """Форма расширяет поле контент"""
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    """Класс админ панели для модели новостей"""
    form = NewsAdminForm
    list_display = (
        'id',
        'title',
        'created_at',
        'updated_at',
        'is_published',
        'category',
        'get_photo')
    list_display_links = ('id', 'title')           #поля ссылки
    search_fields = ('title', 'content')           #Поиск по полям
    list_editable = ('is_published',)              #Редактировать на месте
    list_filter = ('is_published', 'category')     #Фильтр статей
    fields = (                                     #Поля отображаемые внутри редактора статей
        'title',
        'category',
        'content',
        'photo',
        'get_photo',
        'is_published',
        'views',
        'created_at',
        'updated_at',
        )
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at')     # Поля только для чтения

    def get_photo(self, obj):     # Вывод картинки в список таблиц новостей
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return f'Фото не установлено'

    get_photo.short_description = 'Миниатюра'     #Как будет выглядеть название метода в админгке


class CategoryAdmin(admin.ModelAdmin):
    """Класс для админ панели модели категорий"""
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
