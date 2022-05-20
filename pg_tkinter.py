import tkinter as tk

from puzzlegame_setup import piece_nums, piece_types, all_pieces
from puzzlegame_setup import piece_colors, piece_symbols, get_texts_in_language
from db_functions import get_languages_from_db, get_default_language, set_default_language
from positions import Positions
from puzzlegame import Puzzlegame


class PuzzlegameParameters:
    def __init__(self):
        self.languages = get_languages_from_db()
        # self.current_language = self.languages[0]
        self.current_language = get_default_language()
        self.texts = get_texts_in_language(self.current_language)
        # self.directions = tuple([self.texts[f"direction{i}_TEXT"] for i in range(4)])
        self.move_text = ('', '', '', '')
    
    def change_language(self):
        self.current_language = self.languages[(self.languages.index(self.current_language) + 1) % len(self.languages)]
        self.texts = get_texts_in_language(self.current_language)
        set_default_language(self.current_language)
        # self.directions = tuple([self.texts[f"direction{i}"] for i in range(4)])
        # if any(self.previous_move_text):
        #     updated_move_text = []

    def get_move_text(self):
        text_parts = []
        for text in self.move_text:
            if "TEXT" in text:
                text_parts.append(self.texts[text])
            else:
                text_parts.append(text)
        return " ".join(text_parts)



