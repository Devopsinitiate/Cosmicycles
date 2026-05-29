from datetime import datetime
from .models import UserProfile, Business, QuizQuestion, UserLessonProgress, CycleTemplate
from .utils import (
    get_current_daily_cycle_period, get_current_yearly_cycle_period,
    get_current_soul_cycle_period, get_current_business_cycle_period,
    get_current_health_cycle_period, get_current_human_cycle_period,
    get_current_reincarnation_cycle_period, get_upcoming_transitions,
)

def get_all_current_periods(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    daily = get_current_daily_cycle_period(current_time)
    yearly = get_current_yearly_cycle_period(profile.birth_date, current_date)
    soul = get_current_soul_cycle_period(current_date)
    health = get_current_health_cycle_period(current_date)
    reincarnation = get_current_reincarnation_cycle_period(profile.birth_date, current_date)
    human = get_current_human_cycle_period(profile.birth_date, current_date)

    business = None
    biz = Business.objects.filter(user=user).first()
    if biz:
        business = get_current_business_cycle_period(biz.start_date, current_date)

    return {
        'daily': daily,
        'yearly': yearly,
        'soul': soul,
        'health': health,
        'reincarnation': reincarnation,
        'human': human,
        'business': business,
    }


def get_experience_based_recommendations(user, current_period_ids):
    if not current_period_ids:
        return []

    from django.urls import reverse

    completed_ids = set(UserLessonProgress.objects.filter(
        user=user, completed=True,
        cycle_period_id__in=current_period_ids,
    ).values_list('cycle_period_id', flat=True))

    incomplete = QuizQuestion.objects.filter(
        cycle_period_id__in=current_period_ids,
    ).exclude(
        cycle_period_id__in=completed_ids,
    ).select_related('cycle_period__cycle_template').distinct()[:3]

    recommendations = []
    for q in incomplete:
        recommendations.append({
            'period': q.cycle_period,
            'cycle_type': q.cycle_period.cycle_template.cycle_type,
            'question': q.question[:80] + '\u2026' if len(q.question) > 80 else q.question,
            'quiz_url': reverse('education_quiz', args=[q.cycle_period.id]),
            'period_url': reverse('education_period_detail', args=[
                q.cycle_period.cycle_template.cycle_type, q.cycle_period.id]),
        })
    return recommendations
