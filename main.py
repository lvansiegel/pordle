# https://www.youtube.com/watch?v=epDKamC-V-8
# https://www.youtube.com/watch?v=X5yyKZpZ4vU&list=PL-osiE80TeTsllUYGWPRStXSSKwonuvei&index=2

import tkinter as tk
from tkinter import ttk
import random

import os.path
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
                          "theme":"default"}
        config['COLORS'] = {"fg":"#000000",
                            "bg":"#f0f0f0",
                            "abg":"#fafafa",
                            "glc":"#00aa00",
                            "gla":"#ffff00",
                            "gli":"#000000",
                            "lfg":"#aa0000",
                            "lbg":"#c0c0c0",
                            "kbd":"#ffffff",
                            "kbc":"#00ff00",
                            "kba":"#ffff00",
                            "kbi":"#555555",
                            "kbbg":"#000000",
                            "theme":"default"}
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
        config['COLORS'] = {"fg":"#000000",
                            "bg":"#f0f0f0",
                            "abg":"#fafafa",
                            "glc":"#00aa00",
                            "gla":"#ffff00",
                            "gli":"#000000",
                            "lfg":"#aa0000",
                            "lbg":"#c0c0c0",
                            "kbd":"#ffffff",
                            "kbc":"#00ff00",
                            "kba":"#ffff00",
                            "kbi":"#555555",
                            "kbbg":"#000000",
                            "theme":"default"}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

configInit()


wordlength = int(config.get('VARS', 'wordsize'))

root = tk.Tk()
root.title("pordle")
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
sposx = str(int((screenWidth/2)-351))
sposy = str(int((screenHeight/2)-343-60))
root.geometry("702x686+"+sposx+"+"+sposy)
root.config(padx=3,pady=3)
root.resizable(0,0)

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

f = open("words/legalwords{}.txt".format(wordlength))
ln = [i[:5].upper() for i in f.readlines()]
f.close()

f = open("words/words{}.txt".format(wordlength))
lnFull = [i[:5].upper() for i in f.readlines()]
f.close()


prevGuess = ""

hardMode = tk.IntVar()

###############
# definitions #
###############

def updateTheme():
    fl = themeSetDropdown.get() + ".the"
    if fl:
        try:
            f = open("themes/"+fl)
            config.set('VARS', 'theme', fl)
        except:
            log("unable to locate theme file " + fl + ". updating current theme instead.")
            f = open("themes/"+config.get('VARS', 'theme'))
    else:
        f = open("themes/"+config.get('VARS', 'theme'))
    
    col = ["#"+i[:6] for i in f.readlines() if i[:3] != "---" and i != "\n"]
    if len(col) == 13:
        config['COLORS'] = {"fg":col[0],
                            "bg":col[1],
                            "abg":col[2],
                            "glc":col[3],
                            "gla":col[4],
                            "gli":col[5],
                            "lfg":col[6],
                            "lbg":col[7],
                            "kbd":col[8],
                            "kbc":col[9],
                            "kba":col[10],
                            "kbi":col[11],
                            "kbbg":col[12]}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        log("incorrect number of colors in theme file.")
        
    
    setTheme()


def resetVars():
    #idk if i should set these to global here but whatever
    hardModeButton['state'] = 'normal'
    maxGuessesDropdown['state'] = 'readonly'
    maxGuessesButton['state'] = 'normal'
    hardModeButton.config(cursor="hand2")
    maxGuessesButton.config(cursor="hand2")
    
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

    #global hardMode
    #hardMode = True

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
    # keyboard.insert(tk.END, "\n")
    
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
    
    #keyboard.insert(tk.END, '\n')
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
                    #corrl.append(i)
                    corrLetters.append(s[i])
                    corrNums.append(i)
                    #guessList.insert(tk.END, s[i], ('correct'))
                    codes[i] = 2
                    lcd[s[i]] -= 1
            for i in range(wordlength):
                if codes[i] == 0:
                    if s[i] in lcd.keys(): # al(most)correct letter check
                        if lcd[s[i]] > 0:
                            lcd[s[i]] -= 1
                            #alcorrl.append(i)
                            alcorrLetters.append(s[i])
                            #guessList.insert(tk.END, s[i], ('alcorrect'))
                            codes[i] = 1
                        else:
                            # guessList.insert(tk.END, s[i], ('incorrect'))
                            incorrLetters.append(s[i])
                            codes[i] = 0
                    else: # incorrect letter set
                        # guessList.insert(tk.END, s[i], ('incorrect'))
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
                hardModeButton.config(cursor="arrow")
                maxGuessesButton.config(cursor="arrow")

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
                    # else:
                    #     log("Word not valid [hard mode restriction].")
            else:
                log("Word " + text + " not in dictionary.")
        else:
            log("Word must contain only letters.")
    else:
        #errortxt.config(text="Word must be 5 characters long.")
        if len(text) > 0:
            log("Word must be {} letters long.".format(str(wordlength)))
    logKeyboard()
    errortxt.see(tk.END)

