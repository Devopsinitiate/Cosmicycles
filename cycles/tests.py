from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, time, timedelta, date
from .models import CycleTemplate, CyclePeriodDetail, UserProfile, QuizQuestion, UserLessonProgress
from .utils import (
    parse_recommendations,
    get_current_daily_cycle_period,
    get_current_yearly_cycle_period,
    get_current_soul_cycle_period,
    get_current_business_cycle_period,
    get_current_health_cycle_period,
    get_current_reincarnation_cycle_period,
)


class ParseRecommendationsTestCase(TestCase):
    def test_parse_empty_string(self):
        self.assertEqual(parse_recommendations(""), {})

    def test_parse_none(self):
        self.assertEqual(parse_recommendations(None), {})

    def test_parse_json_recommendations(self):
        json_str = '{"Morning": ["Meditate", "Exercise"], "Evening": ["Review day"]}'
        result = parse_recommendations(json_str)
        self.assertIn("Morning", result)
        self.assertEqual(len(result["Morning"]), 2)

    def test_parse_semicolon_string(self):
        result = parse_recommendations("Meditate; Exercise; Review")
        self.assertIn("General", result)
        self.assertEqual(len(result["General"]), 3)


class DailyCycleUtilsTestCase(TestCase):
    def setUp(self):
        template = CycleTemplate.objects.create(
            name="Daily Cycle - Monday", cycle_type="daily"
        )
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Morning",
            start_value=360,
            end_value=600,
            description="Morning period",
            recommendations="Meditate",
            color="blue",
        )

    def test_get_current_daily_cycle_period_found(self):
        current_time = time(8, 0)
        period = get_current_daily_cycle_period(current_time)
        self.assertIsNotNone(period)
        self.assertEqual(period.period_name, "Morning")

    def test_get_current_daily_cycle_period_not_found(self):
        current_time = time(1, 0)
        period = get_current_daily_cycle_period(current_time)
        self.assertIsNone(period)


class YearlyCycleUtilsTestCase(TestCase):
    def setUp(self):
        template = CycleTemplate.objects.create(
            name="Yearly Cycle", cycle_type="yearly"
        )
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Period 1",
            start_value=1,
            end_value=52,
            description="First period",
            recommendations='{"Focus": ["Plan"]}',
            color="blue",
        )

    def test_get_current_yearly_cycle_period(self):
        birth_date = datetime(1990, 1, 1).date()
        current_date = datetime(2024, 2, 1).date()
        result = get_current_yearly_cycle_period(birth_date, current_date)
        self.assertIsNotNone(result)
        self.assertIn("period", result)
        self.assertIn("days_into_period", result)
        self.assertIn("period_duration", result)

    def test_get_current_yearly_cycle_period_no_birth_date(self):
        result = get_current_yearly_cycle_period(None, datetime.now().date())
        self.assertIsNone(result)


class SoulCycleUtilsTestCase(TestCase):
    def setUp(self):
        template = CycleTemplate.objects.create(
            name="Soul Cycle", cycle_type="soul"
        )
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Soul Period 1",
            start_value=101,
            end_value=331,
            description="Soul period",
            recommendations="Reflect",
            color="orange",
        )

    def test_get_current_soul_cycle_period(self):
        current_date = datetime(2024, 3, 15).date()
        period = get_current_soul_cycle_period(current_date)
        self.assertIsNotNone(period)
        self.assertEqual(period.period_name, "Soul Period 1")


class BusinessCycleUtilsTestCase(TestCase):
    def setUp(self):
        template = CycleTemplate.objects.create(
            name="Business Cycle", cycle_type="business"
        )
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Biz Period 1",
            start_value=1,
            end_value=52,
            description="First business period",
            recommendations="Plan growth",
            color="green",
        )

    def test_get_current_business_cycle_period(self):
        start_date = datetime(2020, 1, 1).date()
        current_date = datetime(2024, 2, 1).date()
        result = get_current_business_cycle_period(start_date, current_date)
        self.assertIsNotNone(result)
        self.assertIn("period", result)

    def test_get_current_business_cycle_period_no_start(self):
        result = get_current_business_cycle_period(None, datetime.now().date())
        self.assertIsNone(result)


class HealthCycleUtilsTestCase(TestCase):
    def setUp(self):
        template = CycleTemplate.objects.create(
            name="Health Cycle", cycle_type="health"
        )
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Health Period 1",
            start_value=1,
            end_value=52,
            description="First health period",
            recommendations="Rest",
            color="red",
        )

    def test_get_current_health_cycle_period(self):
        current_date = datetime(2024, 2, 1).date()
        result = get_current_health_cycle_period(current_date)
        self.assertIsNotNone(result)
        self.assertIn("period", result)


