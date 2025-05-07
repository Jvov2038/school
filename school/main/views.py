# Стандартные библиотеки
import csv
import logging
import os
import random
import uuid

# Сторонние библиотеки
import openai
from allauth.account.views import SignupView
from dal import autocomplete

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import (
    Http404, HttpResponse, HttpResponseNotFound,
    HttpResponseRedirect, JsonResponse
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.utils.formats import number_format
from django.db.models import Q
from django.db import IntegrityError
from django.db import transaction
from django.views.generic import (
    CreateView, DetailView, ListView, TemplateView
)

from dal import autocomplete

# Локальные импорты
from .forms import *
from .models import *
from .utils import *
from userprofile.models import District, School, SchoolClass, UserProfile, Location





from .forms import PersonalAreaForm
from .models import Documents, Lecture, Prog



def location_geojson(request):
    location_id = request.GET.get('id')
    if not location_id:
        return JsonResponse({"type": "FeatureCollection", "features": []})
    
    location = get_object_or_404(Location, id=location_id, lat__isnull=False, lon__isnull=False)
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [location.lon, location.lat],
        },
        "properties": {
            "popup": location.geomap_popup_view,
        }
    }

    return JsonResponse({"type": "FeatureCollection", "features": [feature]})


def contact_location_geojson(request, contact_id):
    try:
        contact = Contact.objects.get(id=1)
        location = contact.location
        if location and location.lat and location.lon:
            data = {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [location.lon, location.lat],
                    },
                    "properties": {
                        "popup": contact.name,
                    }
                }]
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"type": "FeatureCollection", "features": []})
    except Contact.DoesNotExist:
        return JsonResponse({"type": "FeatureCollection", "features": []})


def school_search(request):
    query = request.GET.get('query', '')
    if query:
        schools = School.objects.filter(name__icontains=query)  # Поиск по названию
        results = [{'name': school.name} for school in schools]
        return JsonResponse({'schools': results})
    else:
        return JsonResponse({'schools': []})
        



class SchoolAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return School.objects.none()

        qs = School.objects.all()

        if self.q:
            terms = self.q.split()
            for term in terms:
                qs = qs.filter(
                    Q(title__icontains=term) |
                    Q(location__name__icontains=term)  # ищем по названию местоположения
                )

        return qs



@csrf_exempt  # временно отключаем CSRF для простоты (в продакшене лучше использовать DRF)
def chat_api(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        
        bot_reply = response.choices[0].message["content"]
        return JsonResponse({"reply": bot_reply})
    
    return JsonResponse({"error": "Only POST requests are allowed"}, status=400)
    
    

@login_required
def complete_profile(request):
    # Получаем профиль пользователя или создаем его, если он не существует
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('personal_area')  # Перенаправляем в личный кабинет
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'school/complete_profile.html', {'form': form})


class CustomSignupView(SignupView):
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse('complete_profile'))


class SitemapXmlView(TemplateView):
    template_name = 'sitemapxml.html'
    content_type = 'application/xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all()
        context['programs'] = Prog.objects.all()
        context['docs'] = Documents.objects.all()
        context['lectures'] = Lecture.objects.all()
        return context
        

class Index(DataMixin, ListView):
    queryset = News.objects.order_by('-time_update')
    model = News
    template_name = 'school/index.html'
    context_object_name = 'news'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Образовательный центр")
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def post_carusel():
        post_carusel = News.objects.all()[:1]
        return post_carusel

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3

    @staticmethod
    def post_last6():
        post_last6 = News.objects.reverse()[:6]
        return post_last6

    @staticmethod
    def get_page_index():
        get_page_index = request.GET.get('page')
        return get_page_index

    @staticmethod
    def post_is_published():
        post_is_published = News.objects.all()
        return post_is_published

    @staticmethod
    def program_last6():
        program_last6 = Prog.objects.all()
        return program_last6


class ShowNews(DataMixin, DetailView):
    paginate_by = 1
    model = News
    template_name = 'school/news.html'
    slug_url_kwarg = 'news_slug'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['news'])
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3

    @staticmethod
    def post_last6():
        post_last6 = News.objects.reverse()[:6]
        return post_last6


class ShowDoc(DataMixin, DetailView):
    paginate_by = 1
    model = Documents
    template_name = 'school/doc-view.html'
    slug_url_kwarg = 'doc_slug'
    context_object_name = 'doc'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['doc'])
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3

    @staticmethod
    def post_last6():
        post_last6 = News.objects.reverse()[:6]
        return post_last6