def hardModeToggle():
    if config.getboolean('VARS','hardmode'):
        log("Hard mode disabled.")
        config.set('VARS','hardmode', "0")
        hardModeButton.config(relief="raised", background=bgc)
    else:
        log("Hard mode enabled.")
        config.set('VARS','hardmode', "1")
        hardModeButton.config(relief="sunken", background=abgc)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    errortxt.see(tk.END)

def setTheme():
    global bgc
    global abgc
    bgc = config.get('COLORS', "bg")
    abgc = config.get('COLORS', "abg")#addToHex(bgc, -20, -20, -20)#config.get('COLORS', "abg")#
    dbgc = makeDisabledColor(bgc, +60, +60, +60)
    fgc = config.get('COLORS', "fg")
    afgc = makeDisabledColor(fgc, -20, -20, -20)
    dfgc = makeDisabledColor(fgc, 60, 60, 60)#addToHex(fgc, -40, 40, -40)

    glc = config.get('COLORS', "glc")
    gla = config.get('COLORS', "gla")
    gli = config.get('COLORS', "gli")

    logfg = config.get('COLORS', "lfg")
    logbg = config.get('COLORS', "lbg")
    
    kbd = config.get('COLORS', "kbd")
    kbc = config.get('COLORS', "kbc")
    kba = config.get('COLORS', "kba")
    kbi = config.get('COLORS', "kbi")
    kbbg = config.get('COLORS', "kbbg")

    root.config(background=bgc)

    uframe.config(background=bgc)

    guessList.config(background=bgc)
    guessList.tag_config('correct', foreground=glc)
    guessList.tag_config('alcorrect', foreground=gla)
    guessList.tag_config('incorrect', foreground=gli)

    hardModeButton.config(background=bgc, activebackground=abgc, foreground=fgc, activeforeground=afgc, disabledforeground=dfgc)

    themeSetButton.config(background=bgc, activebackground=abgc, foreground=fgc, activeforeground=afgc, disabledforeground=fgc)
    
    #https://tkdocs.com/shipman/ttk-map.html
    #at some point i'd like to be able to set the relief of all of the combobox elements but whatever ig
    tsds.theme_settings('combostyle', settings={'TCombobox': { 'configure': {
                                                                            'foreground':fgc,
                                                                            # 'relief':'flat',
                                                                            'padding':'flat',
                                                                            'selectforeground':fgc,
                                                                            'selectbackground':bgc,
                                                                            'fieldbackground':bgc,
                                                                            'background':abgc,
                                                                            'arrowcolor':fgc,
                                                                            'padding':2,
                                                                            }}})
    mframe.config(background=bgc)

    errortxt.config(foreground=logfg,background=logbg)

    keyboardFrame.config(background=kbbg)

    keyboard.config(background=kbbg)
    keyboard.tag_config('correct', foreground=kbc)
    keyboard.tag_config('alcorrect', foreground=kba)
    keyboard.tag_config('incorrect', foreground=kbi)
    keyboard.tag_config('def', foreground=kbd)

    lframe.config(background=bgc)

    #guessLabel.config(background=bgc, foreground=fgc)
    maxGuessesButton.config(background=bgc, activebackground=abgc, foreground=fgc, activeforeground=afgc, disabledforeground=dfgc)

    entry.config(background=bgc, foreground=fgc, disabledbackground=dbgc, disabledforeground=dfgc)

    submit.config(background=bgc, activebackground=abgc, foreground=fgc, activeforeground=afgc, disabledforeground=dfgc)


    if config.getboolean('VARS','hardmode'):
        hardModeButton.config(relief="sunken", background=abgc)
    else:
        hardModeButton.config(relief="raised", background=bgc)
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
guessList.tag_config('def', font="Consolas 32", justify="center")
guessList.tag_add('def', '1.0', tk.END)
guessList['state'] = 'disabled'
guessList.config(height=27, width=16, relief='flat')

