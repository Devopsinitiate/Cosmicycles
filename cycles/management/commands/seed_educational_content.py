from django.core.management.base import BaseCommand
from cycles.models import CyclePeriodDetail, GlossaryTerm, QuizQuestion

SOUL_DESCRIPTIONS = {
    "Period 1 - Polarity A": "The first polarity of the Soul Cycle ignites the year with fiery ambition and raw leadership energy. Those born under this influence possess a natural magnetism and an unyielding drive to take charge. This is a period of initiation, where the soul's executive qualities are brought to the forefront, demanding action and purposeful direction.",
    "Period 1 - Polarity B": "The second polarity of Period 1 tempers the fire with refinement. Here the soul expresses its determination through artistic and cultured channels. The raw leadership of Polarity A is polished into genteel influence, making this a time for subtle persuasion rather than direct command. Creative pursuits and diplomatic endeavors flourish.",
    "Period 2 - Polarity A": "This period highlights the soul's intellectual agility. Quick thinking, versatility, and mental adaptability are the dominant traits. The soul is drawn to activities that require rapid analysis and multi-tasking. It is a favorable time for learning new skills, engaging in stimulating conversation, and pursuing knowledge across diverse fields.",
    "Period 2 - Polarity B": "The B polarity of Period 2 turns the intellect inward toward intuition and deeper understanding. Education, law, and the arts are natural arenas for this energy. The soul's memory is sharp, and intuitive insights come readily. This is a period for study, contemplation, and developing one's inner wisdom.",
    "Period 3 - Polarity A": "Adventure and exploration define this polarity. The soul feels a restless urge to push boundaries, take risks, and discover new horizons. Natural leadership emerges through bold action and a willingness to venture into the unknown. This energy supports entrepreneurs, pioneers, and those who chart new paths.",
    "Period 3 - Polarity B": "The second polarity of Period 3 channels the adventurous spirit into dignified leadership. There is a regal bearing and a love of ceremony and tradition. Those influenced by this energy are drawn to positions of authority and public recognition. The key teaching is to wield power with grace and to guard against the pitfalls of pride.",
    "Period 4 - Polarity A": "This polarity brings together intellect, artistry, and spirituality. The soul is drawn to the higher realms of thought and beauty. Educational and philosophical pursuits come naturally. There is a tendency toward idealism and vision, balanced by a need to stay grounded. Restlessness and fantasy are the shadows to watch.",
    "Period 4 - Polarity B": "Balance, logic, and aesthetic harmony define this polarity. The soul seeks equilibrium in all things and possesses a refined sense of beauty and proportion. Logical reasoning is strong, making this a favorable time for analytical work, design, and any endeavor requiring measured judgment and a steady hand.",
    "Period 5 - Polarity A": "Aggressive determination and business acumen mark this polarity. The soul is driven to achieve material success through focused effort and competitive spirit. There is a risk of rashness leading to setbacks, so patience and careful planning are advised. This energy rewards those who channel their intensity constructively.",
    "Period 5 - Polarity B": "The B polarity of Period 5 turns toward peace, humanitarian service, and mystical understanding. The soul's aggressive edge softens into compassion and a desire to help others. Intellectual mastery now serves higher purposes. This is a time for philanthropy, spiritual study, and bringing visionary ideas into practical form.",
    "Period 6 - Polarity A": "This polarity brings a serious, critical, and esthetic energy. The soul becomes a natural teacher and reformer, with a keen eye for what needs improvement. There is a talent for criticism that, when applied constructively, can elevate the arts and sciences. The challenge is to avoid becoming overly harsh or judgmental.",
    "Period 6 - Polarity B": "The second polarity of Period 6 lightens the critical edge with impulsiveness and entertainment. The soul's critical nature now manifests as a sharp wit and a talent for performance. Though prone to unrest and sudden changes, this energy also brings deep insight and the gift of uplifting others through humor and creativity.",
    "Period 7 - Polarity A": "Profundity, reserve, and diligence define this polarity. The soul operates best in specialized and unconventional fields, where its depth of focus can shine. Consistent effort and reliability are hallmarks. This is a time for quiet mastery, patient craftsmanship, and the kind of steady work that builds lasting foundations.",
    "Period 7 - Polarity B": "The final polarity of the Soul Cycle is dual-natured, mystical, and magnetic. The soul possesses both a talent for public engagement and a deep need for private contemplation. Magnetic personality and spiritual insight are the greatest gifts. This period closes the cycle with integration, bringing together all the polarities into a unified whole.",
}

