from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        self.subsession.dice = random.randint(1, 3)
        print('this round the second dice is', self.subsession.dice)
        if self.subsession.dice == 3:
            self.session.vars['third_max_round'] = self.subsession.round_number
            print('the third final round is', self.session.vars['third_max_round'])
            self.session.vars['paying_round3'] = random.randint(1, self.session.vars['third_max_round'])
            print('the first payment round is', self.session.vars['paying_round1'])
            print('the third payment round is', self.session.vars['paying_round3'])

class Shuffle(Page):
    def is_displayed(self):
        if self.round_number == 1:
            pass


class SendWaitPage(WaitPage):
    pass


class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'player'
    form_fields = ['sender_allocation', 'sender_expectation']

    def is_displayed(self):
        return self.player.role() != 'distributor'



class SBSelfWaitPage(WaitPage):
    pass


class SBSelf(Page):

    def is_displayed(self):
        return self.player.role() == 'distributor'

    form_model = 'group'
    form_fields = ['kept_amount']

    def kept_amount_max(self):
        allocations = []
        players = self.player.get_others_in_group()
        for p in players:
            allocations.append(p.sender_allocation)
            print(allocations)
        self.group.total_sender_allocation = sum(allocations)
        return self.group.total_sender_allocation * Constants.multiplier

    def vars_for_template(self):
        endowment = Constants.endowment
        allocations = []
        players = self.player.get_others_in_group()
        for p in players:
            allocations.append(p.sender_allocation)
            print(allocations)
        self.group.total_sender_allocation = sum(allocations)

        tripled_amount = self.group.total_sender_allocation * Constants.multiplier

        return {
            'endowment': endowment,
            'tripled_amount': tripled_amount,
            'prompt': 'Please select an amount from 0 to '
                      '{} to keep for yourself before equal redistribution to the senders'.format(tripled_amount)}

    def before_next_page(self):
        print('sum of sent', self.group.total_sender_allocation)
        total_budget = self.group.total_sender_allocation * Constants.multiplier

        self.group.returned1_points = (total_budget - self.group.kept_amount) / 3
        self.group.returned2_points = (total_budget - self.group.kept_amount) / 3
        self.group.returned3_points = (total_budget - self.group.kept_amount) / 3


class RoundResultsWaitPage(WaitPage):
    pass


class RoundResults(Page):
    def vars_for_template(self):
        sender1 = self.group.get_player_by_role('sender 1')
        sender2 = self.group.get_player_by_role('sender 2')
        sender3 = self.group.get_player_by_role('sender 3')

        if self.player.role() == 'sender 1':
            sender_allocation = sender1.sender_allocation
            sender_kept = Constants.endowment - sender_allocation
            returned_sender = self.group.returned1_points
            payoff = Constants.endowment - sender_allocation + returned_sender
            allocated_low = (returned_sender - 10)
            allocated_high = (returned_sender + 10)
            e_test = sender1.sender_expectation
            if allocated_low <= e_test <= allocated_high:
                e_verdict = 'You have correctly guessed the number of points allocated to you'
                payoff += c(40)
            else:
                e_verdict = 'You have incorrectly guessed the number of points allocated to you'

            return {
                'e_test': e_test,
                'e_verdict': e_verdict,
                'sender_allocation': sender_allocation,
                'sender_kept': sender_kept,
                'returned_sender': returned_sender,
                'payoff': payoff}
        elif self.player.role() == 'sender 2':
            sender_allocation = sender2.sender_allocation
            sender_kept = Constants.endowment - sender_allocation
            returned_sender = self.group.returned2_points
            payoff = Constants.endowment - sender_allocation + returned_sender
            allocated_low = (returned_sender - 10)
            allocated_high = (returned_sender + 10)
            e_test = sender2.sender_expectation
            if allocated_low <= e_test <= allocated_high:
                e_verdict = 'You have correctly guessed the number of points allocated to you'
                payoff += c(40)
            else:
                e_verdict = 'You have incorrectly guessed the number of points allocated to you'
            return {
                'allocated_low': allocated_low,
                'allocated_high': allocated_high,
                'e_test': e_test,
                'e_verdict': e_verdict,
                'sender_allocation': sender_allocation,
                'sender_kept': sender_kept,
                'returned_sender': returned_sender,
                'payoff': payoff}
        elif self.player.role() == 'sender 3':
            sender_allocation = sender3.sender_allocation
            sender_kept = Constants.endowment - sender_allocation
            returned_sender = self.group.returned3_points
            payoff = Constants.endowment - sender_allocation + returned_sender
            allocated_low = (returned_sender - 10)
            allocated_high = (returned_sender + 10)
            e_test = sender3.sender_expectation
            if allocated_low <= e_test <= allocated_high:
                e_verdict = 'You have correctly guessed the number of points allocated to you'
                payoff += c(40)
            else:
                e_verdict = 'You have incorrectly guessed the number of points allocated to you'
            return {
                'allocated_low': allocated_low,
                'allocated_high': allocated_high,
                'e_test': e_test,
                'e_verdict': e_verdict,
                'sender_allocation': sender_allocation,
                'sender_kept': sender_kept,
                'returned_sender': returned_sender,
                'payoff': payoff}
        else:
            endowment = Constants.endowment
            sender_allocation = self.group.total_sender_allocation
            total_allocated = sender_allocation * Constants.multiplier
            payoff = Constants.endowment + self.group.kept_amount
            return {
                'endowment': endowment,
                'sender_allocation': sender_allocation,
                'total_allocated': total_allocated,
                'payoff': payoff}


class Dice(Page):
    def vars_for_template(self):
        return {'dice': self.subsession.dice}


class ResultsWaitPage(WaitPage):

    def is_displayed(self):
        if self.subsession.dice == 3:
            return True
        else:
            return False

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    """This page displays the earnings of each player"""

    def is_displayed(self):
        if self.subsession.dice == 3:
            return True
        else:
            return False

    def vars_for_template(self):

        payment = self.participant.payoff_plus_participation_fee()
        return {
            'payment': payment,
            'paying_round1': self.session.vars['paying_round1'],
            'paying_round2': self.session.vars['paying_round2'],
            'paying_round3': self.session.vars['paying_round3'],
            'tripled_amount': self.group.total_sender_allocation * Constants.multiplier
        }



class Survey(Page):
    def is_displayed(self):
        if self.subsession.dice == 3:
            return True
        else:
            return False

    form_model = 'player'
    form_fields = ['survey1', 'survey2', 'survey3']


class Finished(Page):
    def is_displayed(self):
        if self.subsession.dice == 3:
            return True
        else:
            return False


page_sequence = [
    ShuffleWaitPage,
    Shuffle,
    SendWaitPage,
    Send,
    SBSelfWaitPage,
    SBSelf,
    RoundResultsWaitPage,
    RoundResults,
    Dice,
    ResultsWaitPage,
    Results,
    Survey,
    Finished
]
