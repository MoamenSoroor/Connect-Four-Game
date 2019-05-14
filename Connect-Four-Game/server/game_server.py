from server.components import *
from server.server_conn import *
import threading as thr

olive_color = (128, 128, 0)
black_color = (0, 0, 0)
wight_color = (255, 255, 255)
green_color = (0, 255, 0)
red_color = (255, 0, 0)

STATE_NONE = "NONE"
STATE_PLAYER = "PLAYER"
STATE_ENEMY = "ENEMY"

class Game:

    def __init__(self, game_name="Connect-Four-Server"):

        self.server = ServerComm(("127.0.0.1" , 5555))

        self.game_name = game_name
        self.window = None
        self.box_width, self.box_height = 64, 64
        self.column_count, self.row_count = 7, 7
        self.win_width = self.column_count * self.box_width
        self.win_height =(self.row_count + 1) * self.box_height
        self.win_dim = self.win_width, self.win_height
        self.game_map = None
        self.player_color = green_color
        self.enemy_color = red_color

        # flag determines the end of the game
        self.play = False

        # flag determines pausing ticks and rendering the screen
        self.pause = False

        # flag determines turn of the player
        self.turn = True

    def start(self):

        pygame.init()
        self.window = pygame.display.set_mode(self.win_dim)
        pygame.display.set_caption(self.game_name)
        clock = pygame.time.Clock()


        self.game_map = Map(self)
        self.game_map.load()

        self.pause = True
        self.server.start()
        self.recv_thr = thr.Thread(target=self.recv_thread)
        self.recv_thr.start()

        self.play = True
        self.pause = False

        # Game loop
        while self.play:
            clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.play = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]and self.pause:
                print("------------- reset game -------------")
                self.reset()

            self.control(events)
            if not self.pause:
                self.tick()
                self.render(self.window)

        self.server.close()
        pygame.quit()

    def control(self,events):
        self.game_map.control(events)

    def tick(self):
        self.game_map.tick()

    def render(self, window):
        window.fill((0, 0, 0))
        self.game_map.render(window)
        pygame.display.update()

    def reset(self):
        self.pause = False
        self.game_map.reset()
        self.send_reset()

    def recv_thread(self):
        while not self.server.closed:
            if not self.play or self.pause or not self.server.play:
                continue
            print("waiting for data...")
            data = self.server.recv()
            if data is not None:
                print("recv:", data)
                pos = str(data).split(" ")
                print("recv pos_ij:", pos)
                self.game_map.set_box_enemy(int(pos[0]), int(pos[1]))
                self.turn = True

        print("server recv out ---------------")

    def send(self, i, j):
        if self.server.is_play():
            data = str(i) + " " + str(j)
            self.server.send(data)
            print("data sent")

    def send_reset(self):
        if self.server.is_play():
            self.server.send("r")
            print("reset data sent")
            print(":::::::::::server reset game")



def main():
    my_game = Game()
    my_game.start()


if __name__ == "__main__":
    main()