GLOSSARY_TERMS = [
    {
        "term": "Cosmic Consciousness",
        "definition": "A state of heightened awareness and understanding of the universe's underlying order and the interconnectedness of all life. In the context of the Cycles of Life, it represents the ultimate goal of aligning one's actions with cosmic rhythms.",
        "related_cycle_type": None,
        "sort_order": 1,
    },
    {
        "term": "Polarity",
        "definition": "The two complementary aspects of a single cycle period (designated A and B). Each polarity represents a different expression of the same essential energy — for example, active vs. receptive, outward vs. inward, or fiery vs. refined. Together they form a complete whole.",
        "related_cycle_type": "soul",
        "sort_order": 2,
    },
    {
        "term": "Karmic Cycle",
        "definition": "A long-term cycle of spiritual cause and effect that spans multiple lifetimes. The Reincarnation Cycle is the primary expression of karmic patterns in this system, tracking the soul's journey through distinct developmental phases from childhood through maturity and rebirth.",
        "related_cycle_type": "reincarnation",
        "sort_order": 3,
    },
    {
        "term": "Personal Magnetism",
        "definition": "An individual's natural power to attract, influence, and inspire others. In the cycle system, certain periods are associated with heightened personal magnetism, making them favorable for leadership, public speaking, and building relationships.",
        "related_cycle_type": None,
        "sort_order": 4,
    },
    {
        "term": "Cycle of Significant Hours",
        "definition": "Another name for the Daily Cycle, which divides each day into seven periods of approximately 3 hours and 25 minutes each. Each period carries a distinct energetic quality that influences the most propitious times for various activities.",
        "related_cycle_type": "daily",
        "sort_order": 5,
    },
    {
        "term": "Birthday Cycle",
        "definition": "The Yearly Cycle, which begins anew on each person's birthday. It divides the 364-day year into seven periods of 52 days each, each with its own theme and guidance. The birthday is considered the true start of the personal year.",
        "related_cycle_type": "yearly",
        "sort_order": 6,
    },
    {
        "term": "Seven-Year Periods",
        "definition": "The divisions of the Human Life Cycle, each lasting approximately seven years. These periods mark distinct phases of human development from birth through old age, each with its own physical, emotional, and spiritual focus.",
        "related_cycle_type": "human",
        "sort_order": 7,
    },
    {
        "term": "Propitious Times",
        "definition": "Favorable or auspicious moments for specific activities as determined by the current cycle period. By understanding which cycle period is active, one can choose the most harmonious time for work, rest, socializing, creative pursuits, and spiritual practice.",
        "related_cycle_type": "daily",
        "sort_order": 8,
    },
]


