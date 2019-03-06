from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1

class Quiz1(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['submitted_answer1']

    def submitted_answer1_error_message(self, value):
        if value != "1":
            self.player.correct_1 = False
            return 'Incorrect. You will play each role 1 time.'


class Quiz2(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['submitted_answer2']

    def submitted_answer2_error_message(self, value):
        if value != "Both rounds":
            self.player.correct_2 = False
            return 'Incorrect. You will get paid for both rounds.'

    def before_next_page(self):
        return 'Correct!'
        if self.player.submitted_answer2 != "Both rounds":
            self.player.quiz2_correct = True

class OfferWaitPage(WaitPage):
    pass

class Offer(Page):
    form_model = 'player'
    form_fields = ['sent']

    def is_displayed(self):
        return self.player.role() == 'dictator'

    def before_next_page(self):
        self.participant.vars['altruism_measure'] = self.player.sent


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        sent1 = p1.in_round(1).sent
        sent2 = p2.in_round(2).sent
        kept1 = Constants.endowment - p1.in_round(1).sent
        kept2 = Constants.endowment - p2.in_round(2).sent

        return {
            'offer': Constants.endowment - 10,
            'sent2': sent2,
            'sent1': sent1,
            'kept1': kept1,
            'kept2': kept2}


page_sequence = [
    Introduction,
    Instructions,
    Instructions2,
    Quiz1,
    Quiz2,
    Offer,
    ResultsWaitPage,
    Results
]

'''
Instructions,
Instructions2,
    Quiz1,
    Quiz2,
'''