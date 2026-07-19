# 1. Paper Selection
## Candidates
- Scroll, Tilt or Move It: Using Mobile Phones to Continu-ously Control Pointers on Large Public Displays
- Effective 2D Stroke-based Gesture Augmentation for RNNs
- A Technique for Touch Force Sensing using a Waterproof Device's Built-in Barometer

### Citations
Sebastian Boring, Marko Jurmu, and Andreas Butz. 2009. Scroll, tilt or move it: using mobile phones to continuously control pointers on large public displays. In Proceedings of the 21st Annual Conference of the Australian Computer-Human Interaction Special Interest Group: Design: Open 24/7 (OZCHI '09). Association for Computing Machinery, New York, NY, USA, 161–168. https://doi.org/10.1145/1738826.1738853

Mykola Maslych, Eugene Matthew Taranta, Mostafa Aldilati, and Joseph J. Laviola. 2023. Effective 2D Stroke-based Gesture Augmentation for RNNs. In Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems (CHI '23). Association for Computing Machinery, New York, NY, USA, Article 282, 1–13. https://doi.org/10.1145/3544548.3581358

Ryosuke Takada, Wei Lin, Toshiyuki Ando, Buntarou Shizuki, and Shin Takahashi. 2017. A Technique for Touch Force Sensing using a Waterproof Device's Built-in Barometer. In Proceedings of the 2017 CHI Conference Extended Abstracts on Human Factors in Computing Systems (CHI EA '17). Association for Computing Machinery, New York, NY, USA, 2140–2146. https://doi.org/10.1145/3027063.3053130

## Selection process
We first looked at the papers on Ilias for something interesting. Out of the papers that weren't already taken we only discussed **Effective 2D Stroke-based Gesture Augmentation for RNNs** which would have been possible to implement in two weeks but we didn't choose it, because its implementation effort mainly is ML instead of interaction design and it wouldn't be good as a demo for our presentation.  
Therefore we searched for other papers implementing intresting interaction techniques and found **A Technique for Touch Force Sensing using a Waterproof Device's Built-in Barometer** which implements BaroTouch a method using the device integrated Barometer to have different touch strenghs as input which we found interesting and which was also possible to implement in two weeks and would've been something different with the android implementation to get the barometer data. We even thought about a painting app as an extension to the paper to showcase the different touching strenghs based on the barometer data. Then we noticed it could not be tested consistently on all group devices, because of a missing barometer.  

At last we looked at **Scroll, Tilt or Move It: Using Mobile Phones to Continu-ously Control Pointers on Large Public Displays** which implements three different interaction techniques with the mobile phone as input device to control larger displays and was our final decision for this assignment, because it implemented a interaction technique fitting to other assignments but also something we haven't done exactly and is possible to implement using DIPPID. Also this Interaction technique is very good for a demo in our presentation by using the smartphone as a pointer for the presentation and extending the implementation with an application to showcase the mouse control and thought about different control modes modes.

# 3. Documentation
- DIPPID recall
- How to interpret the sensor data (see data, exploration.py)
- Implementation according to paper (V1)
- Laser pointer like implementation (V2)
- Hyperparameter tweaking (sensitivity, deadzone)
- Button mapping and potential usecases (presentationTracker, browsingTracker)
- Demo Game

## Dependencies

We recommend using Python 3.14 to run the code implementation, but older versions should also work.

To install all the dependencies run the following commands.

```bash
python -m .venv venv
.venv/Scripts/activate
pip install -r requirements.txt
```

## Development process
### Scroll, Tilt or Move It
The paper from Sebastian Boring, Marko Jurmu and Andreas Butz describes three techniques to interact with a big screen display from a distance using a mobile- / smartphone. The interaction techniques get increasingly more complex and all have their up and downsides. The techniques are the following:

- **Scrolling:** The cursor on the display gets moved by pressing keys on the mobile phone, e.g. the arrow keys on older mobiles. On modern smartphones this can be mapped to buttons on the touch display. As long as one key/button is pressed the cursor moves in a specific direction (up, down, left, right).
- **Tilting:** Using build in sensors of the mobile- / smartphone the user can tilt the phone on the X- and Y-Axis to move the cursor. Depending on the tilt angle the cursor moves faster or slower, similar to a joystick of a gaming controller.
- **Moving:** In the paper the camera of the phone is used to detect the physical movement of the phone in space. This linear movement in space is directly mapped to the position of the cursor. Here the user controls the speed of movement by how fast the phone is moved in space. This is the most interesting aspect of this paper, yet the implementation using a camera is rather difficult and also we think that we can do better using the given sensors in modern smartphones like a gyroscope, acceleration or gravity sensor.

### Implementation - Scrolling
The implemetation of the scrolling mechanism is straight forward and does not need extensive though since we alreaday implemented similar problems using the DIPPID framework in previous assignments. Yet this was a good starting point to get a feeling for the problem.

### Problems
### Intermediate steps
### Limitations