# -*- coding: utf-8 -*-

###################################################################################################################################
#                                                                                                                                 #
#                                   TRANSVERSAL METACOGNITIVE MONITORING ON MULTIPLE TYPE-I TASKS                                 #
#                                                   Maxime Maheu (M1 Cogmaster)                                                   #
#                                                                                                                                 #
#                                             Behavior, Emotion and Basal Ganglia team                                            #
#                                                   Brain and Spine Institute                                                     #
#                                                                                                                                 #
###################################################################################################################################

######################################################### IMPORT MODULES ##########################################################

#### Import pygame modules
import pygame
from pygame.locals import *
#### Import mathematical modules
import random
import numpy as np
import itertools
#### Import system modules
import csv
import socket
import datetime

####################################################### DEFINE PARAMETERS #########################################################

'''(W, H) = (1024, 768)'''

gray = [127, 127, 127]
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
blue = [0, 0, 255]

interstimuli_timelaps = 1000 # ms
displaying_time = 250 # ms

training_trials_per_task = 10 # trials
trials_per_task = 120 # trials

####################################################### DEFINE FUNCTIONS ##########################################################

def create_file(context):
    #### Print title and copyright
    print 'TRANSVERSAL METACOGNITIVE MONITORING ON MULTIPLE TYPE-I TASKS'
    print '[Copyright 2013 (C) Maxime Maheu]'
    #### If data is recording one subject by one subject
    if context == 1:
        #### Print tasks list
        tasks_name_list = ['', 'TASKS:',
                           '1 - MDT task',
                           '2 - MLT task',
                           '3 - Temporal task',
                           '4 - Gabors task',
                           '5 - Crowding task',
                           '6 - Reaching task','']
        for task_name in tasks_name_list: print task_name
        #### Get a random number to identify the subject and print this number
        subject_number = str(datetime.datetime.today().day) + '-' + str(datetime.datetime.today().month) # random.randint(100, 999)
        print 'Subject number:', subject_number
        #### Get initials and put them in capital letters
        subject_initials = raw_input('Subject initials: ')
        subject_initials = subject_initials.upper()
        #### Get subject age, genre and handedness
        subject_age = 'NaN'
        while (subject_age == 'NaN') or (subject_age <= 0):
            subject_age = raw_input('Subject age: ')
        subject_genre = 'NaN'
        while subject_genre not in ('M', 'F'):
            subject_genre = raw_input('Subject genre ([M]ale or [F]emale): ')
            subject_genre = subject_genre.upper()
        subject_handedness = 'NaN'
        while subject_handedness not in ['L', 'R']:
            subject_handedness = raw_input('Subject handedness ([L]eft or [R]ight): ')
            subject_handedness = subject_handedness.upper()
        print ' '
        #### Keep asking for a task or a tasks' order while it is different from all possible combinations
        all_typeI_tasks = [1, 2, 3, 4, 5, 6]
        possibilities = []
        item = 1
        while item <= len(all_typeI_tasks):
            permutations = list(itertools.permutations(all_typeI_tasks, item))
            for permutation in permutations:
                temporary = list(permutation)
                possibilities.append(temporary)
            item += 1
        typeI_tasks = 'NaN'
        while typeI_tasks not in possibilities:
            typeI_tasks_brut = raw_input('Task or tasks order (1 or 32 or 123456 for instance): ')
            typeI_tasks = map(int, typeI_tasks_brut)
        #### Ask if metacognitive questionnaire has to be displayed at the end of the experiment
        metacognitive_questionnaire = 'NaN'
        while metacognitive_questionnaire not in ['Y', 'N']:
            metacognitive_questionnaire = raw_input('Display the metacognitive questionnaire at the end ([Y]es or [N]o): ')
            metacognitive_questionnaire = metacognitive_questionnaire.upper()
        #### Create the file name
        recording_file_name = 'TraMetaMo_' + subject_initials + '_' + str(subject_number) + '_' + subject_genre + subject_age + subject_handedness  + '_' + str(typeI_tasks_brut) + '_' + 'DATA' + '.dat'
    #### If data is recording during a session in the "Laboratoire d'économie expérimentale de Paris" (LEEP)
    elif context == 0:
        #### Get the desk number from its IP adress
        subject_number = socket.gethostbyname(socket.gethostname())
        subject_number = subject_number[(len(subject_number) - 2):]
        #### Do not record individual data in order to directly launch the program
        subject_initials = 'LEEP'
        subject_age = 'NaN'
        subject_genre = 'NaN'
        subject_handedness = 'NaN'
        #### Randomly displayed the type I tasks
        typeI_tasks = [1, 2, 3, 4, 5, 6]
        random.shuffle(typeI_tasks)
        #### By default, display the metacognitive questionnaire
        metacognitive_questionnaire = 'Y'
        recording_file_name = 'DATA' + '_' + subject_initials + '_' + subject_number + '.dat'
    output_file = open(recording_file_name, 'a')
    #### Record headings in this file
    print >> output_file, 'SUBJECT_INITIALS', 'SUBJECT_NUMBER', 'TYPE_I_TASK', 'TRIAL', 'TYPE_I_DIFFICULTY', 'TYPE_I_DISPLAY', 'TYPE_I_ANSWER', 'TYPE_I_CORRECTION', 'TYPE_I_LABEL', 'TYPE_I_RT', 'TYPE_II_ANSWER', 'TYPE_II_RT'
    output_file.close()
    #### Add a 0 in the first position of the list to avoid crashes and really displayed task 1 when 1 is typed
    typeI_tasks.insert(0,0)
    return context, subject_initials, subject_number, subject_genre, subject_age, subject_handedness, typeI_tasks, metacognitive_questionnaire, recording_file_name, output_file

def wait(duration):
    t0 = pygame.time.get_ticks()
    #### Wait until reaching the "duration" threshold
    while True:
        t = pygame.time.get_ticks() - t0
        if duration > 0 and t > duration: return

