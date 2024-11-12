import tkinter as tk
from tkinter import ttk
import random
import math

import os
import configparser
from colors import makeDisabledColor

################
# config setup #
################

config = configparser.ConfigParser()

def configInit():
    '''creates a new config file if either one doesn't exist or it does exist but is broken'''
    if (os.path.exists('config.ini') == False):
        print("no config file exists, creating new one...")
        config['VARS'] = {"wordsize":5,
                          "maxguesses":6,
                          "hardmode":False,
                          "theme":"default.the"}
        config['COLORS'] = {"bg":"#000000",
                            "buttonBg":"#f0f0f0",
                            "activeBg":"#ececec",
                            "disabledBg":"030303",
                            "fg":"#00aa00",
                            "buttonFg":"#edcd33",
                            "activeFg":"#aaaaaa",
                            "disabledFg":"#aa0000",
                            "guessListCorrect":"#c0c0c0",
                            "guessListAlcorrect":"#ffffff",
                            "guessListIncorrect":"#00ff00",
                            "logFg":"#ffff00",
                            "logBg":"#555555",
                            "keyboardDefault":"#000000",
                            "keyboardCorrect":"#f0f0f0",
                            "keyboardAlcorrect":"#ececec",
                            "keyboardIncorrect":"#00aa00",
                            "keyboardBg":"#00aa00",
                            "entryBg":"#edcd33",
                            "entryFg":"#aaaaaa",
                            "entryDisabledBg":"#aa0000",
                            "entryDisabledFg":"#c0c0c0"}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    try:
        config.read('config.ini')
        if config.sections() != ['VARS', 'COLORS']:
            raise Exception('config.sections != sheets')
    except Exception as e:
        print(e)
        print('config file broken, rewriting default one...')
        config['VARS'] = {"wordsize":5,
                          "maxguesses":6,
                          "hardmode":False,
                          "theme":"default"}
        config['COLORS'] = {"bg":"#000000",
                            "buttonBg":"#f0f0f0",
                            "activeBg":"#ececec",
                            "disabledBg":"030303",
                            "fg":"#00aa00",
                            "buttonFg":"#edcd33",
                            "activeFg":"#aaaaaa",
                            "disabledFg":"#aa0000",
                            "guessListCorrect":"#c0c0c0",
                            "guessListAlcorrect":"#ffffff",
                            "guessListIncorrect":"#00ff00",
                            "logFg":"#ffff00",
                            "logBg":"#555555",
                            "keyboardDefault":"#000000",
                            "keyboardCorrect":"#f0f0f0",
                            "keyboardAlcorrect":"#ececec",
                            "keyboardIncorrect":"#00aa00",
                            "keyboardBg":"#00aa00",
                            "entryBg":"#edcd33",
                            "entryFg":"#aaaaaa",
                            "entryDisabledBg":"#aa0000",
                            "entryDisabledFg":"#c0c0c0"}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

configInit()


wordlength = int(config.get('VARS', 'wordsize'))

root = tk.Tk()
root.title("pordle")
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
sw = math.ceil(screenWidth*.45703125)
sh = math.ceil(screenHeight*.7939814)
sposx = str(int((screenWidth/2)-(sw/2)))
sposy = str(int((screenHeight/2)-(sh/2)-60))
root.geometry(str(sh)+"x"+str(sw)+"+"+sposx+"+"+sposy)
root.config(padx=3,pady=3)
root.resizable(0,0)

fm = {'guesslist': 32,
      'button': 16,
      'dropdown': 12,
      'mgbutton': 10,
      'keyboard': 16}


########
# vars #
########

word = ""
errormessage = ""
corrLetters = []
alcorrLetters = []
incorrLetters = []
corrNums = []

correct = False

guesses = 0
maxguesses = int(config.get('VARS', 'maxguesses'))+1

try:
    f = open("words/legalwords{}.txt".format(wordlength))
    ln = [i[:5].upper() for i in f.readlines()]
    f.close()

    f = open("words/words{}.txt".format(wordlength))
    lnFull = [i[:5].upper() for i in f.readlines()]
    f.close()
except Exception as e:
    print(e, "\nMake sure the ./words/ directory contains legalwords{}.txt and words{}.txt, or delete the config file.".format(wordlength, wordlength))
    os.system('pause')
    exit()

