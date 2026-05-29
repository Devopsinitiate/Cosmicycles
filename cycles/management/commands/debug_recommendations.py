from django.core.management.base import BaseCommand
from cycles.models import CyclePeriodDetail

class Command(BaseCommand):
    help = 'Debug recommendations data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Debugging Recommendations ---'))
        
        periods = CyclePeriodDetail.objects.all()[:5]
        
        for period in periods:
            self.stdout.write(self.style.WARNING(f'Period: {period.period_name}'))
            self.stdout.write(f'Raw recommendations data: {period.recommendations}')
            self.stdout.write(f'Type of recommendations data: {type(period.recommendations)}')
            self.stdout.write('---')

        self.stdout.write(self.style.SUCCESS('--- End of Debugging ---'))
