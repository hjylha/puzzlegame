import tkinter as tk
from puzzlegame_setup import all_pos, piece_nums, piece_types, all_pieces, piece_num, empty_num, initial_positions
from puzzlegame_setup import directions, piece_colors, piece_symbols
from positions import Positions
import move as mv
import puzzlesolver as ps
# import solution_opt_117

# window with two frames on the left and one on the right
main_window = tk.Tk()
main_window.title("An interesting little puzzle to solve")
game_area = tk.LabelFrame(main_window, padx=1, pady=1)
statusline = tk.LabelFrame(main_window, padx=1, pady=1)
sideframe = tk.LabelFrame(main_window, padx=1, pady=1)
game_area.grid(row=0, column=0, padx=1, pady=1)
statusline.grid(row=1, column=0, sticky=tk.W + tk.E)
sideframe.grid(row=0, column=1, rowspan=2, sticky=tk.N+tk.S)

# active global variables
active_piece = -1
highlighted = False
current_pos = Positions(0, initial_positions)
pos_log = [Positions(0, initial_positions)]
move_log = []

# solution stuff
index_opt = 0
solution_mode = False
pos_log_opt = []
move_log_opt = []


def place_pieces(buttons, ebuttons, pos):
    k = 0
    for j in range(len(piece_nums)):
        for i in range(piece_nums[j]):
            buttons[k].grid(row=pos.pieces[k][0], column=pos.pieces[k][1],
                           rowspan=piece_types[j][0], columnspan=piece_types[j][1], sticky=tk.W + tk.E + tk.N + tk.S)
            k += 1
    for i in range(len(pos.set_empties())):
        ebuttons[i].grid(row=pos.set_empties()[i][0], column=pos.set_empties()[i][1])

def is_solved(pos):
    if pos.pieces[-1] == [3,1]:
        solution_text.config(text="You have solved \n the puzzle!")

def show_generation_popup():
    from tkinter import messagebox
    explanation = "The file all_pos_13011.py was not found. It is needed for finding optimal solutions fast. Do you want to generate this file now? The process may take a couple of hours."
    start_generating = messagebox.askyesno("Generating positions", explanation)
    if start_generating:
        # final check about whether the files exist already
        if not(ps.does_all_pos_file_exist()):
            solving_text1.config(text="Generating files, please wait")
            print("Generating files...")
            ps.generate_pos_files()
            solving_text1.config(text="File generated")

def show_generation_popup2():
    from tkinter import messagebox
    explanation = "The file containing optimal solution was not found. Do you want to calculate the optimal solution? The process may take a couple of hours."
    start_generating = messagebox.askyesno("Generating optimal solution", explanation)
    if start_generating:
        if not(ps.does_soln_117_file_exist()):
            if ps.does_all_pos_file_exist():
                solving_text1.config(text="Finding solution, please wait")
                print("Finding solution from Big Data")
                ps.generate_soln_from_all_pos()
                solving_text1.config(text="Solution found")
                solution_from_start()
            else:
                solving_text1.config(text="Finding solution, please wait")
                print("Solving...")
                ps.generate_soln()
                solving_text1.config(text="Solution found")
                solution_from_start()

def restart():
    global active_piece, highlighted, current_pos, pos_log, move_log, solution_mode
    solution_mode = False
    if highlighted:
        highlighted = False
        pieces[active_piece].config(relief=tk.RAISED)
    active_piece = -1
    current_pos = Positions(0, initial_positions)
    pos_log = [Positions(0, initial_positions)]
    move_log = []
    place_pieces(pieces, empties, current_pos)
    statustexts[0].config(text="                              ")
    statustexts[1].config(text="                              ")
    solving_text1.config(text=" ")
    solving_text2.config(text=" ")
    solution_text.config(text=" ")
    undo_button.config(state=tk.DISABLED)


def undo():
    # what if we are in solution mode??
    global active_piece, highlighted, current_pos, pos_log, move_log, index_opt
    if highlighted:
        highlighted = False
        pieces[active_piece].config(relief=tk.RAISED)
    active_piece = -1
    pos_log.pop()
    move_log.pop()
    current_pos = pos_log[-1]
    place_pieces(pieces, empties, current_pos)
    statustexts[0].config(text="Previous move undone")
    is_solved(current_pos)
    if solution_mode:
        index_opt -= 1
        statustexts[1].config(text=str(index_opt + 1) + " / " + str(len(pos_log_opt)))
        if index_opt == 0:
            solution_back.config(state=tk.DISABLED)
    if move_log == []:
        undo_button.config(state=tk.DISABLED)


