import pygame
import math
import os


class TextEditor:

    # scrollfunctionality
    from ._scrollbar_vertical import render_scrollbar_vertical

    # input handling KEYBOARD + MOUSE
    from ._input_handling_keyboard import handle_keyboard_input, handle_keyboard_delete, handle_keyboard_backspace, \
        handle_keyboard_return, handle_keyboard_space, handle_keyboard_tab, \
        handle_keyboard_arrow_left, handle_keyboard_arrow_right, handle_keyboard_arrow_up, handle_keyboard_arrow_down
    from ._input_handling_mouse import handle_mouse_input, mouse_within_texteditor, mouse_within_existing_lines

    # rendering
    from ._rendering import render_background_objects, render_cursor, render_line_contents

    # files for customization of the editor:
    from ._customization import set_color_background, set_color_Scrollbarbackground, set_color_text, \
        set_color_lineNumber, set_color_lineNumberBackground

    from ._usage import get_text

    def __init__(self, offset_x, offset_y, text_area_width, text_area_height, screen, line_numbers=True):

        self.screen = screen
        self.editor_offset_X = offset_x
        self.editor_offset_Y = offset_y
        self.textAreaWidth = text_area_width
        self.textAreaHeight = text_area_height

        self.letter_size_Y = 15
        cdir = os.path.dirname(__file__)
        self.courier_font = pygame.font.Font(os.path.join(cdir, "elements/fonts/Courier.ttf"), self.letter_size_Y)
        self.trennzeichen_image = pygame.image.load(os.path.join(cdir, "elements/graphics/Trennzeichen.png")).convert_alpha()

        # LINES AND CURSOR
        self.Trenn_counter = 0
        self.MaxLinecounter = 0
        self.line_String_array = []  # LOGIC: Array of actual Strings
        self.line_Text_array = []  # VISUAL: Array of the rendered surfaces of the Strings
        self.lineHeight = 18
        self.showable_line_numbers_in_editor = int(math.floor(self.textAreaHeight / self.lineHeight))
        self.maxLines = int(math.floor(self.textAreaHeight / self.lineHeight))
        self.showStartLine = 0  # first line (shown at the top of the editor) <- must be zero during init!
        self.line_gap = 3 + self.letter_size_Y

        for i in range(self.maxLines):  # from 0 to maxLines:
            self.line_String_array.append("")  # Add a line
            self.line_Text_array.append(self.courier_font.render("", 1, (160, 160, 160)))

        # SCROLLBAR
        self.scrollDownButtonImg = pygame.image.load(os.path.join(cdir, "elements/graphics/Scroll_Down.png")).convert()
        self.scrollDownButtonImg_Deactivated = pygame.image.load(os.path.join(cdir, "elements/graphics/Scroll_Down_deactivated.png")).convert()
        self.scrollUpButtonImg = pygame.image.load(os.path.join(cdir, "elements/graphics/Scroll_up.png")).convert()
        self.scrollUpButtonImg_Deactivated = pygame.image.load(os.path.join(cdir, "elements/graphics/Scroll_Up_deactivated.png")).convert()
        self.scrollBarImg = pygame.image.load(os.path.join(cdir, "elements/graphics/Scroll_Bar.png")).convert()
        self.scrollBarWidth = 20
        self.scrollBarButtonHeight = 17
        self.conclusionBarHeight = 18
        self.scrollBarHeight = (self.textAreaHeight-self.scrollBarButtonHeight*2 -2) * self.showable_line_numbers_in_editor / len(self.line_String_array)

        # LINE NUMBERS
        self.displayLineNumbers = line_numbers
        if self.displayLineNumbers:
            self.lineNumberWidth = 27  # line number background width and also offset for text!
        else:
            self.lineNumberWidth = 0
        self.letter_size_X = 9
        self.chosen_LineIndex = 0
        self.chosen_LetterIndex = 0
        self.line_numbers_Y = self.editor_offset_Y

        # TEXT COORDINATES
        self.yline_start = self.editor_offset_Y + 3
        self.yline = self.editor_offset_Y
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
        self.clock = pygame.time.Clock()
        self.FPS = 60  # we need to limit the FPS so we don't trigger the same actions to often (e.g. deletions)

    def display_editor(self):
        # needs to be called within a while loop to be able to catch key/mouse input and update visuals throughout use.
        self.cycleCounter = self.cycleCounter + 1
        # first iteration
        if self.firstiteration_boolean:
            # paint entire area to avoid pixel error beneath line numbers
            pygame.draw.rect(self.screen, self.codingBackgroundColor,
                             (self.editor_offset_X, self.editor_offset_Y, self.textAreaWidth, self.textAreaHeight))
            # Scroll Up Image
            self.screen.blit(self.scrollUpButtonImg,
                             (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth, self.editor_offset_Y))
            # Scroll DownImage
            self.screen.blit(self.scrollDownButtonImg, (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth, self.editor_offset_Y + self.textAreaHeight - self.scrollBarButtonHeight))
            self.firstiteration_boolean = False

        # RENDERING 1 - Background objects
        self.render_background_objects()

        # INPUT - Mouse + Keyboard
        pygame_events = pygame.event.get()

        for event in pygame_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.handle_keyboard_input(pygame_events)
        self.handle_mouse_input(pygame_events, mouse_x, mouse_y)

        # RENDERING 3 - Lines
        self.render_line_contents()
        self.render_cursor()

        self.render_scrollbar_vertical()
        self.clock.tick(self.FPS)



