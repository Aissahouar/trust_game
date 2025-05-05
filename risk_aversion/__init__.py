from otree.api import *
import random

doc = """
Tâche de mesure de l'aversion au risque et de l'aversion à l'ambiguïté dans les gains et les pertes
avec une tâche préliminaire (comptage de chiffres dans π).
"""


class C(BaseConstants):
    NAME_IN_URL = 'risk_aversion'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(25)
    PI_DIGITS = (
        "141 592 653 589 793 238 462 643 383 279 502 884 197 169 399 375 10"
        "5 820 974 944 592 307 816 406 286 208 998 628 034 825 342 117 067 9"
        "82 148 086 513 282 306 647 093 844 609 550 582 231 725 359 408 128"
        "48 111 745 028 410 270 193 852 110 555 964 462 294 895 493 038 196"
    )
    # Options de loterie pour chaque décision
    DECISION_1_LOTTERIES = {
        'A': {'description': '100% de chances de gagner 10 jetons', 'probs': [1.0, 0.0], 'payouts': [10, 0]},
        'B': {'description': '50% de chances de gagner 8 jetons\n50% de chances de gagner 13 jetons', 'probs': [0.5, 0.5], 'payouts': [8, 13]},
        'C': {'description': '50% de chances de gagner 6 jetons\n50% de chances de gagner 16 jetons', 'probs': [0.5, 0.5], 'payouts': [6, 16]},
        'D': {'description': '50% de chances de gagner 4 jetons\n50% de chances de gagner 19 jetons', 'probs': [0.5, 0.5], 'payouts': [4, 19]},
        'E': {'description': '50% de chances de gagner 2 jetons\n50% de chances de gagner 20 jetons', 'probs': [0.5, 0.5], 'payouts': [2, 20]},
        'F': {'description': '50% de chances de gagner 0 jetons\n50% de chances de gagner 25 jetons', 'probs': [0.5, 0.5], 'payouts': [0, 25]},
    }
    
    DECISION_2_LOTTERIES = {
        'A': {'description': '100% de chances de perdre 10 jetons', 'probs': [1.0, 0.0], 'payouts': [-10, 0]},
        'B': {'description': '50% de chances de perdre 8 jetons\n50% de chances de perdre 13 jetons', 'probs': [0.5, 0.5], 'payouts': [-8, -13]},
        'C': {'description': '50% de chances de perdre 6 jetons\n50% de chances de perdre 16 jetons', 'probs': [0.5, 0.5], 'payouts': [-6, -16]},
        'D': {'description': '50% de chances de perdre 4 jetons\n50% de chances de perdre 19 jetons', 'probs': [0.5, 0.5], 'payouts': [-4, -19]},
        'E': {'description': '50% de chances de perdre 2 jetons\n50% de chances de perdre 20 jetons', 'probs': [0.5, 0.5], 'payouts': [-2, -20]},
        'F': {'description': '50% de chances de perdre 0 jetons\n50% de chances de perdre 25 jetons', 'probs': [0.5, 0.5], 'payouts': [0, -25]},
    }
    
    DECISION_3_LOTTERIES = {
        'A': {'description': '50% de chances de gagner 10 jetons', 'probs': [0.5, 0.5], 'payouts': [10, 0]},
        'B': {'description': '50% de chances de gagner 8 jetons\n50% de chances de gagner 13 jetons', 'probs': [0.5, 0.5], 'payouts': [8, 13]},
        'C': {'description': '50% de chances de gagner 6 jetons\n50% de chances de gagner 16 jetons', 'probs': [0.5, 0.5], 'payouts': [6, 16]},
        'D': {'description': '50% de chances de gagner 4 jetons\n50% de chances de gagner 19 jetons', 'probs': [0.5, 0.5], 'payouts': [4, 19]},
        'E': {'description': '50% de chances de gagner 2 jetons\n50% de chances de gagner 20 jetons', 'probs': [0.5, 0.5], 'payouts': [2, 20]},
        'F': {'description': '50% de chances de gagner 0 jetons\n50% de chances de gagner 25 jetons', 'probs': [0.5, 0.5], 'payouts': [0, 25]},
    }
    
    DECISION_4_LOTTERIES = {
        'A': {'description': '100% de chances de perdre 10 jetons', 'probs': [1.0, 0.0], 'payouts': [-10, 0]},
        'B': {'description': '50% de chances de perdre 8 jetons\n50% de chances de perdre 13 jetons', 'probs': [0.5, 0.5], 'payouts': [-8, -13]},
        'C': {'description': '50% de chances de perdre 6 jetons\n50% de chances de perdre 16 jetons', 'probs': [0.5, 0.5], 'payouts': [-6, -16]},
        'D': {'description': '50% de chances de perdre 4 jetons\n50% de chances de perdre 19 jetons', 'probs': [0.5, 0.5], 'payouts': [-4, -19]},
        'E': {'description': '50% de chances de perdre 2 jetons\n50% de chances de perdre 20 jetons', 'probs': [0.5, 0.5], 'payouts': [-2, -20]},
        'F': {'description': '50% de chances de perdre 0 jetons\n50% de chances de perdre 25 jetons', 'probs': [0.5, 0.5], 'payouts': [0, -25]},
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Tâche de comptage
    target_digit = models.IntegerField(initial=0)  # Added initial value to avoid None
    pi_count = models.IntegerField(label="Combien de fois ce chiffre apparaît-il ?")
    task_success = models.BooleanField(initial=False)
    
    # Choix de loteries
    decision_1 = models.StringField(
        label="Décision 1",
        choices=['A', 'B', 'C', 'D', 'E', 'F'],
        widget=widgets.RadioSelect,
    )
    decision_2 = models.StringField(
        label="Décision 2",
        choices=['A', 'B', 'C', 'D', 'E', 'F'],
        widget=widgets.RadioSelect,
    )
    decision_3 = models.StringField(
        label="Décision 3",
        choices=['A', 'B', 'C', 'D', 'E', 'F'],
        widget=widgets.RadioSelect,
    )
    decision_4 = models.StringField(
        label="Décision 4",
        choices=['A', 'B', 'C', 'D', 'E', 'F'],
        widget=widgets.RadioSelect,
    )
    
    # Paiement
    chosen_decision = models.IntegerField()
    lottery_result = models.FloatField()  # Résultat du tirage aléatoire (0-1)
    chosen_lottery = models.StringField()  # Lottery choisie (A, B, C, D, E, F)
    lottery_outcome = models.CurrencyField()  # Résultat de la loterie
    final_payoff = models.CurrencyField()  # Paiement final
    is_gain = models.BooleanField()  # Si vrai: gain, si faux: perte


# === Pages ===

class Instructions(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        # Assign a random digit when moving from Instructions to CountDigitIntro
        player.target_digit = random.randint(0, 9)


class CountDigitIntro(Page):
    def vars_for_template(player):
        return dict(
            pi_digits=C.PI_DIGITS,
            digit=player.target_digit,
        )


class CountDigitTask(Page):
    form_model = 'player'
    form_fields = ['pi_count']
    
    @staticmethod
    def error_message(player, values):
        correct_count = C.PI_DIGITS.count(str(player.target_digit))
        if values['pi_count'] != correct_count:
            return f"Incorrect. Réessayez."
        else:
            player.task_success = True
    
    def vars_for_template(player):
        return dict(
            pi_digits=C.PI_DIGITS,
            digit=player.target_digit,
        )
    
    def is_displayed(player):
        return not player.task_success


class TaskSuccess(Page):
    def is_displayed(player):
        return player.task_success

        
class InvestmentInfo(Page):
    pass


class Investment1(Page):
    form_model = 'player'
    form_fields = ['decision_1']
    
    def vars_for_template(player):
        return {
            'lotteries': C.DECISION_1_LOTTERIES,
            'decision_number': 1,
            'is_gain': True
        }


class Investment2(Page):
    form_model = 'player'
    form_fields = ['decision_2']
    
    def vars_for_template(player):
        return {
            'lotteries': C.DECISION_2_LOTTERIES,
            'decision_number': 2,
            'is_gain': False
        }


class Investment3(Page):
    form_model = 'player'
    form_fields = ['decision_3']
    
    def vars_for_template(player):
        return {
            'lotteries': C.DECISION_3_LOTTERIES,
            'decision_number': 3,
            'is_gain': True
        }


class Investment4(Page):
    form_model = 'player'
    form_fields = ['decision_4']
    
    def vars_for_template(player):
        return {
            'lotteries': C.DECISION_4_LOTTERIES,
            'decision_number': 4,
            'is_gain': False
        }


class LotteryDraw(Page):
    def before_next_page(player, timeout_happened):
        # Choisir une décision au hasard
        decision_number = random.randint(1, 4)
        player.chosen_decision = decision_number
        
        # Obtenir la loterie choisie pour cette décision
        if decision_number == 1:
            chosen_lottery = player.decision_1
            lottery_info = C.DECISION_1_LOTTERIES[chosen_lottery]
            player.is_gain = True
        elif decision_number == 2:
            chosen_lottery = player.decision_2
            lottery_info = C.DECISION_2_LOTTERIES[chosen_lottery]
            player.is_gain = False
        elif decision_number == 3:
            chosen_lottery = player.decision_3
            lottery_info = C.DECISION_3_LOTTERIES[chosen_lottery]
            player.is_gain = True
        else:
            chosen_lottery = player.decision_4
            lottery_info = C.DECISION_4_LOTTERIES[chosen_lottery]
            player.is_gain = False
        
        player.chosen_lottery = chosen_lottery
        
        # Tirage au sort pour déterminer le résultat de la loterie
        player.lottery_result = random.random()  # Nombre aléatoire entre 0 et 1
        
        # Déterminer le résultat de la loterie
        if player.lottery_result <= lottery_info['probs'][0]:
            player.lottery_outcome = cu(lottery_info['payouts'][0])
        else:
            player.lottery_outcome = cu(lottery_info['payouts'][1])
        
        # Calculer le paiement final
        player.final_payoff = C.ENDOWMENT + player.lottery_outcome
        print(f"Paiement final calculé: {player.final_payoff}")  # Debug
    
    def vars_for_template(player):
        # Since chosen_decision is not set yet at this stage, we don't need to use it
        # Instead, we can just show a message informing that a decision will be chosen
        return dict(
            # No need to reference player.chosen_decision here
            decisions_made=[1, 2, 3, 4]  # Just pass the list of decisions for display purposes
        )


class Results(Page):
    def vars_for_template(player):
        # Déterminer quelle loterie a été sélectionnée
        if player.chosen_decision == 1:
            lottery_info = C.DECISION_1_LOTTERIES[player.chosen_lottery]
        elif player.chosen_decision == 2:
            lottery_info = C.DECISION_2_LOTTERIES[player.chosen_lottery]
        elif player.chosen_decision == 3:
            lottery_info = C.DECISION_3_LOTTERIES[player.chosen_lottery]
        else:
            lottery_info = C.DECISION_4_LOTTERIES[player.chosen_lottery]

        # Formater les nombres pour l'affichage
        lottery_result_formatted = f"{player.lottery_result:.4f}"
        threshold_formatted = f"{lottery_info['probs'][0]:.1f}"
        
        return {
            'initial_endowment': C.ENDOWMENT,
            'lottery_outcome': player.lottery_outcome,
            'payoff': player.final_payoff,
            'chosen_decision': player.chosen_decision,
            'chosen_lottery': player.chosen_lottery,
            'lottery_desc': lottery_info['description'],
            'lottery_result': player.lottery_result,  # Valeur originale pour les comparaisons
            'lottery_result_formatted': lottery_result_formatted,  # Valeur formatée pour l'affichage
            'lottery_threshold': lottery_info['probs'][0],  # Valeur originale
            'threshold_formatted': threshold_formatted,  # Valeur formatée
            'high_outcome': cu(lottery_info['payouts'][0]),
            'low_outcome': cu(lottery_info['payouts'][1]),
            'is_gain': player.is_gain,
            # Ajout d'indicateurs clairs pour le template
            'won_high': player.lottery_result <= lottery_info['probs'][0]
        }

page_sequence = [
    Instructions,
    CountDigitIntro,
    CountDigitTask,
    TaskSuccess,
    InvestmentInfo,
    Investment1,
    Investment2,
    Investment3,
    Investment4,
    LotteryDraw,
    Results,
]