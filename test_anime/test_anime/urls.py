"""test_anime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static


from search_anime import views
from search_anime.views import AnimeView, RandomAnime

from higher_or_lower import views as holv
from recommandations import views as recov

router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('list', AnimeView, basename='list')
router.register('random', RandomAnime, basename='random')
router.register('hol_n', holv.GetNewAnime, basename="new_pick")
router.register('get_recom', recov.GetRecommandations, basename="get_recom")
urlpatterns = [
    path('admin/', admin.site.urls),
    path("list/", views.BaseView),
    path("search/", views.SearchView),
    path("anime/<int:id>/", views.AnimeDetail),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),  # Il faut bien penser à ajouter les urls du router dans la liste des urls disponibles.


    path("hol/", holv.Index, name='higher_or_lower'),
    path("hol/game", holv.Game, name="hol_game"),

    path("recom/", recov.BaseView),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

