from positions import Positions
import move as mv

class Puzzlegame:

    def __init__(self):
        # nothing active at the start
        self.active_piece = -1
        # is this variable needed?
        # self.highlighted = False
        self.active_piece_for_dragging = -1
        # should this be the whole object or just the position tuple?
        self.current_pos = Positions().pieces
        self.pos_log = [Positions().pieces]
        self.move_log = []
        # solution stuff
        self.solution_mode = False
        self.pos_log_opt = []
        self.move_log_opt = []

    def show_empties(self):
        return Positions(0, self.current_pos).set_empties()

    def is_solved(self):
        if self.current_pos[-1] == (3, 1):
            return True
        return False

    def reset(self):
        self.active_piece = -1
        self.active_piece_for_dragging = -1
        self.current_pos = Positions().pieces
        self.pos_log = [Positions().pieces]
        self.move_log = []
        self.solution_mode = False
        # self.pos_log_opt = []
        # self.move_log_opt = []

    def set_active(self, piece_id):
        # should this check for valid piece_id?
        if self.active_piece == piece_id:
            self.active_piece = -1
            # nothing highlighted
            return False
        else:
            self.active_piece = piece_id
            # something is highlighted
            return True
    
    # # is this needed?
    # def deactivate(self):
    #     self.active_piece = -1

    def make_move(self, move):
        pos = Positions(0, self.current_pos)
        if mv.move_ok(move, pos):
            self.current_pos = mv.make_move(move, pos).pieces
            self.move_log.append(move)
            self.pos_log.append(self.current_pos)
            return True
        else:
            return False

    def undo_move(self):
        if self.move_log == []:
            return False
        else:
            self.move_log.pop()
            self.pos_log.pop()
            self.current_pos = self.pos_log[-1]
            return True

    # 0 = left, 1 = right
    def cycle_solution(self, direction):
        if not self.solution_mode:
            return False
        if not(self.current_pos in self.pos_log_opt):
            print("Something has gone terribly wrong")
            return False
        index_opt = self.pos_log_opt.index(self.current_pos)
        if direction == 0:
            if index_opt == 0:
                return False
            else:
                self.current_pos = self.pos_log_opt[index_opt - 1]
                self.pos_log.pop()
                self.move_log.pop()
                return True
        elif direction == 1:
            if index_opt == len(self.pos_log_opt) - 1:
                return False
            else:
                self.current_pos = self.pos_log_opt[index_opt + 1]
                self.pos_log.append(self.current_pos)
                self.move_log.append(self.move_log_opt[index_opt])
                return True

    def show_solution(self):
        import solution_opt_117
        self.reset()
        self.solution_mode = True
        pos_log_opt = solution_opt_117.pos_list
        self.move_log_opt = mv.move_list_from_pos_list(pos_log_opt)
        self.pos_log_opt = list(map(lambda x: x.pieces, pos_log_opt))

    def find_solution(self):
        import puzzlesolver
        self.solution_mode = True
        pos = Positions(self.pos_log.index(self.current_pos), self.current_pos)
        # ROPLEMS maybe fixed
        pos_log = [Positions(i, self.pos_log[i]) for i in range(len(self.pos_log))]
        pos_list = puzzlesolver.solve_opt_w_fd(pos)[0]
        pos_log_opt = mv.combine_lists(pos_log, pos_list)
        self.move_log_opt = mv.move_list_from_pos_list(pos_log_opt)
        self.pos_log_opt = list(map(lambda p: p.pieces, pos_log_opt))