class ShowProgram(DataMixin, DetailView):
    paginate_by = 1
    model = Prog
    template_name = 'school/program-view.html'
    slug_url_kwarg = 'program_slug'
    context_object_name = 'program'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['program'])
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3

    @staticmethod
    def post_last6():
        post_last6 = News.objects.reverse()[:6]
        return post_last6
        
        
class ShowLecture(DataMixin, DetailView):
    paginate_by = 1
    model = Lecture
    template_name = 'school/lecture-view.html'
    slug_url_kwarg = 'lecture_slug'
    context_object_name = 'lecture'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['lecture'])
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3

    @staticmethod
    def post_last6():
        post_last6 = News.objects.reverse()[:6]
        return post_last6
        

class About(DataMixin, ListView):
    queryset = News.objects.order_by('-time_update')
    model = News
    template_name = 'school/about.html'
    context_object_name = 'news'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О нас")
        return dict(list(context.items()) + list(c_def.items()))


    @staticmethod
    def docs_all_about():
        docs_all = Documents.objects.filter(section__id=1).order_by('-time_update')
        return  docs_all

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3

    @staticmethod
    def post_last6():
        post_last6 = News.objects.reverse()[:6]
        return post_last6

    @staticmethod
    def get_page_index():
        get_page_index = request.GET.get('page')
        return get_page_index

    @staticmethod
    def post_is_published():
        post_is_published = News.objects.all()
        return post_is_published

    @staticmethod
    def program_last6():
        program_last6 = Prog.objects.all()
        return program_last6

def add_user_to_prog(request, prog_id):
    prog = get_object_or_404(Prog, id=prog_id)
    prog.registration.add(request.user)
    return redirect('personal_area')


logger = logging.getLogger(__name__)

