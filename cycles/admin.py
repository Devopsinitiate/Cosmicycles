from django.contrib import admin
from .models import UserProfile, Business, CycleTemplate, CyclePeriodDetail, JournalEntry, GlossaryTerm, QuizQuestion, UserLessonProgress


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    fields = ('question', 'correct_answer', 'difficulty', 'sort_order')
    show_change_link = True


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_verified', 'birth_date', 'gender', 'verification_sent_at')
    list_filter = ('email_verified', 'gender')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('verification_token', 'verification_sent_at')
    date_hierarchy = 'verification_sent_at'


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_date')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')
    date_hierarchy = 'start_date'


@admin.register(CycleTemplate)
class CycleTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'cycle_type', 'period_count')
    list_filter = ('cycle_type',)
    search_fields = ('name', 'description')

    def period_count(self, obj):
        return obj.period_details.count()
    period_count.short_description = 'Periods'


@admin.register(CyclePeriodDetail)
class CyclePeriodDetailAdmin(admin.ModelAdmin):
    list_display = ('period_name', 'cycle_template', 'start_value', 'end_value', 'color', 'lesson_status')
    list_filter = ('cycle_template__cycle_type', 'cycle_template', 'color')
    search_fields = ('period_name', 'description', 'recommendations')
    list_editable = ('color',)
    inlines = [QuizQuestionInline]

    def lesson_status(self, obj):
        if obj.lesson_content:
            return 'Has lesson'
        return 'No lesson'
    lesson_status.short_description = 'Lesson'


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood', 'cycle_period', 'created_at')
    list_filter = ('mood', 'date', 'user')
    search_fields = ('content', 'user__username')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'related_cycle_type', 'sort_order')
    list_filter = ('related_cycle_type',)
    search_fields = ('term', 'definition')
    list_editable = ('sort_order',)


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('short_question', 'cycle_period', 'difficulty', 'correct_answer')
    list_filter = ('cycle_period__cycle_template__cycle_type', 'difficulty')
    search_fields = ('question',)
    list_editable = ('difficulty',)

    def short_question(self, obj):
        return obj.question[:60] + ('...' if len(obj.question) > 60 else '')
    short_question.short_description = 'Question'


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'cycle_period', 'completed', 'quiz_score', 'viewed_at')
    list_filter = ('completed', 'user', 'cycle_period__cycle_template__cycle_type')
    search_fields = ('user__username', 'cycle_period__period_name')
    date_hierarchy = 'viewed_at'
    readonly_fields = ('viewed_at',)