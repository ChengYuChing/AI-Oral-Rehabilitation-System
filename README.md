# AI-Based Oral Rehabilitation System

A real-time computer vision application for facial motion recognition and interactive oral rehabilitation.

**Tech Stack:** Python · OpenCV · MediaPipe · face_recognition · PyQt5

## Overview

This project implements facial motion recognition for interactive oral rehabilitation. It processes live webcam input, extracts facial landmarks, and uses geometric features and threshold-based rules to detect oral movements. A PyQt5 interface connects motion detection with visual feedback, exercise timing, and repetition tracking.

## Technical Approach

```text
Webcam Input
     ↓
Face & Facial Landmark Detection
     ↓
Mouth and Cheek Feature Extraction
     ↓
Rule-Based Motion Recognition
     ↓
Real-Time GUI Feedback
```

- **Facial landmarks:** Processes webcam frames with MediaPipe Face Mesh and the `face_recognition` landmark interface.
- **Geometric features:** Calculates mouth opening, horizontal mouth measurements, and relative cheek distances.
- **Motion recognition:** Uses geometric ratios and thresholds to identify mouth-opening, horizontal mouth movement, and cheek movements.
- **Application integration:** Displays camera frames and recognition feedback in a PyQt5 application.

## Key Features

| Feature | Description |
| --- | --- |
| Real-Time Face Tracking | Processes webcam frames and overlays facial landmarks. |
| Motion Recognition | Detects selected mouth and cheek movements using geometric measurements. |
| Interactive GUI | Connects webcam processing and exercise controls through PyQt5. |
| Exercise Tracking | Includes timers, repetition counting, and on-screen scores. |
| Visual Feedback | Displays real-time tracking and exercise information. |

**Code:** `main.py` is adapted from the original `main_V2.py`; `mouth_function.py` contains the geometric motion-detection logic, and `Mouth.ui` defines the Qt interface.

**Note:** This is a preserved portfolio version of a prototype. The original application references optional local instructional videos (`1.mov`, `2.mov`, `3.mp4`) and a logo image (`logo (9).png`) that are not included here. The complete GUI workflow and dependencies have not been revalidated in a clean environment.
