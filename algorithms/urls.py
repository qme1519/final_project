from django.urls import path
from . import views

# define url addresses to be used in the project
urlpatterns = [
    path("", views.algorithms_index, name="algorithms_index"),
    path("<int:pk>/", views.algorithms_detail, name="algorithms_detail"),
    path("<category>/", views.algorithms_category, name="algorithms_category"),
    path("succes/", views.algorithms_result, name="algorithms_result"),
    path("error", views.algorithms_error, name='algorithms_error')
]
