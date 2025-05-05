from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'trust_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    ENDOWMENT = cu(10)
    MULTIPLIER = 3

class Subsession(BaseSubsession): pass
class Group(BaseGroup):
    amount_sent = models.CurrencyField(min=0, max=C.ENDOWMENT)
    amount_sent_back = models.CurrencyField()

    def set_payoffs(self):
        sent = self.amount_sent
        sent_back = self.amount_sent_back
        tripled = sent * C.MULTIPLIER

        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        p1.payoff = C.ENDOWMENT - sent + sent_back
        p2.payoff = tripled - sent_back


class Player(BasePlayer):
    pass


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    

class BeginRealGame(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1  # seulement après le test

    def vars_for_template(player):
        return dict(name=player.participant.label or f"Joueur {player.id_in_group}")


class Send(Page):
    form_model = 'group'
    form_fields = ['amount_sent']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1  # joueur A
    

class WaitForResults(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        group.set_payoffs()

    

class WaitForB(WaitPage):
    pass

class SendBack(Page):
    form_model = 'group'
    form_fields = ['amount_sent_back']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2  # joueur B

    @staticmethod
    def vars_for_template(player):
        return {
            'tripled_amount': player.group.amount_sent * C.MULTIPLIER
        }

class Results(Page):
    @staticmethod
    def vars_for_template(player):
        group = player.group
        sent = group.amount_sent
        sent_back = group.amount_sent_back
        tripled = sent * C.MULTIPLIER
        return dict(
            sent=sent,
            sent_back=sent_back,
            tripled=tripled,
            payoff=player.payoff,
            is_test_round=(player.round_number == 1)
        )

page_sequence = [Instructions,Send, WaitForB, SendBack, WaitForResults, Results,BeginRealGame]


