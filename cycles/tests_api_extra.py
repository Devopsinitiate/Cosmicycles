from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Business, CycleTemplate, CyclePeriodDetail
import json
import datetime


User = get_user_model()


class CycleApiExtraTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass')
        self.client.login(username='tester', password='pass')
        self.business = Business.objects.create(
            user=self.user, name='Acme LLC', start_date=datetime.date(2020, 1, 1)
        )

    def _ensure_business_periods(self):
        template, _ = CycleTemplate.objects.get_or_create(
            name='Business Cycle', cycle_type='business'
        )
        CyclePeriodDetail.objects.get_or_create(
            cycle_template=template,
            period_name='Biz Period 1',
            start_value=1,
            end_value=52,
            description='First period',
            recommendations='Plan',
            color='green',
        )

    def _ensure_soul_periods(self):
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

    def test_business_api_returns_cycle_template_data(self):
        self._ensure_business_periods()
        url = reverse('user_cycle_api', args=['business'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn('period_details', data)
        self.assertEqual(data['cycle_type'], 'business')
        self.assertIn('name', data)

    def test_soul_api_returns_period_details(self):
        self._ensure_soul_periods()
        url = reverse('user_cycle_api', args=['soul'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn('period_details', data)
        self.assertIsInstance(data['period_details'], list)
        self.assertEqual(data['cycle_type'], 'soul')
