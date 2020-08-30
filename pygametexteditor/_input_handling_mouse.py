import pygame
from ._scrollbar_vertical import scrollDown, scrollUp

from ._line_getters import get_line_index, get_letter_index, get_number_of_letters_in_line_by_mouse, \
    get_number_of_letters_in_line_by_index

# caret
from ._caret import update_caret_position, update_caret_position_by_drag_end, update_caret_position_by_drag_start, \
    set_drag_start_after_last_line, set_drag_end_after_last_line, \
    set_drag_start_by_mouse, set_drag_end_by_mouse


def handle_mouse_input(self, pygame_events, mouse_x, mouse_y):

    # ___ MOUSE ___ #
    for event in pygame_events:
        # ___ MOUSE CLICKING DOWN ___ #
        # Mouse scrolling wheel should only work if it is within the coding area.
        if event.type == pygame.MOUSEBUTTONDOWN and self.mouse_within_texteditor(mouse_x, mouse_y):
            # ___ MOUSE SCROLLING ___ #
            if event.button == 4 and self.showStartLine > 0:
                scrollUp(self)
            elif event.button == 5 and self.showStartLine + self.showable_line_numbers_in_editor < self.maxLines:
                scrollDown(self)

            # ___ MOUSE LEFT CLICK DOWN ___ #
            elif event.button == 1:  # left mouse button
                if not self.click_hold:
                    # in order not to have the mouse move around after a click,
                    # we need to disable this function until we RELEASE it.
                    self.last_clickdown_cycle = self.cycleCounter
                    self.click_hold = True
                    self.dragged_active = True
                    if self.mouse_within_texteditor(mouse_x, mouse_y):  # editor area
                        if self.mouse_within_existing_lines(mouse_y):  # in area of existing lines
                            self.set_drag_start_by_mouse(mouse_x, mouse_y)
                        else:  # clicked below the existing lines
                            self.set_drag_start_after_last_line()
                        self.update_caret_position_by_drag_start()
                    else:  # mouse outside of editor, don't care.
                        pass

        # ___ MOUSE LEFT CLICK UP ___ #
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # mouse dragging only with left mouse up
            self.last_clickup_cycle = self.cycleCounter
            self.click_hold = False

            if self.mouse_within_texteditor(mouse_x, mouse_y):  # editor area
                if self.mouse_within_existing_lines(mouse_y):  # in area of existing lines
                    self.set_drag_end_by_mouse(mouse_x, mouse_y)
                else:  # clicked beneath the existing lines
                    self.set_drag_end_after_last_line()
                self.update_caret_position_by_drag_end()
            else:  # mouse outside of editor, don't care.
                pass

        # _______ CHECK FOR MOUSE DRAG AND HANDLE CLICK _______ #
        if (self.last_clickup_cycle - self.last_clickdown_cycle) >= 0:
            # clicked the mouse lately and has not been handled yet.
            # we dont have to check how long the mouse was held, to differentiate between click and drag
            # but if the down-click is on the same letter and line as the up-click!
            if self.drag_chosen_LineIndex_end == self.drag_chosen_LineIndex_start and \
                    self.drag_chosen_LetterIndex_end == self.drag_chosen_LetterIndex_start:
                self.dragged_active = False
            else:
                self.dragged_active = True
                # depending on the next action (e.g. KEYDOWN handled in keybaord.py) we do something with
                # the selected area (for instance upon keydown, the selected characters/lines get removed!)

            self.chosen_LineIndex = self.drag_chosen_LineIndex_end
            self.chosen_LetterIndex = self.drag_chosen_LetterIndex_end
            self.update_caret_position()

            # reset after upclick => difference is "-1" and hence smaller than 0. Wait for next clickup.
            self.last_clickdown_cycle = 0
            self.last_clickup_cycle = -1


def mouse_within_texteditor(self, mouse_x, mouse_y):
    return self.editor_offset_X + self.lineNumberWidth < mouse_x < (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth) \
           and self.editor_offset_Y < mouse_y < (self.textAreaHeight + self.editor_offset_Y - self.conclusionBarHeight)


def mouse_within_existing_lines(self, mouse_y):
    return self.editor_offset_Y < mouse_y < self.editor_offset_Y + (self.lineHeight * self.maxLines)

