from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('users/register/', views.create_user, name='create-user'),

    path('', views.get_routes),
    path('files/', views.files_handler, name="files-handler"),
    path('files/<int:file_id>/', views.file_detail_handler, name="file-detail-handler"),

    path('token/', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