def baseline():
    #### Define a list for saving easiness indexes
    actualized_list = [['Nan', 'NaN']]
    #### Define the default easiness index for each type I task
    if typeI_tasks[task] == 1: easiness_index = 3
    if typeI_tasks[task] == 2: easiness_index = 7
    if typeI_tasks[task] == 3: easiness_index = 200
    if typeI_tasks[task] == 4: easiness_index = 0.3
    if typeI_tasks[task] == 5: easiness_index = 50
    if typeI_tasks[task] == 6: easiness_index = 700
    return actualized_list, easiness_index

def staircase_method(coefficient, easiness_index):
    #### Define the stair for each type I task
    MDT_task_stair = 1
    MLT_task_stair = 1
    Temporal_task_stair = 15
    Gabor_task_stair = 0.02
    Crowding_task_stair = 3
    Reaching_task = 20
    #### Decrease the easiness index 
    if coefficient == -1:
        if typeI_tasks[task] == 1: easiness_index -= MDT_task_stair
        if typeI_tasks[task] == 2: easiness_index -= MLT_task_stair
        if typeI_tasks[task] == 3: easiness_index += Temporal_task_stair
        if typeI_tasks[task] == 4: easiness_index += Gabor_task_stair
        if typeI_tasks[task] == 5: easiness_index += Crowding_task_stair
        if typeI_tasks[task] == 6: easiness_index += Reaching_task
    #### Or keep it constant
    if coefficient == 0: return easiness_index
    #### Or increase it
    if coefficient == 1:
        if typeI_tasks[task] == 1: easiness_index += MDT_task_stair
        if typeI_tasks[task] == 2: easiness_index += MLT_task_stair
        if typeI_tasks[task] == 3: easiness_index -= Temporal_task_stair
        if typeI_tasks[task] == 4: easiness_index -= Gabor_task_stair
        if typeI_tasks[task] == 5: easiness_index -= Crowding_task_stair
        if typeI_tasks[task] == 6: easiness_index -= Reaching_task
    #### Avoid having a negative easiness index and return it
    if easiness_index < 0: easiness_index = 0
    return easiness_index

def draw_text(text, position, letters_size):
    #### Providing a simple function to display words and letters
    font = pygame.font.Font(None, letters_size)
    image = font.render(text, 1, black)
    size = image.get_size()
    window.blit(image, [position[0] - size[0]/2, position[1] - size[1]/2])
    return

def draw_fixation_cross():
    #### Display a simple fixation cross at the center of the screen
    pygame.draw.line(window, black, [W/2, H/2 - 5], [W/2, H/2 + 5], 3)
    pygame.draw.line(window, black, [W/2 - 5, H/2], [W/2 + 5, H/2], 3)
    return

def draw_gabor(size, smooth, contrast, spatial_frequency, theta):
    standard_deviation = 0.1
    #### Create a pygame surface at the gabor's size
    gabor = pygame.Surface([size, size])
    #### And an empty numpy matrix
    matrix = np.zeros(size*size).reshape((size, size))
    #### Start from the first lign and the first column of this matrix
    (i, j) = (0, 0)
    while j < size:
        while i < size:
            #### Create second order coordinates by moving the starting point of the matrix from the upper left point to the center
            (i_prime, j_prime) = (i - size/2, j - size/2)
            #### Create a 2D gaussian glob
            gaussian_glob = np.exp(- ((i_prime**2 + j_prime**2) / (2*(smooth/standard_deviation)**2)))
            #### Create a 2D grating
            gratings = contrast*np.sin(2*np.pi*(spatial_frequency*((i_prime*np.cos(np.radians(theta)))+(j_prime*np.sin(np.radians(theta))))))
            #### Calculate the absolute value ([-1, 1]) of each pixel contained in the matrix
            pixel = gaussian_glob*gratings
            #### Convert the absolute value in pixel color values to create a gray colormap (make the base value correspond to background color)
            pixel = (pixel*127) + 128
            #### Convert this value to an integer and add it to the matrix
            matrix[i, j] = int(pixel)
            #### Apply this value to the pygame surface
            gabor.set_at((i, j), (matrix[i, j], matrix[i, j], matrix[i, j]))
            i += 1
            i_prime += 1
        #### Reset i and i' in order to apply this method to the full matrix
        i = 0
        i_prime = 0
        j += 1
        j_prime += 1
    return gabor

def break_screen():
    #### Display instructions during inter-blocks break
    window.fill(gray)
    draw_text(u"PAUSE", [W/2, H/2 - 300], 30)
    draw_text(u"Faîtes une pause d'une ou deux minute(s).", [W/2, H/2 - 30], 30)
    draw_text(u"N'oubliez pas d'utiliser l'ensemble de l'échelle de confiance (de 1 à 6).", [W/2, H/2 + 30], 30)
    draw_text(u"Appuyez sur ESPACE quand vous êtes prêt(e).", [W/2, H/2 + 300], 30)
    pygame.display.flip()
    #### Clear the events from the queue
    pygame.event.clear()
    #### Wait until press on spacebar
    while True:
        for ev in pygame.event.get():            
            if (ev.type == KEYDOWN) and (ev.key == K_SPACE): return

