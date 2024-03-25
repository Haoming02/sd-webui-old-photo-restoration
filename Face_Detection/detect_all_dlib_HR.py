# Copyright (c) Microsoft Corporation

from skimage.transform import SimilarityTransform
from matplotlib.patches import Rectangle
from skimage.transform import warp
from skimage import img_as_ubyte
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import dlib
import os


def _standard_face_pts():
    pts = (
        np.array(
            [196.0, 226.0, 316.0, 226.0, 256.0, 286.0, 220.0, 360.4, 292.0, 360.4],
            np.float32,
        )
        / 256.0
        - 1.0
    )

    return np.reshape(pts, (5, 2))


def get_landmark(face_landmarks, id):
    part = face_landmarks.part(id)
    x = part.x
    y = part.y

    return (x, y)


def search(face_landmarks):

    x1, y1 = get_landmark(face_landmarks, 36)
    x2, y2 = get_landmark(face_landmarks, 39)
    x3, y3 = get_landmark(face_landmarks, 42)
    x4, y4 = get_landmark(face_landmarks, 45)

    x_nose, y_nose = get_landmark(face_landmarks, 30)

    x_left_mouth, y_left_mouth = get_landmark(face_landmarks, 48)
    x_right_mouth, y_right_mouth = get_landmark(face_landmarks, 54)

    x_left_eye = int((x1 + x2) / 2)
    y_left_eye = int((y1 + y2) / 2)
    x_right_eye = int((x3 + x4) / 2)
    y_right_eye = int((y3 + y4) / 2)

    results = np.array(
        [
            [x_left_eye, y_left_eye],
            [x_right_eye, y_right_eye],
            [x_nose, y_nose],
            [x_left_mouth, y_left_mouth],
            [x_right_mouth, y_right_mouth],
        ]
    )

    return results


def compute_transformation_matrix(img, landmark, normalize, target_face_scale=1.0):

    std_pts = _standard_face_pts()  # [-1,1]
    target_pts = (std_pts * target_face_scale + 1) / 2 * 512.0

    # print(target_pts)

    h, w, c = img.shape
    if normalize == True:
        landmark[:, 0] = landmark[:, 0] / h * 2 - 1.0
        landmark[:, 1] = landmark[:, 1] / w * 2 - 1.0

    # print(landmark)

    affine = SimilarityTransform()

    affine.estimate(target_pts, landmark)

    return affine.params


def show_detection(image, box, landmark):
    plt.imshow(image)
    print(box[2] - box[0])
    plt.gca().add_patch(
        Rectangle(
            (box[1], box[0]),
            box[2] - box[0],
            box[3] - box[1],
            linewidth=1,
            edgecolor="r",
            facecolor="none",
        )
    )
    plt.scatter(landmark[0][0], landmark[0][1])
    plt.scatter(landmark[1][0], landmark[1][1])
    plt.scatter(landmark[2][0], landmark[2][1])
    plt.scatter(landmark[3][0], landmark[3][1])
    plt.scatter(landmark[4][0], landmark[4][1])
    plt.show()


def affine2theta(affine, input_w, input_h, target_w, target_h):
    # param = np.linalg.inv(affine)
    param = affine
    theta = np.zeros([2, 3])
    theta[0, 0] = param[0, 0] * input_h / target_h
    theta[0, 1] = param[0, 1] * input_w / target_h
    theta[0, 2] = (
        2 * param[0, 2] + param[0, 0] * input_h + param[0, 1] * input_w
    ) / target_h - 1
    theta[1, 0] = param[1, 0] * input_h / target_w
    theta[1, 1] = param[1, 1] * input_w / target_w
    theta[1, 2] = (
        2 * param[1, 2] + param[1, 0] * input_h + param[1, 1] * input_w
    ) / target_w - 1
    return theta


def detect_hr(input_image: Image) -> list:
    face_detector = dlib.get_frontal_face_detector()
    detected_faces = []

    landmark = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "shape_predictor_68_face_landmarks.dat",
    )
    landmark_locator = dlib.shape_predictor(landmark)

    image = np.array(input_image)
    faces = face_detector(image)

    if len(faces) == 0:
        return detected_faces

    for face_id in range(len(faces)):

        current_face = faces[face_id]
        face_landmarks = landmark_locator(image, current_face)
        current_fl = search(face_landmarks)

        affine = compute_transformation_matrix(
            image, current_fl, False, target_face_scale=1.3
        )

        aligned_face = warp(image, affine, output_shape=(512, 512, 3))
        detected_faces.append(Image.fromarray(img_as_ubyte(aligned_face)))

    return detected_faces