if not os.path.exists('./themes/'):
    print("no themes directory found. creating...")
    os.makedirs(os.curdir+'\\themes')
    f = open(os.path.realpath(os.curdir)+'\\themes\\default.the', 'w+')
    f.write("the parser will interpret every line that is not a single hex code as a comment\nin order, theme files have the following colors:\ngeneral: foreground, background, active background (buttons)\n\n000000\nf0f0f0\nececec\n\nguess list: correct, almost correct, incorrect\n\n00aa00\nedcd33\naaaaaa\n\nconsole: foreground, background\n\naa0000\nc0c0c0\n\nkeyboard: default text color, correct, almost correct, incorrect, background\n\nffffff\n00ff00\nffff00\n555555\n#000000\n(colors can either start with a # or not)")

    config.set('VARS', 'theme', 'default.the')
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    f.close()

prevGuess = ""

hardMode = tk.IntVar()

###############
# definitions #
###############

def isHex(s: str):
    
    '''only includes 6-digit hex numbers'''
    if s[0] == "#":
        ss = s.lower()[1:7]
    else:
        ss = s.lower()[:6]
    for i in ss:
        if i not in "abcdef1234567890":
            return False
    return "#"+ss

def updateTheme():
    oth = config.get('VARS', 'theme')
    fl = themeSetDropdown.get() + ".the"
    if fl:
        try:
            f = open("themes/"+fl)
            config.set('VARS', 'theme', fl)
        except:
            log("unable to locate theme file " + fl + ".")
            f = open("themes/"+config.get('VARS', 'theme'))
    else:
        f = open("themes/"+config.get('VARS', 'theme'))
    
    col = [isHex(i) for i in f.readlines() if isHex(i)]
    if len(col) == 22:
        config['COLORS'] = {"bg":col[0],
                            "buttonBg":col[2],
                            "activeBg":col[3],
                            "disabledBg":col[4],
                            "fg":col[1],
                            "buttonFg":col[5],
                            "activeFg":col[6],
                            "disabledFg":col[7],
                            "guessListCorrect":col[8],
                            "guessListAlcorrect":col[9],
                            "guessListIncorrect":col[10],
                            "logFg":col[12],
                            "logBg":col[11],
                            "keyboardDefault":col[14],
                            "keyboardCorrect":col[15],
                            "keyboardAlcorrect":col[16],
                            "keyboardIncorrect":col[17],
                            "keyboardBg":col[13],
                            "entryBg":col[18],
                            "entryFg":col[19],
                            "entryDisabledBg":col[20],
                            "entryDisabledFg":col[21]}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        if oth != config.get('VARS', 'theme'):
            log("Theme set to {}.".format(config.get('VARS', 'theme')[:-4]))
        else:
            log("Theme {} updated.".format(config.get('VARS', 'theme')[:-4]))
    else:
        log("incorrect number of colors ({1}) in theme file \"{0}\".".format(config.get('VARS', 'theme'), len(col)))
        
    
    setTheme()


def resetVars():
    #idk if i should set these to global here but whatever
    hardModeButton['state'] = 'normal'
    maxGuessesDropdown['state'] = 'readonly'
    maxGuessesButton['state'] = 'normal'
    try:
        hardModeButton.config(cursor="hand2", background=buttonBg)
        maxGuessesButton.config(cursor="hand2", background=buttonBg)
    except:
        hardModeButton.config(cursor='hand2')
        maxGuessesButton.config(cursor='hand2')
    
    global wordlength
    wordlength = int(config.get('VARS', 'wordsize'))

    global word
    word = chooseWord()

    global errormessage
    global corrLetters
    global alcorrLetters
    global incorrLetters
    global prevGuess
    global corrNums
    errormessage = ""
    corrLetters = []
    alcorrLetters = []
    incorrLetters = []
    corrNums = []
    prevGuess = ""

    global correct
    correct = False

    global guesses
    global maxguesses
    guesses = 0
    maxguesses = config.getint('VARS', 'wordsize')

    try:
        setTheme()
    except:
        log("theme broken. please delete config file.")

    global ln
    global lnFull

    f = open("words/legalwords{}.txt".format(wordlength))
    ln = [i[:5].upper() for i in f.readlines()]
    f.close()

    f = open("words/words{}.txt".format(wordlength))
    lnFull = [i[:5].upper() for i in f.readlines()]
    f.close()


    entry['state'] = 'normal'
    entry.delete(0, tk.END)
    guessList['state'] = 'normal'
    guessList.delete(1.0,tk.END)
    guessList['state'] = 'disabled'

