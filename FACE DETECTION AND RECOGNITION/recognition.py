import cv2
import face_recognition
import numpy as np

print("Face Recognition System")

encs = []
names = []

name = input("Enter name: ").strip()
path = input("Enter image path: ").strip().strip("\"'")

try:
    img = face_recognition.load_image_file(path)
    enc = face_recognition.face_encodings(img)[0]
    encs.append(enc)
    names.append(name)
    print(f"{name} loaded!")
except Exception as e:
    print("No valid image. Only detection mode available.")

while True:
    print("""
MENU
1) Detect Faces
2) Recognize Faces
0) Quit
""")
    ch = input(">>> ").strip()
    if ch == '0':
        print("Over")
        break
    if ch not in ['1', '2']:
        print("Invalid. Try 0,1,2")
        continue

    print("Starting cam... (press Q to return)")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret: break

        small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(rgb)

        if ch == '1':
            for (t,r,b,l) in locs:
                cv2.rectangle(frame, (l*2,t*2), (r*2,b*2), (255,0,0), 2)
                cv2.putText(frame, 'Person', (l*2,t*2-10), 0, 0.8, (255,0,0), 2)

        elif ch == '2':
            curr_encs = face_recognition.face_encodings(rgb, locs)
            for (t,r,b,l), enc in zip(locs, curr_encs):
                who = "Unknown"
                if encs:
                    match = face_recognition.compare_faces(encs, enc, tolerance=0.6)
                    dist = np.argmin(face_recognition.face_distance(encs, enc))
                    if match[dist]: who = names[dist]
                cv2.rectangle(frame, (l*2,t*2), (r*2,b*2), (0,255,0), 2)
                cv2.rectangle(frame, (l*2,b*2-20), (r*2,b*2), (0,255,0), -1)
                cv2.putText(frame, who, (l*2+6,b*2-6), 0, 0.6, (0,0,0), 1)

        mode = "Face Detection" if ch=='1' else "Face Recognization"
        cv2.imshow(f"[{mode}] | Press Q to Menu", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