@login_required
def personal_area(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    # Получаем связанные объекты для текущего пользователя
    documents = Documents.objects.filter(executor=user)
    lectures = Lecture.objects.filter(prog__registration=user)  # Получаем лекции, где пользователь зарегистрирован
    programs = Prog.objects.filter(registration=user)  # Программы, в которых участвует пользователь

    if request.method == 'POST':
        form = PersonalAreaForm(
            data=request.POST,
            files=request.FILES,
            user=user,
            instance=user_profile
        )
        if form.is_valid():
            try:
                with transaction.atomic():
                    user.username = form.cleaned_data['username']
                    user.email = form.cleaned_data['email']
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.save()

                    profile = form.save(commit=False)
                    profile.user = user
                    profile.save()

                    messages.success(request, "Данные успешно обновлены.")
                    return redirect('personal_area')
            except IntegrityError as e:
                messages.error(request, "Ошибка: пользователь с таким именем уже существует.")
                logger.error(f"IntegrityError while saving profile: {e}")
            except Exception as e:
                messages.error(request, f"Произошла ошибка: {str(e)}")
                logger.error(f"Error saving profile: {e}")
    else:
        form = PersonalAreaForm(
            instance=user_profile,
            user=user,
            initial={
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        )

    return render(request, 'school/personal-area.html', {
        'form': form,
        'user_profile': user_profile,
        'documents': documents,
        'lectures': lectures,
        'programs': programs,
        'title': 'Личный кабинет',
    })


class Search(ListView):
    model = Documents
    template_name = 'school/search-results.html'
    context_object_name = 'docs'
    paginate_by = 5

    def get_queryset(self):
        search = self.request.GET.get('q')
        documents_all = Documents.objects.all()
        queryset = documents_all.filter(title__istartswith=search) | documents_all.filter(title__iregex=search)
        return queryset


class Vsosh_history(DataMixin, ListView):
    queryset = News.objects.order_by('-time_update')
    model = News
    template_name = 'school/vsosh-history.html'
    context_object_name = 'news'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="ВсОШ История")
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def post_carusel():
        post_carusel = News.objects.all()[:1]
        return post_carusel

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3

    @staticmethod
    def post_last6():
        post_last6 = News.objects.reverse()[:6]
        return post_last6

    @staticmethod
    def get_page_index():
        get_page_index = request.GET.get('page')
        return get_page_index

    @staticmethod
    def post_is_published():
        post_is_published = News.objects.all()
        return post_is_published

    @staticmethod
    def program_last6():
        program_last6 = Prog.objects.all()
        return program_last6
        
    @staticmethod
    def lecture_vsosh():
        lecture_vsosh = Lecture.objects.filter(title='Обращение к участникам олимпиады')
        return lecture_vsosh
        
    @staticmethod
    def brends_vsosh():
        brends_vsosh = News.objects.filter(title='Бренды ВсОШ')
        return brends_vsosh
        
    @staticmethod
    def docs_vsosh():
        docs_vsosh = Documents.objects.filter(title='Документы ВсОШ')
        return docs_vsosh
        

def Subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно подписались на рассылку!')
            return redirect('index')
    else:
        form = SubscriberForm()
    return render(request, 'school/index.html', {'form': form})        
    
    

def Unsubscribe(request):
    if request.method == 'POST':
        form = UnsubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                subscriber = Subscriber.objects.get(email=email, is_active=True)
                # Генерация уникального токена для отписки
                subscriber.unsubscribe_token = uuid.uuid4().hex
                subscriber.save()
                # Отправка письма с подтверждением
                unsubscribe_url = request.build_absolute_uri(
                    f"/unsubscribe/confirm/{subscriber.unsubscribe_token}/"
                )
                send_mail(
                    'Подтверждение отписки',
                    f'Для подтверждения отписки перейдите по ссылке: {unsubscribe_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'На ваш email отправлено письмо с подтверждением отписки.')
            except Subscriber.DoesNotExist:
                messages.error(request, 'Подписка с таким email не найдена.')
            return redirect('unsubscribe_request')
    else:
        form = UnsubscriberForm()
    return render(request, 'school/unsubscribe_form.html', {'form': form})  
    

def Unsubscribe_confirm(request, token):
    subscriber = get_object_or_404(Subscriber, unsubscribe_token=token, is_active=True)
    subscriber.is_active = False
    subscriber.unsubscribe_token = None  # Очищаем токен
    subscriber.save()
    messages.success(request, 'Вы успешно отписались от рассылки.')
    return render(request, 'school/unsubscribe_success.html')
    

class EducationalProgram(DataMixin, ListView):
    paginate_by = 100
    model = Prog
    template_name = 'school/educational_programs.html'
    context_object_name = 'program'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Образовательные программы')
        return dict(list(context.items()) + list(c_def.items()))
        
    @staticmethod
    def program_last6():
        program_last6 = Prog.objects.all()
        return program_last6    
        
        
class Intelligence(DataMixin, ListView):
    model = Documents
    template_name = 'school/intelligence.html'
    context_object_name = 'docs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Сведения об образовательной организации")
        return dict(list(context.items()) + list(c_def.items()))        
      
    @staticmethod
    def basic_information():
        basic_information = Documents.objects.filter(section__id=1)
        return basic_information   
        
    @staticmethod
    def structure_governing_bodies():
        structure_governing_bodies = Documents.objects.filter(section__id=2)
        return structure_governing_bodies      
        
    @staticmethod
    def constituent_documents():
        constituent_documents = Documents.objects.filter(section__id=3)
        return constituent_documents    
            
    @staticmethod
    def regulatory_legal_acts():
        regulatory_legal_acts = Documents.objects.filter(section__id=4)
        return regulatory_legal_acts   
        
    @staticmethod
    def local_acts():
        local_acts = Documents.objects.filter(section__id=5)
        return local_acts     
    
    @staticmethod
    def other_documents():
        other_documents = Documents.objects.filter(section__id=6)
        return other_documents 
    
    @staticmethod
    def archival_documents():
        archival_documents = Documents.objects.filter(section__id=7)
        return archival_documents 
    
    @staticmethod
    def educational():
        educational = Documents.objects.filter(section__id=8)
        return educational 
    
    @staticmethod
    def management():
        management = Documents.objects.filter(section__id=9)
        return management     
    
    @staticmethod
    def mto():
        mto = Documents.objects.filter(section__id=10)
        return mto
        
    @staticmethod
    def paid_services():
        paid_services = Documents.objects.filter(section__id=11)
        return paid_services
        
    @staticmethod
    def financial_activities():
        financial_activities  = Documents.objects.filter(section__id=12)
        return financial_activities 
        
    @staticmethod
    def vacancies():
        vacancies  = Documents.objects.filter(section__id=13)
        return vacancies 
        
    @staticmethod
    def accessible_environment():
        accessible_environment  = Documents.objects.filter(section__id=14)
        return accessible_environment 
        
    @staticmethod
    def international_cooperation():
        international_cooperation  = Documents.objects.filter(section__id=15)
        return international_cooperation 
        
    @staticmethod
    def background_intelligence():
        background_intelligence  = Documents.objects.filter(title="background_intelligence")
        return international_cooperation 
        
        
class Confidential_information(DataMixin, ListView):
    model = Documents
    template_name = 'school/confidential_information.html'
    context_object_name = 'docs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Политика конфиденциальности")
        return dict(list(context.items()) + list(c_def.items()))  
        
    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3
        
    @staticmethod
    def politic():
    	politic = Documents.objects.filter(section__id=20)
    	return politic
        

class GeneralInformation(DataMixin, ListView):
	model = Documents
	template_name = 'school/general_information.html'
	context_object_name = 'docs'
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title="Общая информация")
		return dict(list(context.items()) + list(c_def.items()))
	
	@staticmethod
	def general_information():
		general_information  = Documents.objects.filter(section__id=16)
		return general_information 
	
	@staticmethod
	def post_last3():
		post_last3 = News.objects.reverse()[:3]
		return post_last3
		
	
class Docs(DataMixin, ListView):
	model = Documents
	template_name = 'school/documents.html'
	context_object_name = 'docs'
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title="Документы")
		return dict(list(context.items()) + list(c_def.items()))
	
	@staticmethod
	def constituent_documents():
		constituent_documents = Documents.objects.filter(section__id=3)
		return constituent_documents    
            
	@staticmethod
	def regulatory_legal_acts():
		regulatory_legal_acts = Documents.objects.filter(section__id=4)
		return regulatory_legal_acts   
        
	@staticmethod
	def local_acts():
		local_acts = Documents.objects.filter(section__id=5)
		return local_acts     
    
	@staticmethod
	def other_documents():
		other_documents = Documents.objects.filter(section__id=6)
		return other_documents 
    
	@staticmethod
	def archival_documents():
		archival_documents = Documents.objects.filter(section__id=7)
		return archival_documents 
        
        
