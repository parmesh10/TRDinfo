import random

from django.shortcuts import render, redirect
from django.utils import timezone

from .models import (
    Exam,
    Question,
    ExamAttempt,
    ExamAnswer,
)


def home(request):

    return render(
        request,
        "home.html"
    )


def exam_start(request):

    exam = Exam.objects.filter(
        active=True
    ).first()

    if not exam:

        return render(
            request,
            "exam/no_exam.html"
        )

    if request.method == "POST":

        candidate_name = request.POST.get(
            "candidate_name"
        )

        employee_number = request.POST.get(
            "employee_number"
        )

        if not candidate_name or not employee_number:

            return render(
                request,
                "exam/start.html",
                {
                    "exam": exam,
                    "error": "Please enter candidate name and employee number."
                }
            )

        # Get active questions
        questions = list(
            Question.objects.filter(
                active=True
            )
        )

        # Check enough questions exist
        if len(questions) < exam.number_of_questions:

            return render(
                request,
                "exam/start.html",
                {
                    "exam": exam,
                    "error": (
                        f"Only {len(questions)} active questions "
                        f"are available. "
                        f"{exam.number_of_questions} are required."
                    )
                }
            )

        # Randomize
        random.shuffle(questions)

        # Select required number
        questions = questions[
            :exam.number_of_questions
        ]

        # Store candidate information
        request.session["candidate_name"] = (
            candidate_name
        )

        request.session["employee_number"] = (
            employee_number
        )

        request.session["exam_id"] = exam.id

        request.session["question_ids"] = [
            question.id
            for question in questions
        ]

        return redirect(
            "take_exam"
        )

    return render(
        request,
        "exam/start.html",
        {
            "exam": exam
        }
    )


def take_exam(request):

    exam_id = request.session.get(
        "exam_id"
    )

    question_ids = request.session.get(
        "question_ids"
    )

    if not exam_id or not question_ids:

        return redirect(
            "exam_start"
        )

    exam = Exam.objects.get(
        id=exam_id
    )

    questions = Question.objects.filter(
        id__in=question_ids
    )

    # Preserve random order
    question_dict = {
        question.id: question
        for question in questions
    }

    ordered_questions = [
        question_dict[qid]
        for qid in question_ids
        if qid in question_dict
    ]

    if request.method == "POST":

        candidate_name = request.session.get(
            "candidate_name",
            "Unknown"
        )

        employee_number = request.session.get(
            "employee_number",
            ""
        )

        # Create attempt
        attempt = ExamAttempt.objects.create(
            candidate_name=candidate_name,
            employee_number=employee_number,
            exam=exam,
            total_questions=len(
                ordered_questions
            ),
            submitted_at=timezone.now(),
        )

        correct_count = 0
        wrong_count = 0
        unanswered_count = 0
        score = 0

        for question in ordered_questions:

            selected_answer = request.POST.get(
                f"question_{question.id}",
                ""
            )

            # Unanswered
            if not selected_answer:

                unanswered_count += 1

                ExamAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_answer="",
                    is_correct=False,
                    marks_obtained=0,
                )

                continue

            # Correct answer
            if selected_answer == question.correct_answer:

                correct_count += 1

                marks = 1

                score += marks

                ExamAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=True,
                    marks_obtained=marks,
                )

            # Wrong answer
            else:

                wrong_count += 1

                if exam.negative_marking:

                    marks = -float(
                        exam.negative_marks
                    )

                    score += marks

                else:

                    marks = 0

                ExamAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=False,
                    marks_obtained=marks,
                )

        attempted_count = (
            correct_count +
            wrong_count
        )

        total_questions = len(
            ordered_questions
        )

        if total_questions > 0:

            percentage = (
                score /
                total_questions
            ) * 100

        else:

            percentage = 0

        passed = (
            percentage >=
            exam.pass_percentage
        )

        # Update attempt
        attempt.attempted_questions = (
            attempted_count
        )

        attempt.correct_answers = (
            correct_count
        )

        attempt.wrong_answers = (
            wrong_count
        )

        attempt.unanswered_questions = (
            unanswered_count
        )

        attempt.score = round(
            score,
            2
        )

        attempt.percentage = round(
            percentage,
            2
        )

        attempt.passed = passed

        attempt.submitted_at = timezone.now()

        attempt.save()

        # Save attempt ID
        request.session["attempt_id"] = (
            attempt.id
        )

        # Clear exam session data
        request.session.pop(
            "question_ids",
            None
        )

        request.session.pop(
            "exam_id",
            None
        )

        return redirect(
            "exam_result"
        )

    return render(
        request,
        "exam/exam.html",
        {
            "exam": exam,
            "questions": ordered_questions,
        }
    )


def exam_result(request):

    attempt_id = request.session.get(
        "attempt_id"
    )

    if not attempt_id:

        return redirect(
            "home"
        )

    try:

        attempt = ExamAttempt.objects.get(
            id=attempt_id
        )

    except ExamAttempt.DoesNotExist:

        return redirect(
            "home"
        )

    return render(
        request,
        "exam/result.html",
        {
            "attempt": attempt
        }
    )