from django.urls import include, path
from . import views
from .views import UserView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers


app_name = 'quizapp'

router = routers.DefaultRouter()
router.register('Users',UserView)

urlpatterns = [
    path('',views.home, name = 'home'),
    path('signup/',views.signup, name = 'signup'),
    path('signin/',views.signin, name = 'signin'),
    path('logout/',views.logout, name = 'logout'),
    path('search/',views.search, name = 'search'),
    path('quiz/', views.quiz, name= 'quiz'),
    path('api/get-quiz/', views.get_quiz, name='get_quiz'),
    path('api/v1/',include(router.urls))
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)