def MDT_task(easiness_index):
    #### Precautions for easiness index
    if easiness_index <= 0: easiness_index = 1
    if easiness_index >= 8: easiness_index = 8
    #### Define task parameters
    total_number_of_circles = easiness_index
    eccentricity = 100
    #### Define all the possible positions
    circle_position = [[W/2 - eccentricity, H/2 - eccentricity], [W/2, H/2 - eccentricity], [W/2 + eccentricity, H/2 - eccentricity], [W/2 + eccentricity, H/2],
                       [W/2 + eccentricity, H/2 + eccentricity], [W/2, H/2 + eccentricity], [W/2 - eccentricity, H/2 + eccentricity], [W/2 - eccentricity, H/2]]
    random.shuffle(circle_position)
    #### Define all the possible colors
    circle_color = [[255, 0, 0], [255, 204, 204], [204, 204, 255], [255, 102, 0], [255, 255, 102], [51, 204, 0], [153, 51, 0], [102, 51, 102], [255, 255, 255],
                    [0, 102, 0], [204, 51, 204], [153, 255, 153], [0, 204, 204], [51, 51, 255], [102, 0, 204], [0, 0, 0], [255, 204, 255], [51, 204, 255], [0, 0, 153]]
    random.shuffle(circle_color)
    #### Display all the circles in one screen
    window.fill(gray)
    circle_number = 0
    while circle_number <= (total_number_of_circles - 1):
        #### Walk in the two random lists to create the circles
        pygame.draw.circle(window, circle_color[circle_number], circle_position[circle_number], 25)
        circle_number += 1
    pygame.display.flip()
    #### Display the circles during the displaying time
    wait(displaying_time)
    #### Display a fixation cross
    window.fill(gray)
    draw_fixation_cross()
    pygame.display.flip()
    wait(interstimuli_timelaps)
    #### Randomly choose if the circle was or not in the target stimulus
    typeI_display = 'NaN'
    typeI_display = random.choice([0, 1])
    window.fill(gray)
    #### Find a color and a position unmatched with the target stimuluss
    if typeI_display == 0:
        color_item = 0
        position_item = 0
        while (color_item == position_item):
            color_item = random.randint(0, (len(circle_color) - 1))
            position_item = random.randint(0, (len(circle_position) - 1))
        pygame.draw.circle(window, circle_color[color_item], circle_position[position_item], 25)
    #### Or pick a stimulus among those who were displayed
    elif typeI_display == 1:
        target_stimulus = random.randint(0, (total_number_of_circles - 1))
        pygame.draw.circle(window, circle_color[target_stimulus], circle_position[target_stimulus], 25)
    #### Finally, display the 2AFC
    display_dichotomic_choice('OUI', 'NON', [W/2, H/2 - 200], [W/2, H/2 + 200])
    pygame.display.flip()
    return easiness_index, typeI_display

def MLT_task(easiness_index):
    #### Precautions for easiness index
    if easiness_index <= 0: easiness_index = 1
    if easiness_index > 20: easiness_index = 20
    #### Define task parameters
    total_number_of_words = easiness_index
    retention_time = 60000
    new_list_frequency = 10
    #### Open the file containing all the words
    words_list = csv.reader(open('WORDS.csv', 'rU'))
    #### Create the words list based on the file previously opened
    all_words = []
    for word in words_list: all_words.append(str(word[0]))
    #### Display a new list every 10 items
    if ((subtype == 'TRAINING') and (training_trial in (range(1, training_trials_per_task, new_list_frequency)))) or ((subtype == 'RECORDING') and (trial in (range(1, trials_per_task, new_list_frequency)))):
        #### Random shuffle words list before each new list
        random.shuffle(all_words)
        #### Define all the possible positions
        word_positions = []
        left_column = W/2 - 200
        right_column = W/2 + 200
        horizontal_position = -300
        while horizontal_position <= 300:
            word_positions.append([left_column, H/2 + horizontal_position])
            horizontal_position += 30
        horizontal_position = -300
        while horizontal_position <= 300:
            word_positions.append([right_column, H/2 + horizontal_position])
            horizontal_position += 30
        random.shuffle(word_positions)
        window.fill(gray)
        #### Create a file to stock the target words
        words_temporary_file = csv.writer(open('BUFFER.csv', 'w'))
        #### Save and display the target words
        word_number = 0
        while word_number <= (total_number_of_words - 1):
            words_temporary_file.writerow([str(all_words[word_number])])
            draw_text(str(all_words[word_number]), word_positions[word_number], 30)
            word_number += 1
        pygame.display.flip()
        wait(retention_time)
    #### Display a fixation cross
    window.fill(gray)
    draw_fixation_cross()
    pygame.display.flip()
    #### During a random delay to prevent from learning
    fc_duration = random.randint(interstimuli_timelaps - (0.25 * interstimuli_timelaps), interstimuli_timelaps + (0.25 * interstimuli_timelaps))
    wait(fc_duration) 
    #### Retrieve the target words from the buffer file
    words_temporary_file = csv.reader(open('BUFFER.csv', 'r'))
    target_words = []
    for word in words_temporary_file: target_words.append(str(word[0]))
    #### Choose between displaying target words or distractors
    typeI_display = 'NaN'
    typeI_display = random.choice([0, 1])
    #### Display the word
    window.fill(gray)
    if typeI_display == 0:
        displayed_word = target_words[0]
        while displayed_word in target_words:
            displayed_word = random.choice(all_words)
        draw_text(str(displayed_word), [W/2, H/2], 100)
    elif typeI_display == 1:
        draw_text(str(random.choice(target_words)), [W/2, H/2], 100)
    #### Display 2AFC
    display_dichotomic_choice('Oui', 'Non', [W/2, H/2 - 200], [W/2, H/2 + 200])
    pygame.display.flip()
    return easiness_index, typeI_display

def Temporal_task(easiness_index):
    #### Precautions for easiness index
    if easiness_index <= 0: easiness_index = 15
    if easiness_index >= 990: easiness_index = 990
    #### Define showing delay
    time_delay = easiness_index
    direction = random.choice([-1, 1])
    time_delay *= direction
    time_delay += interstimuli_timelaps
    #### Draw the circle
    window.fill(gray)
    pygame.draw.circle(window, red, [W/2, H/2], 40)
    pygame.display.flip()
    #### Display it during a certain amount of time
    wait(time_delay)
    #### Record the solution
    typeI_display = 'NaN'
    if time_delay < 1000: typeI_display = 0
    elif time_delay > 1000: typeI_display = 1
    #### Display 2AFC
    window.fill(gray)
    display_dichotomic_choice('> 1s', '< 1s', [W/2, H/2 - 200], [W/2, H/2 + 200])
    pygame.display.flip()    
    return easiness_index, typeI_display

