

import pygame
import sys
from collections import deque
import heapq


ROWS        = 30
COLS        = 30
CELL_SIZE   = 22
PANEL_WIDTH = 320
WIN_WIDTH   = COLS * CELL_SIZE + PANEL_WIDTH
WIN_HEIGHT  = ROWS * CELL_SIZE + 40


DIRECTIONS = [
    (-1,  0),   # Up
    ( 0,  1),   # Right
    ( 1,  0),   # Bottom
    ( 1,  1),   # Bottom-Right (diagonal)
    ( 0, -1),   # Left
    (-1, -1),   # Top-Left (diagonal)
]

WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
GRAY        = (180, 180, 180)
CYAN        = (  0, 220, 220)
LIGHT_BLUE  = (173, 216, 230)
PURPLE      = (128,   0, 128)
GREEN       = (  0, 200,   0)
RED         = (210,   0,   0)
DARK_BG     = ( 28,  28,  42)
PANEL_BG    = ( 18,  18,  32)
BTN_GREEN   = ( 46, 160,  67)
BTN_DARK    = ( 45,  50,  70)
BTN_RED     = (150,  28,  28)
BTN_BLUE    = ( 25,  55, 130)
TEXT_WHITE  = (240, 240, 240)
TEXT_GRAY   = (145, 145, 158)

grid        = [[0] * COLS for _ in range(ROWS)]
start_node  = None
end_node    = None
explored    = set()
frontier    = set()
final_path  = []
status_msg  = ""
active_algo = None
screen      = None


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def get_neighbors(r, c):
    result = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc) and grid[nr][nc] != 1:
            result.append((nr, nc))
    return result


def move_cost(r1, c1, r2, c2):
    return 1.414 if (r1 != r2 and c1 != c2) else 1.0


def rebuild_path(came_from, node):
    path = []
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path


def reset_search():
    global explored, frontier, final_path, status_msg
    explored   = set()
    frontier   = set()
    final_path = []
    status_msg = ""


def clear_grid():
    global grid, start_node, end_node
    grid       = [[0] * COLS for _ in range(ROWS)]
    start_node = None
    end_node   = None
    reset_search()


def step_delay():
    draw()
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def run_bfs():
    global explored, frontier, final_path, status_msg, active_algo
    reset_search()
    active_algo = "BFS"

    if not start_node or not end_node:
        status_msg = "Please set Start and End nodes first."
        return

    queue     = deque([start_node])
    came_from = {start_node: None}
    visited   = {start_node}

    while queue:
        current = queue.popleft()
        explored.add(current)
        frontier.discard(current)

        if current == end_node:
            final_path = rebuild_path(came_from, end_node)
            status_msg = (f"BFS: Found!   Explored {len(explored)} nodes   "
                          f"Path {len(final_path)} steps")
            return

        for nb in get_neighbors(*current):
            if nb not in visited:
                visited.add(nb)
                came_from[nb] = current
                queue.append(nb)
                frontier.add(nb)

        step_delay()

    status_msg = f"BFS: No path found!   Explored {len(explored)} nodes"


def run_dfs():
    global explored, frontier, final_path, status_msg, active_algo
    reset_search()
    active_algo = "DFS"

    if not start_node or not end_node:
        status_msg = "Please set Start and End nodes first."
        return

    stack     = [start_node]
    came_from = {start_node: None}
    visited   = {start_node}

    while stack:
        current = stack.pop()
        explored.add(current)
        frontier.discard(current)

        if current == end_node:
            final_path = rebuild_path(came_from, end_node)
            status_msg = (f"DFS: Found!   Explored {len(explored)} nodes   "
                          f"Path {len(final_path)} steps")
            return

        for nb in get_neighbors(*current):
            if nb not in visited:
                visited.add(nb)
                came_from[nb] = current
                stack.append(nb)
                frontier.add(nb)

        step_delay()

    status_msg = f"DFS: No path found!   Explored {len(explored)} nodes"


def run_ucs():
    global explored, frontier, final_path, status_msg, active_algo
    reset_search()
    active_algo = "UCS"

    if not start_node or not end_node:
        status_msg = "Please set Start and End nodes first."
        return

    heap      = [(0.0, start_node)]
    came_from = {start_node: None}
    g_cost    = {start_node: 0.0}
    visited   = set()

    while heap:
        cost, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        explored.add(current)
        frontier.discard(current)

        if current == end_node:
            final_path = rebuild_path(came_from, end_node)
            status_msg = (f"UCS: Found!   Explored {len(explored)} nodes   "
                          f"Path {len(final_path)} steps")
            return

        for nb in get_neighbors(*current):
            new_cost = g_cost[current] + move_cost(current[0], current[1], nb[0], nb[1])
            if nb not in g_cost or new_cost < g_cost[nb]:
                g_cost[nb]    = new_cost
                came_from[nb] = current
                heapq.heappush(heap, (new_cost, nb))
                frontier.add(nb)

        step_delay()

    status_msg = f"UCS: No path found!   Explored {len(explored)} nodes"


