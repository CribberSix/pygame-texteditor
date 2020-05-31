import pygame
import math

class TextEditor:
    from ._scrollbar_vertical import render_scrollbar_vertical
    from ._input_handling import handle_input_mouse_clicks, handle_keyboard_input
    from ._rendering import render_background_objects, render_cursor, render_line_contents

    def __init__(self, offset_X, offset_Y, codingAreaWidth, codingAreaHeight, screen, lineNumbers=True):

        self.screen = screen
        self.editor_offset_X = offset_X
        self.editor_offset_Y = offset_Y
        self.codingAreaWidth = codingAreaWidth
        self.codingAreaHeight = codingAreaHeight

        self.letter_size_Y = 15
        self.Courier_Text_15 = pygame.font.Font("elements/fonts/Courier.ttf", self.letter_size_Y)
        self.trennzeichen_image = pygame.image.load("elements/graphics/Trennzeichen.png").convert_alpha()

        # LINES AND CURSOR
        self.Trenn_counter = 0
        self.MaxLinecounter = 0
        self.line_String_array = []
        self.line_Text_array = []
        self.lineHeight = 18
        self.showable_line_numbers_in_editor = int(math.floor(codingAreaHeight / self.lineHeight))
        self.maxLines = int(math.floor(codingAreaHeight / self.lineHeight))
        self.showStartLine = 0  # first line (shown at the top of the editor) <- must be zero during init!
        self.line_gap = 3 + self.letter_size_Y

        for i in range(self.maxLines):  # from 0 to maxLines:
            self.line_String_array.append("")  # Add a line
            self.line_Text_array.append(self.Courier_Text_15.render("", 1, (160, 160, 160)))

        # SCROLLBAR
        self.scrollDownButtonImg = pygame.image.load("elements/graphics/Scroll_Down.png").convert()
        self.scrollDownButtonImg_Deactivated = pygame.image.load("elements/graphics/Scroll_Down_deactivated.png").convert()
        self.scrollUpButtonImg = pygame.image.load("elements/graphics/Scroll_up.png").convert()
        self.scrollUpButtonImg_Deactivated = pygame.image.load("elements/graphics/Scroll_Up_deactivated.png").convert()
        self.scrollBarImg = pygame.image.load("elements/graphics/Scroll_Bar.png").convert()
        self.scrollBarWidth = 20
        self.scrollBarButtonHeight = 17
        self.conclusionBarHeight =18
        self.scrollBarHeight = (self.codingAreaHeight-self.scrollBarButtonHeight*2 -2) * self.showable_line_numbers_in_editor / len(self.line_String_array)

        # LINE NUMBERS
        self.displayLineNumbers = lineNumbers
        if lineNumbers:
            self.lineNumberWidth = 27  # line number background width and also offset for text!
        else:
            self.lineNumberWidth = 0
        self.letter_size_X = 9
        self.chosen_LineIndex = 0
        self.chosen_LetterIndex = 0
        self.line_numbers_Y = self.editor_offset_Y

        # TEXT COORDINATES
        self.yline_start = offset_Y + 3
        self.yline = offset_Y
        self.xline_start_offset = 28
        if self.displayLineNumbers:
            self.xline_start = self.xline_start_offset+self.editor_offset_X
            self.xline = self.xline_start_offset + self.editor_offset_X
        else:
            self.xline_start = self.editor_offset_X
            self.xline = self.editor_offset_X

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

        # Colors
        self.codingBackgroundColor = (40, 44, 52) # (40, 44, 52)
        self.codingScrollBarBackgroundColor = (40, 44, 52)
        self.textColor = (171, 178, 191)
        self.lineNumberColor = (73, 81, 97)
        self.lineNumberBackgroundColor = (40, 44, 52)  # (0, 0, 0) # 0, 51, 102

        self.deleteCounter = 0

        # Performance enhancing variables
        self.firstiteration_boolean = True
        self.rerenderLineNumbers = True
        self.click_hold = False

        self.cycleCounter = 0

    def display_CodeEditor(self):
        # needs to be called within a while loop to be able to catch key/mouse input and update visuals throughout use.

        self.cycleCounter = self.cycleCounter + 1
        # first iteration
        if self.firstiteration_boolean:
            pygame.draw.rect(self.screen, self.codingBackgroundColor, (self.editor_offset_X, self.editor_offset_Y, self.codingAreaWidth, self.codingAreaHeight))  # paint entire area to avoid pixel error beneath line numbers
            self.screen.blit(self.scrollUpButtonImg, (self.editor_offset_X + self.codingAreaWidth - self.scrollBarWidth, self.editor_offset_Y))  # Scroll Up Image
            self.screen.blit(self.scrollDownButtonImg, (self.editor_offset_X + self.codingAreaWidth - self.scrollBarWidth, self.editor_offset_Y + self.codingAreaHeight - self.scrollBarButtonHeight))  # Scroll DownImage
            self.firstiteration_boolean = False

        # RENDERING 1 - Background objects
        self.render_background_objects()

        # INPUT - Mouse + Keyboard
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.handle_input_mouse_clicks(mouse_x, mouse_y)
        self.handle_keyboard_input(mouse_x, mouse_y)

        # RENDERING 2 - Highlights
        # TODO - calculate the correct area for the highlight
        if self.dragged_active:  # render highlighted area
            pygame.draw.rect(self.screen, (0, 0, 0), (self.drag_cursor_X_start, self.drag_cursor_Y_start,  self.drag_cursor_X_end - self.drag_cursor_X_start,  self.drag_cursor_Y_end - self.drag_cursor_Y_start + self.lineHeight)) # width, height

        # RENDERING 3 - Lines
        self.render_line_contents()
        self.render_cursor()

        self.render_scrollbar_vertical()

