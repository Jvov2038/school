from django.db.models import Count

from .models import *

menu = [
    {'title': "О центре", 'url_name': 'info',
     'submenu': [{'title': 'Сведения об образовательной организации', 'url_name': 'intelligence'},
                 {'title': 'Общая информация', 'url_name': 'info'},
                 #                 {'title': 'Попечительский совет', 'url_name': 'p_advice'},
                 #                 {'title': 'Экспертный совет', 'url_name': 'e_advice'},
                 {'title': "Документы", 'url_name': 'docs'},
                 {'title': 'Новости', 'url_name': 'news'},
                 {'title': 'Контакты', 'url_name': 'contacts'},
                 {'title': 'Политика конфиденциальности', 'url_name': 'conf'},
                 ]},
    {'title': 'Как попасть', 'url_name': 'selection_criteria',
     'submenu': [{'title': 'Критерии отбора', 'url_name': 'selection_criteria'},
                 {'title': 'Правила пребывания', 'url_name': 'stay_rules'},
                 {'title': 'Условия размещения', 'url_name': 'accommodation_conditions'},
                 {'title': 'Памятка для родителей', 'url_name': 'memo_for_parents'},
                 {'title': 'Необходимые документы', 'url_name': 'required_docs'},
                 {'title': 'Часто задаваемые вопросы', 'url_name': 'FAQ'},
                 {'title': 'Лекториум', 'url_name': 'lecture_hall'}
                 ]},
    {'title': "Мероприятия", 'url_name': 'big_challengers',
     'submenu': [{'title': 'Большие вызовы', 'url_name': 'big_challengers'},
                 {'title': 'Сириус лето', 'url_name': 'sirius_leto'},
                 ]},
    {'title': 'Программы', 'url_name': 'educational_programs'},
    {'title': 'ВсОШ', 'url_name': 'vsosh'}]

menu_center = [
    {'title': "О модельном центре", 'url_name': 'info_cms',
     'submenu': [{'title': 'Общая информация', 'url_name': 'info_cms'},
                 {'title': "Нормативные документы РМЦ", 'url_name': 'docs_rmc'},
                 {'title': 'Методические материалы', 'url_name': 'methodological_materials'},
                 {'title': 'Банк лучших практик', 'url_name': 'bank_best_practic'},
                 ]},
    {'title': "Мероприятия", 'url_name': 'big_challengers',
     'submenu': [{'title': 'Шаг в будущее', 'url_name': 'step_into_the_future'},
                 {'title': 'Шаг в будущее Осетии', 'url_name': 'step_to_the_future_rso'},
                 {'title': 'Открытия 2030', 'url_name': 'discoveries_2030'},
                 ]},
    {'title': 'Контакты', 'url_name': 'contacts_cms'}]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = CategoryNews.objects.all()

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

