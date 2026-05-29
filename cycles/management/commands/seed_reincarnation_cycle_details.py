from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate, CyclePeriodDetail
import json

class Command(BaseCommand):
    help = 'Seeds the database with detailed descriptions for the Reincarnation Cycle.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding Reincarnation Cycle details...'))

        # Create or get the main Reincarnation Cycle template
        reincarnation_cycle_template, created = CycleTemplate.objects.update_or_create(
            name='Reincarnation Cycle',
            cycle_type='reincarnation',
            defaults={'description': "The cycle of reincarnation, representing the soul's journey through various stages of existence. Note: The descriptions are an interpretation of the principles in the book and not a direct quote."}
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created "Reincarnation Cycle" template.'))
        else:
            self.stdout.write(self.style.SUCCESS('Found existing "Reincarnation Cycle" template.'))

        reincarnation_cycle_periods = [
            {
                "period_name": "Period 1: Childhood",
                "start_value": 1,
                "end_value": 2190,
                "description": "Childhood and the soul's descent into the body. The personality is latent.",
                "recommendations": json.dumps({'summary': 'The beginning of a new life.'})
            },
            {
                "period_name": "Period 2: Adolescence",
                "start_value": 2191,
                "end_value": 4745,
                "description": "Adolescence and the awakening of personality. The ego begins to assert itself.",
                "recommendations": json.dumps({'summary': 'The emergence of the ego.'})
            },
            {
                "period_name": "Period 3: Early Adulthood",
                "start_value": 4746,
                "end_value": 7670,
                "description": "Early adulthood and the soul's struggle for expression. The personality is dominant.",
                "recommendations": json.dumps({'summary': 'The struggle for self-expression.'})
            },
            {
                "period_name": "Period 4: Maturity",
                "start_value": 7671,
                "end_value": 10950,
                "description": "Maturity and the soul's search for meaning. The personality begins to yield to the soul.",
                "recommendations": json.dumps({'summary': 'The search for meaning.'})
            },
            {
                "period_name": "Period 5: Mid-Life",
                "start_value": 10951,
                "end_value": 15330,
                "description": "Mid-life and the soul's illumination. The personality is now a vehicle for the soul.",
                "recommendations": json.dumps({'summary': "The soul's illumination."})
            },
            {
                "period_name": "Period 6: Later Life",
                "start_value": 15331,
                "end_value": 20075,
                "description": "Later life and the soul's detachment from the physical world. The personality is transcended.",
                "recommendations": json.dumps({'summary': 'Detachment from the physical.'})
            },
            {
                "period_name": "Period 7: Old Age",
                "start_value": 20076,
                "end_value": 25550,
                "description": "Old age and the soul's return to its source. The personality is dissolved.",
                "recommendations": json.dumps({'summary': 'Return to the source.'})
            },
            {
                "period_name": "Period 8: Spiritual Journey",
                "start_value": 25551,
                "end_value": 29200,
                "description": "The soul's journey through the spiritual worlds. The personality is a distant memory.",
                "recommendations": json.dumps({'summary': 'The spiritual journey.'})
            },
            {
                "period_name": "Period 9: Assimilation",
                "start_value": 29201,
                "end_value": 32850,
                "description": "The soul's assimilation of its earthly experiences. The personality is completely absorbed.",
                "recommendations": json.dumps({'summary': 'Assimilation of experiences.'})
            },
            {
                "period_name": "Period 10: Choosing a New Destiny",
                "start_value": 32851,
                "end_value": 36500,
                "description": "The soul's choice of a new destiny. The personality is a seed of future potential.",
                "recommendations": json.dumps({'summary': 'Choosing a new destiny.'})
            },
            {
                "period_name": "Period 11: Preparation for Rebirth",
                "start_value": 36501,
                "end_value": 40150,
                "description": "The soul's preparation for rebirth. The personality is a blueprint for the new life.",
                "recommendations": json.dumps({'summary': 'Preparation for rebirth.'})
            },
            {
                "period_name": "Period 12: Descent into a New Body",
                "start_value": 40151,
                "end_value": 43800,
                "description": "The soul's descent into a new body. The personality is a fresh canvas.",
                "recommendations": json.dumps({'summary': 'Descent into a new body.'})
            }
        ]

        for period_data in reincarnation_cycle_periods:
            CyclePeriodDetail.objects.update_or_create(
                cycle_template=reincarnation_cycle_template,
                period_name=period_data['period_name'],
                defaults={
                    'start_value': period_data['start_value'],
                    'end_value': period_data['end_value'],
                    'description': period_data['description'],
                    'recommendations': period_data['recommendations']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded detailed descriptions for the Reincarnation Cycle.'))