import pygame, sys
import Scripts.LearningEnvironment.Curriculum.Lesson_1 as Lesson_1
import Scripts.LearningEnvironment.Curriculum.Lesson_2 as Lesson_2
import Scripts.LearningEnvironment.Curriculum.Lesson_3 as Lesson_3


# Lesson 1 -> Lesson 2
# Lesson 3
# ....

class LessonClass():

    def __init__(self, screen):

        self.screen = screen
        self.lessonNumber = 0

        # Fonts
        self.Ubuntu_Bold_25 = pygame.font.Font("Misc/UbuntuMono-Bold.ttf", 25)
        self.SourceCodePro_Light_15 = pygame.font.Font("Misc/SourceCodePro-Light.ttf", 15)
        self.SourceCodePro_Light_25 = pygame.font.Font("Misc/SourceCodePro-Light.ttf", 25)

        self.characterWidth = 9

        # Colors
        self.Green = ( 10,160, 10)
        self.Black = (  0,  0,  0)
        self.White = (255,255,255)
        self.Red_Code = (128, 0, 0)
        self.headlineColor = (212, 215, 214)

        # Idea
        self.Caption = ""
        self.introduction_example = ""

        # Instructions:
        self.instruction_1 = ""
        self.instruction_2 = ""
        self.introduction_3 = ""

         # Code Checks
        self.Code_Check_1 = ""
        self.Code_Check_2 = ""
        self.CodeChecks = 0

        self.Output_Check_1 = ""
        self.OutputChecks = 0

        # Lesson Continuation
        self.Continue = False



        # Environment
        self.instruction_icon = pygame.image.load("Graphics/LearningEnvironment/Instruction.png").convert()
        self.Headline_Text_2 =  self.SourceCodePro_Light_25.render( "Instruction" ,1,(10,10,10))
        # Code Checks

    def loadLesson(self, lessonNumber, lessonAreaWidth):

        self.lessonNumber = lessonNumber
        if (self.lessonNumber == 1):
            # Caption
            self.caption = Lesson_1.caption
            # Introduction
            self.introduction_1 = Lesson_1.introduction_1
            self.introduction_2 =  Lesson_1.introduction_2
            self.introduction_example = Lesson_1.introduction_example
            self.introduction_3 = Lesson_1.introduction_3
            # Instructions
            self.instruction_1 = Lesson_1.instruction_1
            self.instruction_2 =  Lesson_1.instruction_2
            # CheckCode Functionality
            self.Code_Check_1 = Lesson_1.Code_Check_1
            self.Code_Check_2 = Lesson_1.Code_Check_2
            self.CodeChecks = Lesson_1.CodeChecks
            # Output Checks Funtionality
            self.Output_Check_1 = Lesson_1.Output_Check_1
            self.OutputChecks = Lesson_1.OutputChecks
            # Continuation
            self.Continue = Lesson_1.Continue

        if (self.lessonNumber == 2):
            # Caption
            self.caption = Lesson_2.caption
            # Introduction
            self.introduction_1 = Lesson_2.introduction_1
            self.introduction_2 =  Lesson_2.introduction_2
            self.introduction_example = Lesson_2.introduction_example
            self.introduction_3 = Lesson_2.introduction_3
            # Instructions
            self.instruction_1 = Lesson_2.instruction_1
            self.instruction_2 =  Lesson_2.instruction_2
            # CheckCode Functionality
            self.Code_Check_1 = Lesson_2.Code_Check_1
            self.Code_Check_2 = Lesson_2.Code_Check_2
            self.CodeChecks = Lesson_2.CodeChecks
            # Output Checks Functionality
            self.Output_Check_1 = Lesson_2.Output_Check_1
            self.OutputChecks = Lesson_2.OutputChecks
            # Continuation
            self.Continue = Lesson_2.Continue

        if (self.lessonNumber == 3):
            # Caption
            self.caption = Lesson_3.caption
            # Introduction
            self.introduction_1 = Lesson_3.introduction_1
            self.introduction_2 = Lesson_3.introduction_2
            self.introduction_example = Lesson_3.introduction_example
            self.introduction_3 = Lesson_3.introduction_3
            # Instructions
            self.instruction_1 = Lesson_3.instruction_1
            self.instruction_2 = Lesson_3.instruction_2
            # CheckCode Functionality
            self.Code_Check_1 = Lesson_3.Code_Check_1
            self.Code_Check_2 = Lesson_3.Code_Check_2
            self.CodeChecks = Lesson_3.CodeChecks
            # Output Checks Functionality
            self.Output_Check_1 = Lesson_3.Output_Check_1
            self.OutputChecks = Lesson_3.OutputChecks
            # Continuation
            self.Continue = Lesson_3.Continue

        if (self.lessonNumber > 3):  # TODO: Implement more lessons
            print("You reached the end of all implemented lessons. Congratulations.")
            pygame.quit()  # Fixes the bug that pygame takes up space in the RAM when game is just closed by sys.exit()
            sys.exit()

        # Split Texts and format code for the display. Applied to every lesson:
        self.lessonAreaWidth = lessonAreaWidth
        maxLineLength = int(((lessonAreaWidth-20)*1.0)/self.characterWidth)  # min 10x2 pixel distance from each side.
        self.introduction_1 = self.lineSplitter_Text(self.introduction_1, maxLineLength)
        self.introduction_2 = self.lineSplitter_Text(self.introduction_2, maxLineLength)
        self.introduction_example = self.lineSplitter_Code(self.introduction_example)
        self.introduction_3 = self.lineSplitter_Text(self.introduction_3, maxLineLength)
        self.instruction_1 = self.lineSplitter_Text(self.instruction_1, maxLineLength)
        self.instruction_2 = self.lineSplitter_Text(self.instruction_2, maxLineLength)


    def lineSplitter_Text(self, startString, maxLineLength):
        self.str_array = startString.split(" ")  # Split by words
        self.str_array_formatted = [] # array for finished lines
        current_line = ""
        for word in self.str_array:
            if ((len(current_line) + (len(word)+1)) <= maxLineLength): # current line + space + next word < possible length of the line
                if len(current_line) == 0: # First line
                    current_line = word # No leading space
                else: # any line after that.
                    current_line = current_line + " " + word  # still fits into the same line.
            else:  # next line
                self.str_array_formatted.append(current_line)
                current_line = word
        self.str_array_formatted.append(current_line) # Append last line.

        return self.str_array_formatted


    def lineSplitter_Code(self, startString):
        return startString.split("\n")  # Split by \n (special Code-regulation)


    def display(self):

        # Caption
        self.screen.blit( self.Ubuntu_Bold_25.render( self.caption , 1, self.Green ) ,(10,50))
        # Introduction_1
        yVar = 100
        for line in self.introduction_1:
            self.screen.blit(self.SourceCodePro_Light_15.render( line , 1, self.Black) ,(10,yVar))
            yVar += 20

        # Introduction_2
        yVar += 30  # Break between the two texts
        for line in self.introduction_2:
            self.screen.blit(self.SourceCodePro_Light_15.render( line , 1, self.Black) ,(10,yVar))
            yVar += 20

        # Code Example
        yVar += 30  # Break between the two texts
        for line in self.introduction_example:
            self.screen.blit(self.SourceCodePro_Light_15.render( line , 1, self.Red_Code) ,(25,yVar))
            yVar += 20

        # Introduction_3
        yVar += 30  # Break between the two texts
        for line in self.introduction_3:
            self.screen.blit(self.SourceCodePro_Light_15.render( line , 1, self.Black) ,(10,yVar))
            yVar += 20


        # Background + Icon + "Instruction"-Header
        yVar += 30
        pygame.draw.rect(self.screen, self.headlineColor ,(0 , yVar , self.lessonAreaWidth , 40))
        self.screen.blit(self.instruction_icon, (5, yVar))
        self.screen.blit(self.Headline_Text_2 , (50, yVar+2))


        # Instruction_1
        yVar += 65  # Break between the two texts
        for line in self.instruction_1:
            self.screen.blit(self.SourceCodePro_Light_15.render( line , 1, self.Black) ,(10,yVar))
            yVar += 20
        # Instruction_2
        yVar += 30  # Break between the two texts
        for line in self.instruction_2:
            self.screen.blit(self.SourceCodePro_Light_15.render( line , 1, self.Black) ,(10,yVar))
            yVar += 20