def Gabors_task(easiness_index):
    #### Precautions for easiness index
    if easiness_index <= 0: easiness_index = 0.03
    if easiness_index > .45: easiness_index = .45
    #### Define task parameters
    increasing_contrast = easiness_index
    radius = 150
    gabor_size = 110.0
    gabors_default_contrast = 0.5
    total_number_of_gabors = 6
    #### Define all the gabors' positions (in circle)
    positions = []
    angle = 0
    while angle < 360:
        position = [W/2 + radius*np.cos(np.radians(angle)), H/2 + radius*np.sin(np.radians(angle))]
        positions.append(position)
        angle += (360/total_number_of_gabors)
    random.shuffle(positions)
    #### Randomly choose if there was or more contrasted gabor or not
    typeI_display = 'NaN'
    typeI_display = random.choice([0, 1])
    window.fill(gray)
    #### Draw all the gabors
    gabor_number = 0
    gabor = draw_gabor(size = gabor_size, smooth = 1.5, contrast = gabors_default_contrast, spatial_frequency = 7.0, theta = 45.0)
    while gabor_number < total_number_of_gabors:
        if (typeI_display == 1) and (gabor_number == (total_number_of_gabors - 1)): gabor = draw_gabor(size = gabor_size, smooth = 1.5, contrast = gabors_default_contrast + increasing_contrast, spatial_frequency = 7.0, theta = 45.0)
        #### Blit the just created gabor (i.e. the pygame surface)
        window.blit(gabor, (positions[gabor_number][0] - (gabor_size/2), positions[gabor_number][1] - (gabor_size/2)))
        gabor_number += 1
    pygame.display.flip()
    wait(displaying_time)
    #### Display 2AFC
    window.fill(gray)
    display_dichotomic_choice('Oui', 'Non', [W/2, H/2 - 200], [W/2, H/2 + 200])
    pygame.display.flip()
    return easiness_index, typeI_display

def Crowding_task(easiness_index):
    #### Precautions for easiness index
    if easiness_index <= 0: easiness_index = 3
    if easiness_index > 498: easiness_index = 498
    #### Define task parameters
    time_delay = easiness_index
    #### Define distance from the screen center and the 4 possibles positions
    eccentricity = 200
    positions = [[W/2, H/2 - eccentricity], [W/2, H/2 + eccentricity], [W/2 + eccentricity, H/2], [W/2 - eccentricity, H/2]]
    #### Define the letters and their spacings
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    vertical_spacing = 50
    horizontal_spacing = 43
    #### Create two set of numbers according to their position to 5 and randomize their orders
    digits_inferior = range(1, 5)
    digits_superior = range(6, 10)
    digit_target_list = [1, 2, 3, 4, 6, 7, 8, 9]
    digit_target = digit_target_list[random.randint(0, (len(digit_target_list) - 1))]
    #### Get two random letters to create the mask
    random.shuffle(letters)
    flankers = [letters[0], letters[1]]
    #### Randomly choose a stimulus position among the four possibles
    choosen_position = random.choice(positions)
    #### Draw the target
    window.fill(gray)
    draw_text(str(digit_target), [choosen_position[0], choosen_position[1]], 100)
    pygame.display.flip()
    wait(time_delay)
    window.fill(gray)
    #### Draw the mask
    draw_text(flankers[0], [choosen_position[0] - horizontal_spacing, choosen_position[1]], 100)
    draw_text(flankers[0], [choosen_position[0] + horizontal_spacing, choosen_position[1]], 100)
    draw_text(flankers[1], [choosen_position[0], choosen_position[1] - vertical_spacing], 100)
    draw_text(flankers[1], [choosen_position[0], choosen_position[1] + vertical_spacing], 100)
    pygame.display.flip()
    wait(displaying_time)
    #### Record the solution
    typeI_display = 'NaN'
    if digit_target in digits_inferior: typeI_display = 0
    elif digit_target in digits_superior: typeI_display = 1
    #### Display 2AFC
    window.fill(gray)
    display_dichotomic_choice('> 5', '< 5', [W/2, H/2 - 200], [W/2, H/2 + 200])
    pygame.display.flip()
    return easiness_index, typeI_display

def Reaching_task(easiness_index):
    #### Precautions for easiness index
    if easiness_index <= 0: easiness_index = 50
    if easiness_index > 1500: easiness_index = 1500
    #### Define task parameters
    time_delay = easiness_index
    allowed_error = 20
    eccentricity = int(0.75*(H/2))
    eccentricity = random.randint((eccentricity - 20), (eccentricity + 20))
    #### Define the 4 possible positions and get the target position
    positions = [[W/2 - eccentricity, H/2 - eccentricity], [W/2 + eccentricity, H/2 - eccentricity],
                 [W/2 + eccentricity, H/2 + eccentricity], [W/2 - eccentricity, H/2 + eccentricity]]
    position = random.randint(1, 4)
    target_position = positions[(position - 1)]
    #### Display the target
    window.fill(gray)
    pygame.draw.circle(window, white, target_position, 12)
    pygame.display.flip()
    wait(displaying_time)
    #### Draw fixation cross
    window.fill(gray)
    draw_text('Allez y !', [W/2, H/2], 100) 
    pygame.display.flip()
    #### Move the cursor to the center of the screen and show it during a certain amount of time 
    pygame.mouse.set_pos([W/2, H/2])
    pygame.mouse.set_visible(True)
    wait(time_delay)
    pygame.mouse.set_visible(False)
    #### Get the target location
    typeI_display = position
    #### Get type I answer and RT
    typeI_answer = 'NaN'
    t0 = pygame.time.get_ticks()
    #### Clear the events from the queue
    pygame.event.clear()
    #### If answer is given before 2 s, record the answer
    while (typeI_answer == 'NaN') and ((pygame.time.get_ticks() - t0) <= 2000):
        event = pygame.event.poll()
        if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            #### Get the cursor's position and record the error between the real position and the answered one
            cursor_position = list(pygame.mouse.get_pos())
            error = [(abs(cursor_position[0] - target_position[0])), (abs(cursor_position[1] - target_position[1]))]
            typeI_answer = max(error[0], error[1])
    #### If answer is given before 2 s, record the RT
    if (pygame.time.get_ticks() - t0) <= 2000:
        typeI_RT = pygame.time.get_ticks() - t0
    #### If answer is given before 2 s, display a warning message instead of recording the answer and the RT 
    if (pygame.time.get_ticks() - t0) > 2000:
        typeI_RT = 'NaN'
        window.fill(gray)
        draw_text('Trop lent !', [W/2, H/2], 100)
        pygame.display.flip()
        wait(interstimuli_timelaps)
    #### Get solution according to the allowed error
    if typeI_answer <= allowed_error: typeI_correction = 1
    if (typeI_answer == 'NaN') or (typeI_answer > allowed_error): typeI_correction = 0
    return easiness_index, typeI_display, typeI_answer, typeI_correction, typeI_RT