def run_dls(depth_limit=15):
    global explored, frontier, final_path, status_msg, active_algo
    reset_search()
    active_algo = "DLS"

    if not start_node or not end_node:
        status_msg = "Please set Start and End nodes first."
        return

    came_from = {start_node: None}

    def dls_recursive(node, depth, visited):
        explored.add(node)

        if node == end_node:
            return True
        if depth == 0:
            return False

        for nb in get_neighbors(*node):
            if nb not in visited:
                visited.add(nb)
                came_from[nb] = node
                frontier.add(nb)
                step_delay()

                if dls_recursive(nb, depth - 1, visited):
                    return True
                frontier.discard(nb)

        return False

    visited = {start_node}
    found   = dls_recursive(start_node, depth_limit, visited)

    if found:
        final_path = rebuild_path(came_from, end_node)
        status_msg = (f"DLS: Found!   Explored {len(explored)} nodes   "
                      f"Path {len(final_path)} steps")
    else:
        status_msg = (f"DLS: No path found within depth {depth_limit}!   "
                      f"Explored {len(explored)} nodes")


def run_iddfs():
    global explored, frontier, final_path, status_msg, active_algo
    reset_search()
    active_algo = "IDDFS"

    if not start_node or not end_node:
        status_msg = "Please set Start and End nodes first."
        return

    for depth_limit in range(1, ROWS * COLS + 1):
        explored.clear()
        frontier.clear()

        came_from = {start_node: None}
        visited   = {start_node}

        def dls(node, depth):
            explored.add(node)

            if node == end_node:
                return True
            if depth == 0:
                return False

            for nb in get_neighbors(*node):
                if nb not in visited:
                    visited.add(nb)
                    came_from[nb] = node
                    frontier.add(nb)
                    step_delay()

                    if dls(nb, depth - 1):
                        return True
                    frontier.discard(nb)

            return False

        if dls(start_node, depth_limit):
            final_path = rebuild_path(came_from, end_node)
            status_msg = (f"IDDFS: Found!   Explored {len(explored)} nodes   "
                          f"Path {len(final_path)} steps")
            return

    status_msg = f"IDDFS: No path found!   Explored {len(explored)} nodes"

def run_bidirectional():
    global explored, frontier, final_path, status_msg, active_algo
    reset_search()
    active_algo = "Bidirectional"

    if not start_node or not end_node:
        status_msg = "Please set Start and End nodes first."
        return

    fwd_queue   = deque([start_node])
    bwd_queue   = deque([end_node])
    fwd_visited = {start_node: None}
    bwd_visited = {end_node:   None}

    def build_full_path(meeting_node):
        fwd_half = []
        node = meeting_node
        while node is not None:
            fwd_half.append(node)
            node = fwd_visited[node]
        fwd_half.reverse()

        bwd_half = []
        node = bwd_visited[meeting_node]
        while node is not None:
            bwd_half.append(node)
            node = bwd_visited[node]

        return fwd_half + bwd_half

    while fwd_queue or bwd_queue:
        if fwd_queue:
            current = fwd_queue.popleft()
            explored.add(current)
            frontier.discard(current)

            if current in bwd_visited:
                final_path = build_full_path(current)
                status_msg = (f"Bidirectional: Found!   Explored {len(explored)} nodes   "
                              f"Path {len(final_path)} steps")
                return

            for nb in get_neighbors(*current):
                if nb not in fwd_visited:
                    fwd_visited[nb] = current
                    fwd_queue.append(nb)
                    frontier.add(nb)

        if bwd_queue:
            current = bwd_queue.popleft()
            explored.add(current)
            frontier.discard(current)

            if current in fwd_visited:
                final_path = build_full_path(current)
                status_msg = (f"Bidirectional: Found!   Explored {len(explored)} nodes   "
                              f"Path {len(final_path)} steps")
                return

            for nb in get_neighbors(*current):
                if nb not in bwd_visited:
                    bwd_visited[nb] = current
                    bwd_queue.append(nb)
                    frontier.add(nb)

        step_delay()

    status_msg = f"Bidirectional: No path found!   Explored {len(explored)} nodes"


