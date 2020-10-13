from positions import Positions

class Puzzlegame:

    def __init__(self):
        # nothing active at the start
        self.active_piece = -1
        self.highlighted = False
        # should this be the whole object or just the position tuple?
        self.current_pos = Positions().pieces
        self.pos_log = [Positions().pieces]
        self.move_log = []
        # solution stuff
        self.solution_mode = False
        self.pos_log_opt = []
        self.move_log_opt = []

    def is_solved(self):
        if self.current_pos[-1] == (3, 1):
            return True
        return False