def pressed(piece_id):
    global active_piece, highlighted
    # is a piece highlighted already, and is it the one we clicked??
    if highlighted and active_piece == piece_id:
        # if we clicked the active piece, it deactivates
        highlighted = False
        active_piece = -1
        pieces[piece_id].config(relief=tk.RAISED)
        statustexts[0].config(text="                              ")
    elif highlighted:
        # switch active piece
        pieces[active_piece].config(relief=tk.RAISED)
        active_piece = piece_id
        pieces[piece_id].config(relief=tk.SUNKEN)
        statustexts[0].config(text="    Piece " + piece_symbols[piece_id] + " is selected    ")
    else:
        # no pieces were active previously
        highlighted = True
        active_piece = piece_id
        pieces[piece_id].config(relief=tk.SUNKEN)
        statustexts[0].config(text="    Piece " + piece_symbols[piece_id] + " is selected    ")


def try_move(empty_id):
    # do we need highlighted or active_piece here??
    global current_pos, pos_log, move_log, solution_mode
    empty_spot = current_pos.set_empties()[empty_id]
    if highlighted:
        move = mv.move_from_coord(active_piece, empty_spot, current_pos)
        if move == -1:
            statustexts[0].config(text=piece_symbols[active_piece] + " cannot move to " + str(empty_spot))
        else:
            if move_log == []:
                undo_button.config(state=tk.NORMAL)
            if solution_mode:
                solution_mode = False
                solution_back.config(state=tk.DISABLED)
                solution_fwd.config(state=tk.DISABLED)
                statustexts[1].config(text="                              ")
                solving_text1.config(text="  ")
                solving_text2.config(text="  ")
            pos_log.append(mv.make_move(move, current_pos))
            move_log.append(move)
            current_pos = mv.make_move(move, current_pos)
            statustexts[0].config(text="Piece " + piece_symbols[active_piece] + " moves " + directions[move%4])
            place_pieces(pieces, empties, current_pos)
    is_solved(current_pos)


def solution_from_start():
    global highlighted, active_piece, current_pos, pos_log, move_log, solution_mode
    global pos_log_opt, move_log_opt, index_opt
    if not(ps.does_soln_117_file_exist()):
        # solution file was not found
        solving_text1.config(text="Solution file not found")
        show_generation_popup2()
        return
    import solution_opt_117
    restart()
    solution_mode = True
    index_opt = 0
    pos_log_opt = solution_opt_117.pos_list
    move_log_opt = mv.move_list_from_pos_list(pos_log_opt)
    solution_fwd.config(state=tk.NORMAL)
    statustexts[1].config(text=str(index_opt + 1) + " / " + str(len(pos_log_opt)))
    solving_text2.config(text="Use the '<<' \n and '>>' buttons \n to cycle through \n the solution")


def solution_from_pos():
    global highlighted, active_piece, current_pos, pos_log, move_log, solution_mode
    global pos_log_opt, move_log_opt, index_opt
    if not(ps.does_all_pos_file_exist()):
        # file all_pos_13011.py does not exist
        solving_text1.config(text="Reference file not found")
        show_generation_popup()
        return
    # solver_output = ps.solve_opt_w_fd(current_pos)
    # pos_list = ps.solve_opt_w_fd(current_pos)[0]
    # pos_list = ps.solve_w_ref_1(current_pos, soln_ref)
    pos_list = ps.solve_opt_w_fd(current_pos)[0]
    solution_mode = True
    solving_text1.config(text="Searching...")
    index_opt = len(pos_log) - 1
    pos_log_opt = mv.combine_lists(pos_log, pos_list)
    move_log_opt = mv.move_list_from_pos_list(pos_log_opt)
    if index_opt > 0:
        solution_back.config(state=tk.NORMAL)
    if index_opt < len(pos_log_opt) - 1:
        solution_fwd.config(state=tk.NORMAL)
    solving_text1.config(text="Solution found!")
    statustexts[1].config(text=str(index_opt + 1) + " / " + str(len(pos_log_opt)))
    solving_text2.config(text="Use the '<<' \n and '>>' buttons \n to cycle through \n the solution")


def soln_back():
    global highlighted, active_piece, current_pos, pos_log, move_log, index_opt
    if highlighted:
        highlighted = False
        pieces[active_piece].config(relief=tk.RAISED)
        active_piece = -1
    pos_log.pop()
    move_log.pop()
    statustexts[0].config(text="Going back")
    index_opt -= 1
    current_pos = pos_log_opt[index_opt]
    place_pieces(pieces, empties, current_pos)
    if move_log == []:
        undo_button.config(state=tk.DISABLED)
    if index_opt < len(move_log_opt):
        solution_fwd.config(state=tk.NORMAL)
    if index_opt == 0:
        solution_back.config(state=tk.DISABLED)
    statustexts[1].config(text=str(index_opt + 1) + " / " + str(len(pos_log_opt)))

