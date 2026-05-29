from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate, CyclePeriodDetail

class Command(BaseCommand):
    help = 'Debug CycleTemplate and CyclePeriodDetail data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Debugging Cycle Templates and Periods ---'))
        
        cycle_templates = CycleTemplate.objects.all()
        if not cycle_templates.exists():
            self.stdout.write(self.style.ERROR('No CycleTemplate objects found in the database.'))
            self.stdout.write(self.style.WARNING('Please ensure you have seeded the database with cycle templates.'))
            return

        for template in cycle_templates:
            self.stdout.write(self.style.WARNING(f'\nCycle Template: {template.name} (Type: {template.cycle_type})'))
            self.stdout.write(f'Description: {template.description}')
            
            period_details = template.period_details.all()
            if not period_details.exists():
                self.stdout.write(self.style.ERROR(f'  No Period Details found for {template.name}.'))
            else:
                self.stdout.write(f'  Found {period_details.count()} Period Details:')
                for period in period_details:
                    self.stdout.write(f'    - {period.period_name} (Start: {period.start_value}, End: {period.end_value})')
                    self.stdout.write(f'      Raw Recommendations: {period.recommendations}')
                    self.stdout.write(f'      Description: {period.description}')

        self.stdout.write(self.style.SUCCESS('\n--- End of Debugging ---'))