class Command(BaseCommand):
    help = 'Seeds educational content: soul cycle descriptions and glossary terms.'

    def handle(self, *args, **options):
        self._seed_soul_descriptions()
        self._seed_glossary()
        self._seed_quiz_questions()
        self.stdout.write(self.style.SUCCESS('Educational content seeded successfully.'))

    def _seed_soul_descriptions(self):
        updated = 0
        for period_name, description in SOUL_DESCRIPTIONS.items():
            count = CyclePeriodDetail.objects.filter(
                period_name=period_name,
                cycle_template__cycle_type='soul',
            ).update(description=description, lesson_content=description)
            if count:
                updated += 1
        self.stdout.write(f'Updated {updated} soul cycle period descriptions.')

    QUIZ_QUESTIONS = [
        {
            "period_name": "Period 1 - Polarity A",
            "cycle_type": "soul",
            "question": "What is the dominant trait of Polarity A in the first period of the Soul Cycle?",
            "option_a": "Intellectual agility and quick thinking",
            "option_b": "Fiery ambition and raw leadership energy",
            "option_c": "Peaceful contemplation and mysticism",
            "option_d": "Critical analysis and reform",
            "correct_answer": "B",
            "explanation": "Period 1 - Polarity A ignites the year with fiery ambition and raw leadership energy, demanding action and purposeful direction.",
            "difficulty": 1,
        },
        {
            "period_name": "Period 1 - Polarity B",
            "cycle_type": "soul",
            "question": "How does Polarity B of Period 1 differ from its corresponding Polarity A?",
            "option_a": "It is more aggressive and competitive",
            "option_b": "It channels determination through artistic and cultured channels",
            "option_c": "It focuses entirely on spiritual pursuits",
            "option_d": "It has no relation to Polarity A",
            "correct_answer": "B",
            "explanation": "Polarity B tempers the fire with refinement, expressing determination through artistic and cultured channels rather than direct command.",
            "difficulty": 2,
        },
        {
            "period_name": "Period 4 - Polarity A",
            "cycle_type": "soul",
            "question": "Which three elements does Period 4 - Polarity A bring together?",
            "option_a": "Wealth, power, and fame",
            "option_b": "Intellect, artistry, and spirituality",
            "option_c": "Adventure, risk, and discovery",
            "option_d": "Discipline, order, and routine",
            "correct_answer": "B",
            "explanation": "Period 4 - Polarity A draws the soul to the higher realms of thought and beauty, combining intellect, artistry, and spirituality.",
            "difficulty": 1,
        },
        {
            "period_name": "Period 7 - Polarity B",
            "cycle_type": "soul",
            "question": "What does Polarity B of Period 7 represent in the Soul Cycle?",
            "option_a": "A fresh start with new energy",
            "option_b": "The integration of all polarities into a unified whole",
            "option_c": "A period of rest and inactivity",
            "option_d": "The beginning of a new cycle",
            "correct_answer": "B",
            "explanation": "Period 7 - Polarity B closes the cycle with integration, combining a talent for public engagement with deep private contemplation.",
            "difficulty": 2,
        },
        {
            "period_name": "Morning",
            "cycle_type": "daily",
            "question": "During which daily period does the Morning period typically occur?",
            "option_a": "Midnight to dawn",
            "option_b": "Early to late morning hours",
            "option_c": "Afternoon",
            "option_d": "Evening",
            "correct_answer": "B",
            "explanation": "The Morning period spans the early to late morning hours, a time of increasing energy and activity.",
            "difficulty": 1,
        },
    ]

    def _seed_quiz_questions(self):
        created = 0
        for q in self.QUIZ_QUESTIONS:
            periods = CyclePeriodDetail.objects.filter(
                period_name=q["period_name"],
                cycle_template__cycle_type=q["cycle_type"],
            )
            for period in periods:
                _, is_new = QuizQuestion.objects.update_or_create(
                    question=q["question"],
                    defaults={
                        "option_a": q["option_a"],
                        "option_b": q["option_b"],
                        "option_c": q["option_c"],
                        "option_d": q["option_d"],
                        "correct_answer": q["correct_answer"],
                        "explanation": q["explanation"],
                        "cycle_period": period,
                        "difficulty": q["difficulty"],
                    },
                )
                if is_new:
                    created += 1
        self.stdout.write(f'Created {created} quiz questions.')

    def _seed_glossary(self):
        created = 0
        for item in GLOSSARY_TERMS:
            _, is_new = GlossaryTerm.objects.update_or_create(
                term=item["term"],
                defaults={
                    "definition": item["definition"],
                    "related_cycle_type": item["related_cycle_type"],
                    "sort_order": item["sort_order"],
                },
            )
            if is_new:
                created += 1
        self.stdout.write(f'Created {created} glossary terms ({len(GLOSSARY_TERMS)} total).')