class Blog(DataMixin, ListView):
	queryset = News.objects.order_by('-time_update')
	model = News
	template_name = 'school/blog.html'
	context_object_name = 'news'
	paginate_by = 9
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title="Новости")
		return dict(list(context.items()) + list(c_def.items()))
	
	@staticmethod
	def all_news():
		all_news = News.objects.order_by('-time_update')
		return all_news    
            


class ContactsView(TemplateView):
    template_name = 'school/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_contact = Contact.objects.filter(is_main=True).select_related('location').first()
        context.update({
            'main_contact': main_contact,
            'contact_groups': ContactGroup.objects.prefetch_related('contacts').all(),
        })

        # Добавим координаты, если они есть
        if main_contact and main_contact.location:
            lat = main_contact.location.lat
            lon = main_contact.location.lon
            context['location_lat'] = f'{lat:.6f}'  # строка с точкой
            context['location_lon'] = f'{lon:.6f}'
            context['location_name'] = main_contact.name

        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact_id = request.POST.get('contact')

        if not all([name, email, message]):
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
            return self.get(request, *args, **kwargs)

        try:
            contact = Contact.objects.get(id=contact_id) if contact_id else None
        except Contact.DoesNotExist:
            contact = None

        ContactRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            contact=contact
        )

        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('contacts')

        
        
class Selection_criteria(DataMixin, ListView):
    model = Documents
    template_name = 'school/selection_criteria.html'
    context_object_name = 'docs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Критерии отбора")
        return dict(list(context.items()) + list(c_def.items()))


    @staticmethod
    def selection_criteria():
        selection_criteria = Documents.objects.filter(section__id=17)
        return selection_criteria

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3  


class Stay_rules(DataMixin, ListView):
    model = Documents
    template_name = 'school/stay_rules.html'
    context_object_name = 'docs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Правила пребывания")
        return dict(list(context.items()) + list(c_def.items()))


    @staticmethod
    def stay_rules():
        stay_rules = Documents.objects.filter(section__id=18)
        return stay_rules

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3


class Accommodation_conditions(DataMixin, ListView):
    model = Documents
    template_name = 'school/accommodation_conditions.html'
    context_object_name = 'docs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Условия размещения")
        return dict(list(context.items()) + list(c_def.items()))


    @staticmethod
    def accommodation_conditions():
        accommodation_conditions = Documents.objects.filter(section__id=19)
        return accommodation_conditions

    @staticmethod
    def post_last3():
        post_last3 = News.objects.reverse()[:3]
        return post_last3
