"""Geometric mouth-motion logic adapted from the original prototype.

Input: one landmark dictionary from face_recognition.face_landmarks().
The threshold is historical and has not been clinically validated.
"""

from math import dist
from typing import Mapping, Sequence

Point = tuple[int, int]
Landmarks = Mapping[str, Sequence[Point]]

MOUTH_OPEN_THRESHOLD = 0.35


def mouth_geometry(landmarks: Landmarks) -> tuple[float, float]:
    """Calculate mouth height and width from the original landmark indices."""
    top = landmarks["top_lip"]
    bottom = landmarks["bottom_lip"]

    # Historical opening measurement: two vertical upper/lower lip pairs.
    height = sum(dist(top[i], bottom[18 - i]) for i in (8, 10))

    # Original width pairs are symmetric; use Euclidean rather than x-only distance.
    width = dist(top[7], top[11])
    return height, width


def mouth_aspect_ratio(landmarks: Landmarks) -> float:
    """Compute height / (2 * width); return zero for degenerate width."""
    height, width = mouth_geometry(landmarks)
    return height / (2.0 * width) if width > 0 else 0.0


def is_mouth_open(
    landmarks: Landmarks, threshold: float = MOUTH_OPEN_THRESHOLD
) -> bool:
    """Classify mouth opening using a prototype-derived threshold."""
    return mouth_aspect_ratio(landmarks) > threshold
