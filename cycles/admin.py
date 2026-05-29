from django.contrib import admin
from .models import UserProfile, Business, CycleTemplate, CyclePeriodDetail, JournalEntry, GlossaryTerm, QuizQuestion, UserLessonProgress

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'gender')

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_date')

@admin.register(CycleTemplate)
class CycleTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'cycle_type')
    list_filter = ('cycle_type',)

@admin.register(CyclePeriodDetail)
class CyclePeriodDetailAdmin(admin.ModelAdmin):
    list_display = ('cycle_template', 'period_name', 'start_value', 'end_value', 'color')
    list_filter = ('cycle_template',)
    search_fields = ('period_name', 'description')

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood', 'cycle_period')
    list_filter = ('user', 'date', 'mood')
    search_fields = ('content',)

@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'related_cycle_type', 'sort_order')
    list_filter = ('related_cycle_type',)
    search_fields = ('term', 'definition')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'cycle_period', 'difficulty', 'correct_answer')
    list_filter = ('cycle_period__cycle_template', 'difficulty')
    search_fields = ('question',)

@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'cycle_period', 'completed', 'quiz_score', 'viewed_at')
    list_filter = ('completed', 'user')