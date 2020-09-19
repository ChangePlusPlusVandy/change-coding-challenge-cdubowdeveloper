INTRODUCTION
------------
Given a tweet by Kanye West or Elon Musk, this game prompts the user to guess which 
public figure made the tweet, and lets the user know if they were correct. The user
has the choice between clicking on two boxes, each of which correspond to either Kanye
West or Elon Musk. Everytime the user clicks on a box, the program lets the user know
if they were correct and then selects another tweet from the query.


REQUIREMENTS
------------
This program utilizes pygame and thus requires the pygame library. Additionally, the
program uses images of Kanye's and Elon's face in the GUI. Both of these images are 
contained inside the programs folder and are required for the game to run.


LIMITATIONS
-----------
For simplicity, I decided to program this game using Pygame, which evidently was a terrible
decision on my end. Because pygame doesn't support multi-line text, I had to filter out
tweets that were too long. I also had to remove all non UNICODE characters because pygame 
doesn't support code points above the range of \uFFFF. Therefore, all emojis's and special 
characters had to go. Finally, pygame turns simple GUI work into bloody rocket science so 
the GUI is extremely rudimentary. 

*If this program cannot on your device, I have created a screen recording of the game for your 
viewing pleasure* 