hardModeButton = tk.Button(uframe)
hardModeButton.place(relx=.1, rely=.5, relwidth=.18, anchor='center')
hardModeButton.config(text="Hard mode", font="Consolas 16 bold", relief='raised', command=hardModeToggle, cursor='hand2')

themeSetButton = tk.Button(uframe)
themeSetButton.place(relx=.9, rely=.5, relwidth=.18, anchor='center')
themeSetButton.config(text="Set Theme", font="Consolas 16 bold", relief='raised', command=updateTheme, cursor='hand2')


test = ["a", "b", "c", "d"]

tsds = ttk.Style()
#tsds.map('TCombobox', fieldbackground=[('readonly', 'red')])
# https://stackoverflow.com/questions/27912250/how-to-set-the-background-color-of-a-ttk-combobox
# tsds.theme_create('combostyle',# parent='alt',
#                          settings = {'TCombobox':
#                                      {'configure':
#                                       {'selectbackground': 'blue',
#                                        'fieldbackground': 'red',
#                                        'background': 'green'
#                                        }}}
#                          )
tsds.theme_create('combostyle')
tsds.theme_use('combostyle')

themeSetDropdown = ttk.Combobox(uframe, values=test, state='readonly')
themeSetDropdown.place(relx=.9, rely=.6, relwidth=.18, relheight= .09, anchor='center')
themeSetDropdown.set(config.get('VARS', 'theme')[:-4])
themeSetDropdown.bind('<FocusIn>', updateThemesList)
themeSetDropdown.config(font='Consolas 12')

# guessLabel = tk.Label(uframe)
# guessLabel.place(relx=0.01, rely=.7, anchor='w')
# guessLabel.config(text="Max guesses: " + config.get('VARS', 'maxguesses'), font="Consolas 14 bold")
maxGuessesButton = tk.Button(uframe)
maxGuessesButton.place(relx=.07, rely=.6, relwidth=.12, relheight= .09, anchor='center')
maxGuessesButton.config(text="Set max\nguesses", font="Consolas 10 bold", relief='raised', command=updateMaxGuesses, cursor='hand2')
mgv = tk.IntVar()
nl = [i for i in range(1,21)]
#nl.append("infinite")
maxGuessesDropdown = ttk.Combobox(uframe, values=nl, state='readonly')
maxGuessesDropdown.set(config.get('VARS', 'maxguesses'))
maxGuessesDropdown.place(relx=.165, rely=.6, relwidth=.05, relheight= .09, anchor='center')
maxGuessesDropdown.config(font="Consolas 11 bold")
# command=updateMaxGuesses

######################################
# middle frame; keys/error reporting #
######################################

mframe = tk.Frame(root)
mframe.grid(row=1,column=0,sticky="nesw")




errortxt = tk.Text(mframe,height=3)
errortxt.place(relx=0, rely=.5, relwidth=.65, relheight=1, anchor='w')

errortxt['state'] = 'disabled'

keyboardFrame = tk.Frame(mframe)
keyboardFrame.place(relx=.65, rely=.5, relwidth=.35, relheight=1, anchor='w')

keyboard = tk.Text(keyboardFrame)
keyboard.place(relx=.5, rely=.5, relwidth=.9, relheight=.6, anchor='center')
keyboard.config(relief='flat', font="Gothic 16", spacing1=4)
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

# ll = tk.Label(lframe)
# ll.grid(row=0,column=0,sticky="nesw")
# ll.config(relief="flat")

entry = tk.Entry(lframe)
# entry.grid(row=0,column=1,sticky="nesw")
entry.place(relx=.48, rely=.5, relwidth=.82, relheight=1, anchor='center')
entry.config(justify='center',font="Consolas 32")

entry.bind("<Return>", lambda event: submitWord())

submit = tk.Button(lframe)
# submit.grid(row=0,column=2,sticky="nesw")
submit.place(relx=.95, rely=.5, relwidth=.09, relheight=1, anchor='center')
submit.config(text="⏎",command=submitWord, font="Consolas 24 bold", cursor='hand2')

###############################
###############################
###############################

logKeyboard()
word = chooseWord()
log("Welcome to Pordle! Enter a {}-letter word to begin.".format(str(wordlength)))
entry.focus()
resetVars()
root.mainloop()