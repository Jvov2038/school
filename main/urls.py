from django.urls import path, re_path
from .views import CustomSignupView
from django.views.decorators.csrf import csrf_exempt
from .views import *
from .views import SchoolAutocomplete


urlpatterns = [
                path('', Index.as_view(), name='index'),
                path('news/<slug:news_slug>/', ShowNews.as_view(), name='news'),
                path('doc/<slug:doc_slug>/', ShowDoc.as_view(), name='doc'),
                path('program/<slug:program_slug>/', ShowProgram.as_view(), name='program'),
                path('lecture/<slug:lecture_slug>/', ShowLecture.as_view(), name='lecture'),
                path('prog/<int:prog_id>/add_user/', add_user_to_prog, name='add_user_to_prog'),
                path('about/', About.as_view(), name='about'),
                path('personal_area/', personal_area, name='personal_area'),
                path('search/', Search.as_view(), name='search'),
                path('vsosh_history', Vsosh_history.as_view(), name='vsosh_history'),
                path("sitemapxml.html", SitemapXmlView.as_view()),
                path('subscribe/', Subscribe, name='subscribe'),
                path('unsubscribe/', Unsubscribe, name='unsubscribe_request'),
    			path('unsubscribe/confirm/<str:token>/', Unsubscribe_confirm, name='unsubscribe_confirm'),
    			path('complete_profile/', complete_profile, name='complete_profile'),
    			path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    			path('educational_programs/', EducationalProgram.as_view(), name='educational_programs'),
    			path('intelligence/', Intelligence.as_view(), name='intelligence'),
    			path('confidential_information/', Confidential_information.as_view(), name='confidential_information'),
    			path('general_information/', GeneralInformation.as_view(), name='general_information'),
    			path('documents/', Docs.as_view(), name='documents'),
    			path('blog/', Blog.as_view(), name='blog'),
    			path('api/chat/', chat_api, name='chat_api'),
    			path('contacts/', ContactsView.as_view(), name='contacts'),
    			path('selection_criteria/', Selection_criteria.as_view(), name='selection_criteria'),
    			path('stay_rules/', Stay_rules.as_view(), name='stay_rules'),
    			path('accommodation_conditions/', Accommodation_conditions.as_view(), name='accommodation_conditions'),
    			path("school-autocomplete/", SchoolAutocomplete.as_view(), name="school-autocomplete"),
    			path('search/', school_search, name='school_search'),

    ]