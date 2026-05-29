from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import user_cycle_api

from .models import CycleTemplate, CyclePeriodDetail, UserProfile, Business
import datetime
import json

class UserCycleIntegrationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='inttest', password='pass')
        up, _ = UserProfile.objects.get_or_create(user=self.user)
        up.birth_date = datetime.date(1990, 1, 1)
        up.save()

    def _create_soul_periods(self):
        template, _ = CycleTemplate.objects.get_or_create(
            name='Soul Cycle', cycle_type='soul'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Soul Period A',
            start_value=101,
            end_value=331,
            description='A soul period',
            recommendations='Reflect',
            color='orange',
        )

    def _create_yearly_periods(self):
        template, _ = CycleTemplate.objects.get_or_create(
            name='Yearly Cycle', cycle_type='yearly'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Yearly Period 1',
            start_value=1,
            end_value=52,
            description='First yearly period',
            recommendations='Plan',
            color='purple',
        )

    def _create_business_periods(self):
        template, _ = CycleTemplate.objects.get_or_create(
            name='Business Cycle', cycle_type='business'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Biz Period 1',
            start_value=1,
            end_value=52,
            description='First business period',
            recommendations='Grow',
            color='green',
        )

    def test_daily_cycle_api_endpoint(self):
        import datetime as dt
        day_name = dt.datetime.now().strftime('%A')
        template, _ = CycleTemplate.objects.get_or_create(
            name=f'Daily Cycle - {day_name}', cycle_type='daily'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Morning',
            start_value=360,
            end_value=600,
            description='Morning hours',
            recommendations='Meditate',
            color='blue',
        )
        request = self.factory.get('/api/cycles/daily/')
        request.user = self.user
        response = user_cycle_api(request, 'daily')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('period_details', data)
        self.assertIn('name', data)
        self.assertEqual(data['cycle_type'], 'daily')

    def test_yearly_cycle_api_endpoint(self):
        self._create_yearly_periods()
        request = self.factory.get('/api/cycles/yearly/')
        request.user = self.user
        response = user_cycle_api(request, 'yearly')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('period_details', data)
        self.assertEqual(data['cycle_type'], 'yearly')

    def test_soul_cycle_api_endpoint(self):
        self._create_soul_periods()
        request = self.factory.get('/api/cycles/soul/')
        request.user = self.user
        response = user_cycle_api(request, 'soul')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('period_details', data)
        self.assertEqual(data['cycle_type'], 'soul')

    def test_health_cycle_api_endpoint(self):
        template, _ = CycleTemplate.objects.get_or_create(
            name='Health Cycle', cycle_type='health'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Health Period 1',
            start_value=1,
            end_value=52,
            description='First health period',
            recommendations='Rest',
            color='red',
        )
        request = self.factory.get('/api/cycles/health/')
        request.user = self.user
        response = user_cycle_api(request, 'health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('period_details', data)

    def test_business_cycle_api_endpoint(self):
        self._create_business_periods()
        request = self.factory.get('/api/cycles/business/')
        request.user = self.user
        response = user_cycle_api(request, 'business')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('period_details', data)
        self.assertEqual(data['cycle_type'], 'business')

    def test_reincarnation_cycle_api_endpoint(self):
        template, _ = CycleTemplate.objects.get_or_create(
            name='Reincarnation Cycle', cycle_type='reincarnation'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Reincarnation Period 1',
            start_value=0,
            end_value=365,
            description='First reincarnation period',
            recommendations='Learn',
            color='indigo',
        )
        request = self.factory.get('/api/cycles/reincarnation/')
        request.user = self.user
        response = user_cycle_api(request, 'reincarnation')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('period_details', data)

    def test_unauthenticated_returns_401_for_non_daily(self):
        self._create_soul_periods()
        from django.contrib.auth.models import AnonymousUser
        request = self.factory.get('/api/cycles/soul/')
        request.user = AnonymousUser()
        response = user_cycle_api(request, 'soul')
        self.assertEqual(response.status_code, 401)

    def test_public_daily_api_allows_anonymous(self):
        import datetime as dt
        day_name = dt.datetime.now().strftime('%A')
        template, _ = CycleTemplate.objects.get_or_create(
            name=f'Daily Cycle - {day_name}', cycle_type='daily'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Morning',
            start_value=360,
            end_value=600,
            description='Morning hours',
            recommendations='Meditate',
            color='blue',
        )
        from django.contrib.auth.models import AnonymousUser
        request = self.factory.get('/api/cycles/daily/')
        request.user = AnonymousUser()
        response = user_cycle_api(request, 'daily')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('period_details', data)
        self.assertEqual(data['cycle_type'], 'daily')

    def test_public_home_loads_for_anonymous(self):
        import datetime as dt
        day_name = dt.datetime.now().strftime('%A')
        template, _ = CycleTemplate.objects.get_or_create(
            name=f'Daily Cycle - {day_name}', cycle_type='daily'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Morning',
            start_value=360,
            end_value=600,
            description='Morning hours',
            recommendations='Meditate',
            color='blue',
        )
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        self.assertIn('Daily Cycle', content)
        self.assertIn('Sign Up for Your Full Cosmic Cycles', content)

    def test_api_returns_404_for_invalid_cycle_type(self):
        request = self.factory.get('/api/cycles/invalid/')
        request.user = self.user
        response = user_cycle_api(request, 'invalid')
        self.assertEqual(response.status_code, 404)

    def test_dashboard_loads_for_authenticated_user(self):
        self._create_yearly_periods()
        self._create_soul_periods()
        self._create_business_periods()
        # Need a health cycle template for the home view
        template, _ = CycleTemplate.objects.get_or_create(
            name='Health Cycle', cycle_type='health'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Health Period 1',
            start_value=1,
            end_value=52,
            description='First health period',
            recommendations='Rest',
            color='red',
        )
        logged = self.client.login(username='inttest', password='pass')
        self.assertTrue(logged)
        Business.objects.create(user=self.user, name='BizA', start_date=datetime.date(2020, 1, 1))
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        self.assertIn('Your Current Cycles', content)
        self.assertIn('Daily Cycle', content)
