# AI-Based Oral Rehabilitation System

**Project:** Real-time, landmark-based mouth movement recognition for oral rehabilitation.

**Focus:** Computer vision · geometric feature engineering · rule-based recognition · real-time Python application

---

## Project at a Glance

| Workstream | Core Challenge | Engineering Approach | Outcome |
|---|---|---|---|
| **P1 — Problem Definition** | Oral movements must be expressed as measurable inputs | Frame mouth opening as a geometric landmark task | A concrete recognition criterion |
| **P2 — Feature Extraction** | Webcam frames are not directly usable as motion measurements | Extract lip landmarks and compute height and width | Numerical mouth geometry |
| **P3 — Motion Recognition** | Geometry must be mapped to a movement state | Calculate a mouth aspect ratio and apply a threshold | Open/closed classification |
| **P4 — Real-Time Integration** | The algorithm needs a live input and observable result | Connect webcam capture, landmark extraction, and text overlay | Minimal interactive OpenCV application |

---

## End-to-End System Overview

```mermaid
flowchart LR
    A["P1 · Define Mouth Movement"] --> B["Webcam Input"]
    B --> C["P2 · Lip Landmark Extraction"]
    C --> D["Mouth Height & Width"]
    D --> E["P3 · Aspect Ratio + Threshold"]
    E --> F["P4 · Real-Time OpenCV Feedback"]
```

**Storyline:** define a measurable movement → extract geometry from camera frames → classify mouth opening → display results in real time.

---

## Project Details

### P1 — Problem Definition

> **Key Question —** How can a mouth-opening exercise be expressed as a measurable computer vision task?

The original rehabilitation prototype explored multiple oral movements. This repository deliberately isolates **mouth opening** as a small, inspectable algorithm example rather than publishing the entire legacy GUI and exercise workflow.

**Takeaway:** Narrow the movement definition to one clear and reproducible recognition task.

### P2 — Facial Feature Extraction

> **Key Question —** How can a video frame be converted into numerical features?

- Read frames from a webcam using **OpenCV**.
- Extract facial landmark coordinates with `face_recognition.face_landmarks()`.
- Compute mouth opening and width from selected upper and lower lip landmark pairs.

**Takeaway:** Separate landmark extraction from downstream movement classification.

### P3 — Motion Recognition

> **Key Question —** How can facial geometry determine whether the mouth is open?

The original prototype used a mouth ratio computed from lip landmark distances. The simplified implementation retains the same conceptual rule while correcting the original width-distance calculation to use Euclidean distance:

```text
mouth_ratio = mouth_height / (2 × mouth_width)
mouth_open = mouth_ratio > 0.35
```

- **Input:** Upper and lower lip landmarks.
- **Feature:** Mouth-height-to-width ratio.
- **Output:** Boolean mouth-open state.

The threshold **0.35** was inherited from the original prototype. It is not presented as clinically validated or as a benchmarked accuracy result.

**Takeaway:** Build interpretable recognition logic from measurable geometric features.

### P4 — Real-Time Integration

> **Key Question —** How can the recognition algorithm be connected to a live application?

- Capture and mirror webcam frames.
- Extract landmarks and evaluate the mouth-opening rule for the first detected face.
- Overlay the current state and feature ratio on the video stream.
- Release camera and display resources when exiting.

**Takeaway:** Integrate a compact vision algorithm into a usable live processing loop.

---

## Key Engineering Takeaways

- **Problem formulation:** Translated a rehabilitation movement into a measurable classification task.
- **Feature engineering:** Derived mouth geometry from facial landmarks.
- **Software integration:** Connected webcam I/O, recognition logic, and live feedback in a minimal Python program.

---

## Tech Stack

| Area | Technologies / Methods |
|---|---|
| Programming | Python |
| Computer Vision | OpenCV · `face_recognition` |
| Algorithm | Facial landmarks · Euclidean distance · geometric ratio · threshold-based classification |
| Runtime | Live webcam inference and text overlay |

---

## Repository Structure

```text
.
├── README.md
├── main.py
├── motion_recognition.py
├── requirements.txt
└── .gitignore
```

## Run Locally

Install dependencies in a Python environment compatible with `face-recognition` and `dlib`:

```bash
pip install -r requirements.txt
python main.py
```

Allow webcam access and press **Q** to exit. Webcam behavior and dependency installation have **not been validated on every operating system**.

**Scope and limitations:** This is a focused, source-derived portfolio example, not the full original PyQt5 rehabilitation application. It does not include exercise videos, face images, patient data, cheek recognition, or a clinical validation study. The original width-distance calculation was corrected; the historical classification threshold remains unvalidated.
