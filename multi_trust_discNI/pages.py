from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class SendWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        self.session.vars['dice'] = random.randint(1, 3)
        self.subsession.dice = self.session.vars['dice']
        print('this round the first dice is', self.subsession.dice)
        if self.subsession.dice == 3:
            self.session.vars['first_max_round'] = self.subsession.round_number
            print('the final round is', self.session.vars['first_max_round'])
            self.session.vars['paying_round1'] = random.randint(1, self.session.vars['first_max_round'])
            print('the first payment round is', self.session.vars['paying_round1'])

        if self.subsession.round_number == 1:
            self.session.vars['end_game'] = False


class Send(Page):

    form_model = 'player'
    form_fields = ['sender_allocation', 'sender_expectation']

    def is_displayed(self):
        return self.subsession.is_playing() and self.player.role() != 'distributor'


class SBSelfWaitPage(WaitPage):
    pass


class SBSelf(Page):

    def is_displayed(self):
        return self.subsession.is_playing() and self.player.role() == 'distributor'

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
        sender1 = self.group.get_player_by_role('sender 1')
        sender2 = self.group.get_player_by_role('sender 2')
        sender3 = self.group.get_player_by_role('sender 3')
        endowment = Constants.endowment
        allocations = []
        players = self.player.get_others_in_group()
        for p in players:
            allocations.append(p.sender_allocation)
            print(allocations)
        self.group.total_sender_allocation = sum(allocations)
        sent1 = sender1.sender_allocation
        sent2 = sender2.sender_allocation
        sent3 = sender3.sender_allocation

        tripled_amount = self.group.total_sender_allocation * Constants.multiplier

        return {
            'sent1': sent1,
            'sent2': sent2,
            'sent3': sent3,
            'endowment': endowment,
            'tripled_amount': tripled_amount,
            'prompt': 'Please select an amount from 0 to '
                      '{} to keep for yourself before equal redistribution to the senders'.format(tripled_amount)}


class SBRemainderWaitPage(WaitPage):
        pass


class SBRemainder(Page):
        """This page is only for P2
        P2 sends back some amount (of the tripled amount received) to P1"""

        form_model = 'group'
        form_fields = ['send_back_amount1', 'send_back_amount2', 'send_back_amount3']

        def is_displayed(self):
            return self.subsession.is_playing() and self.player.role() == 'distributor'

        def vars_for_template(self):
            sender1 = self.group.get_player_by_role('sender 1')
            sender2 = self.group.get_player_by_role('sender 2')
            sender3 = self.group.get_player_by_role('sender 3')
            allocations = []
            players = self.player.get_others_in_group()
            for p in players:
                allocations.append(p.sender_allocation)
                print(allocations)
            self.group.total_sender_allocation = sum(allocations)
            sent1 = sender1.sender_allocation
            sent2 = sender2.sender_allocation
            sent3 = sender3.sender_allocation
            remainder_allocation = (self.group.total_sender_allocation * Constants.multiplier) - self.group.kept_amount

            return {
                'sent1': sent1,
                'sent2': sent2,
                'sent3': sent3,
                'remainder_allocation': remainder_allocation,
                'prompt': 'Please enter an amount from 0 to 100%'}

        def error_message(self, values):
            if values["send_back_amount1"] + values["send_back_amount2"] + values["send_back_amount3"] != 100:
                return 'The numbers must add up to 100'

        def before_next_page(self):
            allocations = []
            players = self.player.get_others_in_group()
            for p in players:
                allocations.append(p.sender_allocation)
            self.group.total_sender_allocation = sum(allocations)

            budget = self.group.total_sender_allocation * 3

            self.group.returned1_points = (budget - self.group.kept_amount) * float(self.group.send_back_amount1 / 100)

            self.group.returned2_points = (budget - self.group.kept_amount) * float(self.group.send_back_amount2 / 100)

            self.group.returned3_points = (budget - self.group.kept_amount) * float(self.group.send_back_amount3 / 100)


class RoundResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.subsession.is_playing()


class RoundResults(Page):

    def is_displayed(self):
        return self.subsession.is_playing()

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
                payoff += c(20)
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
                payoff += c(20)
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
                payoff += c(20)
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

    def is_displayed(self):
        return self.subsession.is_playing()

    def vars_for_template(self):
        return {'dice': self.subsession.dice}

    def before_next_page(self):
        if self.subsession.dice == 3:
            self.group.set_payoffs()
            self.session.vars['end_game'] = True
            print("end", self.session.vars['end_game'])



page_sequence = [
    SendWaitPage,
    Send,
    SBSelfWaitPage,
    SBSelf,
    SBRemainderWaitPage,
    SBRemainder,
    RoundResultsWaitPage,
    RoundResults,
    Dice,

]

