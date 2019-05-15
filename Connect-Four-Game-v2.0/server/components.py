import pygame

olive_color = (128, 128, 0)
black_color = (0, 0, 0)
shadow_color = (242, 244, 244)
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
        # background rectangle
        pygame.draw.rect(window, olive_color, self.rect)
        # circle to play in it
        pygame.draw.circle(window, self.circle_color, self.center, self.radius)

    def is_in_box(self, x, y):
        if self.x < x < self.x + self.box_width and self.y < y < self.y + self.box_height:
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
        self.connect_level = game.connect_level
        self.box_width, self.box_height = game.box_width, game.box_height
        self.column_count, self.row_count = game.column_count, game.row_count
        self.map_width = self.column_count * self.box_width
        self.map_height = self.row_count * self.box_height

        self.boxes_map = []
        self.player_win = False
        self.enemy_win = False

        self.win_boxes = None

        self.is_clicked = False

        self.map_columns_level = [self.row_count - 1] * self.column_count
        print("map_column_level: ", self.map_columns_level)
        self.mouse_pos = self.pos_x, self.pos_y = 0.0, 0.0
        self.marked_column_index = 0


        font = pygame.font.SysFont("comicsansms", 20)

        self.text_win = font.render("You win :)", True, (0, 150, 0))
        self.text_loss = font.render("You loss :(", True, (255, 0, 0))

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
                    print("mouse clicked at x,y = ", self.pos_x, self.pos_y)
                    self.game.turn = False

    def tick(self):
        if self.is_clicked and self.is_click_on_map(self.pos_x, self.pos_y):
            self.marked_column_index = self.pos_x // self.box_width
            print("marked column index: ", self.marked_column_index)
            self.add_player_box_at_column(self.marked_column_index)
            self.game.send(self.marked_column_index)
            self.is_clicked = False
            self.check_win()

    def render(self, window):
        for row in self.boxes_map:
            for box in row:
                box.render(window)

        if self.player_win:
            window.blit(self.text_win, (self.txt_x, self.txt_y))
            self.game.turn = True
            self.game.pause = True
            (x1, y1) = self.win_boxes[0].center_x , self.win_boxes[0].center_y
            (x2, y2) = self.win_boxes[-1].center_x, self.win_boxes[-1].center_y
            pygame.draw.aaline(window,black_color,(x1,y1),(x2, y2), 5)

        elif self.enemy_win:
            window.blit(self.text_loss, (self.txt_x, self.txt_y))
            self.game.turn = False
            self.game.pause = True
            (x1, y1) = self.win_boxes[0].center_x, self.win_boxes[0].center_y
            (x2, y2) = self.win_boxes[-1].center_x, self.win_boxes[-1].center_y
            pygame.draw.aaline(window, black_color, (x1, y1), (x2, y2), 5)

    def reset(self):
        print("reset game...")
        for row in self.boxes_map:
            for box in row:
                box.set_none()

        self.map_columns_level = [self.row_count - 1] * self.column_count

        self.player_win = False
        self.enemy_win = False

    def add_player_box_at_column(self, col_index):
        i = col_index
        j = self.map_columns_level[col_index]
        if  0 <= j < self.row_count:
            self.boxes_map[i][j].set_player()
            self.map_columns_level[col_index] -= 1

    def add_enemy_box_at_column(self, col_index):
        i = col_index
        j = self.map_columns_level[col_index]
        if 0 <= j < self.row_count:
            self.boxes_map[i][j].set_enemy()
            self.map_columns_level[col_index] -= 1
        self.check_win()

    def is_click_on_map(self, x,y):
        if 0 < x < self.map_width and 0 < y < self.map_height:
            return True
        else:
            return False

    def check_win_boxes(self, row):
        player_sum = 0
        enemy_sum = 0

        for box in row:
            if box.is_player():
                player_sum += 1
                enemy_sum = 0
            elif box.is_enemy():
                player_sum = 0
                enemy_sum += 1
            else:
                if player_sum < self.connect_level:
                    player_sum = 0
                if enemy_sum < self.connect_level:
                    enemy_sum = 0

        if player_sum >= self.connect_level:
            self.player_win = True
            self.enemy_win = False
            self.win_boxes = row
            return True

        elif enemy_sum >= self.connect_level:
            self.player_win = False
            self.enemy_win = True
            self.win_boxes = row
            return True
        else:
            return False

    def check_columns(self):
        # check columns
        print("check columns...")
        for i in range(self.column_count):
            row_box = []
            print("check new columns")
            for j in range(self.row_count):
                row_box.append(self.boxes_map[i][j])
                print("i,j = ", i, j)

            if self.check_win_boxes(row_box):
                return True

    def check_rows(self):
        # check columns
        print("check rows...")
        for i in range(self.column_count):
            row_box = []
            print("check new row")
            for j in range(self.row_count):
                row_box.append(self.boxes_map[j][i])
                print("i,j = ", i, j)

            if self.check_win_boxes(row_box):
                return True

    def check_diagonal(self):
        # check diag 1
        print("check diags 1")
        d = self.row_count
        for k in range(0, d):
            row_box = []
            print("check new diag")
            for i, j in zip(range(0, k + 1), range(k, -1, -1)):
                row_box.append(self.boxes_map[i][j])
                print("i,j = ",i, j)

            if self.check_win_boxes(row_box):
                return True

        # check diag 2
        print("check diag 2")
        for k in range(0, d):
            row_box = []
            print("check new diag")
            for i, j in zip(range(d - k - 1, d), range(d - 1 , d - k - 2 , -1 )):
                row_box.append(self.boxes_map[i][j])
                print("i,j = ", i, j)

            if self.check_win_boxes(row_box):
                return True

        # check diag 3
        print("check diag 3")
        d = self.row_count
        for k in range(0, d):
            row_box = []
            print("check new diag")
            for i, j in zip(range(d - k - 1, d + 1), range(0, k + 1)):
                row_box.append(self.boxes_map[i][j])
                print("i,j = ", i, j)

            if self.check_win_boxes(row_box):
                return True

        # check diag 4
        print("check diag 4")
        d = self.row_count
        for k in range(0, d):
            row_box = []
            print("check new diag")
            for i, j in zip(range(0, k + 1), range(d - k - 1, d + 1)):
                row_box.append(self.boxes_map[i][j])
                print("i,j = ", i, j)

            if self.check_win_boxes(row_box):
                return True

        return False

    def check_win(self):
        if self.check_columns() or self.check_rows() or self.check_diagonal():
            print("Win Boxes: ", self.win_boxes)
            print("player:", self.player_win)
            print("enemy:", self.enemy_win)
            return True
        else:
            return False
