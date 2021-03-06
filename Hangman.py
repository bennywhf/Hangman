from random import randrange
from cs1graphics import *
from sys import exit
from math import *
from time import *




class word():
    def __init__(self,paper,picture,WL,gam,difficulty,Turn):
        self.diff=difficulty
        self.words=('icecream','party','apple','jazz') #dictionary of words to choose from
        self.Hardwords=('jazz','egg','arc','arcade','toy','banjo','galaxy','bikini','ivy','injury')#hard words
        self.Easywords=('elephant','party','apple','school','food','relax','book','python')#easy words
        self.Mediumwords=('movie','music','television','piano','guitar','orange','cake')#medium words
        if self.diff=='Easy':
            self.wordinuse=self.Easywords[randrange(0,len(self.words))]# taking out one random word from my list of words
            self.lives=8
        elif self.diff=='Hard':
            self.wordinuse=self.Hardwords[randrange(0,len(self.words))]#taking out the word from the list of Hard words
            self.lives=12
        elif self.diff=='Medium':
            self.wordinuse=self.Mediumwords[randrange(0,len(self.words))]#taking out the word from the list of Medium words.
            self.lives=10
        self.wordinuse=list(self.wordinuse)# turning the word into a list of letters
        self.wordinuse.reverse() # I had to reverse the word because it came up backwards in the graphic window.
        self._paper=paper# refrencing the graphic window
        self.W=paper.getWidth()# getting Width of window just incase
        self.H=paper.getHeight()#getting Height of window just inscase
        self.pic=picture#this is the Hangman picture class I'm  refering to.
        self.wronglist=list()# this list will collect the letters that are used incorrectly
        self.WL=WL# reference to the Text that will display the incorrect letters.
        self.checklist=[False]*len(self.wordinuse)#this will determine if you have the word right depending on how many True's there is per letter
        self.game=gam
        self.constantlives=self.lives
        self.turn=Turn
        self.turn.setMessage('Turns left: '+str(self.lives))

        
    def Checkword(self,word):# here I will check if any of the letters used match the letters in the secret word.
    
        
        drow=list(word) #turned the inputed word into a list in order to compare to the secretword
        drow.reverse() #reversed it since the secret word is also reversed.
        counter=len(self.wordinuse)

        for i in range(len(self.wordinuse)):
            if(drow==self.wordinuse):#if player enters full word, then display the word!
                T=Text(self.wordinuse[i],12,Point((self.W/2+(30*(len(self.wordinuse)/2)-i*30)),500))#if the words are equeal then just print the word

                self._paper.add(T)#print...
                self.checklist[i]=True

                if False not in self.checklist:
                    sleep(.3)
                    self.game.win(self.wordinuse)

    

            elif(word==self.wordinuse[i]):# if only one letter matches then place that letter in its corresponding place
                    
                T=Text(word,12,Point((self.W/2+(30*(len(self.wordinuse)/2)-i*30)),500))
    
                self._paper.add(T)
                self.checklist[i]=True

                if False not in self.checklist:
                    sleep(.3)
                    self.game.win(self.wordinuse)


            elif(word=='init'): # initialize by only placing dashes in places of the secret words.
                T=Text('__',12,Point((self.W/2+(30*(len(self.wordinuse)/2)-i*30)),500))
                self._paper.add(T)
                
            else:
                counter-=1
                if(counter==0):# at the end of every turn
                    if False in self.checklist:
                        self.lives-=1#taking away one 'life' from the player.
                        self.turn.setMessage('Turns left: '+str(self.lives))
                        if self.lives==0:#if player runs out of turns, he will lose
                            self.pic.drawall()#if there are any parts of the hangman not drawn yet, it will be drawn here
                            sleep(.3)#wait two seconds before showing the player the secrete word and asking to play again
                            self.game.lose(self.wordinuse)#sending the word to the game class to show it to the player
                    if (len(word)==1):#here we are appending the wrong letters to a list.
                        if word not in self.wronglist:#''
                            self.wronglist.append(word)#''
                            self.wronglist.sort()#''
                            self.WL.setMessage(','.join(self.wronglist))#''
                    
                
                    self.pic.draw(self.constantlives)#this will draw the hangman, the constant lives is used to devide the number of parts so that the parts are put evenly.
                    break


    
