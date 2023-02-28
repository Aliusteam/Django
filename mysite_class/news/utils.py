class MyMixin(object):
    # mixin_prop - это свойство мы можем переопределять
    mixin_prop = ''

    def get_prop(self):
        # Переведем строку во верхний регистр
        return self.mixin_prop.upper()

    # Или тоже самое
    def get_upper(self, s):
        # Если S это строка
        if isinstance(s, str):
            return s.upper()
        else: # Если это обьект
            return s.title.upper()