def display_instructions(typeI_task, training):
    #### Instructions for MDT task
    if typeI_task == 1:
        instructions = [u"Vous allez voir un certain nombre de cercles",
                        u"de couleurs différentes disposés de manière différente.",
                        u"Essayez de vous souvenir au mieux de cet écran car il",
                        u"vous sera par la suite présenté un seul cercle d'une certaine",
                        u"couleur et dans une position particulière. Vous devrez alors",
                        u"dire si ce cercle (de cette couleur et dans cette position)",
                        u"était présent ou non dans le premier écran."]
    #### Instructions for MLT task
    if typeI_task == 2:
        instructions = [u"Vous allez voir une liste de mots. Essayez de vous en souvenir",
                        u"au mieux car il vous sera ensuite successivement présenté des",
                        u"mots dont vous devrez dire s'ils étaient présents, ou non,",
                        u"dans la liste initialement présenté. Il vous sera régulièrement",
                        u"présentées de nouvelles listes, vous ne devrez vous rappeler",
                        u"que de la dernière liste."]
    #### Instructions for temporal task
    if typeI_task == 3:
        instructions = [u"Vous allez voir un cercle noir présenté à l'écran pendant",
                        u"un certain temps. Essayez d'être le(la) plus attentif(ve)",
                        u"possible à sa durée de présentation car il vous sera par",
                        u"la suite demandé de dire si le cercle en question était",
                        u"presenté pendant plus ou moins d'une seconde."]
    #### Instructions for gabors task
    if typeI_task == 4:
        instructions = [u"Vous allez voir 6 cercles zebrés présentés en cercle. Essayez",
                        u"d'y être le(la) plus attentif(ve) car il vous sera aussitôt",
                        u"demandé si un des 6 cercles en question était plus contrasté",
                        u"(effet de brillance) que les autres, ou non.",]
    #### Instructions for crowding task
    if typeI_task == 5:
        instructions = [u"Vous allez voir un chiffre apparaitre sur l'écran puis très",
                        u"rapidement être caché par des lettres. Essayez d'être le(la)",
                        u"plus attentif(ve) possible à ce chiffre car il vous sera par",
                        u"la suite demandé de dire si le chiffre en question était plus",
                        u"grand ou plus petit que cinq."]
    #### Instructions for reaching task
    if typeI_task == 6:
        instructions = [u"Vous allez voir un cercle rapidement presenté dans l'un des",
                        u"quatre coins de l'écran. Essayez d'y etre le(la) plus",
                        u"attentif(ve) possible car il vous sera aussitôt demandé de",
                        u"cliquer avec la souris sur la position de ce point. Soyez rapide",
                        u"(car le curseur de la souris à une durée d'affichage limitée) et précis(e).",
                        u"Merci de remettre la souris dans sa position intiale après chaque essai."]
    window.fill(gray)
    #### Display items type (i.e. training or not)
    if training == 0: draw_text((str(trials_per_task) + " " + u"ESSAIS DIVISÉS EN 2 BLOCKS"), [W/2, H/2 - 300], 30)
    elif training == 1: draw_text((str(training_trials_per_task) + " " + u"ESSAIS D'ENTRAINEMENT"), [W/2, H/2 - 300], 30)
    #### Walk back in the instructions list to fully display the type I instruction on the top of the screen
    lign = len(instructions) - 1
    vertical_position = H/2 - 30
    while lign >= 0:
        draw_text(instructions[lign], [W/2, vertical_position], 30)
        lign -= 1
        vertical_position -= 30
    #### Instructions for metacognitive step
    instructions = [u"Vous devrez ensuite juger de la confiance que vous",
                    u"avez dans votre réponse en utilisant une échelle : ",
                    u"de 1 (très peu confiant) à 6 (absolument sûr).",
                    u"N'oubliez pas d'utiliser l'ensemble de l'échelle",
                    u"(de 1 à 6) pour rapporter votre confiance.",
                    u"Utilisez toujours votre main droite pour répondre à la",
                    u"tâche, et votre main gauche pour donner votre confiance."]
    lign = 0
    vertical_position = H/2 + 30
    #### Walk in the consigns list to fully display the metacognitive consign on the back of the screen
    while lign <= (len(instructions) - 1):
        draw_text(instructions[lign], [W/2, vertical_position], 30)
        lign += 1
        vertical_position += 30
    #### Display instructions to begin the task
    draw_text(u"Appuyez sur ESPACE quand vous êtes prêt(e).", [W/2, H/2 + 300], 30)
    #### Display all these instructions
    pygame.display.flip()
    #### Clear the events from the queue
    pygame.event.clear()
    #### Check the events and begin the task when spacebar is pressed
    while True:
        for ev in pygame.event.get():            
            if (ev.type == KEYDOWN) and (ev.key == K_SPACE): return

def display_typeI_task(typeI_task, easiness_index):
    #### Display one of the 6 type I task
    if typeI_task == 1: (easiness_index, typeI_display) = MDT_task(easiness_index)
    if typeI_task == 2: (easiness_index, typeI_display) = MLT_task(easiness_index)
    if typeI_task == 3: (easiness_index, typeI_display) = Temporal_task(easiness_index)
    if typeI_task == 4: (easiness_index, typeI_display) = Gabors_task(easiness_index)
    if typeI_task == 5: (easiness_index, typeI_display) = Crowding_task(easiness_index)
    if typeI_task == 6: (easiness_index, typeI_display, typeI_answer, typeI_correction, typeI_RT) = Reaching_task(easiness_index)
    typeI_label = 5
    #### For each task except for the reaching motor one
    if typeI_task in [1, 2, 3, 4, 5]:
        #### Get answer and RT
        (typeI_answer, typeI_RT) = get_typeI_answer_and_RT()
        #### Get correction
        if typeI_answer == typeI_display: typeI_correction = 1
        elif typeI_answer != typeI_display: typeI_correction = 0
        #### Get label
        if (typeI_display == 1) and (typeI_answer == 1): typeI_label = 1 # Hit
        if (typeI_display == 0) and (typeI_answer == 1): typeI_label = 2 # False alarm
        if (typeI_display == 1) and (typeI_answer == 0): typeI_label = 3 # Miss
        if (typeI_display == 0) and (typeI_answer == 0): typeI_label = 4 # Correct reject
    return easiness_index, typeI_display, typeI_answer, typeI_correction, typeI_label, typeI_RT

