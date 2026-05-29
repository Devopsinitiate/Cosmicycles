from datetime import datetime, timedelta
from .models import CycleTemplate, CyclePeriodDetail
import json

def parse_recommendations(recommendations_str):
    if not recommendations_str:
        return {}
    try:
        # Try to parse as JSON first (for Yearly, Soul, Business, Health, Reincarnation)
        return json.loads(recommendations_str)
    except json.JSONDecodeError:
        # If not JSON, assume it's a simple string (for Daily Cycle)
        # Convert it into a dictionary with a 'General' category
        # Split by semicolon and strip whitespace
        recommendations_list = [rec.strip() for rec in recommendations_str.split(';') if rec.strip()]
        return {"General": recommendations_list}
    except (ValueError, SyntaxError):
        # Fallback for other parsing errors (e.g., malformed ast.literal_eval input)
        return {"General": [recommendations_str]} # Return as a single item in 'General' category

def get_current_daily_cycle_period(current_time):
    """
    Calculates the current daily cycle period based on the current time.
    """
    day_name = current_time.strftime('%A')
    template_name = f'Daily Cycle - {day_name}'
    try:
        daily_cycle_template = CycleTemplate.objects.get(name=template_name)
        daily_periods = daily_cycle_template.period_details.all()

        current_minutes = current_time.hour * 60 + current_time.minute

        for period in daily_periods:
            # Handle periods that cross midnight
            if period.start_value > period.end_value:
                if current_minutes >= period.start_value or current_minutes < period.end_value:
                    period.recommendations = parse_recommendations(period.recommendations)
                    return period
            else:
                if period.start_value <= current_minutes < period.end_value:
                    period.recommendations = parse_recommendations(period.recommendations)
                    return period
    except CycleTemplate.DoesNotExist:
        return None
    return None 

def get_current_yearly_cycle_period(birth_date, current_date):
    """
    Calculates the current yearly cycle period based on birth date and current date.
    Returns the period, days into the period, and total period duration.
    """
    if not birth_date:
        return None

    current_year_birthday = birth_date.replace(year=current_date.year)
    if current_date < current_year_birthday:
        current_year_birthday = birth_date.replace(year=current_date.year - 1)

    days_since_birthday = (current_date - current_year_birthday).days + 1

    try:
        yearly_cycle_template = CycleTemplate.objects.get(cycle_type='yearly')
        yearly_periods = yearly_cycle_template.period_details.all()
    except CycleTemplate.DoesNotExist:
        return None

    for period in yearly_periods:
        if period.start_value <= days_since_birthday <= period.end_value:
            period_duration = period.end_value - period.start_value + 1
            days_into_period = days_since_birthday - period.start_value + 1
            period.recommendations = parse_recommendations(period.recommendations)
            return {
                'period': period,
                'days_into_period': days_into_period,
                'period_duration': period_duration,
            }
    return None

def get_current_soul_cycle_period(current_date):
    """
    Calculates the current soul cycle period based on the current date.
    """
    try:
        soul_cycle_template = CycleTemplate.objects.get(cycle_type='soul')
        soul_periods = soul_cycle_template.period_details.all()
    except CycleTemplate.DoesNotExist:
        return None

    current_mmdd = current_date.month * 100 + current_date.day

    for period in soul_periods:
        if period.start_value > period.end_value:  # Crosses year boundary
            if current_mmdd >= period.start_value or current_mmdd <= period.end_value:
                period.recommendations = parse_recommendations(period.recommendations)
                return period
        else:
            if period.start_value <= current_mmdd <= period.end_value:
                period.recommendations = parse_recommendations(period.recommendations)
                return period
    return None

def get_current_business_cycle_period(business_start_date, current_date):
    """
    Calculates the current business cycle period based on business start date and current date.
    Returns the period, days into the period, and total period duration.
    """
    if not business_start_date:
        return None

    current_year_anniversary = business_start_date.replace(year=current_date.year)
    if current_date < current_year_anniversary:
        current_year_anniversary = business_start_date.replace(year=current_date.year - 1)

    days_since_anniversary = (current_date - current_year_anniversary).days + 1

    try:
        business_cycle_template = CycleTemplate.objects.get(cycle_type='business')
        business_periods = business_cycle_template.period_details.all()

        for period in business_periods:
            if period.start_value <= days_since_anniversary <= period.end_value:
                period_duration = period.end_value - period.start_value + 1
                days_into_period = days_since_anniversary - period.start_value + 1
                period.recommendations = parse_recommendations(period.recommendations)
                return {
                    'period': period,
                    'days_into_period': days_into_period,
                    'period_duration': period_duration,
                }
    except CycleTemplate.DoesNotExist:
        return None
    return None

def get_current_health_cycle_period(current_date):
    """
    Calculates the current health cycle period based on the current date.
    Returns the period, days into the period, and total period duration.
    """
    try:
        health_cycle_template = CycleTemplate.objects.get(cycle_type='health')
        health_periods = health_cycle_template.period_details.all()
    except CycleTemplate.DoesNotExist:
        return None
    
    days_since_jan1 = (current_date - current_date.replace(month=1, day=1)).days + 1

    for period in health_periods:
        if period.start_value <= days_since_jan1 <= period.end_value:
            period_duration = period.end_value - period.start_value + 1
            days_into_period = days_since_jan1 - period.start_value + 1
            period.recommendations = parse_recommendations(period.recommendations)
            return {
                'period': period,
                'days_into_period': days_into_period,
                'period_duration': period_duration,
            }
    return None

