# main.py
# Tic-Tac-Toe using Kivy. Save as main.py and run with `python main.py`
# On Android, run via Kivy Launcher or package as APK.

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

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
            if not self.running:
                return
            if instance.text != '':
                return
            instance.text = self.current
            if self.check_winner(self.current):
                self.status_label.text = f"Player {self.current} wins!"
                self.running = False
                Clock.schedule_once(lambda dt: None, 0)  # small pause
                return
            if all(b.text != '' for b in self.buttons):
                self.status_label.text = "It's a draw!"
                self.running = False
                return
            # switch player
            self.current = 'O' if self.current == 'X' else 'X'
            self.status_label.text = f"Turn: {self.current}"
        return _on_press

    def check_winner(self, mark):
        b = [btn.text for btn in self.buttons]
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,bidx,c in wins:
            if b[a] == b[bidx] == b[c] == mark:
                # highlight winning buttons
                self.buttons[a].background_color = (0.8, 0.9, 0.5, 1)
                self.buttons[bidx].background_color = (0.8, 0.9, 0.5, 1)
                self.buttons[c].background_color = (0.8, 0.9, 0.5, 1)
                return True
        return False

    def reset_game(self, *args):
        self.current = 'X'
        self.running = True
        self.status_label.text = f"Turn: {self.current}"
        # if buttons already exist, clear them
        for btn in getattr(self, 'buttons', []):
            try:
                btn.text = ''
                btn.background_color = (1,1,1,1)
            except Exception:
                pass

class TicTacToeApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=8, spacing=8)
        self.status = Label(text="Turn: X", size_hint=(1, 0.12), font_size='20sp')
        self.grid = TicTacToeGrid(status_label=self.status, size_hint=(1, 0.78))
        bottom = BoxLayout(size_hint=(1, 0.1), spacing=8)
        reset_btn = Button(text='Reset', size_hint=(0.5, 1))
        reset_btn.bind(on_release=self.on_reset)
        exit_btn = Button(text='Exit', size_hint=(0.5, 1))
        exit_btn.bind(on_release=self.stop_app)
        bottom.add_widget(reset_btn)
        bottom.add_widget(exit_btn)

        root.add_widget(self.status)
        root.add_widget(self.grid)
        root.add_widget(bottom)
        return root

    def on_reset(self, instance):
        self.grid.reset_game()

    def stop_app(self, instance):
        App.get_running_app().stop()

if __name__ == '__main__':
    TicTacToeApp().run()