"""
Labyrinth-Solver mit Hand-an-der-Wand-Algorithmus
Visualisiert die Erkundung mittels Prüflinie und Sound-Effekten
"""
import pygame


# ============================================================================
# KONSTANTEN - Farben
# ============================================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
LIGHT_GRAY = (220, 220, 220)
GRID_COLOR = (50, 50, 50)
BUTTON_COLOR = (100, 100, 200)
BUTTON_HOVER_COLOR = (150, 150, 255)


# ============================================================================
# KONSTANTEN - Richtungen und Koordinaten
# ============================================================================
DIRS = [
    (-1, 0),  # North
    (0, 1),   # East
    (1, 0),   # South
    (0, -1),  # West
]

CELL_SIZE = 40


# ============================================================================
# KONSTANTEN - Button-Positionen (werden nach Fenster-Init aktualisiert)
# ============================================================================
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60


# ============================================================================
# HILFSFUNKTIONEN - Datei-Operationen
# ============================================================================
def load_maze(filename):
    """
    Lädt das Labyrinth aus einer Textdatei.
    
    Format:
    - Zahlen durch Leerzeichen getrennt
    - 1 = Wand, 0 = Gang, S = Start, Z = Ziel
    
    Returns:
        list: 2D-Liste mit Labyrinth oder None bei Fehler
    """
    try:
        with open(filename, 'r') as f:
            maze = []
            for line in f:
                row = []
                for cell in line.strip().split():
                    # Wandle 1 und 0 zu Integer um, behalte S und Z als String
                    # Das ermöglicht später pattern matching mit match/case
                    if cell in ['S', 'Z']:
                        row.append(cell)
                    else:
                        row.append(int(cell))
                if row:  # Ignoriere leere Zeilen
                    maze.append(row)
            return maze
    except FileNotFoundError:
        print(f"Fehler: Datei '{filename}' nicht gefunden!")
        return None
    except ValueError as e:
        print(f"Fehler beim Laden der Labyrinth-Datei: {e}")
        return None


# ============================================================================
# LABYRINTH LADEN / INITIALISIEREN
# ============================================================================
MAZE = load_maze('labyrinth.txt')
if MAZE is None:
    print("Fallback auf Standard-Labyrinth")
    MAZE = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 'S', 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 'Z', 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

ROWS = len(MAZE)
COLS = len(MAZE[0])

# Layout: Oberer Teil = Labyrinth, Unterer Teil = Info/Status
MAZE_HEIGHT = ROWS * CELL_SIZE
INFO_PANEL_HEIGHT = 150  # Bereich für Algorithmus-Auswahl / Status-Anzeige
TOTAL_WIDTH = COLS * CELL_SIZE
TOTAL_HEIGHT = MAZE_HEIGHT + INFO_PANEL_HEIGHT

# Button-Positionen berechnen (im Info-Panel)
INFO_Y_START = MAZE_HEIGHT  # Wo der Info-Panel beginnt
INFO_CENTER_Y = INFO_Y_START + INFO_PANEL_HEIGHT // 2
BUTTON_Y = INFO_CENTER_Y
LEFT_BUTTON_X = TOTAL_WIDTH // 4 - BUTTON_WIDTH // 2
RIGHT_BUTTON_X = 3 * TOTAL_WIDTH // 4 - BUTTON_WIDTH // 2


# ============================================================================
# HILFSFUNKTIONEN - Prüfungen
# ============================================================================
def is_cell_free(row, col):
    """
    Prüft, ob eine Zelle begehbar ist.
    Eine Zelle ist begehbar wenn sie innerhalb der Grenzen liegt und keine Wand ist.
    
    Args:
        row (int): Zeile der Zelle
        col (int): Spalte der Zelle
        
    Returns:
        bool: True wenn begehbar, False sonst
    """
    return 0 <= row < ROWS and 0 <= col < COLS and MAZE[row][col] != 1


def is_button_clicked(pos, button_x, button_y):
    """
    Prüft, ob eine Mausposition auf einem Button liegt.
    
    Args:
        pos (tuple): Mausposition (x, y)
        button_x (int): X-Koordinate des Buttons
        button_y (int): Y-Koordinate des Buttons
        
    Returns:
        bool: True wenn geklickt, False sonst
    """
    return (button_x <= pos[0] <= button_x + BUTTON_WIDTH and
            button_y <= pos[1] <= button_y + BUTTON_HEIGHT)


