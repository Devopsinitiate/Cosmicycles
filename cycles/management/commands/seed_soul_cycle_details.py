from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate, CyclePeriodDetail
import json

class Command(BaseCommand):
    help = 'Seeds the database with detailed descriptions for the Soul Cycle.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding Soul Cycle details...'))

        # Create or get the main Soul Cycle template
        soul_cycle_template, created = CycleTemplate.objects.update_or_create(
            name='Soul Cycle',
            cycle_type='soul',
            defaults={'description': 'The soul cycle, based on the solar year, divided into seven periods, each with two polarities.'}
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created "Soul Cycle" template.'))
        else:
            self.stdout.write(self.style.SUCCESS('Found existing "Soul Cycle" template.'))

        soul_cycle_periods = [
            {
                "period_name": "Period 1 - Polarity A",
                "start_value": 322, "end_value": 417,
                "description": "The first polarity of the Soul Cycle ignites the year with fiery ambition and raw leadership energy. Those born under this influence possess a natural magnetism and an unyielding drive to take charge. This is a period of initiation, where the soul's executive qualities are brought to the forefront, demanding action and purposeful direction.",
                "recommendations": json.dumps({'summary': 'Ambitious and energetic leaders.', 'advice': 'Use your energy and determination to achieve leadership roles. Your fiery constitution and strong personal magnetism are your assets.'})
            },
            {
                "period_name": "Period 1 - Polarity B",
                "start_value": 418, "end_value": 512,
                "description": "The second polarity of Period 1 tempers the fire with refinement. Here the soul expresses its determination through artistic and cultured channels. The raw leadership of Polarity A is polished into genteel influence, making this a time for subtle persuasion rather than direct command. Creative pursuits and diplomatic endeavors flourish.",
                "recommendations": json.dumps({'summary': 'Refined, determined, and artistic.', 'advice': 'Channel your determination into the fine arts and more subtle pursuits. Your genteel nature is a strength.'})
            },
            {
                "period_name": "Period 2 - Polarity A",
                "start_value": 513, "end_value": 608,
                "description": "This period highlights the soul's intellectual agility. Quick thinking, versatility, and mental adaptability are the dominant traits. The soul is drawn to activities that require rapid analysis and multi-tasking. It is a favorable time for learning new skills, engaging in stimulating conversation, and pursuing knowledge across diverse fields.",
                "recommendations": json.dumps({'summary': 'Quick-witted and versatile.', 'advice': 'Utilize your quick intellect in mentally stimulating professions. Your versatility allows you to excel in multiple areas at once.'})
            },
            {
                "period_name": "Period 2 - Polarity B",
                "start_value": 609, "end_value": 703,
                "description": "The B polarity of Period 2 turns the intellect inward toward intuition and deeper understanding. Education, law, and the arts are natural arenas for this energy. The soul's memory is sharp, and intuitive insights come readily. This is a period for study, contemplation, and developing one's inner wisdom.",
                "recommendations": json.dumps({'summary': 'Intellectual and intuitive.', 'advice': 'Your strengths lie in education, the arts, and law. Cultivate your intuitive senses and excellent memory.'})
            },
            {
                "period_name": "Period 3 - Polarity A",
                "start_value": 704, "end_value": 731,
                "description": "Adventure and exploration define this polarity. The soul feels a restless urge to push boundaries, take risks, and discover new horizons. Natural leadership emerges through bold action and a willingness to venture into the unknown. This energy supports entrepreneurs, pioneers, and those who chart new paths.",
                "recommendations": json.dumps({'summary': 'Adventurous and born leaders.', 'advice': 'Embrace your exploratory nature and leadership qualities. You are well-suited for roles that involve risk and conquest.'})
            },
            {
                "period_name": "Period 3 - Polarity B",
                "start_value": 801, "end_value": 824,
                "description": "The second polarity of Period 3 channels the adventurous spirit into dignified leadership. There is a regal bearing and a love of ceremony and tradition. Those influenced by this energy are drawn to positions of authority and public recognition. The key teaching is to wield power with grace and to guard against the pitfalls of pride.",
                "recommendations": json.dumps({'summary': 'Natural-born leaders with a regal bearing.', 'advice': 'You are destined for high office and leadership. Embrace your love of pomp and ceremony, and guard against weaknesses that could jeopardize your position.'})
            },
            {
                "period_name": "Period 4 - Polarity A",
                "start_value": 825, "end_value": 920,
                "description": "This polarity brings together intellect, artistry, and spirituality. The soul is drawn to the higher realms of thought and beauty. Educational and philosophical pursuits come naturally. There is a tendency toward idealism and vision, balanced by a need to stay grounded. Restlessness and fantasy are the shadows to watch.",
                "recommendations": json.dumps({'summary': 'Intellectual, artistic, and spiritual.', 'advice': 'You shine in educational and intellectual fields. Cultivate your artistic and spiritual tendencies. Be mindful of a tendency towards restlessness and fantasy.'})
            },
            {
                "period_name": "Period 4 - Polarity B",
                "start_value": 921, "end_value": 1015,
                "description": "Balance, logic, and aesthetic harmony define this polarity. The soul seeks equilibrium in all things and possesses a refined sense of beauty and proportion. Logical reasoning is strong, making this a favorable time for analytical work, design, and any endeavor requiring measured judgment and a steady hand.",
                "recommendations": json.dumps({'summary': 'Balanced, logical, and esthetic.', 'advice': 'Use your logical reasoning and love of balance in all that you do. Your appreciation for beauty and harmony can be a source of strength and a guide for others.'})
            },
            {
                "period_name": "Period 5 - Polarity A",
                "start_value": 1016, "end_value": 1111,
                "description": "Aggressive determination and business acumen mark this polarity. The soul is driven to achieve material success through focused effort and competitive spirit. There is a risk of rashness leading to setbacks, so patience and careful planning are advised. This energy rewards those who channel their intensity constructively.",
                "recommendations": json.dumps({'summary': 'Aggressive and determined in business.', 'advice': 'Your determination and energy make you a force in the business world. Be mindful of a tendency towards accidents and delays due to rashness.'})
            },
            {
                "period_name": "Period 5 - Polarity B",
                "start_value": 1112, "end_value": 1206,
                "description": "The B polarity of Period 5 turns toward peace, humanitarian service, and mystical understanding. The soul's aggressive edge softens into compassion and a desire to help others. Intellectual mastery now serves higher purposes. This is a time for philanthropy, spiritual study, and bringing visionary ideas into practical form.",
                "recommendations": json.dumps({'summary': 'Peaceful, humanitarian, and mystical.', 'advice': 'You are a natural peacemaker and humanitarian. Your strength lies in your mystical understanding and intellectual mastership.'})
            },
            {
                "period_name": "Period 6 - Polarity A",
                "start_value": 1207, "end_value": 101,
                "description": "This polarity brings a serious, critical, and esthetic energy. The soul becomes a natural teacher and reformer, with a keen eye for what needs improvement. There is a talent for criticism that, when applied constructively, can elevate the arts and sciences. The challenge is to avoid becoming overly harsh or judgmental.",
                "recommendations": json.dumps({'summary': 'Serious, esthetic, and critical.', 'advice': 'You have a talent for teaching and reform. Your critical eye can be a force for good in the arts and sciences.'})
            },
            {
                "period_name": "Period 6 - Polarity B",
                "start_value": 102, "end_value": 127,
                "description": "The second polarity of Period 6 lightens the critical edge with impulsiveness and entertainment. The soul's critical nature now manifests as a sharp wit and a talent for performance. Though prone to unrest and sudden changes, this energy also brings deep insight and the gift of uplifting others through humor and creativity.",
                "recommendations": json.dumps({'summary': 'Critical, impulsive, and entertaining.', 'advice': 'Your critical nature can lead to unrest, but also to a deep understanding of life. You are a wonderful friend and entertainer.'})
            },
            {
                "period_name": "Period 7 - Polarity A",
                "start_value": 128, "end_value": 223,
                "description": "Profundity, reserve, and diligence define this polarity. The soul operates best in specialized and unconventional fields, where its depth of focus can shine. Consistent effort and reliability are hallmarks. This is a time for quiet mastery, patient craftsmanship, and the kind of steady work that builds lasting foundations.",
                "recommendations": json.dumps({'summary': 'Profound, reserved, and diligent.', 'advice': 'You excel in unusual and specialized occupations. Your diligent and consistent nature makes you a valuable friend and employee.'})
            },
            {
                "period_name": "Period 7 - Polarity B",
                "start_value": 224, "end_value": 321,
                "description": "The final polarity of the Soul Cycle is dual-natured, mystical, and magnetic. The soul possesses both a talent for public engagement and a deep need for private contemplation. Magnetic personality and spiritual insight are the greatest gifts. This period closes the cycle with integration, bringing together all the polarities into a unified whole.",
                "recommendations": json.dumps({'summary': 'Dual-natured, mystical, and magnetic.', 'advice': 'You have a talent for both public life and private contemplation. Your magnetic personality and mystical tendencies are your greatest assets.'})
            }
        ]

        for period_data in soul_cycle_periods:
            CyclePeriodDetail.objects.update_or_create(
                cycle_template=soul_cycle_template,
                period_name=period_data['period_name'],
                defaults={
                    'start_value': period_data['start_value'],
                    'end_value': period_data['end_value'],
                    'description': period_data['description'],
                    'recommendations': period_data['recommendations']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded detailed descriptions for the Soul Cycle.'))