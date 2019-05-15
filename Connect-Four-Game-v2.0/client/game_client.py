from server.components import *
from client.client_conn import *
import threading as thr

olive_color = (128, 128, 0)
black_color = (0, 0, 0)
wight_color = (255, 255, 255)
green_color = (0, 255, 0)
red_color = (255, 0, 0)

class Game:

    def __init__(self, game_name="Connect-Four-Client"):

        print("start client...")

        self.client = ClientComm(("127.0.0.1" , 5555))
        self.recv_thr = None

        self.game_name = game_name
        self.window = None
        self.connect_level = 4
        self.box_width, self.box_height = 64, 64
        self.column_count, self.row_count = 7, 7
        self.win_width = self.column_count * self.box_width
        self.win_height =(self.row_count + 1) * self.box_height
        self.win_dim = self.win_width, self.win_height
        self.game_map = None
        self.player_color = red_color
        self.enemy_color = green_color

        # flag determines the end of the game
        self.play = False

        # flag determines pausing ticks and rendering the screen
        self.pause = False

        # flag determines turn of the player
        self.turn = False
        print("init client...")

    def start(self):

        pygame.init()
        print("init pygame...")
        self.window = pygame.display.set_mode(self.win_dim)
        pygame.display.set_caption(self.game_name)
        clock = pygame.time.Clock()


        self.game_map = Map(self)
        self.game_map.load()

        self.client.start()
        self.recv_thr = thr.Thread(target=self.recv_thread)
        self.recv_thr.start()

        self.play = True
        self.pause = False
        # Game loop
        print("go to game loop...")
        while self.play:
            clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.play = False

            self.control(events)
            if not self.pause:
                self.tick()
                self.render(self.window)

        self.client.close()
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

    def recv_thread(self):
        while not self.client.closed:
            if self.play and not self.pause and self.client.play:
                print("waiting for data...")
                data = self.client.recv()
                if data is not None or data == "":
                    print("recv:", data)
                    if data == "r":
                        self.reset()
                    else:
                        self.game_map.add_enemy_box_at_column(int(data))
                        self.turn = True
                else:
                    self.close_game()

        print("recv out ---------------")

    def send(self, column_index):
        if self.client.is_play():
            self.client.send(str(column_index))
            print("data sent")

    def close_game(self):
        self.play = False


def main():
    my_game = Game()
    my_game.start()


if __name__ == "__main__":
    main()