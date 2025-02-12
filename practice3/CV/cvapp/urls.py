from django.urls import path
from .views import create_cv, share_cv_email, success_view

urlpatterns = [
    path('create-cv/', create_cv, name='create_cv'),
    path('cv-list/', success_view, name='cv_list'),
    path('share/email/<int:cv_id>/', share_cv_email, name='share_cv_email'),
]

