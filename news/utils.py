class MyMixin(object):
    """Класс миксин расширяет функционал представлений"""
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()

    def get_upper(self, s):
        """Метод для работы со строкой и queryset"""
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()