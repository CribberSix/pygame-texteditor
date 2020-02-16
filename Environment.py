import pygame, sys
from io import StringIO
from Scripts.LearningEnvironment.TextEditor import TextEditorClass
from Scripts.MiscScripts import Button
from Scripts.LearningEnvironment.Curriculum import Lesson

class LearningEnvironment_Class():


    def __init__(self):
        self.idea_icon = pygame.image.load("Graphics/LearningEnvironment/Idea.png").convert()
        self.checkCodeGreen_image = pygame.image.load("Graphics/LearningEnvironment/CheckCodeGreen.png").convert()
        self.checkCodeRed_image = pygame.image.load("Graphics/LearningEnvironment/CheckCodeRed.png").convert()
        self.checkCodes_image = pygame.image.load("Graphics/LearningEnvironment/CodeChecks.png").convert()

        self.HeadlineFont = pygame.font.Font("Misc/Ultra-Regular.ttf",20)
        self.Courier_Text_15_Font = pygame.font.Font("Misc/Courier.ttf", 15)
        self.Ubuntu_Regular_25 = pygame.font.Font("Misc/UbuntuMono-Regular.ttf", 25)
        self.Ubuntu_Bold_25 = pygame.font.Font("Misc/UbuntuMono-Bold.ttf", 25)
        self.SourceCodePro_Light_25 = pygame.font.Font("Misc/SourceCodePro-Light.ttf", 25)
        self.SourceCodePro_Light_15 = pygame.font.Font("Misc/SourceCodePro-Light.ttf", 15)

        self.Headline_Text = self.SourceCodePro_Light_25.render( "Learn" ,1,(10,10,10))

        self.buttonCreater = Button.Buttons()
        self.output_string = ""
        self.backgroundColor = (21, 43, 57)
        self.instructionBackgroundColor = (250,250,250)
        self.headlineColor = (212, 215, 214)
        self.codingOutputBackgroundColor = (70, 88, 117)
        self.codingOutputLetterColor = (255,255,255)

        self.codeCheckString = ""

        # FPS
        self.FPS = 30
        self.clock = pygame.time.Clock()

        self.CheckCodeComplete = 0
        self.CheckOutputComplete = 0
        self.CheckCodeComplete_Bool = False
        self.lessonsfinishedduringthissession = 0

    def display_Learner(self, screen, SettingsObj, lessonNumber):
        self.SettingsObj = SettingsObj

        self.w, self.h = pygame.display.get_surface().get_size()
        self.TX = TextEditorClass(self.w*0.3, 0, int((self.w*0.7)), self.h*0.7, screen) # X_offset, Y_offset, codeAreaWidth, codeAreaHeight   # TODO: (check how high I actually want it to be!)
        self.Lesson = Lesson.LessonClass(screen)
        self.Lesson.loadLesson(lessonNumber, self.w * 0.3 )


        while(True):
            ####_________ENVIRONMENTS_________####
            pygame.draw.rect(screen, self.codingOutputBackgroundColor, (self.w*0.3, self.h*0.7, self.w*0.7, self.h*0.3))
            pygame.draw.rect(screen, self.instructionBackgroundColor, (0, 0, self.w*0.3, self.h)) # Instructions (left side - entire window)

            ####_________INSTRUCTIONS__________####
            # LEARN Icon+Caption
            pygame.draw.rect(screen, self.headlineColor, (0, 0, self.w*0.3, 40))
            screen.blit(self.idea_icon, (5, 0))
            screen.blit(self.Headline_Text, (50, 2))

            ####_________CURRICULUM_LESSON__________####
            # Contains all introductions, an example, the "Instruction-Header + Icon" and instructions
            self.Lesson.display()  # line-length + line-amount + header&icon are dynamically regulated.

            ####_________TEXTBOX__________####
            self.TX.display_CodeEditor()

            ####_________BUTTONS__________####
            # Run Code # TODO maybe delete this button - only have "check code" button.
            #if ("RunCode" == self.buttonCreater.createCodeEnvButton(screen, self.w*0.3, (self.h*0.7)+1, "RunCode" )):
            #    code_string = ""
            #    for line in self.TX.line_String_array:
            #        if line != "":
            #            code_string = code_string + "\n" + line
            #    oo = self.execute_Code(code_string)
            #    if oo != None:
            #        self.output_string = oo[1]
            #    else:
            #        self.output_string = ""

            # Run & Check Code.
            checkmyCode = self.buttonCreater.createCodeEnvButton(screen, self.w*0.3, (self.h*0.7)+1, "CheckCode" )
            if ("CheckCode" == checkmyCode):
                self.CheckCodeComplete = 0
                self.CheckOutputComplete = 0
                code_string = ""
                for line in self.TX.line_String_array:
                    if line != "":
                        code_string = code_string + "\n" + line
                oo = self.execute_Code(code_string)
                if oo != None:
                    self.output_string = oo[1]
                    if oo[0]:  # Code is executable (No Error occurred)

                        # Check user code for compliance with instructions & lesson parameters
                        # Code Check 1
                        if self.Lesson.CodeChecks > 0:
                            self.codeCheckString = code_string + "\n" + self.Lesson.Code_Check_1
                            t1 = self.execute_Code(self.codeCheckString)
                            if t1[0]:
                                self.CheckCodeComplete += 1
                            else:
                                print("Error during First Code Check.")
                                # TODO - Explain what / why? (Add "2nd Test not yet satisfied"?)

                        # Code Check 2
                        if self.Lesson.CodeChecks > 1:
                            self.codeCheckString = code_string + "\n" + self.Lesson.Code_Check_2
                            t2 = self.execute_Code(self.codeCheckString)
                            if t2[0]:
                                self.CheckCodeComplete += 1
                            else:
                                print("Error during Second Code Check.")
                                # TODO - Explain what / why? (Add "2nd Test not yet satisfied"?)


                        # Output Check 1
                        if self.Lesson.OutputChecks > 0:
                            if self.Lesson.Output_Check_1 in self.output_string:
                                self.CheckOutputComplete += 1
                            else:
                                print("Error during first output check.")
                                # TODO - Explain what / why? (Add "2nd Test not yet satisfied"?)


                        if self.CheckCodeComplete == self.Lesson.CodeChecks and self.CheckOutputComplete == self.Lesson.OutputChecks:
                            self.CheckCodeComplete_Bool = True  # enable continuing to next chapter / back to the game.

                else:
                    # Something went wrong.
                    # Code was not executable.
                    self.output_string = ""

            # Code Check Visuals
            screen.blit(self.checkCodes_image, (self.w*0.7, (self.h*0.7)+1))
            codeCheck_CoordX = self.w*0.7+150
            posChecks = self.CheckCodeComplete + self.CheckOutputComplete
            for _ in range(self.Lesson.CodeChecks + self.Lesson.OutputChecks):
                if posChecks > 0:
                    screen.blit(self.checkCodeGreen_image, (codeCheck_CoordX, (self.h*0.7)+1))
                    codeCheck_CoordX += 35
                    posChecks -= 1
                else:
                    screen.blit(self.checkCodeRed_image, (codeCheck_CoordX, (self.h*0.7)+1))
                    codeCheck_CoordX += 35

            # Continue to next Lesson Button
            if self.CheckCodeComplete_Bool:
                if "Continue" == self.buttonCreater.createCodeEnvButton(screen, self.w*0.3+300, (self.h*0.7)+1, "Continue" ):
                    self.CheckCodeComplete = 0 # Restore
                    self.CheckOutputComplete = 0 # Restore
                    self.CheckCodeComplete_Bool = False # Restore
                    self.output_string = "" # Restore
                    if self.Lesson.Continue:  # Continue to learn with the next lesson.
                        lessonNumber = self.display_Learner(screen, SettingsObj, lessonNumber+1) # command returns here.
                        return lessonNumber  # Return until the "stack of sub-lessons" are handled.
                    else:
                        return lessonNumber  # Return immediately to the game.

            # DEV Button # TODO: Remove
            #if "ToGame" == self.buttonCreater.createMenuButton(screen, "BackToGame", screen_wdith*0.5, screen_height*0.9, "ToGame"):
            #    return 1 # lessonNumber = 1; DEV Default

            ###_________CONSOLE__________####
            self.Console_Output_Text =  self.Courier_Text_15_Font.render(">>> Terminal <<<", 1, self.codingOutputLetterColor)
            screen.blit(self.Console_Output_Text, ((self.w * 0.3) + 10, (self.h * 0.7) + 40))

            count = (self.h*0.7)+60

            x = self.output_string.split("\n")
            for line in x:
                blitLine = self.Courier_Text_15_Font.render(line, 1, self.codingOutputLetterColor)
                screen.blit(blitLine,((self.w*0.3)+10,count))
                count += 17

            # FPS ticker
            self.clock.tick(self.FPS)
            text = self.HeadlineFont.render("FPS: " + str(round(self.clock.get_fps(),1)),1,(10,10,10))
            screen.blit(text,(0.9 * self.w, 0.9 * self.h))

            ####_________PYGAME__________####
            pygame.display.flip()


    def execute_Code(self, code_string):
        # create file-like string to capture output
        codeOut = StringIO()
        codeErr = StringIO()
        s_err = ""

        # capture output and errors
        sys.stdout = codeOut
        sys.stderr = codeErr

        try:
            exec(code_string)
        # TODO: better error messages (+line in which it occurred)
        except RuntimeError:
            print("A RuntimeError occurred")
            s_err = "RuntimeError"
        except TypeError:
            print("A TypeError occurred!")
            s_err = "TypeError"
        except NameError:
            print("A NameError occurred!")
            s_err = "NameError"
        except ValueError:
            print("A ValueError occurred!")
            s_err = "ValueError"
        except SyntaxError:
            print("SyntaxError: invalid Syntax")
            s_err = "SyntaxError"
        except Exception:
            print("Another unknown error occurred!")
            s_err = "UnknownError"

        # restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        if s_err != "":
            codeOut.close()  # TODO Do I need this in here or can i put it above (duplicate code)
            codeErr.close()
            print("S_ERR")  # TODO Remove
            return (False, s_err)

        s_succ = codeOut.getvalue()
        if s_succ != "":
            codeOut.close() # TODO Do I need this in here or can i put it above (duplicate code)
            codeErr.close()
            print("S_SUCC") # TODO Remove
            return (True, s_succ)

        codeOut.close()
        codeErr.close()
        return (True, "") # Code executed properly, but had no "print" statement.


