from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instruction(Page):
    pass

class Instruction2(Page):
    pass

class Instruction3(Page):
    pass


class Quiz1(Page):
    pass

    form_model = 'player'
    form_fields = ['submitted_answer1']

    def vars_for_template(self):
        return {
            'prompt': 'How many groups will you be assigned to throughout the course of this task?'
        }

    def submitted_answer1_error_message(self, value):
        if value != "3":
            self.player.correct_1 = False
            return 'Incorrect. Your group will be shuffled twice so you will participate in three total group ' \
                   'throughout this task.'

class Quiz2(Page):

    form_model = 'player'
    form_fields = ['submitted_answer2']

    def vars_for_template(self):
        return {
            'prompt': 'True or False: You will know the final earnings of each sender at the end of each round'
        }

    def submitted_answer2_error_message(self, value):
        if value != "False":
            self.player.correct_2 = False
            return 'Incorrect. You will only be made aware of your earnings and how much was kept by the distributor.'


class Quiz3(Page):

    form_model = 'player'
    form_fields = ['submitted_answer3']

    def vars_for_template(self):
        return {
            'prompt': 'True or False: Your final monetary earnings depend on what you earned in a randomly '
                      'selected round from each group.'
        }

    def submitted_answer3_error_message(self, value):
        if value != "True":
            self.player.correct_3 = False
            return 'Incorrect. Your final monetary earnings depend on what you earned in a randomly ' \
                   'selected round from each group.'


class Quiz4(Page):

    form_model = 'player'
    form_fields = ['submitted_answer4']

    def vars_for_template(self):
        return {
            'prompt': 'How many rounds will occur in this task?'
        }

    def submitted_answer4_error_message(self, value):
        if value != "A randomly selected amount":
            self.player.correct_3 = False
            return {'Incorrect. There is a randomly selected number generator which dictates when the game ends, '
                    'so the round number varies'}


page_sequence = [
    Instruction,
    Instruction2,
    Instruction3,
    Quiz1,
    Quiz2,
    Quiz3,
    Quiz4,
]
