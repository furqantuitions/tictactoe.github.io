from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from functools import partial

class TicTacToeApp(App):
    def build(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_turn = 'X'
        self.winner = None
        
        layout = GridLayout(cols=3, spacing=5, padding=10)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                button = Button(
                    text='',
                    font_size=48,
                    background_normal='',
                    background_color=(0.4, 0.7, 1, 1)  # Light Blue Background
                )
                button.bind(on_release=partial(self.make_move, row, col))
                self.buttons[row][col] = button
                layout.add_widget(button)
        
        # Restart Button
        restart_button = Button(
            text="Restart Game",
            font_size=24,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        restart_button.bind(on_release=self.restart_game)
        
        self.result_label = Label(
            text='',
            font_size=36,
            size_hint_y=None,
            height=50,
            color=(1, 0.2, 0.2, 1)  # Red Text Color
        )
        
        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(layout)
        root_layout.add_widget(restart_button)
        root_layout.add_widget(self.result_label)
        
        return root_layout
    
    def restart_game(self, instance):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_turn = 'X'
        self.winner = None
        self.result_label.text = ''
        
        for row in self.buttons:
            for button in row:
                button.text = ''
                button.background_color = (0.4, 0.7, 1, 1)
                button.disabled = False
    
    def make_move(self, row, col, button):
        if self.board[row][col] == ' ' and not self.winner:
            button.text = self.player_turn
            self.board[row][col] = self.player_turn
            winner = self.check_winner()
            
            if winner:
                self.display_winner(winner)
            else:
                self.player_turn = 'O' if self.player_turn == 'X' else 'X'
                if self.player_turn == 'O':
                    self.ai_move()
    
    def ai_move(self):
        if not self.winner:
            empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']
            if empty_cells:
                row, col = self.get_best_move()
                self.make_move(row, col, self.buttons[row][col])
    
    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    self.board[row][col] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        return best_move
    
    def minimax(self, board, depth, is_maximizing):
        scores = {'X': -1, 'O': 1, 'Tie': 0}
        result = self.check_winner(board)
        
        if result:
            return scores[result]
        
        if is_maximizing:
            best_score = -float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = ' '
                        best_score = min(score, best_score)
            return best_score
    
    def check_winner(self, board=None):
        if board is None:
            board = self.board

        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] != ' ':
                return board[row][0]
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != ' ':
                return board[0][col]
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]
        if all(cell != ' ' for row in board for cell in row):
            return 'Tie'
    
    def display_winner(self, winner):
        self.winner = winner
        if winner == 'Tie':
            self.result_label.text = "It's a Tie!"
        else:
            self.result_label.text = f"Player {winner} wins!"
        for row in self.buttons:
            for button in row:
                button.disabled = True
                button.background_color = (0.7, 0.7, 0.7, 1)  # Grayed out background

if __name__ == '__main__':
    TicTacToeApp().run()