def draw():
    screen.fill(DARK_BG)
    gx = COLS * CELL_SIZE

    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE

            if   (r, c) == start_node:  color = GREEN
            elif (r, c) == end_node:    color = RED
            elif grid[r][c] == 1:       color = BLACK
            elif (r, c) in final_path:  color = PURPLE
            elif (r, c) in explored:    color = CYAN
            elif (r, c) in frontier:    color = LIGHT_BLUE
            else:                       color = WHITE

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE - 1, CELL_SIZE - 1))

    for r in range(ROWS + 1):
        pygame.draw.line(screen, GRAY, (0, r * CELL_SIZE), (gx, r * CELL_SIZE))
    for c in range(COLS + 1):
        pygame.draw.line(screen, GRAY, (c * CELL_SIZE, 0), (c * CELL_SIZE, ROWS * CELL_SIZE))

    pygame.draw.rect(screen, PANEL_BG, (gx, 0, PANEL_WIDTH, WIN_HEIGHT))

    f_title  = pygame.font.SysFont("Segoe UI", 21, bold=True)
    f_sub    = pygame.font.SysFont("Segoe UI", 12)
    f_label  = pygame.font.SysFont("Segoe UI", 10)
    f_btn    = pygame.font.SysFont("Segoe UI", 13, bold=True)
    f_small  = pygame.font.SysFont("Segoe UI", 11)
    f_status = pygame.font.SysFont("Segoe UI", 11)

    screen.blit(f_title.render("AI Pathfinder", True, TEXT_WHITE), (gx + 15, 14))
    screen.blit(f_sub.render("AI2002 \u2013 Uninformed Search", True, TEXT_GRAY), (gx + 15, 40))
    screen.blit(f_label.render("ALGORITHMS", True, TEXT_GRAY), (gx + 15, 68))

    algos = [
        ("BFS",           "Press  1"),
        ("DFS",           "Press  2"),
        ("UCS",           "Press  3"),
        ("DLS",           "Press  4"),
        ("IDDFS",         "Press  5"),
        ("Bidirectional", "Press  6"),
    ]

    for i, (name, hint) in enumerate(algos):
        by     = 84 + i * 56
        active = (name == active_algo)
        color  = BTN_GREEN if active else BTN_DARK
        pygame.draw.rect(screen, color, (gx + 12, by, 296, 46), border_radius=6)
        screen.blit(f_btn.render(name,  True, TEXT_WHITE), (gx + 22, by + 8))
        screen.blit(f_small.render(hint, True, TEXT_GRAY),  (gx + 22, by + 27))

    sy = 84 + 6 * 56 + 6
    screen.blit(f_small.render(
        f"Nodes explored: {len(explored)}   Path length: {len(final_path) if final_path else 0}",
        True, TEXT_GRAY), (gx + 15, sy))

    pygame.draw.rect(screen, BTN_RED,  (gx + 12, sy + 24, 296, 42), border_radius=6)
    screen.blit(f_btn.render("Reset Search",  True, TEXT_WHITE), (gx + 88, sy + 32))
    screen.blit(f_small.render("Press  R",    True, TEXT_GRAY),  (gx + 110, sy + 47))

    pygame.draw.rect(screen, BTN_BLUE, (gx + 12, sy + 74, 296, 42), border_radius=6)
    screen.blit(f_btn.render("Clear Grid",    True, TEXT_WHITE), (gx + 96, sy + 82))
    screen.blit(f_small.render("Press  SPACE", True, TEXT_GRAY), (gx + 100, sy + 97))

    hy = sy + 128
    screen.blit(f_label.render("CONTROLS",         True, TEXT_GRAY),  (gx + 15, hy))
    screen.blit(f_small.render("Left Click:",       True, TEXT_GRAY),  (gx + 15, hy + 16))
    screen.blit(f_small.render("Set Start / End / Wall", True, TEXT_WHITE), (gx + 90, hy + 16))
    screen.blit(f_small.render("Right Click:",      True, TEXT_GRAY),  (gx + 15, hy + 32))
    screen.blit(f_small.render("Remove node",       True, TEXT_WHITE), (gx + 90, hy + 32))

    pygame.draw.rect(screen, (10, 10, 20), (0, ROWS * CELL_SIZE, WIN_WIDTH, 40))
    if "Found" in status_msg:
        sc = (50, 220, 100)
    elif "No path" in status_msg:
        sc = (220, 60, 60)
    else:
        sc = TEXT_GRAY
    screen.blit(f_status.render(status_msg, True, sc), (10, ROWS * CELL_SIZE + 12))

    pygame.display.flip()

def main():
    global start_node, end_node, grid, status_msg, active_algo, screen

    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Algorithms for UnInformed Searches")
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx < COLS * CELL_SIZE and my < ROWS * CELL_SIZE:
                    r = my // CELL_SIZE
                    c = mx // CELL_SIZE

                    if event.button == 1:
                        if start_node is None:
                            start_node = (r, c)
                            grid[r][c] = 0
                        elif end_node is None and (r, c) != start_node:
                            end_node = (r, c)
                            grid[r][c] = 0
                        elif (r, c) != start_node and (r, c) != end_node:
                            grid[r][c] = 1

                    elif event.button == 3:
                        if (r, c) == start_node:
                            start_node = None
                        elif (r, c) == end_node:
                            end_node = None
                        else:
                            grid[r][c] = 0

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    mx, my = pygame.mouse.get_pos()
                    if mx < COLS * CELL_SIZE and my < ROWS * CELL_SIZE:
                        r = my // CELL_SIZE
                        c = mx // CELL_SIZE
                        if (r, c) != start_node and (r, c) != end_node:
                            grid[r][c] = 1

            elif event.type == pygame.KEYDOWN:
                if   event.key == pygame.K_1: run_bfs()
                elif event.key == pygame.K_2: run_dfs()
                elif event.key == pygame.K_3: run_ucs()
                elif event.key == pygame.K_4: run_dls()
                elif event.key == pygame.K_5: run_iddfs()
                elif event.key == pygame.K_6: run_bidirectional()
                elif event.key == pygame.K_r: reset_search()
                elif event.key == pygame.K_SPACE: clear_grid()


if __name__ == "__main__":
    main()
