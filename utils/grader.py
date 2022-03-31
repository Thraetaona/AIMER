#
# This file is part of AIMER.
# Unpublished Copyright (C) 2022  Fereydoun Memarzanjany ("AUTHOR"), All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property of AUTHOR.  The intellectual and technical concepts contained herein are 
# proprietary to AUTHOR and may be covered by U.S. and Foreign Patents, patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from AUTHOR.
# Access to the source code contained herein is hereby forbidden to anyone except current AUTHOR employees, managers or contractors who have executed 
# Confidentiality and Non-disclosure agreements explicitly covering such access.
#
# The copyright notice above does not evidence any actual or intended publication or disclosure of this source code, which includes information
# that is confidential and/or proprietary, and is a trade secret, of AUTHOR.  ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC PERFORMANCE, 
# OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS SOURCE CODE WITHOUT THE EXPRESS WRITTEN CONSENT OF AUTHOR IS STRICTLY PROHIBITED, AND IN VIOLATION OF 
# APPLICABLE LAWS AND INTERNATIONAL TREATIES.  THE RECEIPT OR POSSESSION OF THIS SOURCE CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY 
# RIGHTS TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE, USE, OR SELL ANYTHING THAT IT MAY DESCRIBE, IN WHOLE OR IN PART.
#

import cv2 as cv
import numpy as np

# TODO: Move these to a centralized configuration section or file.
#
NUM_CHOICES = int(4)
NUM_QUESTIONS = int(5)
# TODO: Make this more 'natural' and 1-based instead of 0-based.
ANSWERS_KEY = list([0, 2, 3, 1, 0])

# TODO: Merge these two functions.
#
def check_answers(answers_provided, answers_key):
    correct_answers = int(0)

    for answer in range(0, NUM_QUESTIONS):
        if answers_provided[answer] == answers_key[answer]:
            correct_answers += 1 # Award a single credit for the correct answer.
        else:
            correct_answers += 0 # No credits, pass.

    # Converts the student's score to a percentage.
    score = float( (correct_answers / NUM_QUESTIONS) * 100 )

    return score

def display_gradings_on_paper(score, answers_provided, answers_key, paper):
    # The following lines will draw a grid over the paper image.
    #
    # Properties of the supplied paper.
    paper_width = paper.shape[1]
    paper_height = paper.shape[0]

    # Properties of each cell in the overall grid.
    cell_width = (paper_width // NUM_CHOICES) # Height // Questions
    cell_height = (paper_height // NUM_QUESTIONS) # Width // Choices


    line_color = (255, 0, 0) # Blue
    line_thickness = 2

    # TODO: Maybe merge the two below for loops?
    # TODO: Also, this would overflow beyond the image.
    #
    for step in range(0, NUM_QUESTIONS*NUM_CHOICES):
        # Vertical lines
        start = (0, cell_height*step)
        end = (paper_width, cell_height*step)
        cv.line(paper, start, end, line_color, line_thickness)

        # Horizontal lines
        start = (cell_width*step, 0)
        end = (cell_width*step, paper_height)
        cv.line(paper, start, end, line_color, line_thickness)


    # The following lines will draw a circle over the correct answers provided by the key.
    #
    for step in range(0, NUM_QUESTIONS):
        current_cell_center_x = (ANSWERS_KEY[step] * cell_width) + (cell_width // 2)
        current_cell_center_y = (step * cell_height) + (cell_height // 2)
        current_cell_center = (current_cell_center_x, current_cell_center_y)

        bubble_size = 35
        correct_bubble_color = (0, 255, 0) # Green
        wrong_bubble_color = (0, 0, 255) # Red

        bubble_color = (0, 0, 0)
        if answers_provided[step] == ANSWERS_KEY[step]:
            bubble_color = correct_bubble_color
        else:
            bubble_color = wrong_bubble_color
        cv.circle(paper, current_cell_center, bubble_size, bubble_color, cv.FILLED)

    # The following lines will display the grade/score right on the paper's center.
    #
    # Text setup
    text = str(float(score)) + "%" # E.g., "82.5%"
    text_color = (255, 255, 0) # Cyan
    text_thickness = 5
    text_font = cv.FONT_HERSHEY_SIMPLEX
    text_font_scale = 2

    # Get the image's center coordinates, accounting for the text's size too.
    text_size = cv.getTextSize(text, text_font, text_font_scale, text_thickness)[0]
    center_x = (paper_width - text_size[0]) // 2
    center_y = (paper_height + text_size[1]) // 2
    text_coordinates = (center_x, center_y)

    # Lastly, add the text.
    cv.putText(paper, text, text_coordinates, text_font, text_font_scale, text_color, text_thickness)

    return paper

def extract_answers_from_paper(paper):
    paper = cv.cvtColor(paper, cv.COLOR_BGR2GRAY)
    paper = cv.threshold(paper, 127, 255, cv.THRESH_BINARY_INV)[1]


    # The answer grid is a 2-D array filled with zeros at first that will later hold the 'weight' of choices.
    answer_grid = np.zeros( (NUM_QUESTIONS, NUM_CHOICES) ) 
    # Evenly splits the paper into seperate rows of questions, each having a number of choices.
    questions = list(np.array_split(paper, NUM_QUESTIONS, axis=0)) #np.vsplit(paper, NUM_QUESTIONS)


    for count_question, question in enumerate(questions):
        # Evenly splits every column of choices in each row into multiple 'cells' or choice.
        choices = list(np.array_split(question, NUM_CHOICES, axis=1)) #np.hsplit(question, NUM_CHOICES)
        for count_choice, choice in enumerate(choices):
            # Stores the 'weight' of the choice/cell (i.e., how many filled pixels it had.)
            answer_grid[count_question][count_choice] = cv.countNonZero(choice)

    # Since each cell is more or less going to have a number of filled-in pixels, we will
    # find the maximumly-filled area along the x-axis or the choices of each question.
    answer_list = np.argmax(answer_grid, axis=1)

    #cv.namedWindow("test")
    #while True:
    #    cv.imshow("test", question)
    #    if (cv.waitKey(33) == ord('z')):
    #        break

    return answer_list


def grade(paper):
    answers = extract_answers_from_paper(paper)

    score = check_answers(answers, ANSWERS_KEY)

    paper = display_gradings_on_paper(score, answers, ANSWERS_KEY, paper)

    return score, paper