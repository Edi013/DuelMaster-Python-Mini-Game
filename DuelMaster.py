import random

# Utility for stat variation
def varied_stat(base, variation):
    return max(1, base + random.randint(-variation, variation))

class Character:
    def __init__(self, name, description, health, accuracy):
        self.name = name
        self.description = description
        self.health = health
        self.max_health = health
        self.accuracy = accuracy
        self.alive = True

    def describe(self):
        return f"{self.name}\n{self.description}\nHealth: {self.health}\nAccuracy: {self.accuracy}%"

    def attempt_hit(self):
        return random.randint(1, 100) <= self.accuracy

class Weapon:
    def __init__(self, name, min_dmg, max_dmg):
        self.name = name
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def attack(self):
        return random.randint(self.min_dmg, self.max_dmg)

class Enemy(Character):
    def __init__(self, name, description, weapon, health, accuracy):
        super().__init__(name, description, health, accuracy)
        self.weapon = weapon

    def reset(self):
        self.health = self.max_health
        self.alive = True

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False
            return f"{self.name} has been defeated!"
        return f"{self.name} has {self.health} HP left."

    def attack_player(self, player):
        if self.attempt_hit():
            dmg = self.weapon.attack()
            return player.take_damage(dmg), f"{self.name} hits you with {self.weapon.name} for {dmg} damage."
        else:
            return "", f"{self.name} missed their attack!"

class ShadowForce(Enemy):
    def __init__(self):
        health = varied_stat(110, 30)
        accuracy = varied_stat(70, 30)
        super().__init__("Shadow Force", "A dark entity", Weapon("Darkness", 0, 0), health, accuracy)

    def attack_player(self, player):
        results = []
        messages = []
        for _ in range(2):
            if self.attempt_hit():
                dmg = 25
                results.append(player.take_damage(dmg))
                messages.append(f"{self.name} hits you for 25 damage.")
            else:
                messages.append(f"{self.name} missed one of their attacks.")
        return "\n".join(results), "\n".join(messages)

class Orc(Enemy):
    def __init__(self):
        health = varied_stat(130, 25)
        accuracy = varied_stat(40, 15)
        super().__init__("Orc", "A strong brute", Weapon("Club", 5, 60), health, accuracy)

class Elf(Enemy):
    def __init__(self):
        health = varied_stat(90, 15)
        accuracy = varied_stat(60, 15)
        super().__init__("Elf", "A swift archer", Weapon("Bow", 30, 36), health, accuracy)

class Goblin(Enemy):
    def __init__(self):
        health = varied_stat(80, 10)
        accuracy = varied_stat(65, 10)
        super().__init__("Goblin", "A foul creature", Weapon("Rusty Knife", 10, 30), health, accuracy)

class Player(Character):
    def __init__(self):
        self.wins = 0
        alive = True
        health = varied_stat(110, 10)
        accuracy = varied_stat(55, 5)
        self.base_accuracy = accuracy
        self.base_health = health
        self.weapon = Weapon("Sword", 10, 50)
        super().__init__("Hero", "The brave warrior", health, accuracy)

    def update_stats(self):
        self.max_health = self.base_health + 2.5 * self.wins
        self.accuracy = min(100, self.base_accuracy + 1 * self.wins)  
        self.health = self.max_health  

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False
            return f"You have been defeated!"
        return f"You have {self.health} HP left."

    def reset(self):
        self.health = self.max_health
        self.alive = True

class Game:
    def __init__(self):
        self.running = True
        self.player = Player()
        self.enemies = {
            "goblin": Goblin(),
            "orc": Orc(),
            "elf": Elf(),
            "shadow-force": ShadowForce()
        }

    def run(self):
        print("🏟 Welcome to the battle arena!")

        while self.running and self.player.alive:
            print("\nChoose an enemy to fight:")
            enemies = [
                ("1", "orc"),
                ("2", "shadow-force"),
                ("3", "elf"),
                ("4", "goblin")
            ]

            for num, name in enemies:
                print(f"{num}. {name.capitalize()}")
            print("Type 'examine' to view your stats or 'quit' to exit.")

            choice = input(">>> : ").strip().lower()

            if choice == "quit":
                print("👋 Game over.")
                break
            elif choice == "examine":
                print("\n📊 Your stats:")
                print(self.player.describe())
            elif choice in dict(enemies):
                enemy_name = dict(enemies)[choice]
                enemy = self.enemies[enemy_name].__class__()
                self.fight_loop(enemy)
                if self.player.alive and not enemy.alive:
                    self.player.wins += 1
                    self.player.update_stats()
                    print("🏅 You won! Your stats have improved.")
            else:
                print("❌ Invalid option.")


    def fight_loop(self, enemy):
        print("\n⚔️  You are now fighting the " + enemy.name +' !')
        print("\nYour stats:")
        print(self.player.describe())  # Player stats
        print("\nYour enemy stats:")
        print(enemy.describe()) 
        while enemy.alive and self.player.alive:
            command = input(">>> : ").strip().lower()
            if command.startswith("hit"):
                if self.player.attempt_hit():
                    dmg = self.player.weapon.attack()
                    print(f"You strike with your {self.player.weapon.name} for {dmg} damage!")
                    print(enemy.take_damage(dmg))
                else:
                    print("❌ You missed your attack!")
                if enemy.alive:
                    result, msg = enemy.attack_player(self.player)
                    print(msg)
                    if result:
                        print(result)
            elif command.startswith("examine"):
                print("\n⚔️  You are now fighting the " + enemy.name +' !')
                print("\nYour stats:")
                print(self.player.describe())  # Player stats
                print("\nYour enemy stats:")
                print(enemy.describe()) 
            
            elif command == "flee":
                print("🏃 You try to flee!")
                num_attacks = random.randint(0, 2)
                for _ in range(num_attacks):
                    if enemy.alive:
                        result, msg = enemy.attack_player(self.player)
                        print(f"While fleeing... {msg}")
                        print(result)
                if self.player.alive:
                    self.player.health = self.player.max_health
                    print("✅ You fled successfully and fully healed!")
                    return  # Go back to enemy selection
                print("You died while trying to flee !")
                return # Player is dead, stop

            elif command == "quit":
                self.running = False
                print("👋 Game over.")
                return

            elif command == "help":
                print("Commands:")
                print("- hit")
                print("- examine")
                print("- flee")
                print("- quit")

            else:
                print("❓ Unknown command. Type 'help'.")


if __name__ == "__main__":
    Game().run()