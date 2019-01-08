from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

class Quiz1(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['submitted_answer1']

    def submitted_answer1_error_message(self, value):
        if value != "1":
            return 'Incorrect. You will play each role 1 time.'

    def before_next_page(self):
        return 'Correct!'
        if self.player.submitted_answer1 != "1":
            self.player.quiz1_correct = False
        else:
            self.player.quiz1_correct = True

class Quiz2(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['submitted_answer2']

    def submitted_answer2_error_message(self, value):
        if value != "Both rounds":
            return 'Incorrect. You will get paid for both rounds.'

    def before_next_page(self):
        return 'Correct!'
        if self.player.submitted_answer2 != "Both rounds":
            self.player.quiz2_correct = True

class OfferWaitPage(WaitPage):
    pass

class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    def is_displayed(self):
        return self.player.role() == 'dictator'

    def before_next_page(self):
        self.participant.vars['altruism_measure'] = self.group.kept


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        kept1 = self.group.in_round(1).kept
        kept2 = self.group.in_round(2).kept
        sent1 = Constants.endowment - self.group.in_round(1).kept
        sent2 = Constants.endowment - self.group.in_round(2).kept

        return {
            'offer': Constants.endowment - 10,
            'sent2': sent2,
            'sent1': sent1,
            'kept1': kept1,
            'kept2': kept2}


page_sequence = [
    Introduction,
    OfferWaitPage,
    Offer,
    ResultsWaitPage,
    Results
]

'''
Instructions,
    Quiz1,
    Quiz2,
'''