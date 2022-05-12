from positions import Positions
import position_lists as pl
import db_functions as dbf

class Puzzlegame:

    def __init__(self):
        # nothing active at the start
        self.active_piece = -1
        # is this variable needed?
        # self.highlighted = False
        self.active_piece_for_dragging = -1
        # should this be the whole object or just the position tuple?
        self.index_opt = 0
        # pos = Positions()
        pos = dbf.get_pos_by_id(self.index_opt)
        self.current_pos = pos.pieces
        self.current_pos_id = pos.pos_id
        self.possible_next_pos = dbf.get_pos_by_ids(pos.neighbors)
        self.pos_log = [pos.pieces]
        self.move_log = []
        # solution stuff
        self.solution_mode = False
        self.pos_log_opt = []
        self.move_log_opt = []
        if not dbf.does_db_exist():
            print("NO DATABASE")
            return
        if not dbf.check_pos_db():
            print("SOMETHING WRONG WITH DATABASE")

    def show_empties(self):
        return tuple(Positions(self.current_pos, self.index_opt).set_empties())

    def is_solved(self):
        if self.current_pos[-1] == (3, 1):
            return True
        return False

    def reset(self):
        self.active_piece = -1
        self.active_piece_for_dragging = -1
        self.index_opt = 0
        # pos = Positions()
        pos = dbf.get_pos_by_id(self.index_opt)
        self.current_pos = pos.pieces
        self.current_pos_id = pos.pos_id
        self.possible_next_pos = dbf.get_pos_by_ids(pos.neighbors)
        self.pos_log = [pos.pieces]
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

    def update_id_and_neighbors(self):
        curr_pos = Positions(self.current_pos)
        for pos in self.possible_next_pos:
            if curr_pos == pos:
                self.current_pos_id = pos.pos_id
                self.possible_next_pos = dbf.get_pos_by_ids(pos.neighbors)
                break

    def make_move(self, move):
        pos = Positions(self.current_pos, self.index_opt)
        if pos.move_ok(move):
            next_pos = pos.make_move(move)
            self.current_pos = next_pos.pieces
            self.update_id_and_neighbors()
            self.move_log.append(move)
            self.pos_log.append(self.current_pos)
            self.index_opt += 1
            if not(self.current_pos == self.pos_log[self.index_opt]):
                print("problems!!!!")
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
            self.update_id_and_neighbors()
            self.index_opt -= 1
            if not(self.current_pos == self.pos_log[self.index_opt]):
                print("problems!!!!")
            return True

    # 0 = left, 1 = right
    def cycle_solution(self, direction):
        if not self.solution_mode:
            return False
        if not(self.current_pos in self.pos_log_opt):
            print("Something has gone terribly wrong")
            return False
        # going back
        if direction == 0:
            if self.index_opt == 0:
                return False
            else:
                self.current_pos = self.pos_log_opt[self.index_opt - 1]
                self.update_id_and_neighbors()
                self.pos_log.pop()
                self.move_log.pop()
                self.index_opt -= 1
                if not(self.current_pos == self.pos_log[self.index_opt]):
                    print("problems!!!!")
                return True
        # going forward
        elif direction == 1:
            if self.index_opt == len(self.pos_log_opt) - 1:
                return False
            else:
                self.current_pos = self.pos_log_opt[self.index_opt + 1]
                self.update_id_and_neighbors()
                self.pos_log.append(self.current_pos)
                self.move_log.append(self.move_log_opt[self.index_opt])
                self.index_opt += 1
                if not(self.current_pos == self.pos_log[self.index_opt]):
                    print("problems!!!!")
                return True

    def show_solution(self):
        self.reset()
        self.solution_mode = True
        ##### Choose the first 2 or last 2 lines of the 4 next lines (file or database)
        # import solution_opt_117
        # pos_log_opt = solution_opt_117.pos_list
        # import puzzlesolver
        # pos_log_opt = puzzlesolver.find_soln_from_start()
        pos_log_opt = dbf.find_opt_solution(self.current_pos_id)
        #####
        self.move_log_opt = pl.move_list_from_pos_list(pos_log_opt)
        self.pos_log_opt = list(map(lambda x: x.pieces, pos_log_opt))

    def find_solution(self):
        self.solution_mode = True
        # pos = Positions(self.current_pos, self.index_opt)
        pos_log = [Positions(self.pos_log[i], i) for i in range(len(self.pos_log))]
        ##### Choose one of the two lines below (file or database)
        # pos_list = puzzlesolver.solve_opt_w_fd(pos)
        # import puzzlesolver
        # pos_list = puzzlesolver.solve_opt_w_db(pos)
        pos_list = dbf.find_opt_solution(self.current_pos_id)
        ##### 
        pos_log_opt = pl.combine_lists(pos_log, pos_list)
        self.move_log_opt = pl.move_list_from_pos_list(pos_log_opt)
        self.pos_log_opt = list(map(lambda p: p.pieces, pos_log_opt))
