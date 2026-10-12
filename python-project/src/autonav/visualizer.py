"""Pygame drawing and keyboard controls for the deterministic simulator."""

from __future__ import annotations

import pygame

from .models import Scenario
from .simulator import Simulator

WINDOW_WIDTH = 1180
WINDOW_HEIGHT = 780
PANEL_WIDTH = 300
BACKGROUND = (10, 17, 28)
PANEL = (16, 26, 40)
GRID_BACKGROUND = (20, 32, 48)
GRID_LINE = (34, 50, 69)
WALL = (83, 102, 124)
PATH = (39, 210, 177)
ROBOT = (255, 185, 74)
GOAL = (255, 107, 122)
TEXT = (226, 236, 245)
MUTED = (132, 153, 174)
ACCENT = (78, 155, 255)


def run_visualizer(scenario: Scenario) -> None:
    pygame.init()
    pygame.display.set_caption("AI-Based Autonomous Navigation System")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 32)
    body_font = pygame.font.Font(None, 23)
    small_font = pygame.font.Font(None, 18)
    simulation = Simulator(scenario)
    last_step = 0
    cell_size = 34

    running = True
    while running:
        screen_width, screen_height = screen.get_size()
        panel_x = screen_width - PANEL_WIDTH
        map_area_width = max(300, panel_x - 48)
        map_area_height = max(300, screen_height - 130)
        cell_size = max(
            16,
            min(
                42,
                map_area_width // scenario.width,
                map_area_height // scenario.height,
            ),
        )
        map_width = scenario.width * cell_size
        map_height = scenario.height * cell_size
        map_x = max(24, (panel_x - map_width) // 2)
        map_y = max(88, (screen_height - map_height) // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if simulation.status == "running":
                        simulation.pause()
                    else:
                        simulation.start()
                elif event.key == pygame.K_r:
                    simulation.reset()

        now = pygame.time.get_ticks()
        if simulation.status == "running" and now - last_step >= 150:
            simulation.step()
            last_step = now

        screen.fill(BACKGROUND)
        title = title_font.render("AUTONOMOUS NAVIGATION LAB", True, TEXT)
        screen.blit(title, (26, 22))
        subtitle = small_font.render(
            "GRID-WORLD SIMULATION  /  A* PLANNER  /  SYNTHETIC MAP KNOWLEDGE",
            True,
            MUTED,
        )
        screen.blit(subtitle, (28, 52))

        map_rect = pygame.Rect(map_x, map_y, map_width, map_height)
        pygame.draw.rect(screen, GRID_BACKGROUND, map_rect, border_radius=8)
        route = simulation.route or []
        for y in range(scenario.height):
            for x in range(scenario.width):
                cell = (x, y)
                rect = pygame.Rect(
                    map_x + x * cell_size,
                    map_y + y * cell_size,
                    cell_size,
                    cell_size,
                )
                pygame.draw.rect(screen, GRID_LINE, rect, 1)
                if cell in scenario.obstacles:
                    inner = rect.inflate(-4, -4)
                    pygame.draw.rect(screen, WALL, inner, border_radius=4)
                elif cell in route[1:-1]:
                    inner = rect.inflate(-5, -5)
                    pygame.draw.rect(screen, PATH, inner, border_radius=5)

        start_x, start_y = scenario.start
        goal_x, goal_y = scenario.goal
        pygame.draw.circle(
            screen,
            (118, 153, 201),
            (map_x + start_x * cell_size + cell_size // 2, map_y + start_y * cell_size + cell_size // 2),
            max(4, cell_size // 5),
        )
        pygame.draw.circle(
            screen,
            GOAL,
            (map_x + goal_x * cell_size + cell_size // 2, map_y + goal_y * cell_size + cell_size // 2),
            max(5, cell_size // 4),
        )
        robot_x, robot_y = simulation.robot
        robot_center = (
            map_x + robot_x * cell_size + cell_size // 2,
            map_y + robot_y * cell_size + cell_size // 2,
        )
        pygame.draw.circle(screen, (60, 44, 26), robot_center, max(9, cell_size // 2 - 3))
        pygame.draw.circle(screen, ROBOT, robot_center, max(5, cell_size // 3))

        pygame.draw.rect(screen, PANEL, (panel_x, 0, PANEL_WIDTH, screen_height))
        panel_padding = panel_x + 22
        screen.blit(title_font.render("Run status", True, TEXT), (panel_padding, 28))
        status_color = PATH if simulation.status == "completed" else ACCENT
        if simulation.status in {"blocked", "no_path"}:
            status_color = GOAL
        screen.blit(
            body_font.render(simulation.status.replace("_", " ").upper(), True, status_color),
            (panel_padding, 66),
        )
        screen.blit(title_font.render(scenario.name, True, TEXT), (panel_padding, 112))
        description_lines = _wrap(scenario.description, small_font, PANEL_WIDTH - 44)
        for line_index, line in enumerate(description_lines[:4]):
            screen.blit(small_font.render(line, True, MUTED), (panel_padding, 145 + 21 * line_index))

        metrics = simulation.metrics()
        stats_y = 248
        stats = (
            ("ROUTE LENGTH", str(metrics.planned_cells)),
            ("STEPS TAKEN", str(metrics.steps_taken)),
            ("COLLISIONS", str(metrics.collisions)),
            ("ROUTE EFFICIENCY", f"{metrics.efficiency:.0%}" if metrics.steps_taken else "—"),
        )
        for label, value in stats:
            screen.blit(small_font.render(label, True, MUTED), (panel_padding, stats_y))
            screen.blit(body_font.render(value, True, TEXT), (panel_padding, stats_y + 22))
            stats_y += 63

        divider_y = stats_y + 2
        pygame.draw.line(screen, GRID_LINE, (panel_padding, divider_y), (screen_width - 22, divider_y), 1)
        screen.blit(title_font.render("Controls", True, TEXT), (panel_padding, divider_y + 22))
        help_lines = [
            "SPACE  Start / pause",
            "R            Reset run",
            "ESC        Exit simulator",
        ]
        for index, line in enumerate(help_lines):
            screen.blit(body_font.render(line, True, MUTED), (panel_padding, divider_y + 62 + 32 * index))
        note = "Synthetic, static grid map. No camera model or learned perception."
        for index, line in enumerate(_wrap(note, small_font, PANEL_WIDTH - 44)):
            screen.blit(small_font.render(line, True, MUTED), (panel_padding, screen_height - 62 + 18 * index))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def _wrap(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and font.size(candidate)[0] > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines
