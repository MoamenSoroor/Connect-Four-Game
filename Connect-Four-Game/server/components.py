import pygame

olive_color = (128, 128, 0)
black_color = (0, 0, 0)
wight_color = (255, 255, 255)
green_color = (0, 255, 0)
red_color = (255, 0, 0)

STATE_NONE = "NONE"
STATE_PLAYER = "PLAYER"
STATE_ENEMY = "ENEMY"


class Box:

    def __init__(self, game, x, y, i, j):
        self.game = game
        self.x, self.y = x, y
        self.i, self.j = i, j
        self.box_width, self.box_height = game.box_width, game.box_height
        self.rect = self.x, self.y, self.box_width, self.box_width
        self.center_x = self.x + self.box_width // 2
        self.center_y = self.y + self.box_width // 2
        self.center = self.center_x, self.center_y
        self.radius = self.box_width // 2 - 5

        self.circle_color = wight_color
        self.box_state = STATE_NONE

        self.player_color = game.player_color
        self.enemy_color = game.enemy_color

    def control(self, events):
        pass

    def tick(self):
        pass

    def render(self, window):
        pygame.draw.rect(window, olive_color, self.rect)
        pygame.draw.circle(window, self.circle_color, self.center, self.radius)

    def is_in_box(self, x, y):
        if x > self.x and x < self.x + self.box_width \
                and y > self.y and y < self.y + self.box_height:
            return True
        else:
            return False

    def location(self):
        return self.x, self.y

    def set_player(self):
        self.circle_color = self.player_color
        self.box_state = STATE_PLAYER
        print("box is player:", self.x, self.y, self.i, self.j)

    def set_enemy(self):
        self.circle_color = self.enemy_color
        self.box_state = STATE_ENEMY
        print("box is enemy:", self.x, self.y, self.i, self.j)

    def set_none(self):
        self.circle_color = wight_color
        self.box_state = STATE_NONE
        print("box is none:", self.x, self.y, self.i, self.j)

    def is_player(self):
        return self.box_state == STATE_PLAYER

    def is_enemy(self):
        return self.box_state == STATE_ENEMY

    def is_none(self):
        return self.box_state == STATE_NONE


class Map:
    def __init__(self, game):
        self.game = game
        self.box_width, self.box_height = game.box_width, game.box_height
        self.column_count, self.row_count = game.column_count, game.row_count
        self.map_width = self.column_count * self.box_width
        self.map_height = self.row_count * self.box_height

        self.boxes_map = []
        self.player_win = False
        self.enemy_win = False

        self.win_boxes = None

        self.is_clicked = False
        self.mouse_pos = self.pos_x, self.pos_y = 0, 0

        font = pygame.font.SysFont("comicsansms", 20)

        self.text_win = text = font.render("You win :)", True, (0, 150, 0))
        self.text_loss = text = font.render("You loss :(", True, (255, 0, 0))

        self.txt_x = self.map_width // 2 - 20
        self.txt_y = self.map_height + 20

    def load(self):
        for i in range(self.column_count):
            row = []
            for j in range(self.row_count):
                x, y = i * self.box_width, j * self.box_height
                print("locs:", x, y, i, j)
                row.append(Box(self.game, x, y, i, j))
            self.boxes_map.append(row)
            print(self.boxes_map)

    def control(self, events):
        if self.game.turn:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.pos_x, self.pos_y = pygame.mouse.get_pos()
                    self.is_clicked = True
                    print("mouse pressed: ", self.pos_x, self.pos_y)
                    self.game.turn = False

    def tick(self):
        if self.check_win():
            self.game.pause = True

    def render(self, window):
        for row in self.boxes_map:
            for box in row:
                if self.is_clicked and box.is_in_box(self.pos_x, self.pos_y):
                    box.set_player()
                    self.game.send(box.i, box.j)
                    self.is_clicked = False
                    self.game.turn = False

                box.render(window)

        if self.player_win:
            window.blit(self.text_win, (self.txt_x, self.txt_y))
            self.game.turn = True
            self.game.pause = True

        elif self.enemy_win:
            window.blit(self.text_loss, (self.txt_x, self.txt_y))
            self.game.turn = False
            self.game.pause = True

    def reset(self):
        for row in self.boxes_map:
            for box in row:
                box.set_none()
        self.player_win = False
        self.enemy_win = False

    def get_box(self, pos_x, pos_y):
        box_i = self.pos_x // self.box_width + 1
        box_j = self.pos_y // self.box_height + 1
        return self.boxes_map[box_i][box_j]

    def set_box_none(self, i, j):
        self.boxes_map[i][j].set_none()

    def set_box_player(self, i, j):
        self.boxes_map[i][j].set_player()

    def set_box_enemy(self, i, j):
        self.boxes_map[i][j].set_enemy()

    def is_player(self, i, j):
        return self.boxes_map[i][j].is_player(self)

    def is_enemy(self, i, j):
        return self.boxes_map[i][j].is_enemy(self)

    def is_none(self, i, j):
        return self.boxes_map[i][j].is_none(self)

    def check_win_boxes(self, row):
        player_sum = 0
        enemy_sum = 0

        for box in row:
            if box.is_player():
                player_sum += 1
            elif box.is_enemy():
                enemy_sum += 1

        if player_sum >= 4:
            self.player_win = True
            self.win_boxes = row
            return True

        elif enemy_sum >= 4:
            self.enemy_win = True
            self.win_boxes = row
            return True
        else:
            return False

    def check_columns(self):
        # check columns
        for i in range(self.column_count):
            row_box = []
            for j in range(self.row_count):
                row_box.append(self.boxes_map[i][j])

            if self.check_win_boxes(row_box):
                return True

    def check_rows(self):
        # check columns
        for i in range(self.column_count):
            row_box = []
            for j in range(self.row_count):
                row_box.append(self.boxes_map[j][i])

            if self.check_win_boxes(row_box):
                return True

    def check_diagonal(self):
        player_win = False
        enemy_win = False
        player_sum = 0
        enemy_sum = 0

        # check rows
        d = self.row_count
        for k in range(0, d):
            row_box = []
            for i, j in zip(range(0, k + 1), range(k, -1, -1)):
                row_box.append(self.boxes_map[i][j])

            if self.check_win_boxes(row_box):
                return True

        # check rows
        for k in range(0, d):
            row_box = []
            for i, j in zip(range(k, -1, -1), range(0, k + 1)):
                row_box.append(self.boxes_map[i][j])

            if self.check_win_boxes(row_box):
                return True

        # check rows
        d = self.row_count
        for k in range(0, d):
            row_box = []
            for i, j in zip(range(d - k - 1, d + 1), range(0, k + 1)):
                row_box.append(self.boxes_map[i][j])

            if self.check_win_boxes(row_box):
                return True

        # check rows
        d = self.row_count
        for k in range(0, d):
            row_box = []
            for i, j in zip(range(0, k + 1), range(d - k - 1, d + 1)):
                row_box.append(self.boxes_map[i][j])

            if self.check_win_boxes(row_box):
                return True
        return False

    def check_win(self):
        if self.check_columns() or self.check_columns() or self.check_diagonal():
            print("Win Boxes: ", self.win_boxes)
            print("player:", self.player_win)
            print("enemy:", self.enemy_win)
            return True
        else:
            return False
