from django.db import models


class Subject(models.Model):

    name = models.CharField(
        max_length=300,
        unique=True
    )

    number = models.PositiveIntegerField(
        unique=True
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"{self.number}. {self.name}"


class Question(models.Model):

    DIFFICULTY_CHOICES = [
        ("EASY", "Easy"),
        ("MEDIUM", "Medium"),
        ("HARD", "Hard"),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="questions",
        null=True,
        blank=True
    )

    question_text = models.TextField(
        verbose_name="Question"
    )

    option_a = models.CharField(
        max_length=500,
        verbose_name="Option A"
    )

    option_b = models.CharField(
        max_length=500,
        verbose_name="Option B"
    )

    option_c = models.CharField(
        max_length=500,
        verbose_name="Option C"
    )

    option_d = models.CharField(
        max_length=500,
        verbose_name="Option D"
    )

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ],
        verbose_name="Correct Answer"
    )

    explanation = models.TextField(
        blank=True,
        verbose_name="Explanation"
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default="MEDIUM"
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.question_text[:80]


class Exam(models.Model):

    name = models.CharField(
        max_length=200,
        default="TRD Examination"
    )

    number_of_questions = models.PositiveIntegerField(
        default=20
    )

    duration_minutes = models.PositiveIntegerField(
        default=30
    )

    pass_percentage = models.PositiveIntegerField(
        default=40
    )

    negative_marking = models.BooleanField(
        default=False
    )

    negative_marks = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class ExamAttempt(models.Model):

    candidate_name = models.CharField(
        max_length=200
    )

    employee_number = models.CharField(
        max_length=100
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="attempts"
    )

    total_questions = models.PositiveIntegerField(
        default=0
    )

    attempted_questions = models.PositiveIntegerField(
        default=0
    )

    correct_answers = models.PositiveIntegerField(
        default=0
    )

    wrong_answers = models.PositiveIntegerField(
        default=0
    )

    unanswered_questions = models.PositiveIntegerField(
        default=0
    )

    score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    percentage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    passed = models.BooleanField(
        default=False
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):

        return (
            f"{self.candidate_name} - "
            f"{self.employee_number} - "
            f"{self.exam.name}"
        )


class ExamAnswer(models.Model):

    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    selected_answer = models.CharField(
        max_length=1,
        blank=True
    )

    is_correct = models.BooleanField(
        default=False
    )

    marks_obtained = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    def __str__(self):

        return (
            f"{self.attempt.candidate_name} - "
            f"Question {self.question.id}"
        )