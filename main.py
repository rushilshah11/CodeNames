import discord
import os
from keep_alive import keep_alive
from words import wordList
import replit
import random
import copy
import tabulate
from prettytable import PrettyTable
replit.clear()

client = discord.Client()
intents = discord.Intents.all()
client = discord.Client(intents=intents)

print("test")

initialWords = []
answerKey = []
shuffledWords = []
assignList = []
randInts = []
redList = []
blueList = []
bomb = []
playerUIDList = []
gameStarted = True
currentTurn = "red"

row1 = []
row2 = []
row3 = []
row4 = []
row5 = []

redPlayers = []
redSpymasters = []
bluePlayers = []
blueSpymasters = []

redCorrectSelectedList = []
blueCorrectSelectedList = []

redCorrect = 0
blueCorrect = 0

print(wordList)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

print(len(wordList))


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content == '$start':
        if (len(playerUIDList) == 0):
            await msg.channel.send('Add players before beginning')
        elif (len(playerUIDList) < 4):
            await msg.channel.send(f'You currently have {len(playerUIDList)} players, the minimum player requirement is 4')
        else:
            await msg.channel.send('Game starting...')
            start_game()
            for userid in redSpymasters:
                user = client.get_user(int(userid))
                await user.send(makeAnswerKey())
            for userid in blueSpymasters:
                user = client.get_user(int(userid))
                await user.send(makeAnswerKey())
            await msg.channel.send(makeTable())
            await msg.channel.send(f'{currentTurn}, it is your turn')

    if gameStarted:
        if msg.content.startswith('$select'):
            column = msg.content[len(msg.content) - 3]
            row = msg.content[len(msg.content) - 1]
            await msg.channel.send(row_select(int(column), int(row), msg.author.id))
            await msg.channel.send(check_win())

    if(msg.content == '&red'):
        playerUIDList.append(f'{msg.author.id}')
        redPlayers.append(f'{msg.author.id}')
        await msg.channel.send("You have joined team red! \U0001F534")
    if(msg.content == '&blue'):
        playerUIDList.append(f'{msg.author.id}')
        bluePlayers.append(f'{msg.author.id}')
        await msg.channel.send("You have joined team blue! \U0001F535")
    if(msg.content == '&red spymaster'):
        playerUIDList.append(f'{msg.author.id}')
        redSpymasters.append(f'{msg.author.id}')
        await msg.channel.send("You are a red spymaster! \U0001F534")
    if(msg.content == '&blue spymaster'):
        playerUIDList.append(f'{msg.author.id}')
        blueSpymasters.append(f'{msg.author.id}')
        await msg.channel.send("You are a blue spymaster! \U0001F535")

    if (msg.content == '$reset'):
        resetGame()
        await msg.channel.send("Resetted")


def currentTurnToggle():
    global currentTurn
    if currentTurn == 'red':
        currentTurn = 'blue'
    else:
        currentTurn = 'red'


def start_game():
    randInts = random.sample(range(0, 399), 25)
    for i in randInts:
        initialWords.append(wordList[i])
    shuffledWords = copy.deepcopy(initialWords)
    global answerKey
    answerKey = copy.deepcopy(initialWords)
    print("ANSWERS", answerKey)
    random.shuffle(shuffledWords)
    for x in range(0, len(shuffledWords)-1):
        if x < 13:
            redList.append(shuffledWords[x])
        elif (x == 25):
            bomb.append(shuffledWords[x])
        else:
            blueList.append(shuffledWords[x])
    for i in range(0, 25):
        spy_master(i)
    gameStarted = True


