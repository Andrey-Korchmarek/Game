import pygame
from engine.game_loop import GameLoop
from engine.state_manager import StateManager
from scenes.menu_scene import MenuScene
from scenes.game_scene import GameScene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Моя игра")

        self.state_manager = StateManager()
        self.state_manager.add_state("menu", MenuScene(self))
        self.state_manager.add_state("game", GameScene(self))

        self.state_manager.change_state("menu")

    def run(self):
        game_loop = GameLoop()
        game_loop.run()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()