def play_puzzlegame():

    # some text stuff
    params = PuzzlegameParameters()
    # default_language = "FIN"

    def move_text(piece_id, move):
        params.move_text = ("PIECE_TEXT", piece_symbols[piece_id], "MOVE_TEXT", f"DIRECTION{move % 4}_TEXT")
        return params.get_move_text()
    
    def no_move_text(piece_id, num):
        params.move_text = ("PIECE_TEXT", piece_symbols[piece_id], "NO_MOVE_TEXT", f"DIRECTION{num}_TEXT")
        # return f"{params.texts['PIECE_TEXT']} {piece_symbols[piece_id]} {params.texts['NO_MOVE_TEXT']} {params.directions[num]}"
        return params.get_move_text()
    
    def selection_text(piece_id):
        params.move_text = ("PIECE_TEXT", piece_symbols[piece_id], "SELECT_TEXT", '')
        return f"{params.get_move_text()}"
        # return f"    {params.texts['PIECE_TEXT']} {piece_symbols[piece_id]} {params.texts['SELECT_TEXT']}    "

    # window with two frames on the left and one on the right
    main_window = tk.Tk()
    main_window.title(params.texts["TITLE_TEXT"])
    # game_window = tk.LabelFrame(main_window, padx=1, pady=1)
    game_area = tk.LabelFrame(main_window, padx=1, pady=1)
    statusline = tk.LabelFrame(main_window, padx=1, pady=1)
    sideframe = tk.LabelFrame(main_window, padx=1, pady=1)
    # game_window.grid(row=0, column=0, padx=0, pady=0)
    game_area.grid(row=0, column=0, padx=0, pady=0)
    statusline.grid(row=1, column=0, sticky=tk.W + tk.E)
    sideframe.grid(row=0, column=1, rowspan=2, sticky=tk.N+tk.S)

    # # black borders around the game area (going with another implementation)
    # game_area = tk.LabelFrame(game_window, padx=1, pady=1)
    # black_bar_up = tk.Label(game_window, text="", bg="black")
    # black_bar_left = tk.Label(game_window, text="", bg="black")
    # black_bar_right = tk.Label(game_window, text="", bg="black")
    # black_bar_down = tk.Label(game_window, text="", bg="black")
    # black_bar_up.grid(row=0, column=0, columnspan=3, sticky=tk.W + tk.E)
    # black_bar_left.grid(row=1, column=0, sticky=tk.N + tk.S)
    # game_area.grid(row=1, column=1, padx=0, pady=0)
    # black_bar_right.grid(row=1, column=2, sticky=tk.N + tk.S)
    # black_bar_down.grid(row=2, column=0, columnspan=3, sticky=tk.W + tk.E)

    # active global variables
    # highlighted = False
    # mb1_pressed = False
    global_vars = [False, False]
    # highlighted_sortof = False
    puzzlegame = Puzzlegame()

    def place_pieces(buttons, ebuttons):
        pos = puzzlegame.current_pos
        k = 0
        for j in range(len(piece_nums)):
            for i in range(piece_nums[j]):
                buttons[k].grid(row=pos[k][0]+1, column=pos[k][1]+1,
                            rowspan=piece_types[j][0], columnspan=piece_types[j][1], sticky=tk.W + tk.E + tk.N + tk.S)
                k += 1
        for i in range(len(puzzlegame.show_empties())):
            ebuttons[i].grid(row=puzzlegame.show_empties()[i][0]+1, column=puzzlegame.show_empties()[i][1]+1)

    def is_solved():
        if puzzlegame.is_solved():
        # if pos.pieces[-1] == (3,1):
            solution_text.config(text=params.texts["SOLVED_TEXT"])
        else:
            solution_text.config(text=params.texts["NOT_SOLVED_TEXT"])

    def deactivate():
        if global_vars[0]:
            pieces[puzzlegame.active_piece].config(relief=tk.RAISED)
        global_vars[0] = False
        puzzlegame.active_piece = -1

    def restart():
        deactivate()
        puzzlegame.reset()
        place_pieces(pieces, empties)
        statustexts[0].config(text="                              ")
        statustexts[1].config(text="                              ")
        solving_text1.config(text=" ")
        solving_text2.config(text=" ")
        solution_text.config(text=" ")
        undo_button.config(state=tk.DISABLED)
        solution_back.config(state=tk.DISABLED)
        solution_fwd.config(state=tk.DISABLED)


    def undo():
        # what if we are in solution mode??
        deactivate()
        puzzlegame.undo_move()
        place_pieces(pieces, empties)
        params.move_text = ("", "", "UNDONE_TEXT", "")
        statustexts[0].config(text=params.get_move_text())
        is_solved()
        if puzzlegame.solution_mode:
            # index_opt = len(puzzlegame.move_log)
            statustexts[1].config(text=str(puzzlegame.index_opt + 1) + " / " + str(len(puzzlegame.pos_log_opt)))
            if puzzlegame.index_opt == 0:
                solution_back.config(state=tk.DISABLED)
            elif puzzlegame.index_opt < len(puzzlegame.move_log_opt):
                solution_fwd.config(state=tk.NORMAL)
        if puzzlegame.move_log == []:
            undo_button.config(state=tk.DISABLED)
        is_solved()


    def pressed(piece_id):
        # is a piece highlighted already, and is it the one we clicked??
        if global_vars[0] and puzzlegame.active_piece == piece_id:
            # if we clicked the active piece, it deactivates
            deactivate()
            statustexts[0].config(text="                              ")
        elif global_vars[0]:
            # switch active piece
            pieces[puzzlegame.active_piece].config(relief=tk.RAISED)
            puzzlegame.active_piece = piece_id
            pieces[piece_id].config(relief=tk.SUNKEN)
            statustexts[0].config(text=selection_text(piece_id))
        else:
            # no pieces were active previously
            global_vars[0] = True
            puzzlegame.active_piece = piece_id
            pieces[piece_id].config(relief=tk.SUNKEN)
            statustexts[0].config(text=selection_text(piece_id))


    def try_move(empty_id):
        # do we need highlighted or active_piece here??
        empty_spot = puzzlegame.show_empties()[empty_id]
        current_pos = Positions(puzzlegame.current_pos)
        if global_vars[0]:
            move = current_pos.move_from_coord(puzzlegame.active_piece, empty_spot)
            if move == -1:
                # statustexts[0].config(text=piece_symbols[puzzlegame.active_piece] + " cannot move to " + str(empty_spot))
                params.move_text = ("PIECE_TEXT", piece_symbols[puzzlegame.active_piece], "NO_MOVE_TO_TEXT", str(empty_spot))
                # statustexts[0].config(text=f"{params.texts['PIECE_TEXT']} {piece_symbols[puzzlegame.active_piece]} {params.texts['NO_MOVE_TO_TEXT']} {str(empty_spot)}")
                statustexts[0].config(text=params.get_move_text())
            else:
                if puzzlegame.move_log == []:
                    undo_button.config(state=tk.NORMAL)
                if puzzlegame.solution_mode:
                    puzzlegame.solution_mode = False
                    solution_back.config(state=tk.DISABLED)
                    solution_fwd.config(state=tk.DISABLED)
                    statustexts[1].config(text="                              ")
                    solving_text1.config(text="  ")
                    solving_text2.config(text="  ")
                puzzlegame.make_move(move)
                # statustexts[0].config(text="Piece " + piece_symbols[puzzlegame.active_piece] + " moves " + params.directions[move%4])
                statustexts[0].config(text=move_text(puzzlegame.active_piece, move))
                place_pieces(pieces, empties)
        is_solved()


    def solution_from_start():
        restart()
        puzzlegame.show_solution()
        solution_fwd.config(state=tk.NORMAL)
        statustexts[1].config(text=str(1) + " / " + str(len(puzzlegame.pos_log_opt)))
        solving_text2.config(text=params.texts["SOLN_HELP_TEXT"])


    def solution_from_pos():
        puzzlegame.find_solution()
        # index_opt = len(puzzlegame.move_log)
        if puzzlegame.index_opt > 0:
            solution_back.config(state=tk.NORMAL)
        if puzzlegame.index_opt < len(puzzlegame.pos_log_opt) - 1:
            solution_fwd.config(state=tk.NORMAL)
        solving_text1.config(text=params.texts["SOLN_FOUND_TEXT"])
        statustexts[1].config(text=str(puzzlegame.index_opt + 1) + " / " + str(len(puzzlegame.pos_log_opt)))
        solving_text2.config(text=params.texts["SOLN_HELP_TEXT"])


    def soln_back():
        if global_vars[0]:
            deactivate()
        params.move_text = ("", "", "BACK_TEXT", "")
        statustexts[0].config(text=params.get_move_text())
        puzzlegame.cycle_solution(0)
        # index_opt = len(puzzlegame.move_log)
        place_pieces(pieces, empties)
        if puzzlegame.move_log == []:
            undo_button.config(state=tk.DISABLED)
        if puzzlegame.index_opt < len(puzzlegame.move_log_opt):
            solution_fwd.config(state=tk.NORMAL)
        if puzzlegame.index_opt == 0:
            solution_back.config(state=tk.DISABLED)
        statustexts[1].config(text=str(puzzlegame.index_opt + 1) + " / " + str(len(puzzlegame.pos_log_opt)))
        is_solved()

    def soln_fwd():
        if global_vars[0]:
            deactivate()
        if puzzlegame.move_log == []:
            undo_button.config(state=tk.NORMAL)
        puzzlegame.cycle_solution(1)
        move = puzzlegame.move_log[-1]
        # statustexts[0].config(text="Piece " + piece_symbols[move//4] + " moves " + params.directions[move%4])
        statustexts[0].config(text=move_text(move // 4, move))
        solution_back.config(state=tk.NORMAL)
        place_pieces(pieces, empties)
        if puzzlegame.index_opt == len(puzzlegame.move_log_opt):
            solution_fwd.config(state=tk.DISABLED)
        statustexts[1].config(text=str(puzzlegame.index_opt + 1) + " / " + str(len(puzzlegame.pos_log_opt)))
        is_solved()
    

    def change_language():
        params.change_language()
        main_window.title(params.texts["TITLE_TEXT"])
        restart_button.config(text=params.texts["RESTART_TEXT"])
        description.config(text=params.texts["DESCR_TEXT"])
        undo_button.config(text=params.texts["UNDO_TEXT"])
        show_soln_button.config(text=params.texts["SHOW_SOLN_TEXT"])
        solve_button.config(text=params.texts["FIND_SOLN_TEXT"])
        language_text.config(text=params.texts["LANGUAGE_TEXT"])
        language_button.config(text=params.current_language)
        if puzzlegame.is_solved():
            # solving_text1.config(text=params.texts["SOLN_FOUND_TEXT"])
            solution_text.config(text=params.texts["SOLVED_TEXT"])
        if puzzlegame.solution_mode:
            solving_text2.config(text=params.texts["SOLN_HELP_TEXT"])
            if solving_text1.cget("text").strip():
                solving_text1.config(text=params.texts["SOLN_FOUND_TEXT"])
        if statustexts[0].cget("text").strip():
            statustexts[0].config(text=params.get_move_text())
            

    ####################### GUI VISIBLE STUFF
    # movable pieces
    # first the button dimensions [width, height]
    def b_d(piece_id):
        if all_pieces[piece_id][0] == 1 and all_pieces[piece_id][1] == 1:
            return [12,6]
        if all_pieces[piece_id][0] == 2 and all_pieces[piece_id][1] == 1:
            return [12,13]
        if all_pieces[piece_id][0] == 1 and all_pieces[piece_id][1] == 2:
            return [25,6]
        if all_pieces[piece_id][0] == 2 and all_pieces[piece_id][1] == 2:
            return [25,13]

    # (approx) width and height of buttons (in pixels)
    button_width = 95
    button_height = 100

    pieces = []
    k = 0
    for j in range(len(piece_nums)):
        for i in range(piece_nums[j]):
            piece = tk.Button(game_area, text=piece_symbols[k], bg=piece_colors[j], width=b_d(k)[0],
                            height=b_d(k)[1], command=lambda k=k: pressed(k))
            pieces.append(piece)
            pieces[k].grid(row=puzzlegame.current_pos[k][0]+1, column=puzzlegame.current_pos[k][1]+1,
                        rowspan=piece_types[j][0], columnspan=piece_types[j][1], sticky=tk.W+tk.E+tk.N+tk.S)
            k += 1

    # where the pieces might move
    empties = []
    for i in range(len(puzzlegame.show_empties())):
        empty_square = tk.Button(game_area, text="", width=12, height=6, command=lambda i=i: try_move(i))
        empties.append(empty_square)
        empties[i].grid(row=puzzlegame.show_empties()[i][0]+1, column=puzzlegame.show_empties()[i][1]+1)

    # black borders around game area
    black_bar_up = tk.Label(game_area, text="", bg="black")
    black_bar_left = tk.Label(game_area, text="   ", bg="black")
    black_bar_right = tk.Label(game_area, text="   ", bg="black")
    black_bar_down1 = tk.Label(game_area, text="", bg="black")
    black_bar_down2 = tk.Label(game_area, text="", bg="black")
    black_bar_up.grid(row=0, column=0, columnspan=6, sticky=tk.W + tk.E)
    black_bar_left.grid(row=1, column=0, rowspan=5, sticky=tk.N +tk.S)
    black_bar_right.grid(row=1, column=5, rowspan=5, sticky=tk.N +tk.S)
    black_bar_down1.grid(row=6, column=0, columnspan=2, sticky=tk.W + tk.E)
    black_bar_down2.grid(row=6, column=4, columnspan=2, sticky=tk.W + tk.E)

    ################## status line things
    # 2 status texts for some reason
    statustexts = []
    for i in range(2):
        statustext = tk.Label(statusline, text="                              ", width=30)
        statustexts.append(statustext)
        statustexts[i].grid(row=i, column=1, padx=30, pady=2)

    # buttons to navigate solutions
    solution_back = tk.Button(statusline, text="<<", state=tk.DISABLED, command=soln_back)
    solution_fwd = tk.Button(statusline, text=">>", state=tk.DISABLED, command=soln_fwd)
    solution_back.grid(row=0, column=0, rowspan=3, padx=20, sticky=tk.E)
    solution_fwd.grid(row=0, column=2, rowspan=3, padx=20, sticky=tk.W)


    # sideframe buttons and stuff
    sidebuttons = []
    some_space_at_the_top = tk.Label(sideframe, text=" \n \n \n")
    sidebuttons.append(some_space_at_the_top)
    restart_button = tk.Button(sideframe, text=params.texts["RESTART_TEXT"], width=20, command=restart)
    sidebuttons.append(restart_button)
    description = tk.Label(sideframe, text=params.texts["DESCR_TEXT"])
    sidebuttons.append(description)
    undo_button = tk.Button(sideframe, text=params.texts["UNDO_TEXT"], width=20, state=tk.DISABLED, command=undo)
    sidebuttons.append(undo_button)
    show_soln_button = tk.Button(sideframe, text=params.texts["SHOW_SOLN_TEXT"], width=20, command=solution_from_start)
    sidebuttons.append(show_soln_button)
    solve_button = tk.Button(sideframe, text=params.texts["FIND_SOLN_TEXT"], width=20, command=solution_from_pos)
    sidebuttons.append(solve_button)
    solving_text1 = tk.Label(sideframe, text="", width=20)
    sidebuttons.append(solving_text1)
    solving_text2 = tk.Label(sideframe, text="", width=20)
    sidebuttons.append(solving_text2)
    solution_text = tk.Label(sideframe, text="")
    sidebuttons.append(solution_text)
    some_space_near_the_bottom = tk.Label(sideframe, text="\n")
    sidebuttons.append(some_space_near_the_bottom)
    language_text =  tk.Label(sideframe, text=params.texts["LANGUAGE_TEXT"])
    sidebuttons.append(language_text)
    language_button = tk.Button(sideframe, text=params.current_language, width=20, command=change_language)
    sidebuttons.append(language_button)

    # putting the buttons onto the sideframe
    for i in range(len(sidebuttons)):
        sidebuttons[i].grid(row=i, column=0, padx=1, pady=5)


    ################# KEYBINDS
    # selecting pieces (assuming default pieces)
    keybinds = ["1", "2", "3", "4", "q", "w", "e", "r", "s", "d"]

    def press_button(event):
        piece_id = piece_symbols.index(event.char.upper())
        pressed(piece_id)

    for character in keybinds:
        main_window.bind(character, press_button)
        main_window.bind(character.upper(), press_button)

    # moving active pieces
    # num = 0, 1, 2, 3
    def try_move_direction(num):
        if global_vars[0]:
            move = puzzlegame.active_piece * 4 + num
            if Positions(puzzlegame.current_pos).move_ok(move):
                if puzzlegame.move_log == []:
                    undo_button.config(state=tk.NORMAL)
                if puzzlegame.solution_mode:
                    puzzlegame.solution_mode = False
                    solution_back.config(state=tk.DISABLED)
                    solution_fwd.config(state=tk.DISABLED)
                    statustexts[1].config(text="                              ")
                    solving_text1.config(text="  ")
                    solving_text2.config(text="  ")
                puzzlegame.make_move(move)
                place_pieces(pieces, empties)
                # statustexts[0].config(text="Piece " + piece_symbols[puzzlegame.active_piece] + " moves " + params.directions[num])
                statustexts[0].config(text=move_text(puzzlegame.active_piece, num))
                is_solved()
            else:
                # big piece cannot actually move down to complete the puzzle, but no need to point this out
                if not(move == 39 and puzzlegame.current_pos[-1] == (3, 1)):
                    # statustexts[0].config(text=piece_symbols[puzzlegame.active_piece] + " cannot move " + params.directions[num])
                    statustexts[0].config(text=no_move_text(puzzlegame.active_piece, num))

    def try_left(event):
        try_move_direction(0)

    def try_right(event):
        try_move_direction(1)

    def try_up(event):
        try_move_direction(2)

    def try_down(event):
        try_move_direction(3)

    # moving pieces while holding mouse button 1
    def try_to_move_piece(event):
        mb1_x_curr = event.x
        mb1_y_curr = event.y
        curr_piece = event.widget
        # solving_text1.config(text=str(mb1_x_curr) + ", " + str(mb1_y_curr))
        if curr_piece == pieces[puzzlegame.active_piece_for_dragging]:
            # solving_text2.config(text=str(active_piece_sortof))
            if mb1_x_curr < 1:
                deactivate()
                global_vars[0] = True
                puzzlegame.active_piece = puzzlegame.active_piece_for_dragging
                # try to go left
                try_move_direction(0)
                global_vars[0] = False
            elif mb1_y_curr < 1:
                deactivate()
                global_vars[0] = True
                puzzlegame.active_piece = puzzlegame.active_piece_for_dragging
                # try to go up
                try_move_direction(2)
                global_vars[0] = False
            elif mb1_x_curr > button_width and puzzlegame.active_piece_for_dragging in [0, 1, 2, 3, 4, 5, 6, 7]:
                deactivate()
                global_vars[0] = True
                puzzlegame.active_piece = puzzlegame.active_piece_for_dragging
                # try to go right
                try_move_direction(1)
                global_vars[0] = False
            elif mb1_x_curr > 2 * button_width and puzzlegame.active_piece_for_dragging in [8, 9]:
                deactivate()
                global_vars[0] = True
                puzzlegame.active_piece = puzzlegame.active_piece_for_dragging
                # try to go right
                try_move_direction(1)
                global_vars[0] = False
            elif mb1_y_curr > button_height and puzzlegame.active_piece_for_dragging in [0, 1, 2, 3, 8]:
                deactivate()
                global_vars[0] = True
                puzzlegame.active_piece = puzzlegame.active_piece_for_dragging
                # try to go down
                try_move_direction(3)
                global_vars[0] = False
            elif mb1_y_curr > 2 * button_height and puzzlegame.active_piece_for_dragging in [4, 5, 6, 7, 9]:
                deactivate()
                global_vars[0] = True
                puzzlegame.active_piece = puzzlegame.active_piece_for_dragging
                # try to go down
                try_move_direction(3)
                global_vars[0] = False
                

    def mb1_down(event):
        global_vars[1] = True
        # mb1_x_start = event.x
        # mb1_y_start = event.y
        curr_piece = event.widget
        if curr_piece in pieces:
            puzzlegame.active_piece_for_dragging = pieces.index(curr_piece)
            # print(curr_piece.geometry())

    def mb1_up(event):
        global_vars[1] = False

    main_window.bind("<Left>", try_left)
    main_window.bind("<Right>", try_right)
    main_window.bind("<Up>", try_up)
    main_window.bind("<Down>", try_down)

    main_window.bind("<Button-1>", mb1_down)
    main_window.bind("<ButtonRelease-1>", mb1_up)
    main_window.bind("<B1-Motion>", try_to_move_piece)


    main_window.mainloop()