def makeTable():
    table = PrettyTable()
    table.field_names = ["", "CUTIE", "HACK", "2021", " "]
    row1 = [initialWords[0], initialWords[1],
            initialWords[2], initialWords[3], initialWords[4]]
    row2 = [initialWords[5], initialWords[6],
            initialWords[7], initialWords[8], initialWords[9]]
    row3 = [initialWords[10], initialWords[11],
            initialWords[12], initialWords[13], initialWords[14]]
    row4 = [initialWords[15], initialWords[16],
            initialWords[17], initialWords[18], initialWords[19]]
    row5 = [initialWords[20], initialWords[21],
            initialWords[22], initialWords[23], initialWords[24]]
    table.add_row(row1)

    table.add_row(row2)

    table.add_row(row3)

    table.add_row(row4)

    table.add_row(row5)
    # return(tabulate(table, headers = 'firstrow', tablefmt = 'grid'))
    return '```'+f'{table}'+'```'


def makeAnswerKey():
    table = PrettyTable()
    table.field_names = ["", "CUTIE", "HACK", "2021", " "]
    row1 = [answerKey[0], answerKey[1],
            answerKey[2], answerKey[3], answerKey[4]]
    row2 = [answerKey[5], answerKey[6],
            answerKey[7], answerKey[8], answerKey[9]]
    row3 = [answerKey[10], answerKey[11],
            answerKey[12], answerKey[13], answerKey[14]]
    row4 = [answerKey[15], answerKey[16],
            answerKey[17], answerKey[18], answerKey[19]]
    row5 = [answerKey[20], answerKey[21],
            answerKey[22], answerKey[23], answerKey[24]]
    table.add_row(row1)

    table.add_row(row2)

    table.add_row(row3)

    table.add_row(row4)

    table.add_row(row5)
    # return(tabulate(table, headers = 'firstrow', tablefmt = 'grid'))
    return '```'+f'{table}'+'```'


def row_select(column, row, user):
    correctList = []
    incorrectList = []
    user = f'{user}'
    isRed = True
    if user in redPlayers:
        correctList = redList
        incorrectList = blueList
    elif user in bluePlayers:
        correctList = blueList
        incorrectList = redList
        isRed = False
    else:
        return "You have not selected a team! You may still add yourself to a team, however"
    index = ((row - 1) * 5) + (column - 1)
    if (initialWords[index] in redCorrectSelectedList) or (initialWords[index] in blueCorrectSelectedList):
        return "Word already Selected"
    if initialWords[index] in correctList:
        initialWords[index] = answerKey[index]
        redCorrectSelectedList.append(f'${initialWords[index]}$')
        blueCorrectSelectedList.append(f'#{initialWords[index]}#')
        if currentTurn == "red":
            global redCorrect
            redCorrect += 1
        else:
            global blueCorrect
            blueCorrect += 1
        return makeTable() + "Correct! Your turn will continue!"
    elif initialWords[index] in incorrectList:
        initialWords[index] = answerKey[index]
        redCorrectSelectedList.append(f'${initialWords[index]}$')
        blueCorrectSelectedList.append(f'#{initialWords[index]}#')
        currentTurnToggle()
        return makeTable() + "L! Your turn will not continue!"
    elif initialWords[index] in bomb:
        return "GAME OVER, You have hit the bomb!"
    else:
        return "Reentered the same word"


def spy_master(index):
    print("ANSER KEY", answerKey)
    if answerKey[index] in redList:
        answerKey[index] = f'${answerKey[index]}$'
    elif answerKey[index] in blueList:
        answerKey[index] = f'#{answerKey[index]}#'
    else:
        answerKey[index] = f'xX{answerKey[index]}Xx'


def resetGame():
    global initialWords
    global shuffledWords
    global assignList
    global randInts
    global redList
    global blueList
    global bomb
    global playerUIDList
    global gameStarted

    initialWords = []
    shuffledWords = []
    assignList = []
    randInts = []
    redList = []
    blueList = []
    bomb = []
    playerUIDList = []
    gameStarted = True


def check_win():
    if(redCorrect == 13):
        return 'THE RED CUTIES WINNNNN'
    elif(blueCorrect == 13):
        return 'THE BLUE CUTIES WINNNNN'
    else:
        return f'{currentTurn}, it is your turn {redCorrect}'


keep_alive()
client.run(os.getenv('TOKEN'))