def get_typeI_answer_and_RT():
    typeI_answer = 'NaN'
    typeI_RT = 'NaN'
    t0 = pygame.time.get_ticks()
    #### Clear the events from the queue
    pygame.event.clear()
    #### Get answer with right keys
    while (typeI_answer == 'NaN') and ((pygame.time.get_ticks() - t0) <= 5000):
        for ev in pygame.event.get():            
            if ev.type == KEYDOWN:
                if ev.key == K_UP: typeI_answer = 1
                elif ev.key == K_DOWN: typeI_answer = 0
    #### If answer is given before 2 s, record it (and the RT) then provide feedback (only for the answer)
    if (pygame.time.get_ticks() - t0) <= 5000:
        typeI_RT = (pygame.time.get_ticks() - t0)
        feedbackpos = [150, -250]
        pygame.draw.rect(window, red, pygame.Rect(W/2 - 80, H/2 + feedbackpos[typeI_answer], 160, 100), 5)
        pygame.display.flip()
    #### If confidence is given after 2 s, display a warning message
    elif (pygame.time.get_ticks() - t0) > 5000:
        window.fill(gray)
        draw_text('Trop lent !', [W/2, H/2], 100)
        pygame.display.flip()
    wait(interstimuli_timelaps)
    return typeI_answer, typeI_RT

def display_dichotomic_choice(first_possibility, second_possibility, first_possibility_poistion, second_possibility_position):
    #### Create 2AFC answers
    draw_text(first_possibility, first_possibility_poistion, 100)
    draw_text(second_possibility, second_possibility_position, 100)
    return
    
def display_typeII_task():
    #### Display the metacognitive scale
    window.fill(gray)
    digit = 1
    digit_pos = -250
    while digit <= 6:
        draw_text(str(digit), [W/2 + digit_pos, H/2], 100)
        digit += 1
        digit_pos += 100        
    pygame.display.flip()
    typeII_answer = 'NaN'
    typeII_RT = 'NaN'
    t0 = pygame.time.get_ticks()
    #### Clear the events from the queue
    pygame.event.clear()
    while (typeII_answer == 'NaN') and ((pygame.time.get_ticks() - t0) <= 10000):
        #### Get confidence score with left keys
        for ev in pygame.event.get():
            if ev.type == KEYDOWN:
                if ev.key == K_1: typeII_answer = 1
                if ev.key == K_2: typeII_answer = 2
                if ev.key == K_3: typeII_answer = 3
                if ev.key == K_4: typeII_answer = 4
                if ev.key == K_5: typeII_answer = 5
                if ev.key == K_6: typeII_answer = 6
    #### If confidence is given before 3,5 s, record it (and the RT) then provide feedback (only for confidence)
    if (pygame.time.get_ticks() - t0) <= 10000:
        typeII_RT = (pygame.time.get_ticks() - t0)
        feedback_position = [0, -300, -200, -100, 0, 100, 200]
        pygame.draw.rect(window, red, pygame.Rect(W/2 + feedback_position[typeII_answer], H/2 - 50, 100, 100), 5)
        pygame.display.flip()
    #### If confidence is given after 3,5 s ...
    elif (pygame.time.get_ticks() - t0) > 10000:
        #### Record 7 if type I answer was given before 2 s but type II answer was not given before 3,5 s (this allowed ROC curves plots)
        typeII_answer = 7
        #### Display a warning message
        window.fill(gray)
        draw_text('Trop lent !', [W/2, H/2], 100)
        pygame.display.flip()
    wait(interstimuli_timelaps)
    return typeII_answer, typeII_RT

