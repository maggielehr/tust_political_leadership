from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'multilateral_trust'
    players_per_group = 4
    num_rounds = 3

    endowment = c(100)
    multiplier = 3

    instructions_template = 'multi_trust_simple/Instructions.html'

    sender_choices = []
    for i in range(1, players_per_group):
        choice = [i, 'Redistribute to sender {}'.format(i)]
        sender_choices.append(choice)



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    sender_id = models.IntegerField(
        choices=Constants.sender_choices,
        widget=widgets.RadioSelect,
        doc="""0 means no purchase made"""
    )
    total_sender_allocation = models.CurrencyField()
    allocated_amount = models.CurrencyField()
    send_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
        min=c(0))

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = Constants.endowment

        if self.sender_id != 0:
            sender = self.get_player_by_id(self.sender_id)
            distributor = self.get_player_by_role('distributor')

            all_allocations = [p.sender_allocation for p in self.get_players()]
            self.total_sender_allocation = sum(all_allocations[0:3])
            self.allocated_amount = sender.sender_allocation
            distributor.payoff += (self.total_sender_allocation * Constants.multiplier) - self.send_back_amount
            sender.payoff += self.send_back_amount - self.allocated_amount


class Player(BasePlayer):
    sender_allocation = models.CurrencyField(min=0, max=Constants.endowment)

    def role(self):
        if self.id_in_group == Constants.players_per_group:
            return 'distributor'
        return 'sender {}'.format(self.id_in_group)


