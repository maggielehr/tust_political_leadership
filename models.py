from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
One player, titled the decision maker, decides how much of a 100 point endowment to share between themselves
and their partner, titled the receiver. The game will last two rounds and roles will reverse half way through. 



"""


class Constants(BaseConstants):
    name_in_url = 'dictator'
    players_per_group = 2
    num_rounds = 2

    instructions_template = 'dictator/Instructions.html'

    # Initial amount allocated to the dictator
    endowment = 100


class Subsession(BaseSubsession):
    def creating_session(self):
        print('in creating_session', self.get_group_matrix(), self.round_number)
        if self.round_number == 1:
            self.group_randomly()
            print("group is shuffled", self.get_group_matrix())
        else:
            self.group_like_round(1)
            print("round 2", self.get_group_matrix())


class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=c(0), max=c(Constants.endowment),
    )

    def set_payoffs(self):
        p1 = self.get_player_by_role('dictator')
        p2 = self.get_player_by_role('receiver')

        p1.payoff = 0
        p2.payoff = 0

        if


class Player(BasePlayer):

    def role(self):
        if self.round_number == 1:
            if self.id_in_group == Constants.players_per_group:
                return 'receiver'
            else:
                return 'dictator'
        else:
            if self.id_in_group == Constants.players_per_group:
                return 'dictator'
            else:
                return 'receiver'

    def get_partner(self):
        return self.get_others_in_group()[0]

    submitted_answer1 = models.StringField(choices=['0', '1', '2', '3'], widget=widgets.RadioSelect)
    submitted_answer2 = models.StringField(choices=['One randomly selected round',
                                                    'The first round',
                                                    'Both rounds'], widget=widgets.RadioSelect)
    quiz1_correct = models.BooleanField()
    quiz2_correct = models.BooleanField()

