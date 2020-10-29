
def play_puzzlegame():
    import tkinter as tk
    from puzzlegame_setup import all_pos, piece_nums, piece_types, all_pieces, piece_num, empty_num
    from puzzlegame_setup import directions, piece_colors, piece_symbols
    from positions import Positions
    from puzzlegame import Puzzlegame
    import puzzlesolver as ps
    # import solution_opt_117

    # window with two frames on the left and one on the right
    main_window = tk.Tk()
    main_window.title("An interesting little puzzle to solve")
    # game_window = tk.LabelFrame(main_window, padx=1, pady=1)
    game_area = tk.LabelFrame(main_window, padx=1, pady=1)
    statusline = tk.LabelFrame(main_window, padx=1, pady=1)
    sideframe = tk.LabelFrame(main_window, padx=1, pady=1)
    # game_window.grid(row=0, column=0, padx=0, pady=0)
    game_area.grid(row=0, column=0, padx=1, pady=1)
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
            solution_text.config(text="You have solved \n the puzzle!")
        else:
            solution_text.config(text="      ")

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
        statustexts[0].config(text="Previous move undone")
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
            statustexts[0].config(text="    Piece " + piece_symbols[piece_id] + " is selected    ")
        else:
            # no pieces were active previously
            global_vars[0] = True
            puzzlegame.active_piece = piece_id
            pieces[piece_id].config(relief=tk.SUNKEN)
            statustexts[0].config(text="    Piece " + piece_symbols[piece_id] + " is selected    ")


    def try_move(empty_id):
        # do we need highlighted or active_piece here??
        empty_spot = puzzlegame.show_empties()[empty_id]
        current_pos = Positions(0, puzzlegame.current_pos)
        if global_vars[0]:
            move = current_pos.move_from_coord(puzzlegame.active_piece, empty_spot)
            if move == -1:
                statustexts[0].config(text=piece_symbols[puzzlegame.active_piece] + " cannot move to " + str(empty_spot))
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
                statustexts[0].config(text="Piece " + piece_symbols[puzzlegame.active_piece] + " moves " + directions[move%4])
                place_pieces(pieces, empties)
        is_solved()


    def solution_from_start():
        if not(ps.does_soln_117_file_exist()):
            # solution file was not found
            solving_text1.config(text="Solution file not found")
            show_generation_popup2()
            return
        restart()
        puzzlegame.show_solution()
        solution_fwd.config(state=tk.NORMAL)
        statustexts[1].config(text=str(1) + " / " + str(len(puzzlegame.pos_log_opt)))
        solving_text2.config(text="Use the '<<' \n and '>>' buttons \n to cycle through \n the solution")


    def solution_from_pos():
        if not(ps.does_all_pos_file_exist()):
            # file all_pos_13011.py does not exist
            solving_text1.config(text="Reference file not found")
            show_generation_popup()
            return
        puzzlegame.find_solution()
        # index_opt = len(puzzlegame.move_log)
        if puzzlegame.index_opt > 0:
            solution_back.config(state=tk.NORMAL)
        if puzzlegame.index_opt < len(puzzlegame.pos_log_opt) - 1:
            solution_fwd.config(state=tk.NORMAL)
        solving_text1.config(text="Solution found!")
        statustexts[1].config(text=str(puzzlegame.index_opt + 1) + " / " + str(len(puzzlegame.pos_log_opt)))
        solving_text2.config(text="Use the '<<' \n and '>>' buttons \n to cycle through \n the solution")


    def soln_back():
        if global_vars[0]:
            deactivate()
        statustexts[0].config(text="Going back")
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
        statustexts[0].config(text="Piece " + piece_symbols[move//4] + " moves " + directions[move%4])
        solution_back.config(state=tk.NORMAL)
        place_pieces(pieces, empties)
        if puzzlegame.index_opt == len(puzzlegame.move_log_opt):
            solution_fwd.config(state=tk.DISABLED)
        statustexts[1].config(text=str(puzzlegame.index_opt + 1) + " / " + str(len(puzzlegame.pos_log_opt)))
        is_solved()

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
        if global_vars[0]:
            move = puzzlegame.active_piece * 4 + num
            if Positions(0, puzzlegame.current_pos).move_ok(move):
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
                statustexts[0].config(text="Piece " + piece_symbols[puzzlegame.active_piece] + " moves " + directions[num])
                is_solved()
            else:
                statustexts[0].config(text=piece_symbols[puzzlegame.active_piece] + " cannot move " + directions[num])

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
