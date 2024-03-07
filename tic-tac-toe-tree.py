from manim import *


# This is just a static diagram but could be turned into an algorithm demo for min-max
class TicTacToe(MovingCameraScene):
    def construct(self):
        turn = "X"
        state1 = ["", "", "", "O", "X", "", "O", "X", ""]
        board1 = self.create_tic_tac_toe_board(state1).scale(0.75).shift(UP * 2)

        self.add(board1)

        board_row = VGroup()
        for i, board_and_pos in enumerate(self.potential_boards(state1, turn)):
            board_state, new_pos = board_and_pos
            board = self.create_tic_tac_toe_board(
                board_state, highlight_ind=new_pos
            ).scale(0.5)
            circle = Circle()
            circle.surround(board, buffer_factor=1.0)
            circle.set_stroke(width=2)
            if i < 2:
                circle.set_color(RED)
            else:
                circle.set_color(BLUE)
            circled_board = VGroup(board, circle)
            board_row.add(circled_board)

        board_row.arrange(RIGHT, buff=0.8)
        board_row.next_to(board1, DOWN * 4, buff=0.5)

        for i, circled_board in enumerate(board_row):
            start_point = board1.get_bottom()
            end_point = circled_board.get_top()
            arrow = Arrow(
                start_point + DOWN * 0.1,
                end_point + UP * 0.1,
                buff=0.1,
                stroke_width=2,
                color=GOLD,
            )
            self.add(arrow)

        self.add(board_row)

    def potential_boards(self, state, turn):
        for i, pos in enumerate(state):
            if pos == "":
                new_state = state[:]
                new_state[i] = turn
                yield (new_state, i)

    def create_tic_tac_toe_board(self, state, highlight_ind=None):
        if len(state) != 9:
            raise ValueError("State list must contain 9 elements.")

        squares = VGroup()
        for y in range(1, -2, -1):
            for x in range(-1, 2):
                square = Square(side_length=1).move_to(np.array([x * 1, y * 1, 0]))
                square.set_opacity(0.2)
                squares.add(square)

        x_turn = sum([item == "O" or item == "X" for item in state])
        if highlight_ind is not None:
            cur_square = squares[highlight_ind]
            cur_square.set_fill(RED if x_turn else BLUE)
            cur_square.set_opacity(0.3)
            cur_square.set_stroke(width=0)

        elements = VGroup()
        for square, grid_el in zip(squares, state):
            if grid_el == "O":
                circle = Circle(radius=1 / 3, color=BLUE).move_to(square.get_center())
                elements.add(circle)
            elif grid_el == "X":
                line1 = Line(UP + LEFT, DOWN + RIGHT).scale(1 / 3)
                line2 = Line(UP + RIGHT, DOWN + LEFT).scale(1 / 3)
                cross = VGroup(line1, line2).move_to(square.get_center())
                cross.set_color(RED)
                elements.add(cross)

        board = VGroup(squares, elements)
        return board
