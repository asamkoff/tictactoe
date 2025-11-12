# main.py
# Kivy Tic Tac Toe with player name & avatar selection screen

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
import os

# --------- Setup Screen ---------
class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        title = Label(text="Tic Tac Toe Setup", font_size='28sp', size_hint=(1, 0.1))
        layout.add_widget(title)

        # Player 1 section
        p1_box = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        p1_box.add_widget(Label(text="Player 1 Name:", font_size='18sp', size_hint=(1, 0.2)))
        self.p1_name = TextInput(text="", multiline=False, size_hint=(1, 0.2))
        p1_box.add_widget(self.p1_name)
        p1_box.add_widget(Label(text="Choose Avatar:", font_size='16sp', size_hint=(1, 0.2)))

        p1_avatars = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        self.p1_choice = None
        self.avatar_images = []
        img_dir = os.path.join(os.getcwd(), "images")
        for img in os.listdir(img_dir):
            if img.lower().endswith((".png", ".jpg", ".jpeg")):
                avatar = Button(background_normal=os.path.join(img_dir, img),
                                background_down=os.path.join(img_dir, img))
                avatar.bind(on_release=lambda inst, path=img: self.set_avatar(1, path))
                self.avatar_images.append(avatar)
                p1_avatars.add_widget(avatar)
        p1_box.add_widget(p1_avatars)
        layout.add_widget(p1_box)

        # Player 2 section
        p2_box = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        p2_box.add_widget(Label(text="Player 2 Name:", font_size='18sp', size_hint=(1, 0.2)))
        self.p2_name = TextInput(text="", multiline=False, size_hint=(1, 0.2))
        p2_box.add_widget(self.p2_name)
        p2_box.add_widget(Label(text="Choose Avatar:", font_size='16sp', size_hint=(1, 0.2)))

        p2_avatars = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        self.p2_choice = None
        for img in os.listdir(img_dir):
            if img.lower().endswith((".png", ".jpg", ".jpeg")):
                avatar = Button(background_normal=os.path.join(img_dir, img),
                                background_down=os.path.join(img_dir, img))
                avatar.bind(on_release=lambda inst, path=img: self.set_avatar(2, path))
                p2_avatars.add_widget(avatar)
        p2_box.add_widget(p2_avatars)
        layout.add_widget(p2_box)

        start_btn = Button(text="Start Game", font_size='20sp', size_hint=(1, 0.15))
        start_btn.bind(on_release=self.start_game)
        layout.add_widget(start_btn)

        self.add_widget(layout)

    def set_avatar(self, player, img_path):
        if player == 1:
            self.p1_choice = img_path
        else:
            self.p2_choice = img_path

    def start_game(self, instance):
        p1 = self.p1_name.text.strip() or "Player 1"
        p2 = self.p2_name.text.strip() or "Player 2"

        if not self.p1_choice or not self.p2_choice:
            # Must select avatars
            self.manager.current_screen.ids.get('status', None)
            return

        game_screen = self.manager.get_screen('game')
        game_screen.set_players(p1, self.p1_choice, p2, self.p2_choice)
        self.manager.current = 'game'


# --------- Game Screen ---------
class TicTacToeGrid(GridLayout):
    def __init__(self, status_label, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.spacing = 5
        self.padding = 5
        self.buttons = []
        self.status_label = status_label
        self.reset_game()

        for i in range(9):
            btn = Button(text='', font_size='32sp')
            btn.bind(on_release=self.make_move(i))
            self.buttons.append(btn)
            self.add_widget(btn)

    def make_move(self, index):
        def _on_press(instance):
            if not self.running or instance.text != '':
                return
            instance.text = self.current_symbol
            if self.check_winner(self.current_symbol):
                self.status_label.text = f"{self.current_name} wins!"
                self.running = False
                return
            if all(b.text != '' for b in self.buttons):
                self.status_label.text = "It's a draw!"
                self.running = False
                return
            # switch turn
            self.switch_player()
        return _on_press

    def set_players(self, p1, img1, p2, img2):
        self.player1 = {"name": p1, "symbol": "X", "image": img1}
        self.player2 = {"name": p2, "symbol": "O", "image": img2}
        self.current = self.player1
        self.current_name = self.current["name"]
        self.current_symbol = self.current["symbol"]
        self.status_label.text = f"{self.current_name}'s turn"

    def switch_player(self):
        self.current = self.player1 if self.current == self.player2 else self.player2
        self.current_name = self.current["name"]
        self.current_symbol = self.current["symbol"]
        self.status_label.text = f"{self.current_name}'s turn"

    def check_winner(self, mark):
        b = [btn.text for btn in self.buttons]
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,bidx,c in wins:
            if b[a] == b[bidx] == b[c] == mark:
                self.buttons[a].background_color = (0.7, 1, 0.7, 1)
                self.buttons[bidx].background_color = (0.7, 1, 0.7, 1)
                self.buttons[c].background_color = (0.7, 1, 0.7, 1)
                return True
        return False

    def reset_game(self):
        self.running = True
        for btn in getattr(self, 'buttons', []):
            btn.text = ''
            btn.background_color = (1, 1, 1, 1)


class GameScreen(Screen):
    grid = ObjectProperty(None)
    status = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=8, spacing=8)

        self.top_bar = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.p1_box = BoxLayout(orientation='horizontal', spacing=5)
        self.p1_img = Image(size_hint=(0.3, 1))
        self.p1_label = Label(text="", font_size='18sp')
        self.p1_box.add_widget(self.p1_img)
        self.p1_box.add_widget(self.p1_label)

        self.p2_box = BoxLayout(orientation='horizontal', spacing=5)
        self.p2_img = Image(size_hint=(0.3, 1))
        self.p2_label = Label(text="", font_size='18sp')
        self.p2_box.add_widget(self.p2_img)
        self.p2_box.add_widget(self.p2_label)

        self.top_bar.add_widget(self.p1_box)
        self.top_bar.add_widget(self.p2_box)

        self.status = Label(text="", size_hint=(1, 0.1), font_size='20sp')
        self.grid = TicTacToeGrid(status_label=self.status, size_hint=(1, 0.6))

        bottom = BoxLayout(size_hint=(1, 0.1))
        reset_btn = Button(text='Reset')
        reset_btn.bind(on_release=self.on_reset)
        back_btn = Button(text='Back')
        back_btn.bind(on_release=self.go_back)
        bottom.add_widget(reset_btn)
        bottom.add_widget(back_btn)

        root.add_widget(self.top_bar)
        root.add_widget(self.status)
        root.add_widget(self.grid)
        root.add_widget(bottom)
        self.add_widget(root)

    def set_players(self, name1, img1, name2, img2):
        self.p1_label.text = name1
        self.p2_label.text = name2
        self.p1_img.source = os.path.join("images", img1)
        self.p2_img.source = os.path.join("images", img2)
        self.grid.set_players(name1, img1, name2, img2)
        self.grid.reset_game()

    def on_reset(self, instance):
        self.grid.reset_game()
        self.status.text = f"{self.grid.current_name}'s turn"

    def go_back(self, instance):
        self.manager.current = 'setup'


# --------- App Entry Point ---------
class TicTacToeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SetupScreen(name='setup'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == '__main__':
    TicTacToeApp().run()