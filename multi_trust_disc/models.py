from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Maggie Lehr'

doc = """
network trust game w/ proportionality discretion from distributor
"""


class Constants(BaseConstants):
    name_in_url = 'multilateral_trust_d'
    players_per_group = 4
    num_rounds = 12

    endowment = c(100)
    multiplier = 3
    correct_guess = c(20)

    instructions_template = 'multi_trust_simple/Instructions.html'


class Subsession(BaseSubsession):
    dice = models.IntegerField()

    def creating_session(self):
        print('creating session')
        if self.round_number == 1:
            self.group_randomly(fixed_id_in_group=True)
            self.session.vars['matrix1'] = self.get_group_matrix()
            print('first group is', self.session.vars['matrix1'])
        if 1 < self.round_number:
            self.group_like_round(1)

    def is_playing(self):
        if self.session.vars['end_game'] == True:
            return False
        else:
            return True


class Group(BaseGroup):
    total_sender_allocation = models.CurrencyField()
    kept_amount = models.CurrencyField(min=(-1 * Constants.endowment))
    returned1_points = models.CurrencyField(min=0)
    returned2_points = models.CurrencyField(min=0)
    returned3_points = models.CurrencyField(min=0)
    allocated_amount1 = models.CurrencyField()
    allocated_amount2 = models.CurrencyField()
    allocated_amount3 = models.CurrencyField()
    expected_1 = models.BooleanField()
    expected_2 = models.BooleanField()
    expected_3 = models.BooleanField()
    send_back_amount1 = models.FloatField(min=0)
    send_back_amount2 = models.FloatField(min=0)
    send_back_amount3 = models.FloatField(min=0)

    def set_payoffs(self):
        print('setting payoffs')
        sender1 = self.get_player_by_role('sender 1')
        sender2 = self.get_player_by_role('sender 2')
        sender3 = self.get_player_by_role('sender 3')
        distributor = self.get_player_by_role('distributor')

        allocated_amount1 = sender1.sender_allocation
        allocated_amount2 = sender2.sender_allocation
        allocated_amount3 = sender3.sender_allocation

        expectation_1 = sender1.sender_expectation
        expectation_2 = sender2.sender_expectation
        expectation_3 = sender3.sender_expectation

        for player in [distributor, sender1, sender2, sender3]:
            if self.subsession.round_number == self.session.vars['paying_round1']:
                distributor.payoff = Constants.endowment + self.kept_amount
                remainder1 = Constants.endowment - allocated_amount1
                remainder2 = Constants.endowment - allocated_amount2
                remainder3 = Constants.endowment - allocated_amount3
                sender1.payoff = remainder1 + self.returned1_points
                sender2.payoff = remainder2 + self.returned2_points
                sender3.payoff = remainder3 + self.returned3_points

                if (allocated_amount1 - 10) < expectation_1 < (
                        allocated_amount1 + 10):
                    sender1.payoff += Constants.correct_guess
                else:
                    pass

                if (allocated_amount2 - 10) < expectation_2 < (
                        allocated_amount2 + 10):
                    sender2.payoff += Constants.correct_guess
                else:
                    pass

                if (allocated_amount3 - 10) < expectation_3 < (
                        allocated_amount3 + 10):
                    sender3.payoff += Constants.correct_guess
                else:
                    pass





'''
class PlayerBot(Bot):

    def play_round(self):
        yeild (pages.Introduction)
        yeild (pages.Send, {'sender_allocation': 20})
        yeild (pages.SBSelfWaitPage)
        yield (pages.SBSelf, {'contribution': 10})
        yeild (pages.SBRemainderWaitPage)
        yeild (pages.SBRemainder, {'send_back_amount1': 160}, {'send_back_amount2': 10}, {'send_back_amount3': 10})
        yeild (pages.RoundResultsWaitPage)
        yeild (pages.RoundResults)
        yeild (pages.ResultsWaitPage)
        yield (pages.Results)
'''


class Player(BasePlayer):
    sender_allocation = models.CurrencyField(min=0, max=Constants.endowment)
    sender_expectation = models.IntegerField(min=0, max=900)

    def role(self):
        if self.id_in_group == Constants.players_per_group:
            return 'distributor'
        return 'sender {}'.format(self.id_in_group)