def chooseWord():
    w = (random.choice(ln)).upper()
    return w

def log(s):
    if s:
        errortxt['state'] = 'normal'
        errortxt.insert(tk.END, str(s)+"\n")
        errortxt['state'] = 'disabled'

def logKeyboard():
    keyboard['state'] = 'normal'
    keyboard.delete(1.0, tk.END)

    uRow = "QWERTYUIOP"
    mRow = "ASDFGHJKL"
    dRow = "ZXCVBNM"
    
    for i in uRow:
        if i in corrLetters:
            keyboard.insert(tk.END, i, ('correct'))
        elif i in alcorrLetters:
            keyboard.insert(tk.END, i, ('alcorrect'))
        elif i in incorrLetters:
            keyboard.insert(tk.END, i, ('incorrect'))
        else:
            keyboard.insert(tk.END, i, ('def'))
        if i != uRow[-1]:
            keyboard.insert(tk.END, " ")
    
    keyboard.insert(tk.END, "\n ")
    for i in mRow:
        if i in corrLetters:
            keyboard.insert(tk.END, i, ('correct'))
        elif i in alcorrLetters:
            keyboard.insert(tk.END, i, ('alcorrect'))
        elif i in incorrLetters:
            keyboard.insert(tk.END, i, ('incorrect'))
        else:
            keyboard.insert(tk.END, i, ('def'))
        if i != uRow[-1]:
            keyboard.insert(tk.END, " ")
    keyboard.insert(tk.END, "\n")
    for i in dRow:
        if i in corrLetters:
            keyboard.insert(tk.END, i, ('correct'))
        elif i in alcorrLetters:
            keyboard.insert(tk.END, i, ('alcorrect'))
        elif i in incorrLetters:
            keyboard.insert(tk.END, i, ('incorrect'))
        else:
            keyboard.insert(tk.END, i, ('def'))
        if i != uRow[-1]:
            keyboard.insert(tk.END, " ")
    keyboard.insert(tk.END, " ")
    
    keyboard.tag_add('just', '1.0', tk.END)
    keyboard['state'] = 'disabled'

def compareWord(s):
    global guesses
    global correct
    global prevGuess
    cont = True
    guessList['state'] = 'normal'
    if guesses >= int(config.get('VARS', 'maxguesses')): # skip main step if # of guesses exceeds max guesses
        cont = False
        return
    
    if cont: # main step
        codes = [0 for i in range(wordlength)] # setup list of codes for adding to the list
        if s == word: # if the guess is equal to the word
            correct = True
            for i in word:
                if i not in corrLetters:
                    corrLetters.append(i)
            logKeyboard()
            guessList.insert(tk.END, s, ('correct'))
            entry['state'] = 'disabled'
            log("Congratulations, you got the word in {1} guesses!\nThe word was {0}. Press enter to restart.".format(word, guesses+1))
        else: # otherwise, 
            lcd = {}
            for i in word: # setup of dictionary of letters in Word
                if i in lcd.keys():
                    lcd[i]+=1
                else:
                    lcd[i]=1
            
            for i in range(wordlength): #do all correct letter checks first
                if s[i] == word[i]: # correct letter check
                    corrLetters.append(s[i])
                    corrNums.append(i)
                    codes[i] = 2
                    lcd[s[i]] -= 1
            for i in range(wordlength):
                if codes[i] == 0:
                    if s[i] in lcd.keys(): # al(most)correct letter check
                        if lcd[s[i]] > 0:
                            lcd[s[i]] -= 1
                            alcorrLetters.append(s[i])
                            codes[i] = 1
                        else:
                            incorrLetters.append(s[i])
                            codes[i] = 0
                    else: # incorrect letter set
                        incorrLetters.append(s[i])
                        codes[i] = 0
            
            for i in range(wordlength): # for each letter in the Guess, take the index from Codes and use it to change the formatting of the word
                if codes[i] == 2:
                    guessList.insert(tk.END, s[i], ('correct'))
                elif codes[i] == 1:
                    guessList.insert(tk.END, s[i], ('alcorrect'))
                else:
                    guessList.insert(tk.END, s[i], ('incorrect'))
            guessList.insert(tk.END, "\n")
        guessList.tag_add('def', '1.0', tk.END)
        guesses += 1
    
    if guesses >= int(config.get('VARS', 'maxguesses')) and s != word:
        guessList.insert(tk.END, "\n"+word, ('incorrect', 'def'))
        log("Out of guesses. The word was {}. Press enter to restart.".format(word))
        entry.delete(0, tk.END)
        entry['state'] = 'disabled'
    guessList.see(tk.END)
    guessList['state'] = 'disabled'

