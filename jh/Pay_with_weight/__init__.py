import random
import math
from otree.api import *

doc = """Pay_with_weight
"""

class Constants(BaseConstants):
    name_in_url = 'Pay_with_weight'
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
    pre_payoff = models.FloatField()
    selected_round = models.FloatField()
    def calculate_round_payoff(self, generated_number):
        if -10 <= generated_number < -6:
            return 100 * self.bar_1
        elif -6 <= generated_number < -2:
            return 100 * self.bar_2
        elif -2 <= generated_number < 2:
            return 100 * self.bar_3
        elif 2 <= generated_number < 6:
            return 100 * self.bar_4
        elif 6 <= generated_number <= 10:
            return 100 * self.bar_5
        else:
            return 0

    def generate_number(self, distribution):
        if distribution == 'uniform':
            generated_number = round(random.uniform(-10, 10), 2)
        elif distribution == 'normal':
            generated_number = round(max(-10, min(10, random.gauss(0, math.sqrt(33.33)))), 2)
        return generated_number

    def calculate_payoff(self):
        if self.round_number == 20:
            generated_number = self.generate_number('uniform')
            self.pre_payoff = self.calculate_round_payoff(generated_number)
        elif self.round_number == 40:
            generated_number = self.generate_number('normal')
            self.pre_payoff = self.calculate_round_payoff(generated_number)
        elif self.round_number == 60:
            generated_number = self.generate_number('normal')
            self.pre_payoff = self.calculate_round_payoff(generated_number)
        elif self.round_number == 80:
            generated_number = self.generate_number('uniform')
            self.pre_payoff = self.calculate_round_payoff(generated_number)


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
        return player.round_number in [20, 40, 60]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.calculate_payoff()

class Decision_last_round(Page):
    form_model = 'player'
    form_fields = ['bar_1', 'bar_2', 'bar_3', 'bar_4', 'bar_5']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 80

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.calculate_payoff()
        selected_round = random.choice([20, 40, 60, 80])
        player.selected_round = selected_round
        player.payoff = player.in_round(selected_round).pre_payoff
        player.payoff *= 0.01
class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 80


page_sequence = [Welcome, Instructions, Round_1_1, Round_1_2, Round_2_1, Round_2_2, Decision, Decision_last_round, Results]
