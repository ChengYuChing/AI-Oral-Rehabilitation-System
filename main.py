"""Minimal real-time mouth movement recognition using a webcam.

Press Q to quit. No GUI assets, recordings, or personal data are included.
"""

import cv2
import face_recognition

from motion_recognition import is_mouth_open, mouth_aspect_ratio


def run() -> None:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("Cannot open webcam (device 0).")

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_landmarks(rgb_frame)

            status = "No face detected"
            if faces:
                ratio = mouth_aspect_ratio(faces[0])
                state = "Open" if is_mouth_open(faces[0]) else "Closed"
                status = f"Mouth: {state} | Ratio: {ratio:.2f}"

            cv2.putText(frame, status, (20, 35), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Oral Motion Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
