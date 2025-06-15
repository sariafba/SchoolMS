from django.urls import path, include
from .views import CooperatorView, RoleView, CooperatorListCreateView, CooperatorRetrieveUpdateDestroyView, RoleViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('roles', RoleViewSet, basename='role')  # Uses ViewSet for list + retrieve
urlpatterns = [

    # dj_rest_auth
    path('auth/', include('dj_rest_auth.urls')),

    # Cooperator
    # path('cooperators/', Cooperator.as_view()),         # GET all, POST
    # path('cooperators/<int:pk>', Cooperator.as_view()), # GET one, PUT, DELETE

    # Role
    # path('roles/', Role.as_view()),
    # path('roles/<int:pk>', Role.as_view()),
    path('cooperators/', CooperatorListCreateView.as_view(), name='cooperator-list-create'),

    # GET (retrieve) / PUT/PATCH (update) / DELETE (destroy) single cooperator
    path('cooperators/<int:pk>/', CooperatorRetrieveUpdateDestroyView.as_view(), name='cooperator-detail'),
    path('', include(router.urls)),
]

