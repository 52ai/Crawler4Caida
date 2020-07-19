Hand Gesture Recognition  
============================

## Detects finger movements of hands and shows appropriate output.    
  
#### Steps:  

+ *Segment hand region from a real-time video sequence*  
  - Background Subtraction  
  - Motion Detection and Thresholding  
  - Contour Extraction
  
+ *Count fingers*  
  - Get convex hull of the segmented hand region and compute the most extreme points in the convex hull  
  - Get center of palm using extremes points  
  - Using center of palm, construct a circle with the maximum Euclidean distance as radius  
  - Perform bitwise AND operation on thresholded hand image and the circular ROI  
  - Compute count of fingers using the finger slices obtained in previous step  

#### To run the file use:    **python sudo.py**  

![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `Memory Intensive Operation`  
![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `This script creates screenshot for every frame captured and stores it in directory 'screenshots'`  
![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `Hence, there is a little delay during frame capture`  

### To-Do List:  
- [x] Segment hand region
- [x] Detect numbers using count of fingers
- [ ] Detect characters using finger motion
- [ ] Capture words using word motion
- [ ] Automate tasks with each character / word  

#### Screenshots:  
#### ![Screenshot1](https://rawgit.com/avidLearnerInProgress/hand-gesture-recognition/master/screenshots/screenshot_1.png)  
#### ![Screenshot2](https://rawgit.com/avidLearnerInProgress/hand-gesture-recognition/master/screenshots/screenshot_2.png)  
#### ![Screenshot3](https://rawgit.com/avidLearnerInProgress/hand-gesture-recognition/master/screenshots/screenshot_3.png)  
#### ![Screenshot4](https://rawgit.com/avidLearnerInProgress/hand-gesture-recognition/master/screenshots/screenshot_4.png)  
#### ![Screenshot5](https://rawgit.com/avidLearnerInProgress/hand-gesture-recognition/master/screenshots/screenshot_5.png)  









  
