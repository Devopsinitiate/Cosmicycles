from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate, CyclePeriodDetail
import json

class Command(BaseCommand):
    help = 'Seeds the database with detailed Yearly Cycle principles from the book.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding Yearly Cycle details...'))

        # Create or get the main Yearly Cycle template
        yearly_cycle_template, created = CycleTemplate.objects.update_or_create(
            name='Yearly Cycle',
            cycle_type='yearly',
            defaults={'description': 'The yearly cycle of human life, divided into seven periods of approximately 52 days each.'}
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created "Yearly Cycle" template.'))
        else:
            self.stdout.write(self.style.SUCCESS('Found existing "Yearly Cycle" template.'))

        yearly_cycle_data = [
            {
                'period_name': 'Period 1',
                'start_value': 1,
                'end_value': 52,
                'description': """This is a period when a person should utilize every personal power and ability to advance his own interests among persons of influence who have powers or privileges to grant or give. It is a period when solicitation should be made for favors, either in seeking employment, benefits, loans, partnerships, investments, special concessions, releases, or even favors in the form of time or postponements or dismissals in court. It is an especially good period to seek favors or honors, help or recognition, from persons who are in high power or high positions such as government officials, judges, mayors, governors, senators, people at the head of large corporations or big business, or persons who hold valuable papers, documents, and matters that may be of great importance, and which may be released, modified, or otherwise affected by your solicitation. This is also a good period for advancing one’s own personal self among the populace, or with the people of your city, state, or country, or in building up your credit standing or your reputation with newspapers and influential people. It is a time to push yourself forward with discrimination and yet determination, for all of the cosmic vibrations are in favor of boosting and helping you personally so far as your name, reputation, honor, and integrity among high persons or the multitudes are concerned.""",
                'recommendations': json.dumps({'summary': 'Leveraging influence and authority for personal advancement.', 'advice': 'Seek favors, honors, employment, loans, or recognition from people in high positions. Promote yourself and build your reputation.'})
            },
            {
                'period_name': 'Period 2',
                'start_value': 53,
                'end_value': 104,
                'description': """This period is distinctly different from the foregoing period, for during these 52 days everything will tend to be favorably directed toward your plans regarding any journeys, especially those that are not for many months’ or a year’s duration, but those that are short, quick, and of immediate importance rather than of importance in the future. Journeys by water or by train are generally favored during this period. It is also an excellent time for moving your home to a new location, or moving your business, or moving your occupation, if it is something under your own control. In other words, this is a period for changes which are quick and soon over with. In a business way this period will be found very favorable for such activities pertaining to movable things, and things of indefinite location. The moving of freight or the dealing with freight business, expressage, automobiles, wagons, carriages, trucks, public conveyances, public lectures, shows, performances, and things of this kind will be found successful. Strange to say, this period is also an excellent one for those who are dealing with liquids, chemicals, milk, water, water power, gasoline, or other things of a liquid nature. Dealing with people who are in lines of business associated with all of the foregoing will also be more successful in this period than in any other. Inversely, one should not plan a change of business or start a new career in business or attempt to build a permanent thing upon any change that is made during this period. Moving one’s home may be successful if done during this period, but at the same time the buying of a new home during this period will be very apt to result in a future change because a change made during this particular period does not make for permanency. Therefore, all things done during this time should be of such a nature as to begin during the period and end shortly afterward or as to be of the present months or year rather than the future.""",
                'recommendations': json.dumps({'summary': 'Favorable for travel, temporary changes, and movable things.', 'advice': 'Plan short journeys, move locations, or make other short-term changes. Good for logistics, transportation, and dealing with liquids. Avoid long-term commitments, permanent contracts, and financial speculation.'})
            },
            {
                'period_name': 'Period 3',
                'start_value': 105,
                'end_value': 156,
                'description': """Here we have a period that may be fortunate or unfortunate according to the application of the cosmic powers, and the discretion and discrimination that a person uses. This period fills the individual with an almost uncontrollable impulse to want to do great and important things, and the fiery energy that goes through the human system during this period wants to express itself in many ways. If directed carefully, this period can be one of the greatest in the whole year for the building up of a business and the accomplishment of those things that call for great physical energy, physical effort, endurance, vitality, determination, and persistency. On the other hand, if the energy is misspent, or applied without discrimination and judgment, great tasks may be undertaken or started that will not be completed in a long time, and too much for one person may be started through the restless energy that wants to express itself. This is an excellent period in which to overcome those obstacles and conditions that in the past periods seemed to check every advancement because of the energy and labor required. It is an excellent period to begin anything that has to start with a bang and have a great impulse during the first month or two of its career. Certainly this is an excellent period for dealing with affairs of the army, the navy, military engineering, munitions, or with those persons or lines of business that deal with heavy muscular or extreme vital energy. It is likewise an excellent period for the building up of a business or interests dealing with iron, steel, cutlery, sharp instruments, or things connected with electrical machinery, furnaces, and fire. It is also a fine period in which to deal with enemies, competitors, and rivals, who have heretofore been obstacles in the path, but it is a poor time to attempt to master those obstacles or persons with arguments or with contracts, papers, or agreements. If sheer energy, persistency, and long hours of activity and hard work will affect competitors or obstacles in the way, this is the period in which to overcome them in this manner.""",
                'recommendations': json.dumps({'summary': 'High energy, power, and potential for conflict.', 'advice': 'Use the high energy to overcome obstacles and start ambitious projects. Good for dealing with military or heavy industry. Avoid arguments and be mindful of misspent energy.'})
            },
            {
                'period_name': 'Period 4',
                'start_value': 157,
                'end_value': 208,
                'description': """This period is considerably different from the preceding one, inasmuch as in it we have the cosmic forces strongly influencing and strengthening the mental, nervous, and psychic side of the nature rather than the physical. It is an excellent period for the writing and mental creation of books, plays, plans, business schemes, and other matters requiring a fertile mind, quick thinking, smooth-flowing language, and an unusual ability to express the thoughts in the mind. In fact, the mind will seem to be highly charged with new thoughts, new ideas, and easily contacted expressions of the Cosmic Mind. Incidentally, it has been noticed that since the mind is very fertile and very sensitive during this period, ideas, impulses, and urges are apt to flow into the mental consciousness very rapidly. To take advantage of most of these, the person must act upon impulse and quickly grasp the ideas and put them into practical application before others crowd them out. Therefore, it is is a dependable period for acting upon impulses or so-called intuitive hunches. The nature of the person becomes optimistic and, because of the mental activity, somewhat nervous and restless, with the imagination highly charged. It is a good period in which to deal with literary persons, reporters, messengers, to engage stenographers and writers, bookkeepers, engravers, artists, and persons whose work is primarily mental and rapid in expression. Artists are more inspired and more nimble in their work during this time. A warning must be given here, however, that great deceptions can be practiced upon persons during this period. Stories, reports, papers, documents, or other written or spoken matter that may come to your attention during this period must be carefully analyzed before being accepted, because it is a period when falsehood is as nimble and eloquently expressed in words or writing as is the truth. Deception, therefore, is not only very easy, but very frequent. Forgeries in regard to personal and business papers, and counterfeits of important papers or money must be watched at this time.""",
                'recommendations': json.dumps({'summary': 'Heightened mental, psychic, and creative activity.', 'advice': 'Focus on writing, planning, and creative endeavors. Act on intuitive hunches. Be wary of deception, forgery, and theft. Good for study, but not for major life changes like marriage or buying a home.'})
            },
            {
                'period_name': 'Period 5',
                'start_value': 209,
                'end_value': 260,
                'description': """Here we enter into what may be called the success period of each year, as far as our personal, private affairs are concerned. During these 52 days the cosmic impulses and tendencies are to bring happy fruition and successful termination of the things with which we have been laboring, or the things we have planned or put into action. It is during this time that our personal affairs expand, grow, and increase in prosperity. The mind of the person becomes filled with higher ideas of courtesy, religion, science, and law, and there is a tendency toward good fellowship, sociability, benevolence, honesty, and sympathy. It is an excellent period for dealing with lawyers or judges of the court, government officials, clergymen, physicians, merchants, or people of wealth. It is also a good period in which to begin a long journey in contradistinction to the good period for short journeys which occurs during the second period of this cycle. This is also a very fine period for renewing or starting interests in philosophical works, metaphysical studies, the preparation of sermons, or legal briefs, or those things requiring very favorable influences to bring to a successful issue. For that reason it is a fine time in which to collect money that is owing or to buy for the purpose of selling, and to sell or speculate or even to borrow. Any attempts during this period, however, to deal with tricky affairs that are not legitimate speculations, or to deal with cattle, to buy or sell cattle, or to deal with meat products on a large scale, or to deal with marine affairs, will prove unsuccessful.""",
                'recommendations': json.dumps({'summary': 'Success, prosperity, and positive growth.', 'advice': 'Conclude projects, deal with professionals, handle finances, and start long journeys or important studies. Avoid illegitimate speculations and dealings in cattle or marine affairs.'})
            },
            {
                'period_name': 'Period 6',
                'start_value': 261,
                'end_value': 312,
                'description': """Here is a period that may be called the holiday of the year. It is a time for pleasure, amusement, relaxation, and entertainment. This does not mean, however, that business will not prosper and that regular affairs of life should be withheld or modified during this period, for all things that are legitimate and good will continue with almost as much success as during the preceding period. However, this is the time in which to deal specifically with certain affairs of life with more intensity than at other periods. Now is the time to make long or short visits for relaxation or for the renewing of friendships. It is a fine period for dealing with women, or for women to deal with men in the pleasurable things of life, and in the higher things of life. It is especially fortunate for such business matters as deal with the higher and more pleasant things of life such as with art, music, poetry, painting, sculpting, personal adornments, perfumes, incense, flowers, and so forth. Short journeys will be happy and successful during this time but not long voyages, or in fact any voyages by water. This is a good period for the consummation of transactions of a speculative nature, or to buy stocks and bonds or to engage employees and assistants.""",
                'recommendations': json.dumps({'summary': 'Pleasure, relaxation, and social activities.', 'advice': 'Take vacations, renew friendships, and focus on business related to arts, beauty, and leisure. Favorable for short journeys and speculative transactions.'})
            },
            {
                'period_name': 'Period 7',
                'start_value': 313,
                'end_value': 365,
                'description': """This is the critical and disruptive period of life each year. I feel sure that after you have outlined the yearly cycle of your life for each year, if you will then look back over the last ten or more years of your life and note the things that occurred during the seventh period of each of your years, that you will see how true this is. It is that sort of a period when devolution precedes evolution, or when the breaking down begins in order that there may be a new building up. It is like the period when the house is torn down, brick by brick, and leveled in order to rebuild again. In one sense it is disruptive, and in another sense it is the first stage to reconstruction. For that reason, each should be warned to take advantage of the natural tendency of this period and at the same time guard against these tendencies that they may not go too far, or that one may not wrongly labor and run counter with the tendencies instead of cooperating with them. It is the period when most things that have been hanging fire and are about to end, or disrupt, do so. If a business or any other affair has been going poorly and has shown a tendency to fail, and go to pieces, this is the period when such a culmination is most apt to occur. If this result is not wanted, care must be exercised not to do those things which will help to bring it about The mind is very apt to become despondent, discouraged, or pessimistic during this period, and that must be kept in mind, for if this attitude is allowed to affect the actions in business or in personal affairs, it will help to bring about a disastrous result. The influences during this period are very subtle, and must be carefully analyzed and reasoned before being applied. We have said that during the fourth period of this cycle the rapidity with which ideas come to the mind, along with the cosmic influences creating them, makes it advisable to be quick and even impulsive in accepting and applying these ideas. The very reverse is true in the present period. Impulsiveness here will bring disaster.""",
                'recommendations': json.dumps({'summary': 'Critical, disruptive, and reconstructive.', 'advice': 'Conclude failing projects. Be cautious, avoid starting new ventures, and guard against pessimism. Postpone new ideas. Good for dealing with elderly persons, real estate, and inventions. Most unfavorable for new business launches.'})
            }
        ]

        for data in yearly_cycle_data:
            period_detail, created = CyclePeriodDetail.objects.update_or_create(
                cycle_template=yearly_cycle_template,
                period_name=data['period_name'],
                defaults={
                    'start_value': data['start_value'],
                    'end_value': data['end_value'],
                    'description': data['description'],
                    'recommendations': data['recommendations']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"""Created {data['period_name']}"""
))
            else:
                self.stdout.write(self.style.SUCCESS(f"""Updated {data['period_name']}"""
))

        self.stdout.write(self.style.SUCCESS('Yearly Cycle seeding complete.'))