def get_current_human_cycle_period(birth_date, current_date):
    """
    Calculates the current human life cycle period based on birth date.
    Book: 9 periods of 7 years each (ages 0-62), using age-based lookup.
    Returns the period, years into period, and period duration.
    """
    if not birth_date:
        return None

    age = current_date.year - birth_date.year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    try:
        human_template = CycleTemplate.objects.get(cycle_type='human')
        period = human_template.period_details.filter(
            start_value__lte=age, end_value__gt=age
        ).first()
        if not period:
            return None

        period_start_age = period.start_value
        period_end_age = period.end_value - 1
        days_into_period = (current_date - birth_date).days - period_start_age * 365
        period_duration = (period_end_age - period_start_age + 1) * 365
        period.recommendations = parse_recommendations(period.recommendations)
        return {
            'period': period,
            'days_into_period': days_into_period,
            'period_duration': period_duration,
            'age': age,
            'period_number': (age // 7) + 1,
        }
    except CycleTemplate.DoesNotExist:
        return None


def get_current_reincarnation_cycle_period(birth_date, current_date):
    """
    Calculates the current reincarnation cycle period based on birth date and current date.
    Returns the period, days into the period, and total period duration.
    """
    if not birth_date:
        return None

    age_in_days = (current_date - birth_date).days

    try:
        reincarnation_cycle_template = CycleTemplate.objects.get(cycle_type='reincarnation')
        reincarnation_periods = reincarnation_cycle_template.period_details.all()
    except CycleTemplate.DoesNotExist:
        return None

    for period in reincarnation_periods:
        if period.start_value <= age_in_days <= period.end_value:
            period_duration = period.end_value - period.start_value + 1
            days_into_period = age_in_days - period.start_value + 1
            period.recommendations = parse_recommendations(period.recommendations)
            return {
                'period': period,
                'days_into_period': days_into_period,
                'period_duration': period_duration,
            }
    return None

def get_upcoming_transitions(birth_date, current_date, current_time):
    transitions = []

    try:
        day_name = current_date.strftime('%A')
        daily_template = CycleTemplate.objects.get(name=f'Daily Cycle - {day_name}')
        daily_periods = list(daily_template.period_details.all().order_by('start_value'))
        cur_min = current_time.hour * 60 + current_time.minute
        for p in daily_periods:
            if p.start_value > cur_min:
                td = datetime.combine(current_date, datetime.min.time()) + timedelta(minutes=p.start_value)
                transitions.append({
                    'cycle_type': 'daily', 'cycle_label': 'Daily Cycle',
                    'period_name': p.period_name, 'color': p.color or 'blue',
                    'transition_datetime': td, 'days_remaining': 0,
                })
                break
    except CycleTemplate.DoesNotExist:
        pass

    try:
        soul_template = CycleTemplate.objects.get(cycle_type='soul')
        soul_periods = list(soul_template.period_details.all().order_by('start_value'))
        cur_mmdd = current_date.month * 100 + current_date.day
        for p in soul_periods:
            ps, pe = p.start_value, p.end_value
            if (ps <= pe and cur_mmdd < ps) or (ps > pe and cur_mmdd < ps and cur_mmdd > pe):
                year = current_date.year
                if ps > pe and ps < cur_mmdd:
                    year += 1
                try:
                    td = datetime(year, ps // 100, ps % 100)
                    days = (td.date() - current_date).days
                    if days >= 0:
                        transitions.append({
                            'cycle_type': 'soul', 'cycle_label': 'Soul Cycle',
                            'period_name': p.period_name, 'color': p.color or 'orange',
                            'transition_datetime': td, 'days_remaining': days,
                        })
                        break
                except (ValueError, AttributeError):
                    pass
    except CycleTemplate.DoesNotExist:
        pass

    cycle_types = [
        ('yearly', 'Yearly Cycle', 'purple'),
        ('health', 'Health Cycle', 'red'),
        ('human', 'Human Life Cycle', 'pink'),
        ('reincarnation', 'Reincarnation Cycle', 'indigo'),
    ]
    for ct, label, color in cycle_types:
        data = None
        if ct == 'yearly':
            data = get_current_yearly_cycle_period(birth_date, current_date)
        elif ct == 'health':
            data = get_current_health_cycle_period(current_date)
        elif ct == 'human':
            data = get_current_human_cycle_period(birth_date, current_date)
        elif ct == 'reincarnation':
            data = get_current_reincarnation_cycle_period(birth_date, current_date)
        if data:
            p = data['period']
            days_left = data['period_duration'] - data['days_into_period']
            transitions.append({
                'cycle_type': ct, 'cycle_label': label,
                'period_name': p.period_name, 'color': p.color or color,
                'transition_datetime': current_date + timedelta(days=days_left),
                'days_remaining': days_left,
            })

    transitions.sort(key=lambda t: (t['days_remaining'], t['transition_datetime']))
    return transitions[:5]
