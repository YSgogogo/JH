import random
import math
from otree.api import *

doc = """game
"""

class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = None
    num_rounds = 80

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    bar_1 = models.FloatField()
    bar_2 = models.FloatField()
    bar_3 = models.FloatField()
    bar_4 = models.FloatField()
    bar_5 = models.FloatField()
    random_number_g1 = models.FloatField()
    random_number_g2 = models.FloatField()
    normal_number_g1 = models.FloatField()
    normal_number_g2 = models.FloatField()



class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Round_1_1(Page):

    @staticmethod
    def vars_for_template(player: Player):
        random_number_g1 = round(random.uniform(-10, 10), 2)
        player.random_number_g1 = random_number_g1
        return {
            'random_number_g1': random_number_g1
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= 20

class Round_1_2(Page):

    @staticmethod
    def vars_for_template(player: Player):
        normal_number_g1 = random.gauss(0, math.sqrt(33.33))
        player.normal_number_g1 = round(max(-10, min(10, normal_number_g1)), 2)
        return {
            'normal_number_g1': player.normal_number_g1
        }

    @staticmethod
    def is_displayed(player: Player):
        return 20 < player.round_number <= 40


class Round_2_1(Page):

    @staticmethod
    def vars_for_template(player: Player):
        normal_number_g2 = random.gauss(0, math.sqrt(33.33))
        player.normal_number_g2 = round(max(-10, min(10, normal_number_g2)), 2)
        return {
            'normal_number_g2': player.normal_number_g2,
            'adjusted_round_number': player.round_number - 40
        }

    @staticmethod
    def is_displayed(player: Player):
        return 40 < player.round_number <= 60


class Round_2_2(Page):

    @staticmethod
    def vars_for_template(player: Player):
        random_number_g2 = round(random.uniform(-10, 10), 2)
        player.random_number_g2 = random_number_g2
        return {
            'random_number_g2': random_number_g2,
            'adjusted_round_number': player.round_number - 40
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 60


class Decision(Page):

    form_model = 'player'
    form_fields = ['bar_1', 'bar_2', 'bar_3', 'bar_4', 'bar_5']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [20, 40, 60, 80]


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 80

page_sequence = [Welcome, Instructions, Round_1_1, Round_1_2, Round_2_1, Round_2_2, Decision, Results]
