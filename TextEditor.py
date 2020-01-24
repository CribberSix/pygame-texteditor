import pygame,sys
import math

class TextEditorClass:

    def __init__(self, offset_X, offset_Y, codingAreaWidth, codingAreaHeight, screen, lineNumbers=True):

        self.screen = screen
        self.offset_X = offset_X
        self.offset_Y = offset_Y
        self.codingAreaWidth = codingAreaWidth
        self.codingAreaHeight = codingAreaHeight

        self.letter_size_Y = 15
        self.Courier_Text_15 = pygame.font.Font("TextEditor_Elements/Courier.ttf", self.letter_size_Y)
        self.trennzeichen_image = pygame.image.load("TextEditor_Elements/Trennzeichen.png").convert_alpha()

        # LINES AND CURSOR
        self.Trenn_counter = 0
        self.MaxLinecounter = 0
        self.line_String_array = []
        self.line_Text_array = []
        self.lineHeight = 18
        self.showableLines = int(math.floor(codingAreaHeight / self.lineHeight))
        self.maxLines = int(math.floor(codingAreaHeight / self.lineHeight))
        self.showStartLine = 0  # first line (shown at the top of the editor) <- must be zero during init!
        self.line_gap = 3 + self.letter_size_Y

        for i in range(self.maxLines):  # from 0 to maxLines:
            self.line_String_array.append("")  # Add a line
            self.line_Text_array.append(self.Courier_Text_15.render("", 1, (160, 160, 160)))

        # SCROLLBAR
        self.scrollDownButtonImg = pygame.image.load("TextEditor_Elements/Scroll_Down.png").convert()
        self.scrollDownButtonImg_Deactivated = pygame.image.load("TextEditor_Elements/Scroll_Down_deactivated.png").convert()
        self.scrollUpButtonImg = pygame.image.load("TextEditor_Elements/Scroll_up.png").convert()
        self.scrollUpButtonImg_Deactivated = pygame.image.load("TextEditor_Elements/Scroll_Up_deactivated.png").convert()
        self.scrollBarImg = pygame.image.load("TextEditor_Elements/Scroll_Bar.png").convert()
        self.scrollBarWidth = 20
        self.scrollBarButtonHeight = 17
        self.conclusionBarHeight =18
        self.scrollBarHeight = (self.codingAreaHeight-self.scrollBarButtonHeight*2 -2) * self.showableLines/len(self.line_String_array)

        # LINE NUMBERS
        self.displayLineNumbers = lineNumbers
        if lineNumbers:
            self.lineNumberWidth = 27  # line number background width and also offset for text!
        else:
            self.lineNumberWidth = 0
        self.letter_size_X = 9
        self.chosen_LineIndex = 0
        self.chosen_LetterIndex = 0
        self.line_numbers_Y = self.offset_Y

        # TEXT COORDINATES
        self.yline_start = offset_Y + 3
        self.yline = offset_Y
        self.xline_start_offset = 28
        if self.displayLineNumbers:
            self.xline_start = self.xline_start_offset+self.offset_X
            self.xline = self.xline_start_offset + self.offset_X
        else:
            self.xline_start = self.offset_X
            self.xline = self.offset_X

        # CURSOR
        self.cursor_Y = self.yline_start - 3
        self.cursor_X = self.xline_start
        self.dragged_active = False

        # click down
        self.drag_cursor_X_start = 0
        self.drag_cursor_Y_start = 0
        self.drag_chosen_LineIndex_start = 0
        self.drag_chosen_LetterIndex_start = 0
        self.last_clickdown_cycle = 0

        # click up
        self.drag_cursor_X_end = 0
        self.drag_cursor_Y_end = 0
        self.drag_chosen_LineIndex_end = 0
        self.drag_chosen_LetterIndex_end = 0
        self.last_clickup_cycle = 0

        # Colors etc
        self.codingBackgroundColor = (40, 44, 52) # (40, 44, 52)
        self.codingScrollBarBackgroundColor = (40, 44, 52)
        self.textColor = (171, 178, 191)
        self.lineNumberColor = (73, 81, 97)
        self.lineNumberBackgroundColor = (40, 44, 52)  # (0, 0, 0) # 0, 51, 102

        self.deleteCounter = 0

        # Performance enhancing variables
        self.setUp = True
        self.rerenderLineNumbers = True
        self.click_hold = False

        self.cycleCounter = 0

    def display_CodeEditor(self): # needs to be called within a while loop to be able to catch key/mouse input and update visuals throughout use.

            self.cycleCounter = self.cycleCounter + 1
            # first iteration
            if self.setUp:
                pygame.draw.rect(self.screen, self.codingBackgroundColor, (self.offset_X, self.offset_Y, self.codingAreaWidth, self.codingAreaHeight))  # paint entire area to avoid pixel error beneath line numbers
                self.screen.blit(self.scrollUpButtonImg, (self.offset_X+self.codingAreaWidth - self.scrollBarWidth, self.offset_Y))  # Scroll Up Image
                self.screen.blit(self.scrollDownButtonImg, (self.offset_X+self.codingAreaWidth - self.scrollBarWidth, self.offset_Y + self.codingAreaHeight - self.scrollBarButtonHeight))  # Scroll DownImage
                self.setUp = False

            # _________BLITTING_OBJECTS__________ #
            # Background
            pygame.draw.rect(self.screen, self.codingBackgroundColor, (self.offset_X+self.lineNumberWidth, self.offset_Y , self.codingAreaWidth-self.scrollBarWidth-self.lineNumberWidth , self.codingAreaHeight)) # Coding Background Coloring

            # Line-Numbers
            if self.displayLineNumbers:
                if self.rerenderLineNumbers:
                    self.rerenderLineNumbers = False
                    pygame.draw.rect(self.screen, self.codingBackgroundColor, (self.offset_X, self.offset_Y , self.lineNumberWidth , self.codingAreaHeight-18))

                    if self.showableLines+self.showStartLine < self.maxLines:
                        renderLineNumber = self.showableLines+self.showStartLine
                    else:
                        renderLineNumber = self.maxLines

                    line_numbers_Y = self.offset_Y
                    for x in range(self.showStartLine, renderLineNumber):

                        # Background for line numbers
                        pygame.draw.rect(self.screen, self.lineNumberBackgroundColor, (self.offset_X, line_numbers_Y, self.lineNumberWidth, 17))

                        # Blitting numbers
                        if x < 10:  # 1-digit numbers
                            text = self.Courier_Text_15.render(" " + str(x), 1, self.lineNumberColor)
                        else:  # 2-digit numbers
                            text = self.Courier_Text_15.render(str(x), 1, self.lineNumberColor)
                        self.screen.blit(text, (self.offset_X + 5, line_numbers_Y + 3))  # Coordinates of line numbers - corrected for visual effect (moved into the 'center' of the background block for the number.)

                        # setup for the next line
                        line_numbers_Y += self.line_gap

            # _________MOUSE_INPUT__________#
            # Mouse clicks
            mouse_x, mouse_y = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if click[0] and not self.click_hold:  # left click and is not already being held
                self.last_clickdown_cycle = self.cycleCounter
                self.click_hold = True  # in order not to have the mouse move around after a click, we need to disable this function until we RELEASE it.
                # Check if I clicked inside the text editors specified area
                if (mouse_x > self.offset_X + self.lineNumberWidth) and (mouse_x < (self.offset_X + self.codingAreaWidth - self.scrollBarWidth)) and (mouse_y > self.offset_Y) and  (mouse_y < (self.codingAreaHeight + self.offset_Y-self.conclusionBarHeight)):

                    # Check if I clicked into the existing Lines
                    if (mouse_y < self.offset_Y+ (self.lineHeight * self.maxLines)):  # clicked INTO the existing lines.
                        # Choose Line (y-axis)
                        self.drag_chosen_LineIndex_start = int(((mouse_y - self.offset_Y) / self.line_gap) + (self.showStartLine))
                        self.drag_cursor_Y_start = self.offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap) - (self.showStartLine * self.lineHeight)

                        # Choose Letter (x-axis)
                        prep_LetterIndex = int((mouse_x - self.offset_X - self.xline_start_offset) / self.letter_size_X)  # cast as integer as we use it as index

                        # check if clicked behind the end of a line
                        if len(self.line_String_array[self.drag_chosen_LineIndex_start]) < prep_LetterIndex:  # end of line
                            self.drag_chosen_LetterIndex_start = len(self.line_String_array[self.drag_chosen_LineIndex_start])
                            self.drag_cursor_X_start = self.xline_start + (len(self.line_String_array[self.drag_chosen_LineIndex_start]) * self.letter_size_X)
                        else:  # within existing line
                            self.drag_chosen_LetterIndex_start = int((mouse_x - self.offset_X - self.xline_start_offset) / self.letter_size_X)  # cast as integer as we use it as index
                            self.drag_cursor_X_start = self.offset_X + self.xline_start_offset + (self.drag_chosen_LetterIndex_start * self.letter_size_X)

                    else:  # clicked beneath the existing lines
                        #  go to the end of the last line.
                        self.drag_chosen_LineIndex_start = self.maxLines-1
                        self.drag_cursor_Y_start = self.offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap)
                        # Last letter of the line
                        self.drag_chosen_LetterIndex_start = len(self.line_String_array[self.drag_chosen_LineIndex_start])
                        self.drag_cursor_X_start = self.offset_X + self.xline_start_offset + (self.drag_chosen_LetterIndex_start * self.letter_size_X)

            # _________KEYBOARD_INPUT__________ #
            self.deleteCounter += 1
            self.deleteCounter = self.deleteCounter % 2  # TODO: find a good option here. If FPS_max = 30; then we can delete 10 characters each second

            # Detect tapping/holding of the "DELETE" and "BACKSPACE" key
            Xkeys = pygame.key.get_pressed()
            if Xkeys[pygame.K_DELETE] and self.deleteCounter == 0:
                if self.chosen_LetterIndex == len(self.line_String_array[self.chosen_LineIndex]): # End of a line  (choose next line)
                    if self.chosen_LineIndex != (self.maxLines-1): # NOT in the last line &(prev) at the end of the line, I cannot delete anything
                        self.line_String_array[self.chosen_LineIndex] += self.line_String_array[self.chosen_LineIndex+1] # add the contents of the next line to the current one
                        self.line_String_array.pop(self.chosen_LineIndex+1) # delete the Strings-line in order to move the following lines one upwards
                        self.maxLines -=1 # Keep the variable aligned
                        self.line_Text_array.pop(self.chosen_LineIndex+1) # delete the Text-line in order to move the following lines one upwards
                        self.rerenderLineNumbers = True
                        if self.showStartLine > 0:
                            if (self.showStartLine + self.showableLines) > self.maxLines: # The scrollbar is all the way down. We delete a line, so we have to "pull everything one visual line down"
                                self.showStartLine -= 1 #  "pull one visual line down" (array-based)
                                self.cursor_Y += self.line_gap # move the curser one down.  (visually based)

                elif self.chosen_LetterIndex < (len(self.line_String_array[self.chosen_LineIndex])): # mid-line (Cursor stays on point)
                    self.line_String_array[self.chosen_LineIndex] =  self.line_String_array[self.chosen_LineIndex][:(self.chosen_LetterIndex)] + self.line_String_array[self.chosen_LineIndex][(self.chosen_LetterIndex+1):]

            if Xkeys[pygame.K_BACKSPACE] and self.deleteCounter == 0:
                self.chosen_LetterIndex = int(self.chosen_LetterIndex)
                if self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0: # One Line back if at X-Position 0 and not in the first Line
                    # Line & Letter Handling
                    self.chosen_LineIndex -= 1
                    self.cursor_Y -= self.line_gap
                    self.cursor_X = self.xline_start + (len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)
                    self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])
                    self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex] + self.line_String_array[self.chosen_LineIndex+1] # take the rest of the line into the previous line
                    self.line_String_array.pop(self.chosen_LineIndex+1) # delete the Strings-line in order to move the following lines one upwards
                    self.maxLines -= 1  # Keep the variable aligned
                    self.line_Text_array.pop(self.chosen_LineIndex+1) # delete the Text-line in order to move the following lines one upwards
                    self.rerenderLineNumbers = True
                    # Scroll Handling
                    if self.showStartLine > 0:
                        if (self.showStartLine + self.showableLines) > self.maxLines:# The scrollbar is all the way down. We delete a line, so we have to "pull everything one visual line down"
                            self.showStartLine -= 1#  "pull one visual line down" (array-based)
                            self.cursor_Y += self.line_gap# move the curser one down.  (visually based)
                    if self.chosen_LineIndex == (self.showStartLine-1): # Im in the first rendered line (but NOT  the "0" line) and at the beginning of the line. => move one upward, change showstartLine & cursor placement.
                        self.showStartLine -= 1
                        self.cursor_Y += self.line_gap

                elif self.chosen_LetterIndex > 0: # Else: mid-lineDelete a letter (but only if there are letters left) (Cursor moves)
                        self.line_String_array[self.chosen_LineIndex] =  self.line_String_array[self.chosen_LineIndex][:(self.chosen_LetterIndex-1)] + self.line_String_array[self.chosen_LineIndex][(self.chosen_LetterIndex):]
                        self.cursor_X -= self.letter_size_X
                        self.chosen_LetterIndex -= 1

            # ALL OTHER KEYS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # Fixes the bug that pygame takes up space in the RAM when game is just closed by sys.exit()
                    sys.exit()

                # ___ MOUSE SCROLLING ___ #
                # Mouse scrolling wheel should only work if it is within the coding area.
                if event.type == pygame.MOUSEBUTTONDOWN and mouse_x > self.offset_X and mouse_x < self.offset_X + self.codingAreaWidth and mouse_y > self.offset_Y and mouse_y < self.offset_Y + self.codingAreaHeight:
                    if event.button == 4 and self.showStartLine > 0:
                        self.scrollUp()
                    elif event.button == 5 and self.showStartLine + self.showableLines < self.maxLines:
                        self.scrollDown()

                # ___ MOUSE DRAGGING ___ #
                # MOUSEBUTTONDOWN is handled previously in the mouse input.
                if event.type == pygame.MOUSEBUTTONUP:
                    self.last_clickup_cycle = self.cycleCounter
                    self.click_hold = False
                    # check if I clicked into the text area:
                    if (mouse_x > self.offset_X + self.lineNumberWidth) and (
                            mouse_x < (self.offset_X + self.codingAreaWidth - self.scrollBarWidth)) and (mouse_y > self.offset_Y) and (
                            mouse_y < (self.codingAreaHeight + self.offset_Y - self.conclusionBarHeight)):

                        # Check if I clicked into the existing Lines
                        if (mouse_y < self.offset_Y + (self.lineHeight * self.maxLines)):  # clicked INTO the existing lines.
                            # Choose Line (y-axis)
                            self.drag_chosen_LineIndex_end = int(((mouse_y - self.offset_Y) / self.line_gap) + (self.showStartLine))
                            self.drag_cursor_Y_end = self.offset_Y + (self.drag_chosen_LineIndex_end * self.line_gap) - (self.showStartLine * self.lineHeight)
                            # Choose Letter (x-axis)
                            prep_LetterIndex_drag = int((mouse_x - self.offset_X - self.xline_start_offset) / self.letter_size_X)  # cast as integer as we use it as index

                            # check if clicked behind the end of a line
                            if len(self.line_String_array[self.drag_chosen_LineIndex_end]) < prep_LetterIndex_drag:  # end of line
                                self.drag_chosen_LetterIndex_end = len(self.line_String_array[self.drag_chosen_LineIndex_end])
                                self.drag_cursor_X_end = self.xline_start + (len(self.line_String_array[self.drag_chosen_LineIndex_end]) * self.letter_size_X)
                            else:  # within existing line
                                self.drag_chosen_LetterIndex_end = int((mouse_x - self.offset_X - self.xline_start_offset) / self.letter_size_X)  # cast as integer as we use it as index
                                self.drag_cursor_X_end = self.offset_X + self.xline_start_offset + (self.drag_chosen_LetterIndex_end * self.letter_size_X)

                        else:  # clicked beneath the existing lines
                            #  go to the end of the last line.
                            self.chosen_LineIndex = self.maxLines - 1
                            self.drag_cursor_Y_end = self.offset_Y + (self.drag_chosen_LineIndex_end * self.line_gap)
                            # Last letter of the line
                            self.drag_chosen_LetterIndex_end = len(self.line_String_array[self.drag_chosen_LineIndex_end])
                            self.drag_cursor_X_end = self.offset_X + self.xline_start_offset + (
                                        self.drag_chosen_LetterIndex_end * self.letter_size_X)

                # _______ CHECK FOR MOUSE DRAG AND HANDLE CLICK _______ #
                if (self.last_clickup_cycle - self.last_clickdown_cycle) >= 0: # clicked the mouse lately and has not been handled yet.
                    # we dont have to check how long the mouse was held, to differentiate between click and drag
                    # but if the down click is on the same letter and line as the upclick!!!
                    if self.drag_chosen_LineIndex_end == self.drag_chosen_LineIndex_start and self.drag_chosen_LetterIndex_end == self.drag_chosen_LetterIndex_start:
                        self.chosen_LineIndex = self.drag_chosen_LineIndex_end
                        self.chosen_LetterIndex = self.drag_chosen_LetterIndex_end
                        self.cursor_X = self.drag_cursor_X_end
                        self.cursor_Y = self.drag_cursor_Y_end
                    else:
                        self.dragged_active = True
                        self.cursor_X = self.drag_cursor_X_end
                        self.cursor_Y = self.drag_cursor_Y_end


                    # reset after upclick => difference is "-1" and hence smaller than 0. Wait for next clickup.
                    self.last_clickup_cycle = -1
                    self.last_clickdown_cycle = 0

                if event.type == pygame.KEYDOWN and self.dragged_active:
                    # TODO: if we type a letter / return / backspace / del we delete the marked area.
                    # TODO: if we type an arrow we jump in front of or at the backend of the area.
                    print("Something with mouse dragging should be happening here.")

                # ___ KEYS ___ #
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)  # Returns string id of pressed key.
                    if len(key) == 1:  # This covers all letters and numbers not on numpad.
                        self.chosen_LetterIndex = int(self.chosen_LetterIndex)
                        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][:self.chosen_LetterIndex] + event.unicode + self.line_String_array[self.chosen_LineIndex][self.chosen_LetterIndex:]
                        self.cursor_X += self.letter_size_X
                        self.chosen_LetterIndex += 1

                    # ___TABULATOR
                    elif key == "tab":
                        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][:self.chosen_LetterIndex] + "    " + self.line_String_array[self.chosen_LineIndex][self.chosen_LetterIndex:]
                        self.cursor_X += self.letter_size_X * 4
                        self.chosen_LetterIndex += 4

                    # ___SPACEBAR
                    elif key == "space":
                        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][:self.chosen_LetterIndex] + " " + self.line_String_array[self.chosen_LineIndex][self.chosen_LetterIndex:]
                        self.cursor_X += self.letter_size_X
                        self.chosen_LetterIndex += 1

                    # ___ARROW_UP
                    elif event.key == pygame.K_UP and self.chosen_LineIndex > 0:
                        self.chosen_LineIndex -= 1
                        self.cursor_Y -= self.line_gap
                        if len(self.line_String_array[self.chosen_LineIndex]) < self.chosen_LetterIndex: # have to reset (toward the left)
                            self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])
                            self.cursor_X = (len(self.line_String_array[self.chosen_LineIndex])) * self.letter_size_X + self.xline_start
                        if self.chosen_LineIndex < self.showStartLine:
                            self.showStartLine -= 1
                            self.cursor_Y += self.line_gap
                            self.rerenderLineNumbers = True

                    # ___ARROW_DOWN
                    elif event.key == pygame.K_DOWN:
                        if (self.chosen_LineIndex < self.maxLines-1): # Not in the last line, i can move downward.
                            self.chosen_LineIndex += 1
                            self.cursor_Y += self.line_gap
                            if len(self.line_String_array[self.chosen_LineIndex]) < self.chosen_LetterIndex:
                                self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])
                                self.cursor_X = ((len(self.line_String_array[self.chosen_LineIndex])) * self.letter_size_X) + self.xline_start
                            if self.chosen_LineIndex > (self.showStartLine+self.showableLines-1): # I move downward outside of the rendered lines => "pull the lines up"
                                self.showStartLine += 1
                                self.cursor_Y -= self.line_gap
                                self.rerenderLineNumbers = True
                        if (self.chosen_LineIndex == self.maxLines-1):# im in the last line and want to jump to its end.
                            self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex]) # end of the line
                            self.cursor_X = self.xline_start + (len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)

                    # ___ARROW_RIGHT
                    elif event.key == pygame.K_RIGHT:
                        if self.chosen_LetterIndex < (len(self.line_String_array[self.chosen_LineIndex])): # mid-line
                            self.chosen_LetterIndex += 1
                            self.cursor_X += self.letter_size_X
                        elif self.chosen_LetterIndex == len(self.line_String_array[self.chosen_LineIndex]) and not(self.chosen_LineIndex == (self.maxLines-1)): # end of line => move over into the start of the next lint
                            self.chosen_LetterIndex = 0
                            self.chosen_LineIndex +=1
                            self.cursor_X = self.xline_start
                            self.cursor_Y += self.line_gap
                            if self.chosen_LineIndex > (self.showStartLine+self.showableLines-1): # I move downward outside of the rendered lines => "pull the lines up"
                                self.showStartLine += 1
                                self.cursor_Y -= self.line_gap
                                self.rerenderLineNumbers = True

                    # ___ARROW_LEFT
                    elif event.key == pygame.K_LEFT:
                        if self.chosen_LetterIndex > 0:  # mid-line
                            self.chosen_LetterIndex -= 1
                            self.cursor_X -= self.letter_size_X
                        elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0: # Move over into previous Line (if there is any)
                            self.chosen_LineIndex -= 1
                            self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex]) # end of previous line
                            self.cursor_X = self.xline_start + (len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)
                            self.cursor_Y -= self.line_gap
                            if self.chosen_LineIndex < self.showStartLine:
                                self.showStartLine -= 1
                                self.cursor_Y += self.line_gap
                                self.rerenderLineNumbers = True

                    # ___RETURN
                    elif event.key == pygame.K_RETURN:
                        transferString = self.line_String_array[self.chosen_LineIndex][(self.chosen_LetterIndex):]  # Transfer letters behind cursor to next line
                        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][:self.chosen_LetterIndex]  # Edit previous line
                        self.line_Text_array[self.chosen_LineIndex] = self.Courier_Text_15.render(self.line_String_array[self.chosen_LineIndex], 1, self.textColor)  # formatting the line
                        self.chosen_LineIndex += 1
                        self.chosen_LetterIndex = 0
                        self.maxLines += 1
                        self.cursor_X = self.xline_start
                        self.line_String_array.insert(self.chosen_LineIndex, "")
                        self.line_Text_array.insert(self.chosen_LineIndex, self.Courier_Text_15.render("", 1, (10, 10, 10)))
                        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex] + transferString  # EDIT new line with transfer letters
                        self.rerenderLineNumbers = True

                        if self.chosen_LineIndex > (self.showableLines-1): # Last row
                            self.showStartLine += 1
                        else:
                            self.cursor_Y += self.line_gap # not in last row, put curser one line down.
                    else:
                        if event.key not in [pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_DELETE, pygame.K_BACKSPACE]: # we handled those separately
                            print("Key outside scope: " + str(pygame.key.name(event.key)))

            #  _________RENDER_THE_HIGHLIGHTED LINE BACKGROUND __________ #
            # TODO - CALCUALTE HIGHLIGHT CORRECT AREA
            if self.dragged_active:
                pygame.draw.rect(self.screen, (0, 0, 0), (self.drag_cursor_X_start, self.drag_cursor_Y_start,  self.drag_cursor_X_end - self.drag_cursor_X_start,  self.drag_cursor_Y_end - self.drag_cursor_Y_start + self.lineHeight)) # width, height

            #  _________RENDER_THE_LINES__________#
            # TODO: Color-coding would be applied here #
            self.line_Text_array[self.chosen_LineIndex] = self.Courier_Text_15.render(self.line_String_array[self.chosen_LineIndex], 1, self.textColor)
            self.yline = self.yline_start
            lineBlitCounter = 0
            for line in self.line_Text_array[self.showStartLine: (self.showStartLine+self.showableLines)]:
                self.screen.blit(line, (self.xline, self.yline))
                self.yline += self.line_gap
                lineBlitCounter += 1
                if lineBlitCounter > (self.maxLines-1):  # Only render lines until max_line is reached.
                    break

            # _________RENDER_THE_CURSOR__________#
            # Blitting Trennzeichen (blinking)
            self.Trenn_counter += 1
            if self.Trenn_counter > 10:  # Appear for 10 frames, disappear for the next 10 frames.
                self.screen.blit(self.trennzeichen_image, (self.cursor_X, self.cursor_Y))
                self.Trenn_counter = self.Trenn_counter % 20

            # _________RENDER_THE_SCROLLBAR_________#
            # Background
            pygame.draw.rect(self.screen, self.codingScrollBarBackgroundColor, (self.offset_X+self.codingAreaWidth-self.scrollBarWidth , self.offset_Y+self.scrollBarButtonHeight, self.scrollBarWidth , self.codingAreaHeight-self.scrollBarButtonHeight*2)) # Separator Coloring (below the coding area)
            # Scroll Buttons
            self.scrollButton(self.offset_X+self.codingAreaWidth -self.scrollBarWidth, self.offset_Y, "ScrollUp") # Scroll Up Button
            self.scrollButton(self.offset_X+self.codingAreaWidth -self.scrollBarWidth, self.offset_Y + self.codingAreaHeight - self.scrollBarButtonHeight, "ScrollDown") # Scroll Down Button
                                         # self.offset_X+self.codingAreaWidth -self.scrollBarWidth, self.offset_Y + self.codingAreaHeight - self.scrollBarButtonHeight
            # Buttons
            if self.showStartLine == 0:
                self.screen.blit(self.scrollUpButtonImg_Deactivated, (self.offset_X+self.codingAreaWidth - self.scrollBarWidth, self.offset_Y))  # Scroll Up (deactivated Button image)
            else:
                self.screen.blit(self.scrollUpButtonImg, (self.offset_X+self.codingAreaWidth - self.scrollBarWidth, self.offset_Y))  # Scroll Up Button (active)

            if self.maxLines <= self.showStartLine + self.showableLines:
                self.screen.blit(self.scrollDownButtonImg_Deactivated, (self.offset_X+self.codingAreaWidth - self.scrollBarWidth, self.offset_Y+ self.codingAreaHeight - self.scrollBarButtonHeight))  # Scroll Down (deactivated Button image)
            else:
                self.screen.blit(self.scrollDownButtonImg, (self.offset_X + self.codingAreaWidth - self.scrollBarWidth, self.offset_Y + self.codingAreaHeight - self.scrollBarButtonHeight))  # Scroll DownB utton (active)

            # Scroll Bar
            if len(self.line_String_array) >= self.showableLines:
                self.scrollBarHeight = int((self.codingAreaHeight - (2*self.scrollBarButtonHeight)) * ((self.showableLines*1.0) / self.maxLines))
            self.scrollBarImg = pygame.transform.scale(self.scrollBarImg, (self.scrollBarWidth, self.scrollBarHeight))
            self.screen.blit(self.scrollBarImg, (self.offset_X+self.codingAreaWidth-self.scrollBarWidth, self.offset_Y+self.scrollBarButtonHeight + int((self.codingAreaHeight-(2*self.scrollBarButtonHeight)) * ((self.showStartLine*1.0) / (self.maxLines)))))

    def scrollButton(self, x, y, action):
        # Description: Creates a button for rendering/blitting and offers action

        mouse = pygame.mouse.get_pos()
        # Mouse coordinates checking (on-button)
        if x + self.scrollBarWidth > mouse[0] > x and y + self.scrollBarWidth > mouse[1] > y and pygame.mouse.get_pressed()[0] == 1:
            pygame.time.delay(100)  # we dont want to click multiple times # TODO: replace with mod counter as counter does not hinder performance?

            if action == "ScrollUp" and self.showStartLine > 0:
                self.scrollUp()
            elif action == "ScrollDown" and self.showStartLine+self.showableLines < self.maxLines:
                self.scrollDown()
            self.rerenderLineNumbers = True
        return None  # Button is not clicked.

    def scrollUp(self):
        self.showStartLine -= 1
        self.cursor_Y += self.line_gap

    def scrollDown(self):
        self.showStartLine += 1
        self.cursor_Y -= self.line_gap