class Hangman():# this class draws the hangman to the canvas

    def __init__(self,paper):# these are the body parts of the Hangman
        self._paper=paper
        self.faceline=Circle(35,Point(300,50+70))

        self.eye1=Circle(10,Point(285,40+70))
        self.eye2=Circle(10,Point(315,40+70))

        self.stickbody=Path(Point(300,85+70),Point(300,200+70))

        self.stickleg1=Path(Point(300,200+70),Point(280,260+70))
        self.stickleg2=Path(Point(300,200+70),Point(320,260+70))

        self.stickarm1=Path(Point(300,100+70),Point(320,160+70))
        self.stickarm2=Path(Point(300,100+70),Point(280,160+70))

        self.rope=Path(Point(300,70),Point(300,75+70))
        self.noose=Circle(13,Point(300,75+13+30+40))

        self.table=Path(Point(100,340),Point(500,340))
        self.tleg=Path(Point(150,340),Point(150,400))
        self.tleg2=Path(Point(450,340),Point(450,400))
        

        self.a=[self.table,self.tleg,self.tleg2,self.rope,self.noose,self.faceline,self.eye1,self.eye2,self.stickbody,self.stickleg1,self.stickleg2,self.stickarm1,self.stickarm2]
        self.full=self.a
        self.nums=len(self.a)
        self.i=0
        
                
    def draw(self,num):#drawing hangman by parts at the end of each turn if use wrong letter, or word
            counter=ceil(self.nums/num)
            x=0
           
            while(x<counter):
                try:
                    self._paper.add(self.a[self.i])# I had to add this because Everytime I played again it gave me an error saying that the object was already on the canvas.
                except ValueError:
                    pass
                
                x+=1
                self.i+=1
    def drawall(self):# at the end of the game if any parts are missing draw the remaining parts
        for c in self.a[self.i:len(self.a)]:
            self._paper.add(c)




class game():# class to check if player wins or loses. then aks to play again.

    def __init__(self,window):
        self._win=window
        
    def win(self,word):# if player wins the end screen will say YOU win!!
        self._win.close()
        playagain(word,1)
            #main(0)
    def lose(self,word):# if palyer loses the end screen will say you lose
        self._win.close()
        playagain(word,0)
        

class savemessage(EventHandler):# this takes the letter/word in the text box and starts the process of checking if it is in the hidden word.
    def __init__(self,textsource,obj,paper):#textsource= Inputbox, Obj=Word, UL=letters used, paper=Paper
        self.objtext=textsource
        self.saved_message=str()
        self.obj=obj
        #self.MAX=self.obj.getsizeofword
        self.paper=paper


    def handle(self,event):

        if event.getDescription()=='mouse click':
            self.saved_message=self.objtext.getMessage()# gets message from button
            self.saved_message=self.saved_message.lower()# makes all letters lowercase incase some one uses a shifted letter
            self.obj.Checkword(self.saved_message)# after the word is lowered then its sent to the object WORD which is incharge of checking if it matches the secret word.
            self.paper.remove(self.objtext)# delets the input box to replace it with one that has nothing in it.
            self.objtext=TextBox(100,25,Point(300,600-20))# ''
            self.paper.add(self.objtext)#''


class saveinfo(EventHandler):# takes the word from a button to use it in the difficulty and to check if player wants to play again.
    def __init__(self,window,value,monit):
        self.textsource=window
        self.monitor=monit
        self.val=value

    def handle(self,event):
        if event.getDescription()=='mouse release':
            obj=event.getTrigger()
            self.val.setMessage(obj.getMessage())
            self.monitor.release()

def intro():# intro screen; shows the maker and asks players to enjoy. then shows the difficulties.
    Titlescreen=Canvas(300,300,'lightyellow2')

    Wel=Text('Hangman by Ebenezer Reyes',15,Point(150,20))
    Titlescreen.add(Wel)

    
    Button_A=Button('Easy',Point(150,75))
    Button_A.setBorderWidth(5)
    Button_A.setBorderColor('yellow')
    Button_A.setFillColor('White')
    
    Button_B=Button('Medium',Point(150,150))
    Button_B.setBorderWidth(5)
    Button_B.setBorderColor('Orange')
    Button_B.setFillColor('White')
    
    Button_C=Button('Hard',Point(150,225))
    Button_C.setBorderWidth(5)
    Button_C.setBorderColor('Red')
    Button_C.setFillColor('White')

    Titlescreen.add(Button_A)
    Titlescreen.add(Button_B)
    Titlescreen.add(Button_C)
    mon=Monitor()
    answer=Text('')
    getinput=saveinfo(Titlescreen,answer,mon)

    Button_A.addHandler(getinput)
    Button_B.addHandler(getinput)
    Button_C.addHandler(getinput)

    mon.wait()
    

    sleep(.5)
    Titlescreen.close()
    return answer.getMessage()


