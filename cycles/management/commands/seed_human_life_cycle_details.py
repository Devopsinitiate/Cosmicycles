from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate, CyclePeriodDetail
import json

class Command(BaseCommand):
    help = 'Seeds the database with detailed Human Life Cycle principles from the book.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding Human Life Cycle details...'))

        # Create or get the main Human Life Cycle template
        human_cycle_template, created = CycleTemplate.objects.update_or_create(
            name='Human Life Cycle',
            cycle_type='human',
            defaults={'description': 'The simple periods of human life, divided into 7-year cycles.'}
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created "Human Life Cycle" template.'))
        else:
            self.stdout.write(self.style.SUCCESS('Found existing "Human Life Cycle" template.'))

        human_life_cycle_data = [
            {
                'period_name': 'Period 1: Birth to 7th Year',
                'start_value': 0,
                'end_value': 7,
                'description': "Consider the first period of seven years. This is the time during which our babyhood and early youth occurs, and when the fundamentals of our education and cultural development are laid. It is really a period of self-discovery, as far as the objective material world and our relation to it are concerned. We learn to walk and talk, control our bodies, and relate ourselves properly to our physical and material environments.",
                'recommendations': json.dumps({'summary': 'Babyhood and early youth, self-discovery, fundamental education.', 'advice': 'Focus on foundational learning and environmental adaptation.'})
            },
            {
                'period_name': 'Period 2: 7th to 14th Year',
                'start_value': 7,
                'end_value': 14,
                'description': "In this period certain physical changes take place in our development, and the mental side of our nature takes a secondary place in the changes going on. It is just before the fulfillment of the second period that the important physical changes in both the male and female occur, preparing the child for the third stage. If these changes do not occur before the end of the second period, the child is psychologically and physiologically subnormal, and both physiology and psychology have unconsciously recognized this second period in the cycle of life.",
                'recommendations': json.dumps({'summary': 'Physical changes, mental development secondary, preparation for third stage.', 'advice': 'Support physical development and observe for subnormalities.'})
            },
            {
                'period_name': 'Period 3: 14th to 21st Year',
                'start_value': 14,
                'end_value': 21,
                'description': "In this period the physical changes drop back into secondary place together with the mental, and the psychic side of human nature is developed primarily. This brings about the sense of responsibility, giving dignity, poise, and character to the individual. It is during this process that the individual attains that degree of psychic or psychological, as well as mental and physiological development, that establishes the individual as a capable entity, qualified to assume legal responsibilities. The person who does not attain this degree by the 21st year is backward in the progress that should have been made, and is classified as subnormal.",
                'recommendations': json.dumps({'summary': 'Psychic development, sense of responsibility, character building, legal maturity.', 'advice': 'Foster responsibility, dignity, and character development.'})
            },
            {
                'period_name': 'Period 4: 21st to 28th Year',
                'start_value': 21,
                'end_value': 28,
                'description': "In this period there is a development strongly centered in the emotional nature carrying on the unfoldment of the emotional spark that was awakened in the preceding period. During these years, the individual acquires stability, a further sense of responsibility, a softening of the nature, and a gradual activity in those higher, dormant faculties known as intuition, mental telepathy, unconscious psychometry, and similar psychic faculties, together with an awakening interest in music, art, language, and what may be termed the religious and higher things in life. An absence of any manifestation of the development of these faculties during this period would indicate to the psychologist or psychiatrist a subnormal development.",
                'recommendations': json.dumps({'summary': 'Emotional development, stability, intuition, psychic faculties, interest in arts and spirituality.', 'advice': 'Encourage emotional maturity, spiritual growth, and artistic interests.'})
            },
            {
                'period_name': 'Period 5: 28th to 35th Year',
                'start_value': 28,
                'end_value': 35,
                'description': "In this period we find the creative processes of the mind most active, and the ability to visualize, imagine, and mentally create greatly developed, with a developing attunement with the Cosmic Consciousness and the ethical standards of life. It is during this period that the greatest inventors have made most progress, and the business man has become energetic and successful. It is also noteworthy that it is during this period that many of the world's greatest philosophers, avatars, and mystics found the sudden Cosmic Illumination which is called complete attunement with the Cosmic Consciousness. The greatest of these have begun their world-wide missions and written their greatest works during this period.",
                'recommendations': json.dumps({'summary': 'Creative peak, visualization, mental creation, attunement with Cosmic Consciousness, success in invention and business.', 'advice': 'Harness creative energy, pursue innovative ideas, and seek spiritual attunement.'})
            },
            {
                'period_name': 'Period 6: 35th to 42nd Year',
                'start_value': 35,
                'end_value': 42,
                'description': "In this period people enter a stage of development that induces the desire to explore, investigate, and reveal great knowledge and the hidden facts of life. A restlessness comes into their nature which makes them dissatisfied with the monotony of selfish and personal attainment, and quickens in their being the humanitarian and brotherly emotion which makes them want to share what they have with the world. Yet even if they have little else than time and knowledge to share, they want to explore or discover and bring these revealed things to the masses for their benefit. It is during this period that people start disposing of great wealth that they have accumulated or inherited by building libraries or contributing to the arts, the sciences, schools, colleges, universities, or explorative and inventive expeditions and speculations. It is truly the culminating period of all the years that have preceded in the life of the average human being, and starts the system of compensation in the average individual’s life whereby the individual feels the need of returning to the Cosmic and to mankind some of the benefits he has enjoyed.",
                'recommendations': json.dumps({'summary': 'Desire to explore, investigate, share knowledge, humanitarianism, dissatisfaction with selfish pursuits.', 'advice': 'Embrace exploration, share knowledge, and engage in humanitarian efforts.'})
            },
            {
                'period_name': 'Period 7: 42nd to 49th Year',
                'start_value': 42,
                'end_value': 49,
                'description': "In this period the desire to rest, meditate, and philosophically speculate builds up in the human being a new chapter, which unfolds strongly and uniquely in each case until the individual becomes a new person with new hopes, new desires, a new viewpoint in life, and a new goal and ideal toward which to labor. The mind is turned more strongly toward religion and philosophy than to business. It is also turned to those humanitarian activities that bring consolation and peace, by giving help, health, and happiness to the downtrodden, disconsolate, or despondent. So surely does this period work out in the average person’s life, to some degree, that one may easily judge the approximate age of any eminent character by noting the tendencies of his habits and the trend of his thoughts, even when such a person is in very moderate circumstances and can do nothing more than wish he were able to do the things that he has in his mind and heart.",
                'recommendations': json.dumps({'summary': 'Rest, meditation, philosophical speculation, new hopes, desires, viewpoints, and humanitarian focus.', 'advice': 'Engage in introspection, philosophical study, and compassionate service.'})
            },
            {
                'period_name': 'Period 8: 49th to 56th Year',
                'start_value': 49,
                'end_value': 56,
                'description': "In this period we find a tendency toward further retirement from personal or selfish ambition, accompanied by a gradual lessening of the vitality and physical prowess, but compensated for by a highly attuned psychic and mental nature. Here the pendulum is beginning to swing from the building up of a physical being to the building up of a spiritual being, and for this reason the physical body begins to lose its power to combat disease and to surmount the strains of accidents and undue strains upon the vitality. Vital statistics prepared by insurance companies and government bureaus plainly show the great changes in the physical body which take place during this period and the preceding one as the pendulum begins to swing from the physical to the spiritual.",
                'recommendations': json.dumps({'summary': 'Retirement from ambition, lessening vitality, increased psychic and mental attunement, shift from physical to spiritual focus.', 'advice': 'Embrace spiritual growth and adapt to changing physical capabilities.'})
            },
            {
                'period_name': 'Period 9: 56th to 63rd Year',
                'start_value': 56,
                'end_value': 63,
                'description': "In this period there is a continuation of the conditions in the preceding period, but accompanied now by a mellowing of the mental faculties together with the weakening of the physical prowess, leaving the individual more and more a psychic and spiritual being in harmony with the entire purpose of the cycle of progression. As man is born to become a living soul, and not merely a soul-animated physical body, so he evolves, period by period, from birth to his 63rd year, from a physical being to a spiritual being, thereby approaching more closely the inevitable purpose of his existence.",
                'recommendations': json.dumps({'summary': 'Mellowing of mental faculties, weakening physical prowess, increased psychic and spiritual being, evolution towards spiritual purpose.', 'advice': 'Continue spiritual evolution and embrace the natural progression of life.'})
            },
        ]

        for data in human_life_cycle_data:
            period_detail, created = CyclePeriodDetail.objects.update_or_create(
                cycle_template=human_cycle_template,
                period_name=data['period_name'],
                defaults={
                    'start_value': data['start_value'],
                    'end_value': data['end_value'],
                    'description': data['description'],
                    'recommendations': data['recommendations']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {data['period_name']}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated {data['period_name']}"))

        self.stdout.write(self.style.SUCCESS('Human Life Cycle seeding complete.'))