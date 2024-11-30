import sys
import pygame
import string
import queue as Queue


class Game:

    def is_valid_value(self, char):
        if (char == ' ' or  # floor
                char == '#' or  # wall
                char == '@' or  # worker on floor
                char == '.' or  # dock
                char == '*' or  # box on dock
                char == '$' or  # box
                char == '+'):  # worker on dock
            return True
        else:
            return False

    levels = [
        [
            ['#', '#', '#', '#', '#'],
            ['#', '@', ' ', ' ', '#'],
            ['#', ' ', '$', '.', '#'],
            ['#', ' ', '$', '.', '#'],
            ['#', ' ', '$', '.', '#'],
            ['#', ' ', '$', '.', '#'],
            ['#', ' ', '$', '.', '#'],
            ['#', ' ', '$', '.', '#'],
            ['#', ' ', '$', '.', '#'],
            ['#', ' ', '$', '.', '#'],
            ['#', '#', '#', '#', '#'],
        ],
        [
            [' ', ' ', '#', '#', '#', ' ', ' ', ' '],
            [' ', ' ', '#', '.', '#', ' ', ' ', ' ', ],
            [' ', ' ', '#', ' ', '#', '#', '#', '#'],
            ['#', '#', '#', '$', ' ', '$', '.', '#'],
            ['#', '.', ' ', '$', '@', '#', '#', '#'],
            ['#', '#', '#', '#', '$', '#', ' ', ' '],
            [' ', ' ', ' ', '#', '.', '#', ' ', ' '],
            [' ', ' ', ' ', '#', '#', '#', ' ', ' '],
        ],
        [
            ['#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', '#'],
            ['#', '@', '$', '$', '#', ' ', '#', '#', '#'],
            ['#', ' ', '$', ' ', '#', ' ', '#', '.', '#'],
            ['#', '#', '#', ' ', '#', '#', '#', '.', '#'],
            [' ', '#', '#', ' ', ' ', ' ', ' ', '.', '#'],
            [' ', '#', ' ', ' ', ' ', '#', ' ', ' ', '#'],
            [' ', '#', ' ', ' ', ' ', '#', '#', '#', '#'],
            [' ', '#', '#', '#', '#', '#'],
        ],
        [
            [' ', '#', '#', '#', '#', '#', '#', '#'],
            [' ', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#'],
            ['#', '#', '$', '#', '#', '#', ' ', ' ', ' ', '#'],
            ['#', ' ', '@', ' ', '$', ' ', ' ', '$', ' ', '#'],
            ['#', ' ', '.', '.', '#', ' ', '$', ' ', '#', '#'],
            ['#', '#', '.', '.', '#', ' ', ' ', ' ', '#'],
            [' ', '#', '#', '#', '#', '#', '#', '#', '#'],
        ],

        [
            ['#', '#', '#', '#', '#', '#', '#', '#'],
            [' ', '#', ' ', ' ', '#', ' ', ' ', '#', '#', '#'],
            ['#', ' ', '$', ' ', '#', '#', ' ', ' ', ' ', '#'],
            ['#', ' ', '@', ' ', ' ', ' ', '$', ' ', '#', '#'],
            ['#', '#', ' ', '$', '#', '#', ' ', '.', '#', '#'],
            [' ', '#', ' ', ' ', ' ', ' ', '.', '.', '#', '#'],
            [' ', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ],
        [
            ['#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
            ['#', '@', '$', '$', '#', ' ', '#', '#', '#', '#'],
            ['#', ' ', '$', ' ', '#', ' ', '#', '.', '#', '#'],
            ['#', '#', '#', ' ', '#', '#', '#', '.', '#', '#'],
            [' ', '#', '#', ' ', ' ', ' ', ' ', '.', '#', '#'],
            [' ', '#', ' ', ' ', ' ', '#', ' ', ' ', '#', '#'],
            [' ', '#', ' ', ' ', ' ', '#', '#', '#', '#', '#'],
            [' ', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ],
        [
            ['#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#'],
            ['#', ' ', '$', ' ', '.', '*', '.', ' ', '$', ' ', '#'],
            ['#', '@', '$', '.', '*', ' ', '*', '.', '$', ' ', '#'],
            ['#', ' ', '$', ' ', '.', '*', '.', ' ', '$', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', '#'],
            [' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
        ],
        [
            ['#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', '$', ' ', ' ', '#', '#', '#', '#'],
            ['#', ' ', '$', '*', '.', '.', '*', ' ', '#'],
            ['#', ' ', '*', '.', '.', '*', '$', ' ', '#'],
            ['#', '#', '#', '#', ' ', ' ', '$', ' ', '#'],
            [' ', ' ', ' ', '#', ' ', '@', ' ', ' ', '#'],
            [' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
        ],
        [
            [' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '.', ' ', ' ', '@', '#'],
            ['#', ' ', ' ', '$', '$', '$', ' ', ' ', '#'],
            ['#', '.', '#', '#', '.', '#', '#', '.', '#'],
            ['#', ' ', ' ', ' ', '$', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', '$', '.', '#', ' ', '#', '#'],
            ['#', '#', '#', '#', ' ', ' ', ' ', '#'],
            [' ', ' ', ' ', '#', '#', '#', '#', '#'],
        ],
        [
            ['#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', '.', ' ', ' ', '$', '.', ' ', '@', '#'],
            ['#', ' ', '.', '$', '.', '$', ' ', ' ', '#'],
            ['#', '#', '$', '.', '$', ' ', '$', '#', '#'],
            ['#', ' ', '.', '$', '.', '$', ' ', ' ', '#'],
            ['#', '.', ' ', ' ', '$', '.', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ],
        [
            [ '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            [ '#', '@', '#', '.', '#', '#', '#', '#', '#', '#'],
            [ '#', ' ', '#', '$', '$', '.', '#', '#', '#', '#'],
            [ '#', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'],
            [ '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            [ '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            [ '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            [ '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],

        ],

    ]

    def __init__(self, level):
        self.queue = Queue.LifoQueue()
        self.matrix = []
        self.current_level = level
        self.move_count = 0

        # Check if the provided level index is within the range
        if 1 <= level <= len(self.levels):
            # Copy the level matrix to the game instance
            self.matrix = [list(row) for row in self.levels[level - 1]]
        else:
            print(f"ERROR: Level {level} is out of range")
            sys.exit(1)

    def increment_move_count(self):
        self.move_count += 1

    def display_move_count(screen, move_count):
        fontobject = pygame.font.Font(None, 25)
        move_count_text = fontobject.render(f"Moves: {move_count}", True, (255, 255, 255))
        screen.blit(move_count_text, (10, 10))

    def next_level(self):
        self.current_level += 1
        if self.current_level <= len(self.levels):
            self.matrix = [list(row) for row in self.levels[self.current_level - 1]]
        else:
            print(f"INFO: Tous les niveaux ont été complétés.")
            sys.exit(0)

    def load_size(self):
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return (x * 160, y * 70)

    def get_matrix(self):
        return self.matrix

    def print_matrix(self):
        for row in self.matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_content(self, x, y):
        return self.matrix[y][x]

    def set_content(self, x, y, content):
        if self.is_valid_value(content):
            self.matrix[y][x] = content
        else:
            print("ERROR: Value '" + content + "' to be added is not valid")

    def worker(self):
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == '@' or pos == '+':
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def can_move(self, x, y):
        return self.get_content(self.worker()[0] + x, self.worker()[1] + y) not in ['#', '*', '$']

    def next(self, x, y):
        return self.get_content(self.worker()[0] + x, self.worker()[1] + y)

    def can_push(self, x, y):
        return (self.next(x, y) in ['*', '$'] and self.next(x + x, y + y) in [' ', '.'])

    def is_completed(self):
        for row in self.matrix:
            for cell in row:
                if cell == '$':
                    return False
        return True

    def move_box(self, x, y, a, b):
        #        (x,y) -> move to do
        #        (a,b) -> box to move
        current_box = self.get_content(x, y)
        future_box = self.get_content(x + a, y + b)
        if current_box == '$' and future_box == ' ':
            self.set_content(x + a, y + b, '$')
            self.set_content(x, y, ' ')
        elif current_box == '$' and future_box == '.':
            self.set_content(x + a, y + b, '*')
            self.set_content(x, y, ' ')
        elif current_box == '*' and future_box == ' ':
            self.set_content(x + a, y + b, '$')
            self.set_content(x, y, '.')
        elif current_box == '*' and future_box == '.':
            self.set_content(x + a, y + b, '*')
            self.set_content(x, y, '.')



    def move(self, x, y, save):
        if self.can_move(x, y):
            current = self.worker()
            future = self.next(x, y)
            if current[2] == '@' and future == ' ':
                self.set_content(current[0] + x, current[1] + y, '@')
                self.set_content(current[0], current[1], ' ')
                if save: self.queue.put((x, y, False))
            elif current[2] == '@' and future == '.':
                self.set_content(current[0] + x, current[1] + y, '+')
                self.set_content(current[0], current[1], ' ')
                if save: self.queue.put((x, y, False))
            elif current[2] == '+' and future == ' ':
                self.set_content(current[0] + x, current[1] + y, '@')
                self.set_content(current[0], current[1], '.')
                if save: self.queue.put((x, y, False))
            elif current[2] == '+' and future == '.':
                self.set_content(current[0] + x, current[1] + y, '+')
                self.set_content(current[0], current[1], '.')
                if save: self.queue.put((x, y, False))
            self.increment_move_count()
        elif self.can_push(x, y):
            current = self.worker()
            future = self.next(x, y)
            future_box = self.next(x + x, y + y)
            if current[2] == '@' and future == '$' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save: self.queue.put((x, y, True))
            elif current[2] == '@' and future == '$' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save: self.queue.put((x, y, True))
            elif current[2] == '@' and future == '*' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))
            elif current[2] == '@' and future == '*' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))
            if current[2] == '+' and future == '$' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save: self.queue.put((x, y, True))
            elif current[2] == '+' and future == '$' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))
            elif current[2] == '+' and future == '*' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))
            elif current[2] == '+' and future == '*' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.put((x, y, True))
            self.increment_move_count()


def print_game(matrix, screen):
    screen.fill(background)
    x = 0
    y = 0
    for row in matrix:
        for char in row:

            if char == '#':  # wall
                screen.blit(wall, (x, y))
            elif char == '@':  # worker on floor
                screen.blit(worker, (x, y))
            elif char == '.':  # dock
                screen.blit(docker, (x, y))
            elif char == '*':  # box on dock
                screen.blit(box_docked, (x, y))
            elif char == '$':  # box
                screen.blit(box, (x, y))
            elif char == '+':  # worker on dock
                screen.blit(worker_docked, (x, y))
            x = x + 70
        x = 0
        y = y + 70


def display_end(screen):
    message = "Level Completed! Press 's' to go to the next level"
    fontobject = pygame.font.Font(None, 18)

    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 150,
                      (screen.get_height() / 2) - 10,
                      300, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255),
                     ((screen.get_width() / 2) - 152,
                      (screen.get_height() / 2) - 12,
                      304, 24), 1)
    screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                ((screen.get_width() / 2) - 150, (screen.get_height() / 2) - 10))
    pygame.display.flip()






def Display_Menu(screen):
    screen.fill((0, 0, 0))  # Couleur de fond

    font = pygame.font.Font(None, 25)
    game_name_text = font.render("SOKOBAN YEAH", True, (255, 250, 250))
    creators_text = font.render("Hemri Samy", True, (250, 250, 250))

    screen.blit(game_name_text, ((screen.get_width() / 2) - 80, (screen.get_height() / 2) - 150))
    screen.blit(creators_text, ((screen.get_width() / 2) - 50, (screen.get_height() / 2) + 150))

    start_text = font.render("POUR COMMENCER, APPUYEZ SUR J", True, (250, 250, 250))
    screen.blit(start_text, ((screen.get_width() / 2) - 160, (screen.get_height() / 2) + 50))
    SCORE_TEXT = font.render("POUR CONSULTER LE MEILLEUR SCORE APPUYEZ SUR X", True, (250, 250, 250))
    screen.blit(SCORE_TEXT, ((screen.get_width() / 2) - 235, (screen.get_height() / 2) + 20))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    return 1


wall = pygame.image.load('woodwall.png')
floor = 250, 235, 210
box = pygame.image.load('boite3.png')
box_docked = pygame.image.load('boiteok3.png')
worker = pygame.image.load('toad3.png')
worker_docked = pygame.image.load('toad3.png')
docker = pygame.image.load('pasteque.png')
background = 250, 235, 210

pygame.init()

wall = pygame.transform.scale(wall, (75, 75))
box = pygame.transform.scale(box, (75, 75))
box_docked = pygame.transform.scale(box_docked, (75, 75))
worker = pygame.transform.scale(worker, (75, 75))
worker_docked = pygame.transform.scale(worker_docked, (75, 75))
docker = pygame.transform.scale(docker, (75, 75))

fontobject = pygame.font.Font(None, 100)

screen = pygame.display.set_mode((500, 500))
level = Display_Menu(screen)
game_instance = Game(level)
size = game_instance.load_size()
screen = pygame.display.set_mode(size)

while True:
    if game_instance.is_completed():
        display_end(screen)  # Affiche le message de fin

        # Bloque l'exécution jusqu'à ce que l'utilisateur appuie sur 's'
        waiting_for_next = True
        while waiting_for_next:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        level += 1  # Passe au niveau suivant
                        game_instance = Game(level)
                        waiting_for_next = False  # Quitte la boucle d'attente

    print_game(game_instance.get_matrix(), screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game_instance.move(0, -1, True)
            elif event.key == pygame.K_DOWN:
                game_instance.move(0, 1, True)
            elif event.key == pygame.K_LEFT:
                game_instance.move(-1, 0, True)
            elif event.key == pygame.K_RIGHT:
                game_instance.move(1, 0, True)
            elif event.key == pygame.K_q:
                sys.exit(0)
            elif event.key == pygame.K_s:
                level += 1
                game_instance = Game(level)
            elif event.key == pygame.K_r:
                game_instance = Game(level)
            elif event.key == pygame.K_j:
                # Commencer au niveau 1
                level = 1
                game_instance = Game(level)
            elif event.key == pygame.K_j:
                game_instance.display_move_count()

    pygame.display.update()