def soln_fwd():
    global highlighted, active_piece, current_pos, pos_log, move_log, index_opt
    if highlighted:
        highlighted = False
        pieces[active_piece].config(relief=tk.RAISED)
        active_piece = -1
    if move_log == []:
        undo_button.config(state=tk.NORMAL)
    move = move_log_opt[index_opt]
    move_log.append(move)
    statustexts[0].config(text="Piece " + piece_symbols[move//4] + " moves " + directions[move%4])
    current_pos = pos_log_opt[index_opt+1]
    pos_log.append(current_pos)
    solution_back.config(state=tk.NORMAL)
    place_pieces(pieces, empties, current_pos)
    index_opt += 1
    if index_opt == len(move_log_opt):
        solution_fwd.config(state=tk.DISABLED)
    statustexts[1].config(text=str(index_opt + 1) + " / " + str(len(pos_log_opt)))
    is_solved(current_pos)

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

pieces = []
k = 0
for j in range(len(piece_nums)):
    for i in range(piece_nums[j]):
        piece = tk.Button(game_area, text=piece_symbols[k], bg=piece_colors[j], width=b_d(k)[0],
                          height=b_d(k)[1], command=lambda k=k: pressed(k))
        pieces.append(piece)
        pieces[k].grid(row=current_pos.pieces[k][0], column=current_pos.pieces[k][1],
                       rowspan=piece_types[j][0], columnspan=piece_types[j][1], sticky=tk.W+tk.E+tk.N+tk.S)
        k += 1

# where the pieces might move
empties = []
for i in range(len(current_pos.set_empties())):
    empty_square = tk.Button(game_area, text="", width=12, height=6, command=lambda i=i: try_move(i))
    empties.append(empty_square)
    empties[i].grid(row=current_pos.set_empties()[i][0], column=current_pos.set_empties()[i][1])


################## status line things
# 2 status texts for some reason
statustexts = []
for i in range(2):
    statustext = tk.Label(statusline, text="                              ", width=30)
    statustexts.append(statustext)
    statustexts[i].grid(row=i, column=1, pady=2)

# buttons to navigate solutions
solution_back = tk.Button(statusline, text="<<", state=tk.DISABLED, command=soln_back)
solution_fwd = tk.Button(statusline, text=">>", state=tk.DISABLED, command=soln_fwd)
solution_back.grid(row=0, column=0, rowspan=3, pady=10, sticky=tk.E)
solution_fwd.grid(row=0, column=2, rowspan=3, pady=10, sticky=tk.E)


# sideframe buttons and stuff
sidebuttons = []
some_space_at_the_top = tk.Label(sideframe, text=" \n \n \n")
sidebuttons.append(some_space_at_the_top)
restart_button = tk.Button(sideframe, text="Restart", width=20, command=restart)
sidebuttons.append(restart_button)
description = tk.Label(sideframe, text="Move the red piece 'D'\n out of the game area.\n " +
                                       "'D' can only exit the area\n through the center \n of the lower border.")
sidebuttons.append(description)
undo_button = tk.Button(sideframe, text="Undo last move", width=20, state=tk.DISABLED, command=undo)
sidebuttons.append(undo_button)
show_soln_button = tk.Button(sideframe, text="Show a solution \n from the start", width=20, command=solution_from_start)
sidebuttons.append(show_soln_button)
solve_button = tk.Button(sideframe, text="Find a solution", width=20, command=solution_from_pos)
sidebuttons.append(solve_button)
solving_text1 = tk.Label(sideframe, text="", width=20)
sidebuttons.append(solving_text1)
solving_text2 = tk.Label(sideframe, text="", width=20)
sidebuttons.append(solving_text2)
solution_text = tk.Label(sideframe, text="")
sidebuttons.append(solution_text)

# putting the buttons onto the sideframe
for i in range(len(sidebuttons)):
    sidebuttons[i].grid(row=i, column=0, padx=1, pady=5)

# check file all_pos_13011.py
if not(ps.does_all_pos_file_exist()):
    show_generation_popup()

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
    global current_pos, pos_log, move_log, solution_mode
    if highlighted:
        move = active_piece * 4 + num
        if mv.move_ok(move, current_pos):
            if move_log == []:
                undo_button.config(state=tk.NORMAL)
            if solution_mode:
                solution_mode = False
                solution_back.config(state=tk.DISABLED)
                solution_fwd.config(state=tk.DISABLED)
                statustexts[1].config(text="                              ")
                solving_text1.config(text="  ")
                solving_text2.config(text="  ")
            current_pos = mv.make_move(move, current_pos)
            pos_log.append(current_pos)
            move_log.append(move)
            place_pieces(pieces, empties, current_pos)
            statustexts[0].config(text="Piece " + piece_symbols[active_piece] + " moves " + directions[num])
            is_solved(current_pos)
        else:
            statustexts[0].config(text=piece_symbols[active_piece] + " cannot move " + directions[num])


def try_left(event):
    try_move_direction(0)


def try_right(event):
    try_move_direction(1)


def try_up(event):
    try_move_direction(2)


def try_down(event):
    try_move_direction(3)


main_window.bind("<Left>", try_left)
main_window.bind("<Right>", try_right)
main_window.bind("<Up>", try_up)
main_window.bind("<Down>", try_down)


main_window.mainloop()