def find_value(value):
    """
    Sucht den ersten Vorkommen eines Wertes im Labyrinth.
    
    Args:
        value: Wert zum Suchen (z.B. 'S' für Start)
        
    Returns:
        tuple: (row, col) oder None wenn nicht gefunden
    """
    for r in range(ROWS):
        for c in range(COLS):
            if MAZE[r][c] == value:
                return (r, c)
    return None


# ============================================================================
# DRAW-FUNKTIONEN - Labyrinth und Elemente
# ============================================================================
def draw_maze(screen):
    """Zeichnet das komplette Labyrinth mit Gitter"""
    for row in range(ROWS):
        for col in range(COLS):
            cell = MAZE[row][col]
            match cell:
                case 0:
                    color = WHITE
                case 1:
                    color = BLACK
                case 'S':
                    color = YELLOW
                case 'Z':
                    color = PURPLE

            pygame.draw.rect(screen, color, 
                           (col * CELL_SIZE, row * CELL_SIZE, 
                            CELL_SIZE, CELL_SIZE))

    # Draw grid lines
    for x in range(0, TOTAL_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, MAZE_HEIGHT))
    for y in range(0, MAZE_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (TOTAL_WIDTH, y))


def draw_labot_body(surface, labot):
    """
    Zeichnet den Körper des Roboters (blauer Kreis).
    
    Args:
        surface: PyGame Surface
        labot (dict): Roboter-State mit 'row' und 'col'
    """
    pygame.draw.circle(
        surface,
        BLUE,
        (labot['col'] * CELL_SIZE + CELL_SIZE // 2,
         labot['row'] * CELL_SIZE + CELL_SIZE // 2),
        CELL_SIZE // 4
    )


def draw_labot_arm(surface, labot, color):
    """
    Zeichnet den Arm des Roboters vom Rand des Kreises zum Zellenrand.
    
    Args:
        surface: PyGame Surface
        labot (dict): Roboter-State mit 'checking_dir'
        color (tuple): RGB-Farbe des Arms
    """
    if labot['checking_dir'] is not None:
        dr, dc = DIRS[labot['checking_dir']]

        # Berechne Geometrie: Arm startet am Kreisrand, endet an der Zellkante
        center_x = labot['col'] * CELL_SIZE + CELL_SIZE // 2
        center_y = labot['row'] * CELL_SIZE + CELL_SIZE // 2
        robot_radius = CELL_SIZE // 4

        # Start: Rand des Roboter-Kreises in die geprüfte Richtung
        # (nicht vom Mittelpunkt, sondern vom äußeren Rand des Kreises)
        start_x = center_x + dc * robot_radius
        start_y = center_y + dr * robot_radius

        # End: Zellenrand in die geprüfte Richtung
        # (dc und dr sind bereits normalisiert: -1, 0 oder 1)
        end_x = center_x + dc * CELL_SIZE // 2
        end_y = center_y + dr * CELL_SIZE // 2

        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 3)


def draw_button(surface, x, y, text, is_hovered=False):
    """
    Zeichnet einen Button mit Text.
    
    Args:
        surface: PyGame Surface
        x (int): X-Koordinate
        y (int): Y-Koordinate
        text (str): Button-Text
        is_hovered (bool): Ob Maus über Button ist
    """
    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(surface, color, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(surface, BLACK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)

    # Text rendern
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(
        center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2)
    )
    surface.blit(text_surface, text_rect)