def submitWord():
    global prevGuess
    if entry['state'] == 'disabled':
        resetVars()
    text = entry.get().upper()
    if len(text) == wordlength:
        log("")
        if text.isalpha():
            if text in lnFull or text in ln: # there may be words in legalWords.txt that are not in words.txt
                hardModeButton['state'] = 'disabled'
                maxGuessesDropdown['state'] = 'disabled'
                maxGuessesButton['state'] = 'disabled'
                hardModeButton.config(cursor="arrow", background=disabledBg)
                maxGuessesButton.config(cursor="arrow", background=disabledBg)

                if config.getboolean('VARS', 'hardmode') == False or prevGuess == "":
                    compareWord(text)
                    prevGuess = text
                    entry.delete(0, tk.END)
                else:
                    validWord = True
                    for i in range(wordlength):
                        if i in corrNums: #going through CORRNUMS and then the PREVIOUS GUESS and THE CURRENT GUESS
                            if prevGuess[i] != text[i]:
                                validWord = False
                                log("[hard mode] Word invalid: " + prevGuess[i] + " of " + prevGuess + " is not " + text[i] + " of " + text)
                                break
                    for i in alcorrLetters:
                        if i not in text:
                            validWord = False
                            log("[hard mode] Word invalid: " + i + " not in " + text)
                            break
                    if validWord:
                        compareWord(text)
                        prevGuess = text
                        entry.delete(0, tk.END)
            else:
                log("Word " + text + " not in dictionary.")
        else:
            log("Word must contain only letters.")
    else:
        if len(text) > 0:
            log("Word must be {} letters long.".format(str(wordlength)))
    logKeyboard()
    errortxt.see(tk.END)

def hardModeToggle():
    if config.getboolean('VARS','hardmode'):
        log("Hard mode disabled.")
        config.set('VARS','hardmode', "0")
        hardModeButton.config(relief="raised", background=buttonBg)
    else:
        log("Hard mode enabled.")
        config.set('VARS','hardmode', "1")
        hardModeButton.config(relief="sunken", background=activeBg)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    errortxt.see(tk.END)

