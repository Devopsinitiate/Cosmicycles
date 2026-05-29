from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import CycleTemplate, CyclePeriodDetail, QuizQuestion, UserLessonProgress, UserProfile


class EducationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")
        self.template = CycleTemplate.objects.create(
            name="Soul Cycle", cycle_type="soul"
        )
        self.period = CyclePeriodDetail.objects.create(
            cycle_template=self.template,
            period_name="Period 1",
            start_value=101,
            end_value=331,
            description="Test",
            recommendations="Reflect",
            color="orange",
        )

    def test_education_hub_loads(self):
        resp = self.client.get(reverse("education"))
        self.assertEqual(resp.status_code, 200)

    def test_education_detail_loads(self):
        resp = self.client.get(
            reverse("education_detail", args=["soul"])
        )
        self.assertEqual(resp.status_code, 200)

    def test_education_period_detail_loads(self):
        resp = self.client.get(
            reverse("education_period_detail", args=["soul", self.period.id])
        )
        self.assertEqual(resp.status_code, 200)

    def test_education_detail_unknown_type_404(self):
        resp = self.client.get(
            reverse("education_detail", args=["invalid_type"])
        )
        self.assertEqual(resp.status_code, 404)

    def test_quiz_get_loads(self):
        resp = self.client.get(
            reverse("education_quiz", args=[self.period.id])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Knowledge Check")

    def test_quiz_post_correct_answer(self):
        QuizQuestion.objects.create(
            question="Test question?",
            option_a="Answer A",
            option_b="Correct B",
            correct_answer="B",
            explanation="Because B is right",
            cycle_period=self.period,
        )
        resp = self.client.post(
            reverse("education_quiz", args=[self.period.id]),
            {"answer": "B"},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["correct"])
        self.assertIn("correct_answer", data)

    def test_quiz_post_wrong_answer(self):
        QuizQuestion.objects.create(
            question="Test question?",
            option_a="Answer A",
            option_b="Correct B",
            correct_answer="B",
            explanation="Because B is right",
            cycle_period=self.period,
        )
        resp = self.client.post(
            reverse("education_quiz", args=[self.period.id]),
            {"answer": "A"},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertFalse(data["correct"])

    def test_quiz_marks_progress_completed(self):
        q = QuizQuestion.objects.create(
            question="Test?",
            option_a="A", option_b="B",
            correct_answer="B", explanation="Right",
            cycle_period=self.period,
        )
        self.client.post(
            reverse("education_quiz", args=[self.period.id]),
            {"answer": "B"},
        )
        progress = UserLessonProgress.objects.get(
            user=self.user, cycle_period=self.period
        )
        self.assertTrue(progress.completed)
        self.assertEqual(progress.quiz_score, 100)


class JournalViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")

    def test_journal_list_loads(self):
        resp = self.client.get(reverse("journal_list"))
        self.assertEqual(resp.status_code, 200)

    def test_journal_create(self):
        resp = self.client.post(reverse("journal_create"), {
            "content": "Test journal entry",
            "mood": 3,
        })
        self.assertRedirects(resp, reverse("journal_list"))
        self.assertContains(
            self.client.get(reverse("journal_list")),
            "Test journal entry",
        )

    def test_journal_delete(self):
        from .models import JournalEntry
        entry = JournalEntry.objects.create(
            user=self.user, content="To be deleted", mood=3
        )
        resp = self.client.post(
            reverse("journal_delete", args=[entry.pk])
        )
        self.assertRedirects(resp, reverse("journal_list"))
        self.assertEqual(JournalEntry.objects.count(), 0)

    def test_journal_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse("journal_list"))
        self.assertEqual(resp.status_code, 302)


class AuthViewTests(TestCase):
    def test_signup_creates_user_and_profile(self):
        resp = self.client.post(reverse("signup"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "testpassword123!",
            "password2": "testpassword123!",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        user = User.objects.get(username="newuser")
        self.assertTrue(hasattr(user, "userprofile"))
        self.assertEqual(user.email, "newuser@example.com")
        self.assertFalse(user.userprofile.email_verified)
        self.assertIsNotNone(user.userprofile.verification_token)

    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse("dashboard"))
        self.assertEqual(resp.status_code, 302)

    def test_visualizations_requires_login(self):
        resp = self.client.get(reverse("visualizations"))
        self.assertEqual(resp.status_code, 302)

    def test_alerts_requires_login(self):
        resp = self.client.get(reverse("alerts"))
        self.assertEqual(resp.status_code, 302)

    def test_verify_email_valid_token(self):
        user = User.objects.create_user(username="verifyuser", email="v@example.com", password="pass123")
        profile = user.userprofile
        token = profile.generate_verification_token()
        resp = self.client.get(reverse("verify_email", args=[token]))
        self.assertRedirects(resp, reverse("login"))
        profile.refresh_from_db()
        self.assertTrue(profile.email_verified)
        self.assertEqual(profile.verification_token, '')

    def test_verify_email_already_verified(self):
        user = User.objects.create_user(username="already", email="a@example.com", password="pass123")
        profile = user.userprofile
        token = profile.generate_verification_token()
        profile.email_verified = True
        profile.save(update_fields=['email_verified'])
        resp = self.client.get(reverse("verify_email", args=[token]))
        self.assertRedirects(resp, reverse("login"))

    def test_verify_email_invalid_token(self):
        resp = self.client.get(reverse("verify_email", args=["bogus-token"]))
        self.assertEqual(resp.status_code, 404)
