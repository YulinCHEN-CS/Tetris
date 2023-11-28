from board import Direction, Rotation, Action
from random import Random
import time
import constants


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
                

            

    def choose_action(self, board):
        self.print_board(board)
        time.sleep(0.5)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])

class StephensPlayer(Player):

    def __init__(self, seed=None):
        self.random = Random(seed)
    
    def choose_action(self, board):
        move_list = []
        max_score = -139987489702
        for num_of_rot in range (0, 4):
            temp_rot_list = []
            clone_board = board.clone()
            width = self.get_width(clone_board)
            height = self.get_height(clone_board)
            for i in range(0, num_of_rot):
                clone_board.falling.rotate(Rotation.Clockwise, clone_board)
                width = self.get_width(clone_board)
                temp_rot_list.append(Rotation.Clockwise)
            for pos in range(0, constants.BOARD_WIDTH - width + 1):
                temp_move_list = []
                clone2_board = clone_board.clone()
                temp_move_list += temp_rot_list
                start_score = clone2_board.score
                row_length = self.get_row_length_list(clone2_board.falling)
                temp_move_list += self.move_to_target(clone2_board, pos)
                end_score = clone2_board.score
                # Landing height
                landing_height = -1
                for i in range(pos, pos + width):
                    for j in range (constants.BOARD_HEIGHT):
                        is_empty = True
                        if (i, j) in clone2_board.cells:
                            is_empty = False
                    if not is_empty:
                        local_height = 24 - min(y for (x, y) in clone2_board.cells if x == i)
                        if local_height > landing_height:
                            landing_height = local_height
                    else:
                        continue
                print("landing height ", landing_height)
                # Eroded Piece Cells
                drop_score = 23 - landing_height
                d_score = end_score - start_score - drop_score
                print(end_score, start_score, drop_score)
                print("d score", d_score)
                num_of_removed = 0
                if d_score == 25:
                    num_of_removed = 1
                elif d_score == 100:
                    num_of_removed = 2
                elif d_score == 400:
                    num_of_removed = 3
                elif d_score == 1600:
                    num_of_removed = 4
                num_of_row = len(row_length)
                num_of_donate = 0
                erodedPieceCells = 0
                print("num of row ", num_of_row)
                print("num of removed ", num_of_removed)
                for i in range(num_of_removed):
                    num_of_donate += row_length[num_of_row - i - 1]
                print("row length ", row_length)
                print("num of donate ", num_of_donate)
                erodedPieceCells = num_of_donate * num_of_removed
                # Board Row Transitions
                row_trans = 0
                if not clone2_board.cells:
                    for j in range(min(y for (x, y) in clone2_board.cells), 24):
                        for i in range(9):
                            if ((i, j) in clone2_board.cells and (i + 1, j) not in clone2_board.cells) or ((i, j) not in clone2_board.cells and (i + 1, j) in clone2_board.cells):
                                row_trans += 1
                print("board row trans ", row_trans)
                # Board Column Transitions
                col_trans = 0
                for j in range(min(y for (x, y) in clone2_board.cells), 23):
                    for i in range(11):
                        if ((i, j) in clone2_board.cells and (i, j + 1) not in clone2_board.cells) or ((i, j) not in clone2_board.cells and (i, j + 1) in clone2_board.cells):
                            col_trans += 1
                print("col trans ", col_trans)
                # num of holes
                num_of_holes = 0
                have_holes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for y in range(constants.BOARD_HEIGHT):
                    for x in range(constants.BOARD_WIDTH):
                        if (x,y) in clone2_board.cells:
                            have_holes[x] = 1
                        if not (x,y) in clone2_board.cells and have_holes[x] == 1:
                            if y > max(y for (x, y) in clone2_board.cells) + landing_height / 2:
                                num_of_holes += 5
                            else:
                                num_of_holes += 1
                print("num of holes ", num_of_holes)
                # wells calculation using sum from 1
                sum_wells = 0
                for x in range(0, constants.BOARD_WIDTH):
                    for y in range (constants.BOARD_HEIGHT):
                        if (x < 1 and (x, y) not in clone2_board.cells and (x + 1, y) in clone2_board.cells) or ((x - 1,y) in clone2_board.cells and (x, y) not in clone2_board.cells and (x + 1, y) in clone2_board.cells) or (x > constants.BOARD_WIDTH - 2 and (x - 1, y) in clone2_board.cells and (x, y) not in clone2_board.cells):
                            well_x = x
                            well_y = y
                            depth_of_well = 1
                            while((well_x, well_y + 1) not in clone2_board.cells and well_y + 1 < constants.BOARD_HEIGHT):
                                depth_of_well += 1
                                well_y += 1
                            print(well_x, "depth of well ", depth_of_well)
                            sum_wells += self.sum_from_1(depth_of_well)
                print("sum wells ", sum_wells)
                # relative height:
                # relative_height = 0
                # if(clone2_board.cells is not None):
                #     for i in range (min (x for (x, y) in clone2_board.cells), max (x for (x, y) in clone2_board.cells) - 1):
                #         h1 = 0
                #         h2 = 0
                #         if (y for (x, y) in clone2_board.cells if x == i) is not None:
                #             h1 = min(y for (x, y) in clone2_board.cells if x == i)
                #             print(h1)
                #         if (y for (x, y) in clone2_board.cells if x == i + 1) is not None:
                #             h2 = min(y for (x, y) in clone2_board.cells if x == i + 1)
                #             print(h2)
                #         relative_height += abs(h1 - h2)
                # print("relative height ", relative_height)
                #total evaluate
                clone2_score = -3.9369638078598443 * landing_height + 4.41696135478181356 * erodedPieceCells -4.666157428785609 * row_trans -4.824500082802795 * col_trans -11.617686834237748 * num_of_holes -4.460981042701126 * sum_wells +5.974247426543533 * num_of_removed
                # self.print_board(clone2_board)
                print("max score", max_score)
                print("current score ", clone2_score)
                if clone2_score > max_score:
                    max_score = clone2_score
                    move_list = temp_move_list
        print(move_list)
        return move_list

    def move_to_target(self, clone_board, tar_pos):
        move_list = []
        if clone_board.falling == None:
            return
        current_left = clone_board.falling.left
        while current_left > tar_pos: 
            current_action = Direction.Left
            move_list.append(current_action)
            clone_board.move(current_action)
            if clone_board.falling == None:
                break
            current_left = clone_board.falling.left
        while current_left < tar_pos:
            current_action = Direction.Right
            move_list.append(current_action)
            clone_board.move(current_action)
            if clone_board.falling == None:
                break
            current_left = clone_board.falling.left
        if clone_board.falling != None:
            move_list.append(Direction.Drop)
            clone_board.move(Direction.Drop)
        return move_list

    def get_width(self, clone_board):
        if clone_board.falling != None:
            return clone_board.falling.right + 1 - clone_board.falling.left
        return 0

    def get_height(self, clone_board):
        return clone_board.falling.top - clone_board.falling.bottom + 1

    def sum_from_1(self, end):
        sum = 0
        for i in range (end + 1):
            sum += i
        return sum

    def get_row_length_list(self, block):
        row_length_list = []
        print(block.top, block.bottom)
        print(block.left, block.right)
        for y in range(block.top, block.bottom + 1):
            count = 0
            for x in range(block.left, block.right + 1):
                if (x, y) in block.cells:
                    count += 1
            row_length_list.append(count)
        return row_length_list

    def score_board(self, clone_board):
        return clone_board.score

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)



SelectedPlayer = StephensPlayer

