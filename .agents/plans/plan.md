# Target: A web based app for exam simulation

## Features:
1. Multiple choice questons
2. Interactive UI hosted on localhost via Flask framework
3. No need for a database or rich backend features. use the mock exam questions, build a json file with correct answer and other wrong choices. use that as a base for exam mock. use all question from all 5 mock-exam.md files in one json.
4. show and record exam result when it is finished. make it available in the frontend.
5. let the user take exams as much as possible and record the results.
6. The exam is random each time. randomly pick 100 questions from the json file and show in the exam. then score it. passing score is 75 out of 100.
7. make the UI optimized for mobile view.
8. design the json to be extended with more questions and answers later.