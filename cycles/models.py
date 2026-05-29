from django.db import models
from django.contrib.auth.models import User
import secrets
from django.utils import timezone


class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, null=True, blank=True)
    verification_sent_at = models.DateTimeField(null=True, blank=True)

    def generate_verification_token(self):
        self.verification_token = secrets.token_urlsafe(48)
        self.verification_sent_at = timezone.now()
        self.save(update_fields=['verification_token', 'verification_sent_at'])
        return self.verification_token

    def __str__(self):
        return self.user.username

class CycleTemplate(models.Model):
    CYCLE_TYPES = (
        ('daily', 'Daily Cycle'),
        ('yearly', 'Yearly Cycle'),
        ('human', 'Human Life Cycle'),
        ('business', 'Business Cycle'),
        ('health', 'Health Cycle'),
        ('soul', 'Soul Cycle'),
        ('reincarnation', 'Reincarnation Cycle'),
    )
    name = models.CharField(max_length=100, unique=True)
    cycle_type = models.CharField(max_length=20, choices=CYCLE_TYPES, default='daily')
    description = models.TextField(blank=True, null=True)
    # Add fields for general cycle information if needed

    def __str__(self):
        return self.name

class CyclePeriodDetail(models.Model):
    cycle_template = models.ForeignKey(CycleTemplate, on_delete=models.CASCADE, related_name='period_details')
    period_name = models.CharField(max_length=100)
    start_value = models.IntegerField(help_text="Start value (e.g., day number, hour, minute)")
    end_value = models.IntegerField(help_text="End value (e.g., day number, hour, minute)")
    description = models.TextField()
    recommendations = models.TextField()
    lesson_content = models.TextField(blank=True, help_text="Deep educational content about this period (rich text)")
    color = models.CharField(max_length=20, default='blue') # For UI representation

    class Meta:
        ordering = ['start_value']

    def __str__(self):
        return f"{self.cycle_template.name} - {self.period_name}"

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    mood = models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Great'), (5, 'Excellent')], default=3)
    cycle_period = models.ForeignKey(CyclePeriodDetail, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Journal entries'

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.get_mood_display()})"


class GlossaryTerm(models.Model):
    term = models.CharField(max_length=100, unique=True)
    definition = models.TextField()
    related_cycle_type = models.CharField(max_length=20, choices=CycleTemplate.CYCLE_TYPES, blank=True, null=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'term']
        verbose_name_plural = 'Glossary terms'

    def __str__(self):
        return self.term


class QuizQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
    ]
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255, blank=True)
    option_d = models.CharField(max_length=255, blank=True)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    explanation = models.TextField(blank=True)
    cycle_period = models.ForeignKey(CyclePeriodDetail, on_delete=models.CASCADE, related_name='quiz_questions')
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"Quiz: {self.cycle_period.period_name} - Q{self.id}"


class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    cycle_period = models.ForeignKey(CyclePeriodDetail, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    quiz_score = models.IntegerField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'User lesson progress'
        unique_together = ['user', 'cycle_period']

    def __str__(self):
        return f"{self.user.username} - {self.cycle_period.period_name} {'✓' if self.completed else '○'}"