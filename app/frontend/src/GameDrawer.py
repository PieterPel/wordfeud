import pygame
import pygame.freetype

from BoardDrawer import BoardDrawer
from PlankDrawer import PlankDrawer
from CurrentMoveDrawer import CurrentMoveDrawer
from ButtonDrawer import ButtonDrawer
from OtherDrawer import OtherDrawer


class GameDrawer:
    # Set up some constants
    CELL_SIZE = 40  # You can change this to whatever you like
    BORDER_WIDTH = 5
    BORDER_COLOR = (0, 0, 0)  # RGB color for black
    BACKGROUND_COLOR = (20, 20, 20)
    TEXT_COLOR = (255, 255, 255)
    HIGHLIGHT_COLOR = (150, 150, 150)

    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.WIDTH = self.board.LENGTH * self.CELL_SIZE
        self.HEIGHT = self.board.HEIGHT * self.CELL_SIZE
        self.FONT = pygame.freetype.SysFont("Calibri", 28)

        self.screen = pygame.display.set_mode(
            (
                self.WIDTH + 2 * self.BORDER_WIDTH,
                self.HEIGHT + 3 * self.CELL_SIZE + 2 * self.BORDER_WIDTH,
            )
        )

        # Initialize dictionaries that contain information on clickable elements
        self.tile_rects = {}
        self.empty_tiles_on_plank_index = {}
        self.coordinates_empty_cells = {}
        self.button_rects = {}

        # Initialize helper classes to draw subelements
        # Note they are updated in the subclasses
        self.board_drawer = BoardDrawer(self)
        self.plank_drawer = PlankDrawer(self)
        self.current_move_drawer = CurrentMoveDrawer(self)
        self.other_drawer = OtherDrawer(self)
        self.button_drawer = ButtonDrawer(self)

    def draw_all(self, player):
        self._reset_dicts()
        self.board_drawer.draw()
        self.current_move_drawer.draw(player)
        self.plank_drawer.draw(player)
        self.button_drawer.draw()
        self.other_drawer.draw(player)

    def _reset_dicts(self):
        self.tile_rects = {}
        self.empty_tiles_on_plank_index = {}
        self.coordinates_empty_cells = {}
        self.button_rects = {}
