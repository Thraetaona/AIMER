<div align="center">

  <h1><code>AIMER</code></h1>

  <p>
    <strong>Artificial Intelligence Mark Evaluator & Recognizer</strong>
  </p>
  
</div>

***

# Background
AIMER is an OCR (**O**ptical **C**haracter **R**ecognition) answer-sheet grader.  It was mainly made and submitted for the "Performance Task" of the official College Board's exam of its [Advanced Placement Computer Science Principles](https://en.wikipedia.org/wiki/AP_Computer_Science_Principles) ("AP CSP") course.  It won a local high school programming competition that it was nominated for, and It was also evaluated by the College Board on July, 2022 towards a full 5/5 examination score; it has been publicized under a GPL-3.0 license at this repository since then.

<p align="center" text-align="justify> <br />
  <img width="400" height="200" align="left"
    src="https://user-images.githubusercontent.com/42461518/177600798-be11f1d5-1e3b-4fc9-816a-2a4fe952ad03.png" 
    alt="A score report card of the AP Computer Science Principles' exam displaying a 5/5 score."
  />
  <img width="300" height="200" align="right"
    src="https://user-images.githubusercontent.com/42461518/177618026-efedf72c-d02b-4585-96ce-5392d7b813ff.jpg" 
    alt="A high school programming competition winning certificate."
  />
  <span>
  <sub>
    Performance Tasks (e.g., AIMER) contribute 30% and up to 1.5 of the total score, while the remaining 70% are based on the answers to 70 multiple choice questions---all of which were, ironically, graded by a program similar to AIMER.
  </sub>
  </span>
<br /> </p>

<br /> <br />

The name stands for "**A**rtificial **I**ntelligence **M**ark **E**valuator & **R**ecognizer," and although the "Artificial Intelligence" part is a bit of an exaggeration, it nonetheless employs the use of computer vision through OpenCV in order to achieve its goal.

---

# Running
To get it running, you need to have python3 installed and run the config.bat (or, you could also manually install the 2 dependencies of OpenCV and NumPy.) \
Then, simply connect a USB camera to your device and double-click the main.py file.

Notice that the best results are achieved in a dimly lit environment---not overly bright and not too dark---on a background that is not the same color as the answer paper and has nothing other than said paper on it.

Also, you may specify the numbers of questions and choices inside of the grader.py file by modifying the *NUM_QUESTIONS* and *NUM_CHOICES* global constants (in the below demo's case there were 4 choices and 5 questions.) \
You could also change the ANSWER_KEYS global list to your liking, in our case the correct (key) answers were:
1. 1 (A)
2. 3 (C)
3. 4 (D)
4. 2 (B)
5. 1 (A)

And the student's answers were:
1. 1 (A)
2. 3 (C)
3. 2 (B)
4. 2 (B)
5. 4 (D)

So, the resulting score was 60% as they got 3 out of 5 questions correct.

---

# Demo
https://user-images.githubusercontent.com/42461518/177596309-cc2eda20-434e-4cc5-97f4-9a412de560ce.mp4
<p align="center" text-align="center">
  <sub>
    A sample paper with 5 questions and 4 choices.  Correct answers were 1, 3, 4, 2, and 1.
  </sub>
<br /> </p>