class ReincarnationCycleUtilsTestCase(TestCase):
    def setUp(self):
        template = CycleTemplate.objects.create(
            name="Reincarnation Cycle", cycle_type="reincarnation"
        )
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Reincarnation Period 1",
            start_value=0,
            end_value=365,
            description="First reincarnation period",
            recommendations="Learn",
            color="indigo",
        )

    def test_get_current_reincarnation_cycle_period(self):
        # Birth 6 months ago falls within the 0-365 day period
        birth_date = datetime.now().date() - timedelta(days=180)
        current_date = datetime.now().date()
        result = get_current_reincarnation_cycle_period(birth_date, current_date)
        self.assertIsNotNone(result)
        self.assertIn("period", result)

    def test_get_current_reincarnation_cycle_period_no_birth(self):
        result = get_current_reincarnation_cycle_period(None, datetime.now().date())
        self.assertIsNone(result)


class UserProfileModelTestCase(TestCase):
    def test_create_user_profile_on_user_creation(self):
        user = User.objects.create_user(username="testuser", password="pass")
        profile = UserProfile.objects.get(user=user)
        self.assertIsNotNone(profile)
        self.assertIsNone(profile.birth_date)

    def test_user_profile_str(self):
        user = User.objects.create_user(username="testuser", password="pass")
        self.assertEqual(str(user.userprofile), "testuser")


class EdgeCaseUtilsTestCase(TestCase):
    def test_daily_cycle_midnight_crossover(self):
        """Period that crosses midnight boundary (start > end)."""
        template = CycleTemplate.objects.create(
            name="Daily Cycle - Monday", cycle_type="daily"
        )
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Late Night",
            start_value=1320,
            end_value=360,
            description="Crosses midnight",
            recommendations="Rest",
            color="indigo",
        )
        # At 11 PM (1380 min) we should be in the midnight-crossover period
        late = time(23, 0)
        period = get_current_daily_cycle_period(late)
        self.assertIsNotNone(period)
        self.assertEqual(period.period_name, "Late Night")
        # At 2 AM (120 min) we should still be in it
        early = time(2, 0)
        period = get_current_daily_cycle_period(early)
        self.assertIsNotNone(period)
        self.assertEqual(period.period_name, "Late Night")

    def test_leap_year_yearly_cycle(self):
        """Yearly cycle should still work on Feb 29."""
        template = CycleTemplate.objects.create(
            name="Yearly Cycle", cycle_type="yearly"
        )
        # Period covering March 1 (day 61 in leap year)
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Post-Feb",
            start_value=61,
            end_value=121,
            description="Covers March",
            recommendations='{"Focus": ["Plan"]}',
            color="blue",
        )
        birth_date = date(2020, 3, 1)  # born March 1
        # On Feb 29 2024 (leap year), birthday hasn't happened yet
        # days_since_birthday would be negative - the function should handle this
        result = get_current_yearly_cycle_period(birth_date, date(2024, 2, 29))
        # Should return None if birthday hasn't happened yet
        # Or return a valid period - either way shouldn't crash
        if result:
            self.assertIn("period", result)

    def test_soul_cycle_year_boundary(self):
        """Soul cycle period that crosses Dec 31 -> Jan 1."""
        template = CycleTemplate.objects.create(
            name="Soul Cycle", cycle_type="soul"
        )
        # Period 6: Dec 7 (1207) to Jan 1 (101) - crosses year boundary
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Year Crosser",
            start_value=1207,
            end_value=101,
            description="Crosses year",
            recommendations="Reflect",
            color="orange",
        )
        p = get_current_soul_cycle_period(date(2024, 12, 25))
        self.assertIsNotNone(p)
        self.assertEqual(p.period_name, "Year Crosser")
        p = get_current_soul_cycle_period(date(2025, 1, 1))
        self.assertIsNotNone(p)
        self.assertEqual(p.period_name, "Year Crosser")

    def test_human_cycle_very_old_user(self):
        """User older than 99 should not crash."""
        template = CycleTemplate.objects.create(
            name="Human Life Cycle", cycle_type="human"
        )
        CyclePeriodDetail.objects.create(
            cycle_template=template,
            period_name="Old Age",
            start_value=98,
            end_value=130,
            description="98+ years",
            recommendations="Reflect",
            color="pink",
        )
        from .utils import get_current_human_cycle_period
        birth_date = date(1900, 1, 1)
        result = get_current_human_cycle_period(birth_date, date(2024, 6, 15))
        self.assertIsNotNone(result)
        self.assertIn("period", result)
