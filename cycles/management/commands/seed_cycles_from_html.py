from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate, CyclePeriodDetail

class Command(BaseCommand):
    help = 'Seeds initial cycle data from Cycles of Life Mastery.html'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding cycle data...'))

        # Daily Cycle Data
        daily_periods_data = [
            {
                "name": "Morning",
                "time": "6:00 AM - 9:26 AM",
                "description": "The Morning Period is for new beginnings, planning, and mental work. It is an ideal time for tasks that require concentration and clear thinking.",
                "recommendations": [
                    "Plan your day and set goals",
                    "Work on tasks requiring focus",
                    "Read or study new material",
                    "Meditate or journal"
                ],
                "color": "blue"
            },
            {
                "name": "Active",
                "time": "9:26 AM - 12:52 PM",
                "description": "The Active Period is for action and execution. It's the most favorable time for physical and business activities that require energy and direct effort.",
                "recommendations": [
                    "Hold important meetings",
                    "Work on physical tasks",
                    "Make business decisions",
                    "Engage in negotiations"
                ],
                "color": "green"
            },
            {
                "name": "Rest",
                "time": "12:52 PM - 4:18 PM",
                "description": "The Period of Rest is for consolidation and rejuvenation. This is a time to review work, rest, and gather energy for the next phase.",
                "recommendations": [
                    "Take a lunch break",
                    "Review morning work",
                    "Do lighter tasks",
                    "Take a short walk"
                ],
                "color": "yellow"
            },
            {
                "name": "Fulfillment",
                "time": "4:18 PM - 7:44 PM",
                "description": "The Period of Fulfillment is when the day's efforts begin to bear fruit. It's a favorable time for completing tasks and seeing results.",
                "recommendations": [
                    "Wrap up projects",
                    "Complete pending tasks",
                    "Review accomplishments",
                    "Prepare for evening"
                ],
                "color": "orange"
            },
            {
                "name": "Preparation",
                "time": "7:44 PM - 11:10 PM",
                "description": "The Period of Preparation is for introspection and preparing for the next day. It is a time for quiet reflection and creative thinking.",
                "recommendations": [
                    "Journal about your day",
                    "Plan for tomorrow",
                    "Engage in creative activities",
                    "Spend time with family"
                ],
                "color": "purple"
            },
            {
                "name": "Dreams",
                "time": "11:10 PM - 2:36 AM",
                "description": "The Period of Dreams is for deep rest and subconscious activity. The book suggests this is a time when the subconscious mind is most active.",
                "recommendations": [
                    "Go to sleep",
                    "Avoid screens before bed",
                    "Practice relaxation techniques",
                    "Keep a dream journal"
                ],
                "color": "indigo"
            },
            {
                "name": "Introspection",
                "time": "2:36 AM - 6:00 AM",
                "description": "The Period of Introspection is for profound spiritual and creative thought. This is a time for the mind to work on complex problems.",
                "recommendations": [
                    "Sleep for physical restoration",
                    "If awake, meditate or contemplate",
                    "Work on creative problems",
                    "Write down insights"
                ],
                "color": "gray"
            }
        ]

        # Yearly Cycle Data
        yearly_periods_data = [
            {
                "name": "Action",
                "days": "1-52",
                "description": "The Period of Action is the most active time of the year. This is when new projects and undertakings should be initiated.",
                "recommendations": [
                    "Start new projects and initiatives",
                    "Set ambitious goals for the year",
                    "Network and make new connections",
                    "Take calculated risks"
                ],
                "color": "purple"
            },
            {
                "name": "Stabilization",
                "days": "53-104",
                "description": "The Period of Stabilization is a time to solidify what was started in the first period. Focus on building and strengthening foundations.",
                "recommendations": [
                    "Strengthen existing projects",
                    "Improve systems and processes",
                    "Focus on quality and details",
                    "Build deeper relationships"
                ],
                "color": "blue"
            },
            {
                "name": "Rejuvenation",
                "days": "105-156",
                "description": "The Period of Rejuvenation is for rest and recovery. This is a time to step back, recharge, and avoid major new undertakings.",
                "recommendations": [
                    "Take time for self-care",
                    "Review and reflect on progress",
                    "Recharge your energy",
                    "Avoid starting new big projects"
                ],
                "color": "green"
            },
            {
                "name": "Fruition",
                "days": "157-208",
                "description": "The Period of Fruition is when the seeds planted earlier in the year come to fruition. This is a time for reaping rewards and success.",
                "recommendations": [
                    "Celebrate achievements",
                    "Harvest results of your work",
                    "Share your successes",
                    "Enjoy the fruits of your labor"
                ],
                "color": "yellow"
            },
            {
                "name": "Reflection",
                "days": "209-260",
                "description": "The Period of Reflection is a time for introspection. This is when the user should review the year and contemplate future goals.",
                "recommendations": [
                    "Review the year's progress",
                    "Analyze what worked and didn't",
                    "Consider future directions",
                    "Journal about lessons learned"
                ],
                "color": "orange"
            },
            {
                "name": "Transition",
                "days": "261-312",
                "description": "The Period of Transition is for letting go of the old and preparing for the new cycle ahead.",
                "recommendations": [
                    "Complete unfinished business",
                    "Release what no longer serves you",
                    "Prepare mentally for new cycle",
                    "Tidy up physical and digital spaces"
                ],
                "color": "red"
            },
            {
                "name": "Preparation",
                "days": "313-365",
                "description": "The Period of Preparation is the final phase before the new birthday. This is the time to prepare mentally and physically for the new year.",
                "recommendations": [
                    "Set intentions for next year",
                    "Plan goals and projects",
                    "Prepare your environment",
                    "Get physically and mentally ready"
                ],
                "color": "indigo"
            }
        ]

        # Soul Cycle Data
        soul_periods_data = [
            {
                "name": "Self-Realization",
                "dates": "March 22 - May 12",
                "description": "The Period of Self-Realization is a time for personal growth, creativity, and the development of new ideas.",
                "recommendations": [
                    "Explore new interests",
                    "Start creative projects",
                    "Focus on personal development",
                    "Set personal growth goals"
                ],
                "color": "orange"
            },
            {
                "name": "Integration",
                "dates": "May 13 - July 3",
                "description": "The Period of Integration is when new ideas and inspirations are integrated into daily life. This is a time for putting plans into action.",
                "recommendations": [
                    "Implement new habits",
                    "Apply learned knowledge",
                    "Make practical changes",
                    "Balance inspiration with action"
                ],
                "color": "yellow"
            },
            {
                "name": "Consolidation",
                "dates": "July 4 - August 24",
                "description": "The Period of Consolidation is a time to solidify relationships and professional connections. It's about strengthening bonds.",
                "recommendations": [
                    "Strengthen important relationships",
                    "Network and build connections",
                    "Focus on teamwork",
                    "Reconnect with old friends"
                ],
                "color": "green"
            },
            {
                "name": "Release",
                "dates": "August 25 - October 15",
                "description": "The Period of Release is a time to let go of old habits and negative influences that no longer serve a purpose.",
                "recommendations": [
                    "Identify limiting habits",
                    "Practice forgiveness",
                    "Declutter physical spaces",
                    "Release emotional baggage"
                ],
                "color": "blue"
            },
            {
                "name": "Regeneration",
                "dates": "October 16 - December 5",
                "description": "The Period of Regeneration is a time of spiritual growth and renewal. It's an excellent time for introspection and personal development.",
                "recommendations": [
                    "Meditate and reflect",
                    "Engage in spiritual practices",
                    "Focus on inner growth",
                    "Practice gratitude"
                ],
                "color": "indigo"
            },
            {
                "name": "Harmony",
                "dates": "December 6 - January 25",
                "description": "The Period of Harmony is a time for finding balance in all aspects of life, including work, family, and personal time.",
                "recommendations": [
                    "Balance work and personal life",
                    "Spend time with loved ones",
                    "Practice stress management",
                    "Find equilibrium in all areas"
                ],
                "color": "purple"
            },
            {
                "name": "Preparation",
                "dates": "January 26 - March 21",
                "description": "The Period of Preparation is the final phase before the new solar year. This is a time to prepare for new beginnings and spiritual growth.",
                "recommendations": [
                    "Set intentions for new cycle",
                    "Plan goals and projects",
                    "Prepare your environment",
                    "Clear space for new energy"
                ],
                "color": "red"
            }
        ]

        # Seed Daily Cycle
        daily_cycle, created = CycleTemplate.objects.get_or_create(name='Daily Cycle', cycle_type='daily')
        for i, period_data in enumerate(daily_periods_data):
            start_hour, start_minute = map(int, period_data['time'].split(' - ')[0].replace(' AM', '').replace(' PM', '').split(':'))
            end_hour, end_minute = map(int, period_data['time'].split(' - ')[1].replace(' AM', '').replace(' PM', '').split(':'))
            
            # Convert to 24-hour format for consistent storage
            if 'PM' in period_data['time'].split(' - ')[0] and start_hour != 12: start_hour += 12
            if 'AM' in period_data['time'].split(' - ')[0] and start_hour == 12: start_hour = 0
            if 'PM' in period_data['time'].split(' - ')[1] and end_hour != 12: end_hour += 12
            if 'AM' in period_data['time'].split(' - ')[1] and end_hour == 12: end_hour = 0

            start_value = start_hour * 60 + start_minute
            end_value = end_hour * 60 + end_minute

            CyclePeriodDetail.objects.get_or_create(
                cycle_template=daily_cycle,
                period_name=period_data['name'],
                defaults={
                    'start_value': start_value,
                    'end_value': end_value,
                    'description': period_data['description'],
                    'recommendations': '; '.join(period_data['recommendations']),
                    'color': period_data['color'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Daily Cycle seeded.'))

        # Seed Yearly Cycle
        yearly_cycle, created = CycleTemplate.objects.get_or_create(name='Yearly Cycle', cycle_type='yearly')
        for i, period_data in enumerate(yearly_periods_data):
            start_day, end_day = map(int, period_data['days'].split('-'))
            CyclePeriodDetail.objects.get_or_create(
                cycle_template=yearly_cycle,
                period_name=period_data['name'],
                defaults={
                    'start_value': start_day,
                    'end_value': end_day,
                    'description': period_data['description'],
                    'recommendations': '; '.join(period_data['recommendations']),
                    'color': period_data['color'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Yearly Cycle seeded.'))

        # Seed Soul Cycle
        soul_cycle, created = CycleTemplate.objects.get_or_create(name='Soul Cycle', cycle_type='soul')
        # For soul cycle, we'll store month and day as start_value and end_value
        # e.g., March 22 - May 12 -> start_value = 322, end_value = 512
        # This is a simplification and might need more robust date handling later
        for i, period_data in enumerate(soul_periods_data):
            start_month_str, start_day_str = period_data['dates'].split(' - ')[0].split(' ')
            end_month_str, end_day_str = period_data['dates'].split(' - ')[1].split(' ')

            month_map = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            }

            start_value = month_map[start_month_str] * 100 + int(start_day_str)
            end_value = month_map[end_month_str] * 100 + int(end_day_str)

            CyclePeriodDetail.objects.get_or_create(
                cycle_template=soul_cycle,
                period_name=period_data['name'],
                defaults={
                    'start_value': start_value,
                    'end_value': end_value,
                    'description': period_data['description'],
                    'recommendations': '; '.join(period_data['recommendations']),
                    'color': period_data['color'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Soul Cycle seeded.'))

        self.stdout.write(self.style.SUCCESS('Cycle data seeding complete.'))