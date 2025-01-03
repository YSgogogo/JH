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
    follow_real_process = models.StringField()

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
    generated_number = models.FloatField()
    selected_round = models.FloatField()
    a = models.IntegerField()
    b = models.IntegerField()
    c = models.IntegerField()
    d = models.IntegerField()

    def calculate_round_payoff(self, generated_number):
        if generated_number < -6:
            return round(10 * self.bar_1, 2)
        elif -6 <= generated_number < -2:
            return round(10 * self.bar_2, 2)
        elif -2 <= generated_number < 2:
            return round(10 * self.bar_3, 2)
        elif 2 <= generated_number < 6:
            return round(10 * self.bar_4, 2)
        elif 6 <= generated_number:
            return round(10 * self.bar_5, 2)
        else:
            return 0

    def generate_number(self, distribution):
        if distribution == 'uniform':
            self.generated_number = round(random.uniform(-10, 10), 2)
        elif distribution == 'normal':
            self.generated_number = round(random.gauss(0, math.sqrt(33.33)), 2)
        return self.generated_number

    def calculate_payoff(self):
        if self.round_number == self.in_round(1).a + 20:
            generated_number = self.generate_number('uniform')
            self.pre_payoff = self.calculate_round_payoff(generated_number)
        elif self.round_number == self.in_round(1).a + 40:
            generated_number = self.generate_number('uniform')
            self.pre_payoff = self.calculate_round_payoff(generated_number)
        elif self.round_number == self.in_round(1).b + 20:
            generated_number = self.generate_number('normal')
            self.pre_payoff = self.calculate_round_payoff(generated_number)
        elif self.round_number == self.in_round(1).b + 40:
            generated_number = self.generate_number('normal')
            self.pre_payoff = self.calculate_round_payoff(generated_number)

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
        if player.round_number == player.in_round(1).a + 21:
            random_number_g2 = player.in_round(player.round_number - 1).generated_number
        else:
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
        if player.round_number == player.in_round(1).b + 21:
            normal_number_g2 = player.in_round(player.round_number - 1).generated_number
        else:
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
        selected_rounds = [20, 40, 60, 80]
        total_payoff = 0
        for round_num in selected_rounds:
            round_payoff = player.in_round(round_num).pre_payoff
            total_payoff += round_payoff
        player.payoff = total_payoff

class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 80

    @staticmethod
    def vars_for_template(player: Player):
        round_20_payoff = player.in_round(20).pre_payoff
        round_40_payoff = player.in_round(40).pre_payoff
        round_60_payoff = player.in_round(60).pre_payoff
        round_80_payoff = player.in_round(80).pre_payoff

        bar1_20 = player.in_round(20).bar_1
        bar2_20 = player.in_round(20).bar_2
        bar3_20 = player.in_round(20).bar_3
        bar4_20 = player.in_round(20).bar_4
        bar5_20 = player.in_round(20).bar_5

        bar1_40 = player.in_round(40).bar_1
        bar2_40 = player.in_round(40).bar_2
        bar3_40 = player.in_round(40).bar_3
        bar4_40 = player.in_round(40).bar_4
        bar5_40 = player.in_round(40).bar_5

        bar1_60 = player.in_round(60).bar_1
        bar2_60 = player.in_round(60).bar_2
        bar3_60 = player.in_round(60).bar_3
        bar4_60 = player.in_round(60).bar_4
        bar5_60 = player.in_round(60).bar_5

        bar1_80 = player.in_round(80).bar_1
        bar2_80 = player.in_round(80).bar_2
        bar3_80 = player.in_round(80).bar_3
        bar4_80 = player.in_round(80).bar_4
        bar5_80 = player.in_round(80).bar_5

        if player.in_round(1).a == 0:
            round_1 = "uniform"
            round_2 = "normal"
            data_6 = 14.93
            data_7 = 21.52
            data_8 = 27.10
            data_9 = 21.52
            data_10 = 14.93
            data_1 = 20
            data_2 = 20
            data_3 = 20
            data_4 = 20
            data_5 = 20
        else:
            round_2 = "uniform"
            round_1 = "normal"
            data_1 = 14.93
            data_2 = 21.52
            data_3 = 27.10
            data_4 = 21.52
            data_5 = 14.93
            data_6 = 20
            data_7 = 20
            data_8 = 20
            data_9 = 20
            data_10 = 20


        return {
            'round_20_payoff': round_20_payoff,
            'round_40_payoff': round_40_payoff,
            'round_60_payoff': round_60_payoff,
            'round_80_payoff': round_80_payoff,
            'round_1': round_1,
            'round_2': round_2,
            'bar1_20': bar1_20,
            'bar2_20': bar2_20,
            'bar3_20': bar3_20,
            'bar4_20': bar4_20,
            'bar5_20': bar5_20,
            'bar1_40': bar1_40,
            'bar2_40': bar2_40,
            'bar3_40': bar3_40,
            'bar4_40': bar4_40,
            'bar5_40': bar5_40,
            'bar1_60': bar1_60,
            'bar2_60': bar2_60,
            'bar3_60': bar3_60,
            'bar4_60': bar4_60,
            'bar5_60': bar5_60,
            'bar1_80': bar1_80,
            'bar2_80': bar2_80,
            'bar3_80': bar3_80,
            'bar4_80': bar4_80,
            'bar5_80': bar5_80,
            'data_6' : data_6,
            'data_7' : data_7,
            'data_8' : data_8,
            'data_9' : data_9,
            'data_10' : data_10,
            'data_1' : data_1,
            'data_2' : data_2,
            'data_3' : data_3,
            'data_4' : data_4,
            'data_5' : data_5,
        }

class Survey(Page):
    form_model = 'player'
    form_fields = ['Gender', 'age', 'Subject', 'Have_you_learned', 'truthfully_report', 'keep_a_record', 'strategy', 'follow_real_process']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 80



    @staticmethod
    def vars_for_template(player: Player):

        if player.in_round(1).a == 0:
            round_1 = "uniform"
            round_2 = "normal"
            data_6 = 14.93
            data_7 = 21.52
            data_8 = 27.10
            data_9 = 21.52
            data_10 = 14.93
            data_1 = 20
            data_2 = 20
            data_3 = 20
            data_4 = 20
            data_5 = 20
        else:
            round_2 = "uniform"
            round_1 = "normal"
            data_1 = 14.93
            data_2 = 21.52
            data_3 = 27.10
            data_4 = 21.52
            data_5 = 14.93
            data_6 = 20
            data_7 = 20
            data_8 = 20
            data_9 = 20
            data_10 = 20


        return {
            'round_1': round_1,
            'round_2': round_2,
            'data_6' : data_6,
            'data_7' : data_7,
            'data_8' : data_8,
            'data_9' : data_9,
            'data_10' : data_10,
            'data_1' : data_1,
            'data_2' : data_2,
            'data_3' : data_3,
            'data_4' : data_4,
            'data_5' : data_5,
        }


page_sequence = [Welcome, Instructions, Round_1_1, Round_1_2, Round_2_1, Round_2_2, Decision, Decision_last_round, Survey, Results]
