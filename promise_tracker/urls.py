
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

# user login patters
urlpatterns = [
    # path("", views.index, name="index"),
    path('', views.PromiseListView.as_view(), name='index'),
    path('promise/create/', views.PromiseCreateView.as_view(), name='promise_create'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # positions
    # path('', views.PositionListView.as_view(), name='all'),
    path('positions/',
         views.PositionListView.as_view(), name='positions'),
    path('positions/<int:pk>/detail',
         views.PositionDetailView.as_view(), name='position_detail'),
    path('positions/create/', views.PositionCreateView.as_view(),
         name='position_create'),
    path('positions/<int:pk>/update/',
         views.PositionUpdateView.as_view(), name='position_update'),
    path('positions/<int:pk>/delete/',
         views.PositionDeleteView.as_view(), name='position_delete'),
     #parties
     path('parties/',
         views.PartyListView.as_view(), name='parties'),
    path('parties/<int:pk>/detail',
         views.PartyDetailView.as_view(), name='party_detail'),
    path('parties/create/', views.PartyCreateView.as_view(),
         name='party_create'),
    path('parties/<int:pk>/update/',
         views.PartyUpdateView.as_view(), name='party_update'),
    path('parties/<int:pk>/delete/',
         views.PartyDeleteView.as_view(), name='party_delete'),
     #politician    
     path('politicians/',
         views.PoliticianListView.as_view(), name='politicians'),
    path('politicians/<int:pk>/detail',
         views.PoliticianDetailView.as_view(), name='politician_detail'),
    path('politicians/create/', views.PoliticianCreateView.as_view(),
         name='politician_create'),
    path('politicians/<int:pk>/update/',
         views.PoliticianUpdateView.as_view(), name='politician_update'),
    path('politicians/<int:pk>/delete/',
         views.PoliticianDeleteView.as_view(), name='politician_delete'),     
]+ static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
