import math
from threading import Thread
import numpy as np



def get_lip_height(lip):
    # distance between two near points up and down
    distance = [math.sqrt((lip[i][0] - lip[12 - i][0]) ** 2 + (lip[i][1] - lip[12 - i][1]) ** 2) for i in [2, 3, 4]]
    summ = sum(distance)
    return summ / 3


def get_horizontal_mouth_distance(lip):

    distance = [math.sqrt((lip[i][0] - lip[18 - i][0]) ** 2 + (lip[i][0] - lip[18 - i][0]) ** 2) for i
                in [7, 11]]
    summ = sum(distance)
    return summ / 2


def get_mouth_height(top_lip, bottom_lip):

    # distance between two near points up and down
    distance = [math.sqrt((top_lip[i][0] - bottom_lip[18 - i][0]) ** 2 + (top_lip[i][1] - bottom_lip[18 - i][1]) ** 2)
                for i in [8, 10]]
    summ = sum(distance)
    return summ

def get_distance(cheek):

    # distance between two near points up and down
    for i in [0]:
        # distance between two near points up and down
        distance1 = math.sqrt( (cheek[i][0] - cheek[1-i][0])**2 +
                              (cheek[i][1] - cheek[1-i][1])**2)
    #
    for i in [1]:
        # distance between two near points up and down
        distance2 = math.sqrt( (cheek[i][0] - cheek[4-i][0])**2 +
                              (cheek[i][1] - cheek[4-i][1])**2)
    #
    for i in [2]:
        # distance between two near points up and down
        distance3 = math.sqrt( (cheek[i][0] - cheek[5-i][0])**2 +
                              (cheek[i][1] - cheek[5-i][1])**2)

    return distance1,distance2,distance3

def cheek_right_distance(face_landmarks):
    left_cheek = face_landmarks["left_cheek"]
    left_cheek_distance = get_distance(left_cheek)

    right_cheek = face_landmarks["right_cheek"]
    right_cheek_distance = get_distance(right_cheek)

    ratio = 1.5
    if left_cheek_distance[1] > right_cheek_distance[1]  * ratio:
        return True
    else:
        return False

def cheek_left_distance(face_landmarks):
    left_cheek = face_landmarks["left_cheek"]
    left_cheek_distance = get_distance(left_cheek)

    right_cheek = face_landmarks["right_cheek"]
    right_cheek_distance = get_distance(right_cheek)

    ratio = 1.5
    if right_cheek_distance[1] > left_cheek_distance[1] * ratio:
        return True
    else:
        return False

def is_mouth_open(face_landmarks):

    top_lip = face_landmarks['top_lip']
    bottom_lip = face_landmarks['bottom_lip']

    A = get_mouth_height(top_lip, bottom_lip)
    C = get_horizontal_mouth_distance(top_lip)

    mar = A / (2.0 * C)
    # if mouth is open more than lip height * ratio, return true.
    mouth = 0.35
    if mar > mouth:
        return True
    else:
        return False


def check_horizontal(face_landmarks):

    top_lip = face_landmarks['top_lip']
    bottom_lip = face_landmarks['bottom_lip']

    top_lip_height = get_lip_height(top_lip)
    bottom_lip_height = get_lip_height(bottom_lip)

    mouth_horizontal = get_horizontal_mouth_distance(top_lip)
    mouth_height = get_mouth_height(top_lip, bottom_lip)

    ratio1 = 2
    ratio2 = 1
    if mouth_horizontal > max(top_lip_height, bottom_lip_height) * 5 * ratio1 and mouth_height > max(top_lip_height,
                                                                                                     bottom_lip_height) * ratio2:
        return True
    else:
        return False