def display_metacognitive_questionnaire(subject_initials, subject_number, subject_genre, subject_age, subject_handedness):
    #### Define instructions
    instructions = [u"Des propositions vont vous être successivement présentées,",
                    u"vous devrez simplement y répondre en suivant la classification",
                    u"présentée ci-dessous (de pas du tout d'accord à tout à fait d'accord)."]
    Lickert_scale = [u"1 - Pas du tout d'accord",
                     u"2 - Pas d'accord",
                     u"3 - Ni en désaccord ni d'accord",
                     u"4 - D'accord",
                     u"5 - Tout à fait d'accord"]
    window.fill(gray)
    #### Display the title
    draw_text(u"QUESTIONNAIRE METACOGNITIF", [W/2, H/2 - 300], 30)
    #### Walk back in the first instructions list to fully display the first part of the instructions on the top of the screen
    lign_1 = len(instructions) - 1
    vertical_position = H/2 - 30
    while lign_1 >= 0:
        draw_text(instructions[lign_1], [W/2, vertical_position], 30)
        lign_1 -= 1
        vertical_position -= 30
    #### Walk in the second instructions list to fully display the second part of the instructions on the bottom of the screen
    lign_2 = 0
    vertical_position = H/2 + 30
    while lign_2 <= (len(Lickert_scale) - 1):
        draw_text(Lickert_scale[lign_2], [W/2, vertical_position], 30)
        lign_2 += 1
        vertical_position += 30
    #### Display instructions to begin the task
    draw_text(u"Appuyez sur ESPACE quand vous êtes prêt(e).", [W/2, H/2 + 300], 30)
    #### Display all these instructions
    pygame.display.flip()
    #### Clear the events from the queue
    pygame.event.clear()
    #### Check the events and begin the task when spacebar is pressed
    start = 0
    while start == 0:
        for ev in pygame.event.get():            
            if (ev.type == KEYDOWN) and (ev.key == K_SPACE): start = 1
    #### Record headings
    if context == 0: questionnaire_file_name = 'QUESTIONNAIRE' + '_' + subject_initials + '_' + subject_number + '.dat'
    elif context == 1: questionnaire_file_name = subject_initials + str(subject_number) + '_' + subject_genre + subject_age + subject_handedness  + '_' + 'QUESTIONNAIRE' + '.dat'
    questionnaire_file = open(questionnaire_file_name, 'a')
    print >> questionnaire_file, 'SUBJECT_INITIALS', 'SUBJECT_NUMBER', 'QUESTIONNAIRE', 'SUB-SCALE', 'ITEM', 'QUESTIONNAIRE_ANSWER', 'QUESTIONNAIRE_RT'
    questionnaire_file.close()
    #### Define the Lickert scale
    answers = [[1, u"Pas du tout d'accord"], [2, u"Pas d'accord"], [3, u"Ni en désaccord ni d'accord"], [4, u"D'accord"], [5, u"Tout à fait d'accord"]]
    #### For each question
    questionnaire = csv.reader(open('QUESTIONNAIRES.csv', 'rb'), delimiter = ';')
    for question in questionnaire:
        #### Display a fixation cross
        window.fill(gray)
        draw_fixation_cross()
        pygame.display.flip()
        wait(interstimuli_timelaps)
        #### Display question
        window.fill(gray)
        draw_text(str(question[5]), [W/2, H/2 - 100], 25)
        #### Display the 5 possible answers
        answer_position = -300
        answer = 0
        while answer <= (len(answers) - 1):
            draw_text(str(answers[answer][0]), [W/2 + answer_position, H/2 + 100], 100)
            draw_text(answers[answer][1], [W/2 + answer_position, H/2 + 200], 15)
            answer_position += 150
            answer += 1
        pygame.display.flip()
        questionnaire_answer = 'NaN'
        t0 = pygame.time.get_ticks()
        #### Clear the events from the queue
        pygame.event.clear()
        #### Get participant's answer with left keys (Lickert scale)
        while questionnaire_answer == 'NaN':
            for ev in pygame.event.get():
                if ev.type == KEYDOWN:
                    if ev.key == K_1: questionnaire_answer = 1
                    if ev.key == K_2: questionnaire_answer = 2
                    if ev.key == K_3: questionnaire_answer = 3
                    if ev.key == K_4: questionnaire_answer = 4
                    if ev.key == K_5: questionnaire_answer = 5
        questionnaire_RT = (pygame.time.get_ticks() - t0)
        #### Provide feedback
        feedback_position = [0, -350, -200, -50, 100, 250]
        pygame.draw.rect(window, red, pygame.Rect(W/2 + feedback_position[questionnaire_answer], H/2 + 50, 100, 100), 5)
        pygame.display.flip()
        wait(interstimuli_timelaps)
        #### Save the result in the output file
        questionnaire_file = open(questionnaire_file_name, 'a')
        print >> questionnaire_file, subject_initials, subject_number, question[2], question[3], question[4], questionnaire_answer, questionnaire_RT
        questionnaire_file.close()
    return

def two_random_trials():
    #### If there is an only one task, randomly choose trials like this
    random_task_1 = 0
    while random_task_1 == 0: random_task_1 = random.choice(typeI_tasks)
    random_trial_1 = random.randint(1, trials_per_task)
    random_task_2 = random_task_1
    random_trial_2 = random_trial_1
    #### If there is more than one type I task, randomly choose trials like this 
    if (len(typeI_tasks) - 1) > 1:
        while (random_task_2 == random_task_1) or (random_task_2 == 0): random_task_2 = random.choice(typeI_tasks)
    if trials_per_task > 1:
        while random_trial_2 == random_trial_1: random_trial_2 = random.randint(1, trials_per_task)
    return random_task_1, random_trial_1, random_task_2, random_trial_2

def record_compensation_trials(typeI_task, trial, typeI_correction, typeII_answer):
    #### Record temporary data that we will need to compute the compensation
    compensation_file = open('COMPENSATION.txt', 'a')
    print >> compensation_file, typeI_task, trial, typeI_correction, typeII_answer
    compensation_file.close()
    return compensation_file

def display_compensation(random_task_1, random_trial_1, random_task_2, random_trial_2):
    #### Define compensations
    baseline_compensation = 10
    bonus_compensations = 5
    #### Collect confidence data from the two randomly choosen trials on which the compensation will be based
    typeI_corrections = []
    confidences = []
    compensation_file = open('COMPENSATION.txt', 'r')
    for ligne in compensation_file:
        data = ligne.split()
        typeI_corrections.append(int(data[2]))
        confidence = data[3]
        if confidence != 'NaN': confidences.append(int(data[3]))
        elif confidence == 'NaN': confidences.append(data[3])
    compensation_file.close()
    #### If the subject did not gave his confidence for one of the two trials on which the compensation is based, then do not provide money
    if (confidences[0] == 7) or (confidences[0] == 'NaN'):
        gain_1 = 0
        (first_dice_1, second_dice_1, lottery_1) = ('NaN', 'NaN', 'NaN')
    if (confidences[1] == 7) or (confidences[1] == 'NaN'):
        gain_2 = 0
        (first_dice_2, second_dice_2, lottery_2) = ('NaN', 'NaN', 'NaN')
    #### Make the first roll dice
    if confidences[0] in [1, 2, 3, 4, 5, 6]:
        first_dice_1 = random.randint(1, 6)
        second_dice_1 = random.randint(1, 6)
        if confidences[0] >= first_dice_1:
            lottery_1 = confidences[0]
            if typeI_corrections[0] == 1: gain_1 = bonus_compensations
            elif typeI_corrections[0] == 0: gain_1 = 0
        elif confidences[0] < first_dice_1:
            lottery_1 = first_dice_1
            if second_dice_1 <= lottery_1: gain_1 = bonus_compensations
            elif second_dice_1 > lottery_1: gain_1 = 0
    #### Make the second roll dice
    if confidences[1] in [1, 2, 3, 4, 5, 6]: 
        first_dice_2 = random.randint(1, 6)
        second_dice_2 = random.randint(1, 6)
        if confidences[1] >= first_dice_2:
            lottery_2 = confidences[1]
            if typeI_corrections[1] == 1: gain_2 = bonus_compensations
            elif typeI_corrections[1] == 0: gain_2 = 0
        elif confidences[1] < first_dice_2:
            lottery_2 = first_dice_2
            if second_dice_2 <= lottery_2: gain_2 = bonus_compensations
            elif second_dice_2 > lottery_2: gain_2 = 0
    #### Sum the two gains (coming from the two dice rolls)
    gain = gain_1 + gain_2
    total_gain = baseline_compensation + gain
    #### Save money data in the GAINS file
    gain_file = open('GAINS.txt', 'w')
    print >> gain_file, subject_initials, subject_number, random_task_1, random_trial_1, typeI_corrections[0], confidences[0], first_dice_1, second_dice_1, lottery_1, gain_1, random_task_2, random_trial_2, typeI_corrections[1], confidences[1], first_dice_2, second_dice_2, lottery_2, gain_2, total_gain
    gain_file.close()
    #### Display the final screen during 5 minutes
    window.fill(gray)
    draw_text(u"Merci d'avoir participé.", [W/2, H/2 - 100], 50)
    draw_text((u"Vous avez gagné : " + str(baseline_compensation) + u"€ + " + str(gain) + u"€."), [W/2, H/2], 50)
    draw_text(u"Vous pouvez maintenant venir chercher vos", [W/2, H/2 + 100], 50)
    draw_text(u"gains dans la salle de contrôle.", [W/2, H/2 + 150], 50)
    pygame.display.flip()
    wait(300000)
    return
        