def playagain(word,res):# shows the player the secret word. lets the player know that he won/lost. then asks if player would like to play again.
    windox=Canvas(400,400,'lightyellow') # creates a window

    if res==1:
        T=Text('You win!!',20,Point(180,40))
    else:
        T=Text('Sorry... You lose',20,Point(180,40))
    word.reverse()
    w=str()
    val=Text('')
    for i in word:
        w+=i
    mon=Monitor()
    wor=Text('The secret word is '+w,18,Point(180,100))
    yes=Button('Yes',Point(150,250))
    no=Button('No',Point(250,250))
    PA=Text('Would you like to play again?',18,Point(200,200))
    getans=saveinfo(windox,val,mon)
    windox.add(PA)
    
    windox.add(yes)
    windox.add(no)
    windox.add(wor)
    windox.add(T)

    yes.addHandler(getans)
    no.addHandler(getans)
        
    mon.wait()

    windox.close()

    again=val.getMessage()

    if again=='Yes':# closes window then starts new game
        windox.close()
        main()
    else:
        windox.close()# closeswindow
        exit()# ends program
        
class exitbutton(EventHandler):# creating exit button class
    def __init__(self,paper,exti=0):# exti will mean If i want to exit the program or not If i do want to exit the program I make exti=1
        self.paper=paper#refrencing the paper which the exit button is on.
        self.exit=exti
    def handle(self,event):
        if event.getDescription()=='mouse release':# if mouse release close graphic windows if self.exit==1 then close program.
            self.paper.close()#''
            if self.exit==1:#''
                exit(0)#''
    
class Helpbutton(EventHandler):
    def __init__(self):
        pass # there is nothign i need to start as soon as i make the object.

    def handle(self,event):
        if event.getDescription()=='mouse click':
            dow=Canvas(300,300,'lightyellow')# creating new Help window
            t=Text('To play, hover mouse over TextBox.',12,Point(150,40))#adding text to window
            t2=Text('Enter word/letter then press OK.',12,Point(150,60))# ''
            dow.add(t)# ''
            dow.add(t2)#''
            EXIT=Button(' Exit ',Point(180,180))#adding exit button to new help window
            EH=exitbutton(dow)# adding the exit button handler to exit button
            EXIT.addHandler(EH)#''
            dow.add(EXIT)#''

    
def main():

    DIFF=intro()# this method will decide what the difficulty is
    Wrong=Text('Wrong Letters',10,Point(300,20))# title for list of wrong letters used
    wrongline=Path(Point(260,30),Point(340,30))# line under the tittle
    Turns=Text('Turns left: ',12,Point(450,580))#displays the number of turns left

    paper=Canvas(600,600,'lightyellow')#creats a Canvas for graphix


    gam=game(paper)#object of class game
    WL=Text('',12,Point(300,40))#list of wrong letters
    picture=Hangman(paper)#object of class Hangman
    WORD=word(paper,picture,WL,gam,DIFF,Turns)#object of class WORD
    TB=TextBox(100,25,Point(300,600-20))# the input Textbox that allows the player to play
    TextEnter=Button(' OK ',Point(190,580))# the okay button that takes in the word/letter used by player
    okbutton=savemessage(TB,WORD,paper)#object of class savemessage
    TextEnter.addHandler(okbutton)# adding the handler of the savemessage object to TextEnter
    paper.add(TB)# adding the Textbox
    WORD.Checkword('init')#initianlizing the game. in this step the dashes under the letters are created.
    paper.add(TextEnter)#adding Textenter
    paper.add(WL)#adding WL to the paper
    paper.add(Wrong)#adding Wrong
    paper.add(wrongline)#adding Wrongline
    paper.add(Turns)#adding turns

    HH=Helpbutton()#creating object of class Helpbutton
    pleh=Button(' Help ',Point(550,20))#creating Help button
    pleh.addHandler(HH)#adding the even handler to the Helpbutton
    
    paper.add(pleh)#adding the help button to the paper

    closebutton=Button(' Exit ',Point(570,580))#creating a close button
    EH=exitbutton(paper,1)#creating object of class exitbutton

    closebutton.addHandler(EH)#adding event handler

    paper.add(closebutton)# adding closebutton to paper.
    

    
    
main()
