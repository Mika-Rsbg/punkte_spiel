class AttackLogic:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender

    def calculate_damage(self):
        # Berechnung des Schadens
        return max(self.attacker.stärke - self.defender.verteidigung, 0)

    def execute_attack(self):
        damage = self.calculate_damage()
        self.defender.leben -= damage
