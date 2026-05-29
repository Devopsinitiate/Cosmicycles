from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate, CyclePeriodDetail

class Command(BaseCommand):
    help = 'Seeds business, health, and reincarnation cycle data from PDF content.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding PDF-based cycle data...'))

        # Business Cycle Data (from Chapter 7)
        business_periods_data = [
            {
                "name": "Period No. 1",
                "description": "Good for promotions, securing approval, favor, recognition, and general goodwill. Not as good for direct sales. Excellent for soliciting endorsements, widespread publicity, dealing with government officials, judges, senators, congressmen. Securing political influence and cooperation.",
                "recommendations": "Push yourself forward with discrimination and determination.",
                "start_value": 1,
                "end_value": 52,
                "color": "blue"
            },
            {
                "name": "Period No. 2",
                "description": "Good for temporary changes (employees, business practice, locations), short-time plans. Unfavorable for new agreements, contracts unless written and sealed. Good for building business friendships, contacting new customers. Favorable for movable things, freight, automobiles, public conveyances, liquids, chemicals, milk, water.",
                "recommendations": "Avoid starting permanent things.",
                "start_value": 53,
                "end_value": 104,
                "color": "green"
            },
            {
                "name": "Period No. 3",
                "description": "Period of construction and energizing power. Good for pushing business to its utmost. Excellent for things requiring physical energy, effort, endurance, vitality, determination, and persistency. Good for overcoming obstacles. Excellent for starting things with a \"bang\" (great impulse). Good for dealing with army, navy, military engineering, munitions, machinery, iron, steel, cutlery, sharp instruments, electrical machinery, furnaces, fire.",
                "recommendations": "Avoid misspent energy or applying without discrimination. Watch out for dangerous accidents, disasters, troubles from enemies, fires, explosions.",
                "start_value": 105,
                "end_value": 156,
                "color": "yellow"
            },
            {
                "name": "Period No. 4",
                "description": "Good for large advertising campaigns (nationwide or local). Excellent for drawing up new contracts, agreements, papers of incorporation, documents, transfers. Good for dealing with newspapermen, diplomats, arbitrators.",
                "recommendations": "Be careful of deception by word of mouth or writing, forgeries, tricky agreements.",
                "start_value": 157,
                "end_value": 208,
                "color": "orange"
            },
            {
                "name": "Period No. 5",
                "description": "Period of growth and financial success. Good for seeking investment, securing credit, extending payment times. Best period for selling and actual distribution. Excellent for collecting bad debts, bringing matters to court. Good for promotion into foreign lands, international matters. Good for dealing with railroad, railway, electric companies, and things catering to public pleasure/happiness.",
                "recommendations": "Avoid dealing with meat products on a large scale, or marine affairs (unsuccessful).",
                "start_value": 209,
                "end_value": 260,
                "color": "purple"
            },
            {
                "name": "Period No. 6",
                "description": "Holiday of the year. Time for pleasure, amusement, relaxation, entertainment. Business can still prosper. Good for dealing with art world, music, poetry, sculpting, artists' materials, women's clothing, adornments, beauty preparations, high-grade shoes, hosiery, evening wraps, hats, luxurious automobiles, oriental rugs, antique furniture, fine books, expensive musical instruments, concerts, operas. Good for making acquaintance with customers, intimate contacts. Good for collecting money, buying stocks/bonds, promoting finances through conservative stocks.",
                "recommendations": "Short journeys are happy and successful, but not long voyages or water voyages.",
                "start_value": 261,
                "end_value": 312,
                "color": "indigo"
            },
            {
                "name": "Period No. 7",
                "description": "Critical and disruptive period. Reconstruction period. Changes of a \"tearing down\" nature. Unfavorable for starting new lines of activity or heavy advertising for new departments. Good for bringing contemplated changes or tearing down processes to issue. Mind apt to be despondent, discouraged, pessimistic. Influences are subtle. Good for dealing with elderly persons, judges, referees, advisers. Guarded attitude, extreme caution, diplomacy. Conserve activities, hold steady.",
                "recommendations": "Do not start new things. Do not go too heavily into advertising for new departments. Avoid new alliances, affiliations, partnerships, agreements, contracts.",
                "start_value": 313,
                "end_value": 365,
                "color": "red"
            }
        ]

        # Seed Business Cycle
        business_cycle, created = CycleTemplate.objects.get_or_create(name='Business Cycle', cycle_type='business')
        for period_data in business_periods_data:
            CyclePeriodDetail.objects.get_or_create(
                cycle_template=business_cycle,
                period_name=period_data['name'],
                defaults={
                    'start_value': period_data['start_value'],
                    'end_value': period_data['end_value'],
                    'description': period_data['description'],
                    'recommendations': period_data['recommendations'],
                    'color': period_data['color'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Business Cycle seeded.'))

        # Health Cycle Data (from Chapter 9)
        health_periods_data = [
            {
                "name": "Period No. 1",
                "description": "Vitality and constitutional health should be at its best. Good for increasing and strengthening health by normal living. Plenty of outdoor walking, good air, drinking plenty of water, eating proper foods. Avoid overheating foods, starches, raw/rare meats. Eyes should be guarded. Good period to start operations or health building systems.",
                "recommendations": "Start health building systems. Guard eyes against overuse or bright lights.",
                "start_value": 1,
                "end_value": 52,
                "color": "blue"
            },
            {
                "name": "Period No. 2",
                "description": "Many light and temporary physical conditions may affect the body, and passing emotional conditions affect the mind. Temporary trouble with stomach, bowels, bloodstream, nerves. Conditions come quickly, last a few days, and pass away quickly. Apt to be days with headaches, upset stomachs, eye/ear trouble, catarrh, coughs, mild colds, aches/pains. Influences bring rapid changes.",
                "recommendations": "Give immediate attention to conditions. Be cheerful and do not dwell on temporary conditions.",
                "start_value": 53,
                "end_value": 104,
                "color": "green"
            },
            {
                "name": "Period No. 3",
                "description": "Accidents may happen, sudden operations (minor or major). Suffering by fire or injury through sharp instruments, falls, or sudden blows more likely. Tendency toward colds, often from overeating or overheating. Bloodstream should be kept clean and bowels active. Blood pressure should be watched. Abnormal strain may cause breakdown.",
                "recommendations": "Be careful of food, do not overeat. Keep body normally warm. Avoid overwork or strain.",
                "start_value": 105,
                "end_value": 156,
                "color": "yellow"
            },
            {
                "name": "Period No. 4",
                "description": "Nervous system tried to its utmost. Many tendencies toward nervousness, restlessness, uneasiness. Too much study, reading, planning, or mind use brings definite reactions. Fretfulness and nervousness may affect digestion, stomach, nervous heart.",
                "recommendations": "More sleep and rest required. Forced to relax and rest to avoid mental breakdown.",
                "start_value": 157,
                "end_value": 208,
                "color": "orange"
            },
            {
                "name": "Period No. 5",
                "description": "Good period for health. Especially good if normal living is indulged. Great outdoors utilized for deep breathing, long walks, good exercise. Tendency to overindulge in pleasures of the flesh (foods, drinks). Good for recovering from fevers, chronic conditions. Mental suggestions, metaphysical principles, right thinking more effective.",
                "recommendations": "Avoid overindulgence. Utilize outdoor activities. Focus on mental and metaphysical healing.",
                "start_value": 209,
                "end_value": 260,
                "color": "purple"
            },
            {
                "name": "Period No. 6",
                "description": "Overindulgence should be carefully avoided (work, mental strain, eating, pleasures). Skin, throat, internal generative system, kidneys may be affected. Bloodstream may be lowered in vitality.",
                "recommendations": "Drink plenty of water, keep bowels open. More rest and outdoor exercise. Avoid mental strain or overwork.",
                "start_value": 261,
                "end_value": 312,
                "color": "indigo"
            },
            {
                "name": "Period No. 7",
                "description": "Chronic or lingering conditions often contracted. Difficult to overcome. Be careful of catching colds or contagious fevers. Mind and nature apt to be despondent. Not a good time for medicine or operations unless emergency or long-term. Eyes, ears, senses may be affected.",
                "recommendations": "Avoid places where contagious things may be contacted. Do not let colds or conditions linger. Seek proper expert attention.",
                "start_value": 313,
                "end_value": 365,
                "color": "red"
            }
        ]

        # Seed Health Cycle
        health_cycle, created = CycleTemplate.objects.get_or_create(name='Health Cycle', cycle_type='health')
        for period_data in health_periods_data:
            CyclePeriodDetail.objects.get_or_create(
                cycle_template=health_cycle,
                period_name=period_data['name'],
                defaults={
                    'start_value': period_data['start_value'],
                    'end_value': period_data['end_value'],
                    'description': period_data['description'],
                    'recommendations': period_data['recommendations'],
                    'color': period_data['color'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Health Cycle seeded.'))

        # Reincarnation Cycle Data (from Chapter 17)
        # The book describes this as a very long cycle (approx 144 years) divided into 7 periods.
        # The descriptions are more about personality traits and life lessons.
        reincarnation_periods_data = [
            {
                "name": "Period No. 1",
                "description": "Inherit a lofty nature, deep-seated desire for high public esteem. Carry lessons from previous incarnations about looking beyond commonplace things and holding high ideals. Recollections of achieving notable positions in past lives.",
                "recommendations": "Strive to live a noble life, above the commonplace. Seek public renown and approval.",
                "start_value": 1,
                "end_value": 7 * 365, # Approximately 7 years
                "color": "blue"
            },
            {
                "name": "Period No. 2",
                "description": "Physical changes take secondary place; psychic side developed. Sense of responsibility, dignity, poise, character. Attainment of psychic/psychological, mental, physiological development to assume legal responsibilities.",
                "recommendations": "Focus on developing responsibility and character. Engage in self-discovery.",
                "start_value": 7 * 365 + 1, # Approximately 7 years
                "end_value": 14 * 365, # Approximately 14 years
                "color": "green"
            },
            {
                "name": "Period No. 3",
                "description": "Development centered in emotional nature. Acquire stability, further sense of responsibility, softening of nature. Gradual activity in higher, dormant faculties (intuition, mental telepathy, unconscious psychometry). Awakening interest in music, art, language, religious/higher things.",
                "recommendations": "Cultivate emotional stability and higher faculties. Engage in artistic and spiritual pursuits.",
                "start_value": 14 * 365 + 1,
                "end_value": 21 * 365,
                "color": "yellow"
            },
            {
                "name": "Period No. 4",
                "description": "Creative processes of mind most active. Ability to visualize, imagine, mentally create greatly developed. Attunement with Cosmic Consciousness and ethical standards. Greatest inventors make progress. Businessmen energetic and successful. Philosophers, avatars, mystics find sudden Cosmic Illumination.",
                "recommendations": "Engage in creative and intellectual pursuits. Seek attunement with cosmic consciousness.",
                "start_value": 21 * 365 + 1,
                "end_value": 28 * 365,
                "color": "orange"
            },
            {
                "name": "Period No. 5",
                "description": "Desire to explore, investigate, reveal great knowledge and hidden facts. Restlessness, dissatisfaction with monotony of selfish attainment. Quickens humanitarian/brotherly emotion to share with the world. Start disposing of wealth (libraries, arts, sciences, schools, expeditions). Culminating period of preceding years.",
                "recommendations": "Explore and share knowledge. Engage in humanitarian activities. Give back to the Cosmic and mankind.",
                "start_value": 28 * 365 + 1,
                "end_value": 35 * 365,
                "color": "purple"
            },
            {
                "name": "Period No. 6",
                "description": "Desire to rest, meditate, philosophically speculate. New hopes, desires, viewpoint, goals. Mind turned to religion/philosophy and humanitarian activities (consolation, peace, help to downtrodden).",
                "recommendations": "Focus on spiritual and philosophical growth. Engage in acts of compassion and service.",
                "start_value": 35 * 365 + 1,
                "end_value": 42 * 365,
                "color": "indigo"
            },
            {
                "name": "Period No. 7",
                "description": "Tendency toward further retirement from personal/selfish ambition. Gradual lessening of vitality/physical prowess, compensated by highly attuned psychic/mental nature. Pendulum swings from physical to spiritual being. Physical body loses power to combat disease.",
                "recommendations": "Embrace spiritual development. Prioritize mental and psychic well-being over physical exertion.",
                "start_value": 42 * 365 + 1,
                "end_value": 144 * 365, # The book mentions approx 144 years for the full cycle
                "color": "red"
            }
        ]

        # Seed Reincarnation Cycle
        reincarnation_cycle, created = CycleTemplate.objects.get_or_create(name='Reincarnation Cycle', cycle_type='reincarnation')
        for period_data in reincarnation_periods_data:
            CyclePeriodDetail.objects.get_or_create(
                cycle_template=reincarnation_cycle,
                period_name=period_data['name'],
                defaults={
                    'start_value': period_data['start_value'],
                    'end_value': period_data['end_value'],
                    'description': period_data['description'],
                    'recommendations': period_data['recommendations'],
                    'color': period_data['color'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Reincarnation Cycle seeded.'))

        self.stdout.write(self.style.SUCCESS('All PDF-based cycle data seeding complete.'))