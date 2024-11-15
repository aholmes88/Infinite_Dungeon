import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

background = pygame.image.load('Cave - 1.jpg')
 

# Fonts
FONT = pygame.font.Font(None, 36)

# Player Class
class Player:
    def __init__(self):
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        self.level = 1
        self.experience = 0
        self.xp_to_next_level = 50

    def attack(self):
        return random.randint(10, 20)

    def cast_spell(self):
        if self.mana >= 10:
            self.mana -= 10
            return random.randint(20, 30)
        return 0

    def rest(self):
        self.health = min(self.max_health, self.health + 20)
        self.mana = min(self.max_mana, self.mana + 20)

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= self.xp_to_next_level
        self.xp_to_next_level += 25
        self.max_health += 20
        self.max_mana += 10
        self.health = self.max_health
        self.mana = self.max_mana
        print(f"Level up! You are now level {self.level}.")

# Monster Class
class Monster:
    def __init__(self, level, multiplier=1):
        self.health = int(level * 20 * multiplier)
        self.max_health = self.health  # Store max health
        self.damage = random.randint(5, 15) + int(level * multiplier)
        self.level = level

    def attack(self):
        return self.damage

# Helper Function to Draw Text
def draw_text(surface, text, x, y, color):
    text_surface = FONT.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Main Game Function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Infinite Dungeon")
    clock = pygame.time.Clock()

    # Initialize game entities
    player = Player()
    monster_multiplier = 1  # Monsters grow stronger over time
    monster = Monster(player.level, monster_multiplier)
    player_turn = True
    monster_defeated_count = 0
    turn_action_taken = False  # Tracks if player has taken an action this turn

    running = True
    while running:
        screen.blit(background, (0,0))



        # Default message to ensure it's always initialized
        message = "Your turn! Press SPACE to attack, C to cast a spell, or R to rest."

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if player_turn:
            if keys[pygame.K_SPACE]:  # Attack
                damage = player.attack()
                monster.health -= damage
                message = f"You dealt {damage} damage to the monster!"
                player_turn = False
                turn_action_taken = True

            elif keys[pygame.K_c]:  # Cast Spell
                damage = player.cast_spell()
                if damage > 0:
                    monster.health -= damage
                    message = f"You cast a spell and dealt {damage} damage!"
                else:
                    message = "Not enough mana to cast a spell!"
                player_turn = False
                turn_action_taken = True

            elif keys[pygame.K_r]:  # Rest
                player.rest()
                message = "You rested and recovered health and mana."
                player_turn = False
                turn_action_taken = True

        else:  # Monster's turn
            damage = monster.attack()
            player.health -= damage
            message = f"The monster attacked and dealt {damage} damage!"
            player.health = max(0, player.health)  # Ensure player's health doesn't go negative
            player_turn = True
            turn_action_taken = False

        # Check for Monster Defeat
        if monster.health <= 0:
            monster_defeated_count += 1
            player.gain_experience(20)
            message = f"You defeated the monster! A Stronger one has now appeared."
            monster_multiplier += 0.2  # Increment monster strength multiplier
            monster = Monster(player.level, monster_multiplier)

        # Check for Player Defeat
        if player.health <= 0:
            message = "Game Over! You were defeated."
            running = False

        # Draw Game Stats
        draw_text(screen, "Turn-Based Game", 300, 20, BLACK)
        draw_text(screen, f"Player Health: {player.health}/{player.max_health}", 50, 100, GREEN)
        draw_text(screen, f"Player Mana: {player.mana}/{player.max_mana}", 50, 150, BLUE)
        draw_text(screen, f"Player Level: {player.level}", 50, 200, BLACK)
        draw_text(screen, f"Experience: {player.experience}/{player.xp_to_next_level}", 50, 250, BLACK)
        draw_text(screen, f"Monster Health: {monster.health}/{monster.max_health}", 50, 300, RED)
        draw_text(screen, message, 50, 400, BLACK)  # Ensure the message is displayed

        # Refresh the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()