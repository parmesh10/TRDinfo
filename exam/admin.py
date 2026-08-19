from django.contrib import admin

from .models import (
    Question,
    Exam,
    ExamAttempt,
    ExamAnswer,
)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "question_text",
        "difficulty",
        "correct_answer",
        "active",
        "created_at",
    )

    list_filter = (
        "difficulty",
        "active",
    )

    search_fields = (
        "question_text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
    )


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "number_of_questions",
        "duration_minutes",
        "pass_percentage",
        "negative_marking",
        "active",
    )

    list_filter = (
        "active",
        "negative_marking",
    )


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "candidate_name",
        "employee_number",
        "exam",
        "total_questions",
        "correct_answers",
        "wrong_answers",
        "unanswered_questions",
        "score",
        "percentage",
        "passed",
        "started_at",
        "submitted_at",
    )

    list_filter = (
        "exam",
        "passed",
    )

    search_fields = (
        "candidate_name",
        "employee_number",
    )


@admin.register(ExamAnswer)
class ExamAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "attempt",
        "question",
        "selected_answer",
        "is_correct",
        "marks_obtained",
    )

    list_filter = (
        "is_correct",
    )