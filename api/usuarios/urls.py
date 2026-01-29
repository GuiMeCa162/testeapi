from django.urls import path
from . import views

usuario_create = views.UsuarioViewSet.as_view({'post': 'create'})
usuario_list = views.UsuarioViewSet.as_view({'get': 'list'})
usuario_detail = views.UsuarioViewSet.as_view(
    {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}
    )
usuario_me = views.UsuarioViewSet.as_view({'get': 'me'})

urlpatterns = [
    path('create/', usuario_create, name='usuario-create'),
    path('list/', usuario_list, name='usuario-list'),
    path('detail/<int:pk>/', usuario_detail, name='usuario-detail'),
    path('me/', usuario_me, name='usuario-me'),
    path('login/', views.LoginView().as_view(), name='user-login'),
    path('logout/', views.LogoutView().as_view(), name='user-logout'),
    path('refresh/', views.CookieTokenRefreshView.as_view(), name='token-refresh')
]