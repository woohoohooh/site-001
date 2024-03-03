from django.urls import path
from .views import index, company_detail, rubric_detail, add_comment, company_detail2, test, toggle_visibility

urlpatterns = [
    path('', index, name='index'),
    path('catalog/<str:slug>/', rubric_detail, name='rubric_detail'),
    path('test/', test, name='test'),
    path('<str:slug>/', company_detail, name='company_detail'),
    path('2/<int:pk>/', company_detail2, name='company_detail2'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('company/<int:pk>/toggle_visibility/', toggle_visibility, name='toggle_visibility'),


]
