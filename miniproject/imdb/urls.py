from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('home/',views.index,name='index_home'),
    path('movie/<slug:movie_id>/',views.movie,name='movie'),
    path('actor/<slug:actor_id>/',views.actor,name='actor'),
    path('director/<int:director_id>/',views.director,name='director'),
    path('analytics/',views.analytics,name='analytics'),
]