def setTheme():
    global buttonBg
    global activeBg
    global disabledBg
    bg = config.get('COLORS', "bg")
    buttonBg = config.get('COLORS', "buttonBg")
    activeBg = config.get('COLORS', "activeBg")
    disabledBg = config.get('COLORS', 'disabledBg')
    fg = config.get('COLORS', "fg")
    buttonFg = config.get('COLORS', "buttonFg")
    activeFg = config.get('COLORS', 'activeFg')
    disabledFg = config.get('COLORS', 'disabledFg')

    guessListCorrect = config.get('COLORS', "guessListCorrect")
    guessListAlcorrect = config.get('COLORS', "guessListAlcorrect")
    guessListIncorrect = config.get('COLORS', "guessListIncorrect")

    logFg = config.get('COLORS', "logFg")
    logBg = config.get('COLORS', "logBg")
    
    keyboardDefault = config.get('COLORS', "keyboardDefault")
    keyboardCorrect = config.get('COLORS', "keyboardCorrect")
    keyboardAlcorrect = config.get('COLORS', "keyboardAlcorrect")
    keyboardIncorrect = config.get('COLORS', "keyboardIncorrect")
    keyboardBg = config.get('COLORS', "keyboardBg")

    entryBg = config.get('COLORS', 'entryBg')
    entryFg = config.get('COLORS', 'entryFg')
    entryDisabledBg = config.get('COLORS', 'entryDisabledBg')
    entryDisabledFg = config.get('COLORS', 'entryDisabledFg')
    

    root.config(background=bg)

    uframe.config(background=bg)

    guessList.config(background=bg)
    guessList.tag_config('correct', foreground=guessListCorrect)
    guessList.tag_config('alcorrect', foreground=guessListAlcorrect)
    guessList.tag_config('incorrect', foreground=guessListIncorrect)

    if config.getboolean('VARS','hardmode'):
        hardModeButton.config(relief="sunken")
    else:
        hardModeButton.config(relief="raised")

    if hardModeButton['state'] == 'normal':
        hardModeButton.config(background=buttonBg, activebackground=activeBg, foreground=buttonFg, activeforeground=activeFg, disabledforeground=disabledFg)
    else:
        hardModeButton.config(background=disabledBg, activebackground=activeBg, foreground=buttonFg, activeforeground=activeFg, disabledforeground=disabledFg)
    

    themeSetButton.config(background=buttonBg, activebackground=activeBg, foreground=buttonFg, activeforeground=activeFg, disabledforeground=disabledFg)
    
    #https://tkdocs.com/shipman/ttk-map.html
    #at some point i'd like to be able to set the relief of all of the combobox elements but whatever ig
    tsds.theme_settings('combostyle', settings={'TCombobox': { 'configure': {
                                                                            'foreground':fg,
                                                                            'padding':'flat',
                                                                            'selectforeground':fg,
                                                                            'selectbackground':bg,
                                                                            'fieldbackground':bg,
                                                                            'background':activeBg,
                                                                            'arrowcolor':fg,
                                                                            'padding':2,
                                                                            }}})
    mframe.config(background=bg)

    errortxt.config(foreground=logFg,background=logBg)

    keyboardFrame.config(background=keyboardBg)

    keyboard.config(background=keyboardBg)
    keyboard.tag_config('correct', foreground=keyboardCorrect)
    keyboard.tag_config('alcorrect', foreground=keyboardAlcorrect)
    keyboard.tag_config('incorrect', foreground=keyboardIncorrect)
    keyboard.tag_config('def', foreground=keyboardDefault)

    lframe.config(background=bg)

    if maxGuessesButton['state'] == 'normal':
        maxGuessesButton.config(background=buttonBg, activebackground=activeBg, foreground=buttonFg, activeforeground=activeFg, disabledforeground=disabledFg)
    else:
        maxGuessesButton.config(background=disabledBg, activebackground=activeBg, foreground=buttonFg, activeforeground=activeFg, disabledforeground=disabledFg)

    entry.config(background=entryBg, foreground=entryFg, disabledbackground=entryDisabledBg, disabledforeground=entryDisabledFg)

    submit.config(background=buttonBg, activebackground=activeBg, foreground=buttonFg, activeforeground=activeFg, disabledforeground=disabledFg)
    updateThemesList()
    
def updateThemesList(*args):
    themesindir = []
    for i in os.listdir("./themes/"):
        if i[-4:] == ".the":
            themesindir.append(i[:-4])
    
    themeSetDropdown['values']=themesindir

def updateMaxGuesses(*args):
    config.set('VARS','maxguesses', maxGuessesDropdown.get())

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    log("Max guesses set to "+config.get('VARS', 'maxguesses')+".")
    errortxt.see(tk.END)

def quitProgram(*args):
    raise SystemExit




########
# root #
########

root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=93)
root.rowconfigure(1,weight=32)
root.rowconfigure(2,weight=17)


######################
# upper frame; words #
######################

uframe = tk.Frame(root)
uframe.grid(row=0,column=0,sticky="nesw")

uframe.columnconfigure(0, weight=1)
uframe.rowconfigure(0, weight=1)
uframe.columnconfigure(1, weight=3)
uframe.columnconfigure(2, weight=1)
uframe.rowconfigure(1, weight=1)

guessList = tk.Text(uframe)
guessList.place(relx=.5, rely=.5, relwidth=.7, anchor='center')
#tags
guessList.tag_config('def', font=("Consolas", fm["guesslist"]), justify="center")
guessList.tag_add('def', '1.0', tk.END)
guessList['state'] = 'disabled'
guessList.config(height=27, width=16, relief='flat')

