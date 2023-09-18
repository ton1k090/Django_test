from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from .models import News, Category
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


def register(request):
    """Функция для регистрации пользователей"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()     # Сохранение данных
            login(request, user)
            messages.success(request, 'Успешно!')     # Вывод сообщения на экран
            return redirect('home')
        else:
            messages.error(request, 'Ошибка!')
    else:
        form = UserRegisterForm()     # Вернет исходную форму
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    """Функция для аунтификации и авторизации"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    """Функция для выхода из аккаунта"""
    logout(request)
    return redirect('login')

"""Представления на основе классов"""


class HomeNews(MyMixin, ListView):
    """Класс для вывода новостей в шаблон"""
    model = News     # Имя используемой модели
    template_name = 'news/home_news_list.html'       # Название используемого шаблона
    context_object_name = 'news'     # Переопределяет имя для использования в шаблоне
    # extra_context = {'title': 'Главная'}
    # queryset = News.objects.select_related('category') - Оптимизирует sql запросы связанных моделей(ForeignKey)
    mixin_prop = 'hello world'     # Атрибут из миксина
    paginate_by = 4

    def get_context_data(self, **kwargs):     # Контекст для исрользования в шаблоне
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')     # Вывод через метод миксина
        context['mixin_prop'] = self.get_prop()     # Метод из класса миксина
        return context

    def get_queryset(self):     # Из какой модели и как взять данные
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    """Класс для вывода категорий"""
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False # Показывать пустые
    paginate_by = 4

    def get_queryset(self):

        """Метод для работы с моделью"""

        return News.objects.filter(
            category_id=self.kwargs['category_id'],
            is_published=True,
        ).select_related('category')

    def get_context_data(self, **kwargs):
        """Контекст вывода данных в шаблон"""
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))  # Вызов метода для queryset
        return context


class ViewNews(DetailView):
    """Класс для просмотра записи отдельно"""
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    """Класс для создания записи"""
    form_class = NewsForm     # Класс используемой формы
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('home')     # Редирект на страницу
    login_url = '/admin/'  # Редирект при срабатывании миксина


"""Представления на основе функций"""

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news,
#                                                   'category': category})


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})


