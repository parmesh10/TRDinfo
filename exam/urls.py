from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "exam/",
        views.exam_start,
        name="exam_start"
    ),

    path(
        "exam/take/",
        views.take_exam,
        name="take_exam"
    ),

    path(
        "result/",
        views.exam_result,
        name="exam_result"
    ),
    path(
    "evaluation/<int:attempt_id>/",
    views.exam_evaluation,
    name="exam_evaluation"
    ),
    
]