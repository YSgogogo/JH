import random
import math
from otree.api import *

doc = """Pay_with_loss_function
"""


class Constants(BaseConstants):
    name_in_url = 'Pay_with_loss_function'
    players_per_group = None
    num_rounds = 80


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Gender =  models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [0, 'Male'],
            [1, 'Female'],
            [2, 'Prefer not to say'],
        ]
    )
    age = models.IntegerField()
    Subject = models.StringField()
    Have_you_learned = models.StringField()
    truthfully_report = models.StringField()
    keep_a_record = models.StringField()
    strategy = models.StringField()


    bar_1 = models.FloatField()
    bar_2 = models.FloatField()
    bar_3 = models.FloatField()
    bar_4 = models.FloatField()
    bar_5 = models.FloatField()
    random_number_g1 = models.FloatField()
    random_number_g2 = models.FloatField()
    normal_number_g1 = models.FloatField()
    normal_number_g2 = models.FloatField()
    payoff_1 = models.FloatField()
    payoff_2 = models.FloatField()
    payoff_3 = models.FloatField()
    payoff_4 = models.FloatField()
    payoff_5 = models.FloatField()
    a = models.IntegerField()
    b = models.IntegerField()
    c = models.IntegerField()
    d = models.IntegerField()

    def calculate_payoff(self):
        if self.round_number in [self.in_round(1).a + 20, self.in_round(1).a + 40]:
            log_sum = sum(math.log(getattr(self, f'bar_{i}') / 100) for i in range(1, 6))
            payoff = max(0, 1000 + 20 * log_sum)
            self.payoff = payoff
        elif self.round_number in [self.in_round(1).b + 20, self.in_round(1).b + 40]:
            log_sum = (
                0.1493 * math.log(self.bar_1 / 100) +
                0.2152 * math.log(self.bar_2 / 100) +
                0.2710 * math.log(self.bar_3 / 100) +
                0.2153 * math.log(self.bar_4 / 100) +
                0.1493 * math.log(self.bar_5 / 100)
            )
            payoff = max(0, 1000 + 100 * log_sum)
            self.payoff = payoff

    def set_a_b(self):
        self.a, self.b, self.c, self.d = random.choice([(40, 0, 2, 1), (0, 40, 1, 2)])

class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.set_a_b()

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
            'random_number_g1': random_number_g1,
            'adjusted_round_number': player.round_number - player.in_round(1).a,
            'adjusted_number': player.in_round(1).c
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).a < player.round_number <= player.in_round(1).a +20


class Round_1_2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        random_number_g2 = round(random.uniform(-10, 10), 2)
        player.random_number_g2 = random_number_g2
        return {
            'random_number_g2': random_number_g2,
            'adjusted_round_number': player.round_number - player.in_round(1).a,
            'adjusted_number': player.in_round(1).c
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).a + 20 < player.round_number <= player.in_round(1).a + 40



class Round_2_1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        normal_number_g1 = random.gauss(0, math.sqrt(33.33))
        player.normal_number_g1 = round(normal_number_g1, 2)
        return {
            'normal_number_g1': player.normal_number_g1,
            'adjusted_round_number': player.round_number - player.in_round(1).b,
            'adjusted_number': player.in_round(1).d
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).b < player.round_number <= player.in_round(1).b + 20



class Round_2_2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        normal_number_g2 = random.gauss(0, math.sqrt(33.33))
        player.normal_number_g2 = round(normal_number_g2, 2)
        return {
            'normal_number_g2': player.normal_number_g2,
            'adjusted_round_number': player.round_number - player.in_round(1).b,
            'adjusted_number': player.in_round(1).d
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).b + 20 < player.round_number <= player.in_round(1).b + 40



class Decision(Page):
    form_model = 'player'
    form_fields = ['bar_1', 'bar_2', 'bar_3', 'bar_4', 'bar_5']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [20, 40, 60, 80]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.calculate_payoff()


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 80

class Survey(Page):
    form_model = 'player'
    form_fields = ['Gender', 'age', 'Subject', 'Have_you_learned', 'truthfully_report', 'keep_a_record', 'strategy']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 80


page_sequence = [Welcome, Instructions, Round_1_1, Round_1_2, Round_2_1, Round_2_2, Decision, Survey, Results]
