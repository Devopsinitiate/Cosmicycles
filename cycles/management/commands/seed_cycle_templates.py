from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate

class Command(BaseCommand):
    help = 'Seed CycleTemplate entries with basic descriptions'

    def handle(self, *args, **options):
        templates = [
            {'name': 'Human Life Cycle', 'cycle_type': 'human', 'description': 'Seven-year periods that shape human development from birth through maturity.'},
            {'name': 'Daily Cycle - Monday', 'cycle_type': 'daily', 'description': 'Seven daily periods for Monday with specific energies and recommendations.'},
            {'name': 'Daily Cycle - Tuesday', 'cycle_type': 'daily', 'description': 'Seven daily periods for Tuesday with specific energies and recommendations.'},
            {'name': 'Daily Cycle - Wednesday', 'cycle_type': 'daily', 'description': 'Seven daily periods for Wednesday with specific energies and recommendations.'},
            {'name': 'Daily Cycle - Thursday', 'cycle_type': 'daily', 'description': 'Seven daily periods for Thursday with specific energies and recommendations.'},
            {'name': 'Daily Cycle - Friday', 'cycle_type': 'daily', 'description': 'Seven daily periods for Friday with specific energies and recommendations.'},
            {'name': 'Daily Cycle - Saturday', 'cycle_type': 'daily', 'description': 'Seven daily periods for Saturday with specific energies and recommendations.'},
            {'name': 'Daily Cycle - Sunday', 'cycle_type': 'daily', 'description': 'Seven daily periods for Sunday with specific energies and recommendations.'},
            {'name': 'Yearly Cycle', 'cycle_type': 'yearly', 'description': 'A 364-day cycle divided into 7 periods of approximately 52 days each, starting from your birthday.'},
            {'name': 'Business Cycle', 'cycle_type': 'business', 'description': 'A 364-day business cycle divided into 7 periods of approximately 52 days each, starting from your business start date.'},
            {'name': 'Health Cycle', 'cycle_type': 'health', 'description': 'An annual health cycle divided into 7 periods of approximately 52 days each.'},
            {'name': 'Soul Cycle', 'cycle_type': 'soul', 'description': 'Seven spiritual periods based on the solar year, each with A/B polarities reflecting deeper soul influences.'},
            {'name': 'Reincarnation Cycle', 'cycle_type': 'reincarnation', 'description': 'Long-term karmic cycles spanning years or decades, reflecting soul progress across incarnations.'},
        ]

        created = 0
        for t in templates:
            obj, was_created = CycleTemplate.objects.update_or_create(
                name=t['name'],
                defaults={'cycle_type': t['cycle_type'], 'description': t['description']}
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Created/Updated {created} CycleTemplate entries'))