######################################################### LAUNCH PROGRAM ##########################################################

try:
    (context, subject_initials, subject_number, subject_genre, subject_age, subject_handedness, typeI_tasks, metacognitive_questionnaire, recording_file_name, output_file) = create_file(1)
    pygame.init()
    #### Create a fullscreen window and get its size
    '''window = pygame.display.set_mode([W, H], DOUBLEBUF)'''
    window = pygame.display.set_mode([1024, 768], FULLSCREEN | DOUBLEBUF | HWSURFACE)
    W, H = window.get_size()

    #### Get two random trials that we will use to quantify the compensation (only for LEEP sessions)
    if context == 0: (random_task_1, random_trial_1, random_task_2, random_trial_2) = two_random_trials()

    #### Mask the cursor during all the experiment (except during certain period of the reaching task)
    pygame.mouse.set_visible(False)

    task = 1
    while task <= (len(typeI_tasks) - 1):

        #### Define a default value (different for each type I task) for easiness index
        (actualized_list, easiness_index) = baseline()
        trial = 1
        training_trial = 1
        while (trial < (trials_per_task + 1)) or (training_trial < (training_trials_per_task + 1)):

            #### Switch to recording trials whan all the training ones have been displayed, and reset the log-list
            if (training_trials_per_task > 0) and (training_trial <= training_trials_per_task):
                subtype = 'TRAINING'
                if training_trial == 1: display_instructions(typeI_tasks[task], 1)
            if (training_trials_per_task == 0) or (training_trial > training_trials_per_task):
                subtype = 'RECORDING'
                if trial == 1:
                    display_instructions(typeI_tasks[task], 0)
                    (actualized_list, easiness_index) = baseline()
                
            #### Display a fixation cross
            window.fill(gray)
            draw_fixation_cross()
            pygame.display.flip()
            #### During a random delay to prevent from learning
            fc_duration = random.randint(interstimuli_timelaps - (0.25 * interstimuli_timelaps), interstimuli_timelaps + (0.25 * interstimuli_timelaps))
            wait(fc_duration)
            
            #### Display type I task and get answer
            (easiness_index, typeI_display, typeI_answer, typeI_correction, typeI_label, typeI_RT) = display_typeI_task(typeI_tasks[task], easiness_index)
            #### Display the metacognitive step only if type I answer was received in time, otherwise save 'NaN'
            if typeI_answer != 'NaN': (typeII_answer, typeII_RT) = display_typeII_task()
            if typeI_answer == 'NaN': (typeII_answer, typeII_RT) = ('NaN', 'NaN')
                
            #### Save data only for recording trials
            if subtype == 'RECORDING':
                output_file = open(recording_file_name, 'a')
                print >> output_file, subject_initials, subject_number, typeI_tasks[task], trial, easiness_index, typeI_display, typeI_answer, typeI_label, typeI_correction, typeI_RT, typeII_answer, typeII_RT
                output_file.close()

            #### Add performances and difficulty (i.e. easiness index) level in a list and modulate the difficulty at each trial according to that list
            actualized_list.append([typeI_correction, easiness_index])
            if (actualized_list[len(actualized_list) - 1][0]) == 0: easiness_index = staircase_method(-1, easiness_index)
            if (actualized_list[len(actualized_list) - 1][0]) == 1: 
                if (actualized_list[len(actualized_list) - 2][0]) == 1: easiness_index = staircase_method(1, easiness_index)
                elif (actualized_list[len(actualized_list) - 2][0]) == 1: easiness_index = staircase_method(0, easiness_index)

            #### Display a break screen when reaching half of trial, but only for recording ones (i.e. not for training)
            if (subtype == 'RECORDING') and (trial == (trials_per_task/2)): break_screen()

            #### Save two random trials in order to compute the amount of compensations (only for LEEP sessions)
            if (context == 0) and (subtype == 'RECORDING') and (((typeI_tasks[task] == random_task_1) and (trial == random_trial_1)) or ((typeI_tasks[task] == random_task_2) and (trial == random_trial_2))): record_compensation_trials(typeI_tasks[task], trial, typeI_correction, typeII_answer)

            if subtype == 'TRAINING': training_trial += 1 
            if subtype == 'RECORDING': trial += 1
        task += 1

    #### Display the metacognitive questionnaire
    if metacognitive_questionnaire == 'Y': display_metacognitive_questionnaire(subject_initials, subject_number, subject_genre, subject_age, subject_handedness)

    #### Roll two dice for each randomly choosen trial in order to get the compensation we have to give to the subject (only for LEEP sessions)
    if context == 0: display_compensation(random_task_1, random_trial_1, random_task_2, random_trial_2)
    
finally:
    try: output_file.close()
    except: pass
    pygame.quit()
