#Caleb Dubow
#Change Plus Plus Application
#Given a tweet by Kanye West or Elon Musk, prompt the user to guess which public figure made the tweet, let the user know if
#they were correct. Once the user is finished let the user know how accurate they were in their guesses.


import requests, os, json, pygame, random, time


pygame.init()

# Set up the Window
WINDOWWIDTH = 1024
height = 512
screen = pygame.display.set_mode([WINDOWWIDTH, height])
windowSurface = pygame.display.set_mode((WINDOWWIDTH, height), 0, 32)

# set up Game vars and constants
ELON = 0
KANYE = 1
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (173, 216, 230)
TITLE_FONT = pygame.font.Font('freesansbold.ttf', 64)
REGULAR_FONT = pygame.font.Font('freesansbold.ttf', 16)


#Connects to Twitter API and pulls a json response from a specified account
def connect_to_endpoint(account, count, headers):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+account+"&count="+str(count)
    response = requests.request("GET", url, headers=headers) # Activate GET request from specific URL
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# Filters the tweets so they do not include 
# any references to other users and URL links
def checkTweet(tweet):
    revisedTweet = ""
    for word in tweet.split():
        if word[0] != "@" and word[0:8] != "https://" :
            revisedTweet += word + " "
    if len(revisedTweet.split()) > 1 and len(revisedTweet) < 100: # Makes sure tweet isn't one word long and also isnt too long
        return revisedTweet.encode("ascii","ignore").decode()

    else:
        return "ERROR: TWEET IS NOT LEGITIMATE FOR GAME"


#Creates new tweet 
def newTweet(tweets):
    randTweeter = int(random.random()*2)
    randTweet = "\" " + tweets[randTweeter][int(random.random() * len(tweets[randTweeter]))] + " \""
    TextSurf, TextRect = textDisp(randTweet, REGULAR_FONT, BLACK)
    TextRect.center = ((WINDOWWIDTH/2),(height/3))

    return {"text": randTweet, "textSurf": TextSurf, "rect": TextRect, "tweeter": randTweeter}     


#Creates text surface for displaying text on screen
def textDisp(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()




#Checks answer. If correct, screen turns green. If incorrect, screen turns red
def checkAnswer(score, currentTweet, tweeter):
    if currentTweet['tweeter'] == tweeter:
        score += 1 
        screen.fill(GREEN)
    else:
        screen.fill(RED)

    pygame.display.flip()
    time.sleep(1)
    return score


def main():
    #Set Up Authentication and headers
    bearer_token = "AAAAAAAAAAAAAAAAAAAAADJRHwEAAAAAOUoluhfugo8wMUEg0aCd5lm7NrA%3DIYTSSKpZD8RNvqLsLYjYMCIHKg2nWaqksVF0oxhN3j4CJMmi6C"
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    tweets = [[],[]]

    #Get Musk tweets
    json_response_elon = connect_to_endpoint("elonmusk", 100, headers)
    for i in range(0, len(json_response_elon)):
        tweet = checkTweet(json_response_elon[i]['text'])
        if tweet != "ERROR: TWEET IS NOT LEGITIMATE FOR GAME":
            tweets[ELON].append(tweet)
            


    #Get Kanye tweets
    json_response_kanye = connect_to_endpoint("kanyewest", 100, headers)
    for i in range(0, len(json_response_kanye)):
        tweet = checkTweet(json_response_kanye[i]['text'])
        if tweet != "ERROR: TWEET IS NOT LEGITIMATE FOR GAME":
            tweets[KANYE].append(tweet)
            

    #GAME LOOP
    running = True
    currentTweet = newTweet(tweets)
    score = 0
    while running:
        
    
        # Fill the background with white
        screen.fill((255, 255, 255))

        #SET UP TITLE
        titleSurf, titleRect = textDisp('WHO TWEETED IT?', TITLE_FONT, BLUE)
        titleRect.center = ((WINDOWWIDTH/2),(height*0.1))
        windowSurface.blit(titleSurf, titleRect) 

        #SET UP TWEET
        windowSurface.blit(currentTweet['textSurf'], currentTweet["rect"])

        #SET UP BUTTONS
        kanyeImage = pygame.image.load('kanye.png')
        elonImage = pygame.image.load('elon.png') 
        elonButton = {'rect':pygame.Rect(WINDOWWIDTH*0.1,height*0.5, WINDOWWIDTH*0.2,WINDOWWIDTH*0.21)}
        kanyeButton = {'rect':pygame.Rect(WINDOWWIDTH*0.7,height*0.5, WINDOWWIDTH*0.2, WINDOWWIDTH*0.21)}
        pygame.draw.rect(windowSurface, BLUE, kanyeButton['rect'])
        pygame.draw.rect(windowSurface, BLUE, elonButton['rect'])
        windowSurface.blit(kanyeImage, (kanyeButton['rect'][0], kanyeButton['rect'][1]-25))
        windowSurface.blit(elonImage, (elonButton['rect'][0]+35, elonButton['rect'][1]+5)) 

        #SKIP MECHANIC
        skipSurf, skipRect = textDisp('CLICK ANYWHERE TO SKIP', REGULAR_FONT, BLUE)
        skipRect.center = ((WINDOWWIDTH/2),(height*0.6))
        windowSurface.blit(skipSurf, skipRect) 
        
        #SET UP SCORE
        scoreSurf, scoreRect = textDisp('Score: ' + str(score), TITLE_FONT, BLACK)
        scoreRect.center = ((WINDOWWIDTH/2),(height*0.9))
        windowSurface.blit(scoreSurf, scoreRect) 
        
        
        # Flip the display
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                if kanyeButton['rect'].collidepoint(x,y):
                    score = checkAnswer(score, currentTweet, KANYE)
                elif elonButton['rect'].collidepoint(x,y):
                    score = checkAnswer(score, currentTweet, ELON)
                
                currentTweet = newTweet(tweets)

    pygame.quit()


if __name__ == "__main__":
    main()
