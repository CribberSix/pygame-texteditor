import pygame
from ._scrollbar_vertical import scrollbar_up, scrollbar_up


def handle_mouse_input(self, pygame_events, mouse_x, mouse_y, mouse_pressed) -> None:
    """
    Handles mouse input based on mouse events (Buttons down/up + coordinates).
    Handles drag-and-drop-select as well as single-click.
    The code only differentiates the single-click only as so far, that
        the DOWN-event is on the same position as the UP-event.

    Implemented so far:
    - left-click (selecting as drag-and-drop or single-click)
    - mouse-wheel (scrolling)
    TODO:
    - right-click
    """

    # ___ MOUSE ___ #
    for event in pygame_events:
        # ___ MOUSE CLICKING DOWN ___ #
        # Scrollbar-handling
        if event.type == pygame.MOUSEBUTTONDOWN and not self.mouse_within_texteditor(mouse_x, mouse_y):
            if self.scrollbar is not None:
                if self.scrollbar.collidepoint(mouse_x, mouse_y):
                    self.scroll_start_y = mouse_y
                    self.scroll_dragging = True

        # Mouse scrolling wheel should only work if it is within the coding area (excluding scrollbar area)
        if event.type == pygame.MOUSEBUTTONDOWN and self.mouse_within_texteditor(mouse_x, mouse_y):
            # ___ MOUSE SCROLLING ___ #
            if event.button == 4 and self.showStartLine > 0:
                self.scrollbar_up()
            elif event.button == 5 and self.showStartLine + self.showable_line_numbers_in_editor < self.maxLines:
                self.scrollbar_down()

            # ___ MOUSE LEFT CLICK DOWN ___ #
            elif event.button == 1:  # left mouse button
                if not self.click_hold:
                    # in order not to have the mouse move around after a click,
                    # we need to disable this function until we RELEASE it.
                    self.last_clickdown_cycle = self.cycleCounter
                    self.click_hold = True
                    self.dragged_active = True
                    self.dragged_finished = False
                    if self.mouse_within_texteditor(mouse_x, mouse_y):  # editor area
                        if self.mouse_within_existing_lines(mouse_y):  # in area of existing lines
                            self.set_drag_start_by_mouse(mouse_x, mouse_y)
                        else:  # clicked below the existing lines
                            self.set_drag_start_after_last_line()
                        self.update_caret_position_by_drag_start()
                    else:  # mouse outside of editor, don't care.
                        pass

        # ___ MOUSE LEFT CLICK UP ___ #
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            self.scroll_dragging = False  # reset scroll (if necessary)

            if self.click_hold:
                # mouse dragging only with left mouse up
                # mouse-up only valid if we registered a mouse-down within the editor via click_hold earlier

                self.last_clickup_cycle = self.cycleCounter
                self.click_hold = False

                if self.mouse_within_texteditor(mouse_x, mouse_y):  # editor area
                    if self.mouse_within_existing_lines(mouse_y):  # in area of existing lines
                        self.set_drag_end_by_mouse(mouse_x, mouse_y)
                    else:  # clicked beneath the existing lines
                        self.set_drag_end_after_last_line()
                    self.update_caret_position_by_drag_end()

                else:  # mouse-up outside of editor
                    if mouse_y < self.editor_offset_Y:
                        # Mouse-up above editor -> set to first visible line
                        self.drag_chosen_LineIndex_end = self.showStartLine
                    elif mouse_y > (self.editor_offset_Y + self.textAreaHeight - self.conclusionBarHeight):
                        # Mouse-up below the editor -> set to last visible line
                        if self.maxLines >= self.showable_line_numbers_in_editor:
                            self.drag_chosen_LineIndex_end = self.showStartLine + self.showable_line_numbers_in_editor - 1
                        else:
                            self.drag_chosen_LineIndex_end = self.maxLines - 1
                    else:  # mouse left or right of the editor outside
                        self.set_drag_end_line_by_mouse(mouse_y)
                    # Now we can determine the letter based on mouse_x (and selected line within the function)
                    self.set_drag_end_letter_by_mouse(mouse_x)

        # _______ CHECK FOR MOUSE DRAG AND HANDLE CLICK _______ #
        if (self.last_clickup_cycle - self.last_clickdown_cycle) >= 0:
            # Clicked the mouse lately and has not been handled yet.
            # To differentiate between click and drag we check whether the down-click
            # is on the same letter and line as the up-click!
            # We set the boolean variables here and handle the caret positioning.
            if self.drag_chosen_LineIndex_end == self.drag_chosen_LineIndex_start and \
                    self.drag_chosen_LetterIndex_end == self.drag_chosen_LetterIndex_start:
                self.dragged_active = False  # no letters are actually selected -> Actual click
            else:
                self.dragged_active = True  # Actual highlight

            self.dragged_finished = True  # we finished the highlighting operation either way

            # handle caret positioning
            self.chosen_LineIndex = self.drag_chosen_LineIndex_end
            self.chosen_LetterIndex = self.drag_chosen_LetterIndex_end
            self.update_caret_position()

            # reset after upclick so we don't execute this block again and again.
            self.last_clickdown_cycle = 0
            self.last_clickup_cycle = -1

    # Scrollbar - Dragging
    if mouse_pressed[0] == 1 and self.scroll_dragging:
        # left mouse is being pressed after click on scrollbar
        if mouse_y < self.scroll_start_y and self.showStartLine > 0:
            # dragged higher
            self.scrollbar_up()
        elif mouse_y > self.scroll_start_y \
                and self.showStartLine + self.showable_line_numbers_in_editor < self.maxLines:
            # dragged lower
            self.scrollbar_down()

def mouse_within_texteditor(self, mouse_x, mouse_y) -> bool:
    """
    Returns True if the given coordinates are within the text-editor area of the pygame window, otherwise False.
    """
    return self.editor_offset_X + self.lineNumberWidth < mouse_x < (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth) \
           and self.editor_offset_Y < mouse_y < (self.textAreaHeight + self.editor_offset_Y - self.conclusionBarHeight)


def mouse_within_existing_lines(self, mouse_y):
    """
    Returns True if the given Y-coordinate is within the height of the text-editor's existing lines.
    Returns False if the coordinate is below existing lines or outside of the editor.
    """
    return self.editor_offset_Y < mouse_y < self.editor_offset_Y + (self.lineHeight * self.maxLines)