def draw_info_panel(screen, state='selecting', algorithm=None):
    """
    Zeichnet das Info-Panel im unteren Bildschirmbereich.
    
    Der Panel zeigt verschiedene Inhalte je nach aktuellem Zustand:
    - 'selecting': Algorithmus-Auswahl mit Buttons
    - 'running': Status während der Labyrinth-Navigation
    - 'completed': Erfolgsmeldung nach Erreichen des Ziels
    
    Args:
        screen: PyGame Surface
        state (str): Aktueller Zustand ('selecting', 'running', 'completed')
        algorithm (str): Gewählter Algorithmus ('left' oder 'right'), nur relevant wenn state != 'selecting'
        
    Returns:
        tuple: (left_hovered, right_hovered) nur bei state='selecting', sonst None
    """
    # Hintergrund-Rechteck für Info-Panel
    pygame.draw.rect(screen, LIGHT_GRAY, (0, INFO_Y_START, TOTAL_WIDTH, INFO_PANEL_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, INFO_Y_START), (TOTAL_WIDTH, INFO_Y_START), 2)
    
    if state == 'selecting':
        # Algorithmus-Auswahl
        font = pygame.font.Font(None, 28)
        title = font.render("Wähle einen Algorithmus:", True, BLACK)
        title_rect = title.get_rect(center=(TOTAL_WIDTH // 2, INFO_Y_START + 30))
        screen.blit(title, title_rect)
        
        # Buttons zeichnen
        mouse_pos = pygame.mouse.get_pos()
        left_hovered = is_button_clicked(mouse_pos, LEFT_BUTTON_X, BUTTON_Y)
        right_hovered = is_button_clicked(mouse_pos, RIGHT_BUTTON_X, BUTTON_Y)
        
        draw_button(screen, LEFT_BUTTON_X, BUTTON_Y, "Linke Hand", left_hovered)
        draw_button(screen, RIGHT_BUTTON_X, BUTTON_Y, "Rechte Hand", right_hovered)
        
        return left_hovered, right_hovered
    
    elif state == 'running':
        # Status während Navigation
        algo_name = "der linken Wand" if algorithm == 'left' else "der rechten Wand"
        status_text = f"Entlang {algo_name}..."
        
        font = pygame.font.Font(None, 24)
        status = font.render(status_text, True, BLACK)
        status_rect = status.get_rect(center=(TOTAL_WIDTH // 2, INFO_CENTER_Y))
        screen.blit(status, status_rect)
        
        return None
    
    elif state == 'completed':
        # End-Bildschirm
        font = pygame.font.Font(None, 32)
        success = font.render("Weg zum Ziel gefunden!", True, GREEN)
        success_rect = success.get_rect(center=(TOTAL_WIDTH // 2, INFO_CENTER_Y))
        screen.blit(success, success_rect)
        
        return None


def draw_algorithm_selection(screen):
    """
    Zeichnet den Algorithmus-Auswahl-Screen.
    
    Nutzt das Info-Panel für die Anzeige der Auswahl.
    
    Args:
        screen: PyGame Surface
        
    Returns:
        tuple: (left_hovered, right_hovered) Buttons
    """
    draw_maze(screen)
    result = draw_info_panel(screen, state='selecting')
    pygame.display.flip()
    return result


# ============================================================================
# LOGIK-FUNKTIONEN - UI und Algorithmus
# ============================================================================
def wait_for_algorithm_selection(screen, clock):
    """
    Wartet auf die Auswahl des Algorithmus durch den Nutzer.
    
    Args:
        screen: PyGame Surface
        clock: PyGame Clock
        
    Returns:
        str: 'left' oder 'right' oder None bei Abbruch
    """
    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                left_hovered, right_hovered = draw_algorithm_selection(screen)
                if left_hovered:
                    return 'left'
                if right_hovered:
                    return 'right'

        draw_algorithm_selection(screen)
        clock.tick(60)


def get_relative_check_order(algorithm):
    """
    Gibt die Reihenfolge der relativen Richtungen zurück.
    
    Die Offsets werden als Modulo-Operationen auf die aktuelle Roboter-Richtung
    angewendet, um immer die richtigen Richtungen relativ zu seiner Ausrichtung
    zu berechnen.
    
    Returns:
        list: Offset-Liste [-1, 0, 1, 2] als Vielfache von 90°
              -1 = Links, 0 = Vorwärts, 1 = Rechts, 2 = Rückwärts
    """
    if algorithm == 'left':
        return [-1, 0, 1, 2]  # Linke-Hand-Algorithmus: Links prüfen ZUERST
    else:  # 'right'
        return [1, 0, -1, 2]  # Rechte-Hand-Algorithmus: Rechts prüfen ZUERST


# ============================================================================
# HAUPTPROGRAMM
# ============================================================================
def main():
    """
    Hauptprogramm: Initialisiert PyGame und startet die Labyrinth-Simulation
    """
    # PyGame initialisieren
    pygame.init()
    pygame.mixer.init()

    # Sound-Dateien laden
    try:
        pygame.mixer.music.load("background_music.wav")
        pygame.mixer.music.play(-1)  # -1 = Endlosschleife
    except pygame.error as e:
        print(f"Warnung: Musik konnte nicht geladen werden: {e}")

    try:
        step_sound = pygame.mixer.Sound("step.wav")
    except pygame.error as e:
        print(f"Warnung: Step-Sound konnte nicht geladen werden: {e}")
        step_sound = None

    # Fenster vorbereiten
    screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Labyrinth Roboter - Hand-an-der-Wand-Algorithmus")
    clock = pygame.time.Clock()

    # Labyrinth zeichnen
    draw_maze(screen)
    pygame.display.flip()

    # Algorithmus-Auswahl
    algorithm = wait_for_algorithm_selection(screen, clock)
    if algorithm is None:
        pygame.quit()
        return

    algorithm_name = "Linke Hand" if algorithm == 'left' else "Rechte Hand"
    pygame.display.set_caption(f"Labyrinth Roboter - {algorithm_name}-Algorithmus")

    # Relative Check-Reihenfolge einmal festlegen (bleibt während ganzen Spiels gleich)
    relative_check_order = get_relative_check_order(algorithm)

    # Roboter initialisieren
    start_row, start_col = find_value('S')
    labot = {
        'row': start_row,
        'col': start_col,
        'dir': 0,  # Startet nach Osten
        'checking_dir': None  # initial keine Prüfrichtung
    }

    # Roboter initial zeichnen
    draw_maze(screen)
    draw_labot_body(screen, labot)
    draw_info_panel(screen, state='running', algorithm=algorithm)
    pygame.display.flip()

    # Hauptloop
    running = True
    while running:
        # Event-Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # === PRÜF-PHASE ===
        # Konvertiere relative Offsets in absolute Richtungen
        # Dies ist kritisch: relative_check_order bleibt gleich,
        # aber durch die Modulo-Operation passen sich die geprüften Richtungen
        # an die aktuelle Roboter-Ausrichtung an
        check_order = []
        for offset in relative_check_order:
            check_order.append((labot['dir'] + offset) % 4)

        next_move = None
        for check_dir in check_order:
            # Prüfe, ob diese Richtung frei ist
            dr, dc = DIRS[check_dir]
            new_row, new_col = labot['row'] + dr, labot['col'] + dc

            labot['checking_dir'] = check_dir

            if is_cell_free(new_row, new_col):
                # Weg frei: Grüner Arm, direkt übernehmen
                draw_maze(screen)
                draw_labot_body(screen, labot)
                draw_labot_arm(screen, labot, GREEN)
                draw_info_panel(screen, state='running', algorithm=algorithm)
                next_move = (new_row, new_col, check_dir)
            else:
                # Weg blockiert: Roter Arm, weiter suchen
                draw_maze(screen)
                draw_labot_body(screen, labot)
                draw_labot_arm(screen, labot, RED)
                draw_info_panel(screen, state='running', algorithm=algorithm)

            pygame.display.flip()
            clock.tick(2)  # 0.5 Sekunden pro Prüfung

            if next_move:
                break  # Gefunden, weiter zur Bewegungsphase

        # === BEWEGUNGS-PHASE ===
        if next_move:
            labot['row'], labot['col'], labot['dir'] = next_move
            labot['checking_dir'] = None

            # Sound abspielen
            if step_sound:
                try:
                    step_sound.play()
                except pygame.error:
                    pass  # Fehler ignorieren

            # Neue Position zeichnen
            draw_maze(screen)
            draw_labot_body(screen, labot)
            draw_info_panel(screen, state='running', algorithm=algorithm)
            pygame.display.flip()
            clock.tick(1)  # 1 Sekunde für Bewegung

            # Prüfe, ob Ziel erreicht
            if MAZE[labot['row']][labot['col']] == 'Z':
                print(f"Ziel erreicht mit {algorithm_name}-Algorithmus!")
                # End-Screen zeichnen
                draw_maze(screen)
                draw_labot_body(screen, labot)
                draw_info_panel(screen, state='completed')
                pygame.display.flip()
                pygame.time.wait(3000)  # 3 Sekunden warten
                running = False

    # PyGame beenden
    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
