from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Maggie Lehr'

doc = """
Instructions for Multilateral Trust Game
"""


class Constants(BaseConstants):
    name_in_url = 'multi_trustE_instructionsni'
    players_per_group = 4
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):


    submitted_answer1 = models.StringField(choices=['1', '2', '3', 'Every other round'],
                                           widget=widgets.RadioSelect)
    submitted_answer2 = models.StringField(choices=['True',
                                                    'False'], widget=widgets.RadioSelect)
    submitted_answer3 = models.StringField(choices=['True',
                                                    'False'], widget=widgets.RadioSelect)
    submitted_answer4 = models.StringField(choices=['10', '15', 'A randomly selected amount',
                                                    'An amount selected by the experimenter'],
                                           widget=widgets.RadioSelect)

    correct_1 = models.BooleanField()
    correct_2 = models.BooleanField()
    correct_3 = models.BooleanField()
    correct_4 = models.BooleanField()

    def role(self):
        if self.id_in_group == Constants.players_per_group:
            return 'distributor'
        return 'sender {}'.format(self.id_in_group)


