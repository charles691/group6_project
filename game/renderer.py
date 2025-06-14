# game/renderer.py
"""
負責渲染遊戲畫面，包括迷宮、Pac-Man、鬼魂和分數顯示。
"""
import pygame
import math
from .entities.pellets import PowerPellet, ScorePellet
from .entities.pacman import PacMan
from .entities.ghost import Ghost
from typing import List, Tuple

from .maze_generator import Map
from config import BLACK, DARK_GRAY, GRAY, GREEN, PINK, RED, BLUE, ORANGE, YELLOW, WHITE, LIGHT_BLUE, CELL_SIZE, TILE_BOUNDARY, TILE_WALL, TILE_PATH, TILE_POWER_PELLET, TILE_GHOST_SPAWN, TILE_DOOR
from .game import Game

class Renderer:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, screen_width: int, screen_height: int):
        """
        初始化渲染器。

        Args:
            screen (pygame.Surface): Pygame 畫面物件。
            font (pygame.font.Font): 用於渲染文字的字體。
            screen_width (int): 螢幕寬度。
            screen_height (int): 螢幕高度。
        """
        self.screen = screen
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height

    def render(self, game: 'Game', control_mode: str, frame_count: int) -> None:
        """
        渲染遊戲畫面。

        Args:
            game (Game): 遊戲實例。
            control_mode (str): 當前控制模式名稱。
            frame_count (int): 動畫幀計數器。
        """
        self.screen.fill(BLACK)  # 清空畫面

        # 渲染迷宮
        maze = game.get_maze()
        for y in range(maze.height):
            for x in range(maze.width):
                tile = maze.get_tile(x, y)
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # 計算格子矩形
                if tile == TILE_BOUNDARY:
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)  # 繪製邊界（深灰色）
                elif tile == TILE_WALL:
                    pygame.draw.rect(self.screen, BLACK, rect)  # 繪製牆壁（黑色）
                elif tile == TILE_PATH:
                    pygame.draw.rect(self.screen, GRAY, rect)  # 繪製路徑（灰色）
                elif tile == TILE_POWER_PELLET:
                    pygame.draw.rect(self.screen, GRAY, rect)  # 繪製能量球位置（綠色）
                elif tile == TILE_GHOST_SPAWN:
                    pygame.draw.rect(self.screen, PINK, rect)  # 繪製鬼魂重生點（粉紅色）
                elif tile == TILE_DOOR:
                    pygame.draw.rect(self.screen, RED, rect)  # 繪製門（紅色）

        # 渲染能量球
        for pellet in game.get_power_pellets():
            pellet_rect = pygame.Rect(
                pellet.x * CELL_SIZE + CELL_SIZE // 4,
                pellet.y * CELL_SIZE + CELL_SIZE // 4,
                CELL_SIZE // 2, CELL_SIZE // 2)  # 計算能量球矩形（居中，半格大小）
            pygame.draw.ellipse(self.screen, ORANGE, pellet_rect)  # 繪製藍色圓形能量球

        # 渲染分數球
        for score_pellet in game.get_score_pellets():
            score_pellet_rect = pygame.Rect(
                score_pellet.x * CELL_SIZE + CELL_SIZE * 3 // 8,
                score_pellet.y * CELL_SIZE + CELL_SIZE * 3 // 8,
                CELL_SIZE // 4, CELL_SIZE // 4)  # 計算分數球矩形（居中，半格大小）
            pygame.draw.ellipse(self.screen, ORANGE, score_pellet_rect)  # 繪製橙色圓形分數球

        # 渲染 Pac-Man
        pacman = game.get_pacman()
        pacman_rect = pygame.Rect(
            pacman.current_x - CELL_SIZE // 4,
            pacman.current_y - CELL_SIZE // 4,
            CELL_SIZE // 2, CELL_SIZE // 2)
        
        if game.is_death_animation_playing():
            # 死亡動畫：縮小 Pac-Man
            progress = game.get_death_animation_progress()  # 動畫進度（0 到 1）
            scale = 1.0 - progress  # 縮放比例，從 1 減小到 0
            radius = int(CELL_SIZE // 2 * scale)  # 計算縮放後的圓半徑
            pacman_center = (
                pacman.current_x,
                pacman.current_y,
                )  # Pac-Man 當前中心坐標
            if radius > 0:
                pygame.draw.circle(self.screen, YELLOW, pacman_center, radius)  # 繪製縮小的黃色圓形
        else:
            # 正常繪製 Pac-Man
            pacman_rect = pygame.Rect(
                pacman.current_x - CELL_SIZE // 4,
                pacman.current_y - CELL_SIZE // 4,
                CELL_SIZE // 2, CELL_SIZE // 2)  # 計算 Pac-Man 矩形（居中，半格大小）
            pygame.draw.ellipse(self.screen, YELLOW, pacman_rect)  # 繪製黃色圓形 Pac-Man

            direction_angle = 180
            while True :
                if (pacman.target_x - pacman.x) > 0: 
                    direction_angle = 0
                elif (pacman.target_x - pacman.x) < 0:
                    direction_angle = 180
                elif (pacman.target_y - pacman.y) > 0:
                    direction_angle = 90
                elif (pacman.target_y - pacman.y) < 0:
                    direction_angle = 270
                break
            direction_rad = math.radians(direction_angle)

            point1 = (pacman.current_x, pacman.current_y)
            point2 = (
                pacman.current_x + CELL_SIZE // 4 * math.cos(direction_rad)*1.3,
                pacman.current_y + CELL_SIZE // 4 * math.sin(direction_rad)*1.3
            )
            point3 = (
                pacman.current_x + CELL_SIZE // 4 * math.cos(direction_rad + math.pi / 4),
                pacman.current_y + CELL_SIZE // 4 * math.sin(direction_rad + math.pi / 4)
            )
            point4 = (
                pacman.current_x + CELL_SIZE // 4 * math.cos(direction_rad - math.pi / 4),
                pacman.current_y + CELL_SIZE // 4 * math.sin(direction_rad - math.pi / 4)
            )
            pygame.draw.polygon(self.screen, GRAY, [point1, point4, point2, point3])

            


        # 渲染鬼魂
        for ghost in game.get_ghosts():
            if ghost.returning_to_spawn:
                base_color = DARK_GRAY
                ghost.alpha = int(128 + 127 * math.sin(frame_count * 0.2))  # 閃爍效果
            elif ghost.edible and ghost.edible_timer > 0:
                base_color = LIGHT_BLUE
                ghost.alpha = 255
            else:
                base_color = ghost.color
                ghost.alpha = 255

            ghost_surface = pygame.Surface((CELL_SIZE // 2, CELL_SIZE // 2), pygame.SRCALPHA)
            ghost_surface.fill((0, 0, 0, 0))  # 透明背景
            pygame.draw.ellipse(ghost_surface, (*base_color, ghost.alpha),
                               (0, 0, CELL_SIZE // 2, CELL_SIZE // 2))
            self.screen.blit(ghost_surface, (ghost.current_x - CELL_SIZE // 4, ghost.current_y - CELL_SIZE // 4))

        # 渲染分數和控制模式
        score_text = self.font.render(f"Score: {pacman.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        mode_text = self.font.render(control_mode, True, WHITE)
        self.screen.blit(mode_text, (self.screen_width - 150, 10))