quitButton = tk.Button(uframe)
quitButton.place(relx=.99, rely=.02, relwidth=.05, relheight=.08, anchor='ne')
quitButton.config(text="X", font="Arial 16", relief='raised', command=quitProgram, cursor='hand2', background="#aa0000", activebackground="#880000", activeforeground="#ffffff", foreground="#ffffff")

hardModeButton = tk.Button(uframe)
hardModeButton.place(relx=.1, rely=.5, relwidth=.18, anchor='center')
hardModeButton.config(text="Hard mode", font="Consolas {} bold".format(fm['button']), relief='raised', command=hardModeToggle, cursor='hand2')

themeSetButton = tk.Button(uframe)
themeSetButton.place(relx=.9, rely=.5, relwidth=.18, anchor='center')
themeSetButton.config(text="Set Theme", font="Consolas {} bold".format(fm['button']), relief='raised', command=updateTheme, cursor='hand2')


tsds = ttk.Style()
tsds.theme_create('combostyle')
tsds.theme_use('combostyle')

themeSetDropdown = ttk.Combobox(uframe, state='readonly')
themeSetDropdown.place(relx=.9, rely=.6, relwidth=.18, relheight= .09, anchor='center')
themeSetDropdown.set(config.get('VARS', 'theme')[:-4])
themeSetDropdown.bind('<FocusIn>', updateThemesList)
themeSetDropdown.config(font=('Consolas', fm['dropdown']))#12

maxGuessesButton = tk.Button(uframe)
maxGuessesButton.place(relx=.065, rely=.6, relwidth=.11, relheight= .09, anchor='center')
maxGuessesButton.config(text="Set max\nguesses", font="Consolas {} bold".format(fm['mgbutton']), relief='raised', command=updateMaxGuesses, cursor='hand2')
mgv = tk.IntVar()
nl = [i for i in range(1,21)]
maxGuessesDropdown = ttk.Combobox(uframe, values=nl, state='readonly')
maxGuessesDropdown.set(config.get('VARS', 'maxguesses'))
maxGuessesDropdown.place(relx=.16, rely=.6, relwidth=.06, relheight= .09, anchor='center')
maxGuessesDropdown.config(font="Consolas 11 bold")

######################################
# middle frame; keys/error reporting #
######################################

mframe = tk.Frame(root)
mframe.grid(row=1,column=0,sticky="nesw")




errortxt = tk.Text(mframe,height=3)
errortxt.place(relx=0, rely=.5, relwidth=.65, relheight=1, anchor='w')
errortxt.config(relief="sunken")

errortxt['state'] = 'disabled'

keyboardFrame = tk.Label(mframe) # frames can't have a relief ig, so i'm using a blank label instead
keyboardFrame.place(relx=.65, rely=.5, relwidth=.35, relheight=1, anchor='w')
keyboardFrame.config(relief="sunken")

keyboard = tk.Text(keyboardFrame)
keyboard.place(relx=.5, rely=.5, relwidth=.95, relheight=.6, anchor='center')
keyboard.config(relief='flat', font="Gothic {}".format(fm['keyboard']), spacing1=4)
keyboard.tag_config('just', justify='center')
keyboard.insert(1.0, "kybard\n")
keyboard['state'] = 'disabled'

#################################
# lower frame; text entry field #
#################################

lframe = tk.Frame(root)
lframe.grid(row=2,column=0,sticky="nesw",pady=10)
lframe.rowconfigure(0, weight=1)
lframe.columnconfigure(0, weight=1)
lframe.columnconfigure(1, weight=5)
lframe.columnconfigure(2, weight=1)

entry = tk.Entry(lframe)
entry.place(relx=.48, rely=.5, relwidth=.82, relheight=1, anchor='center')
entry.config(justify='center',font="Consolas {}".format(fm['guesslist']))

entry.bind("<Return>", lambda event: submitWord())

submit = tk.Button(lframe)
submit.place(relx=.95, rely=.5, relwidth=.09, relheight=1, anchor='center')
submit.config(text="⏎",command=submitWord, font="Consolas 24 bold", cursor='hand2')

#################
# begin program #
#################

logKeyboard()
word = chooseWord()
log("Welcome to Pordle! Enter a {}-letter word to begin.".format(str(wordlength)))
entry.focus()
resetVars()
root.mainloop()