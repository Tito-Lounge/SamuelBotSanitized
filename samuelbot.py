import discord
import random
import string
from config import token
from textblob import TextBlob

def SentimentAnalysis(text):
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return 1
        if analysis.sentiment.polarity == 0:
            return 0
        if analysis.sentiment.polarity < 0:
            return -1

id = '<@1068669152031682630>'
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.guild:
        mem = message.guild.get_member(client.user.id)
        perms = message.channel.permissions_for(mem)
    if perms.send_messages == 0 or perms.read_messages == 0:
        return # Do not send a joke if there is no permissions to send/recieve messages in a channel.
    if message.content.count('|') >= 4:
        return # Do not function if a spoiler is present.
    if message.author.bot:
        return # Do not send a joke if responding to a bot (prevents infinite loops with itself)

    # Set the message to lowercase and rid it of punctuation
    msg = message.content.lower().translate(str.maketrans('','', string.punctuation))
   
    # Isolate the words into a list that can be parsed for phrases to initiate jokes
    wds = msg.split(' ')
    options = []

    for x in range(len(wds)):
        cWord = wds[x]
        # Mention of Samuel Bot?
        # Checks to ensure Samuel Bot is said and that it isn't the only word in the message.
        if ((cWord == "samuel" and wds[x+1] == "bot") or cWord == "samuelbot" or cWord == "id" or client.user.mentioned_in(message)) and (len(wds) > 2):
            if (SentimentAnalysis(msg) == 1):
                options.append("Thank you colon three! *:3*")
                options.append("Nice man!")
                options.append("Thanks man... that makes me smile~")
            elif (SentimentAnalysis(msg) == -1):
                options.append("Now that... was DEFINITELY uncalled for. \U0001F610")
                options.append("Now that... was FASHOLY uncalled for. \U0001F610")
                options.append("Wait...! That was weird... \U0001F928") 
                options.append("As Josh would say.")
            elif (SentimentAnalysis(msg) == 0):
                options.append("\U0001F610")
                options.append("*in Tyler, the Creator voice*: Okay?")
                options.append("Umm... \U0001F928 *awkward taco* \U0001F32E What did you mean by that? \U0001F449\U0001F448 ") 
            break
        # Supporting the LGBT community!
        if cWord.startswith('trans') or cWord.endswith ('trans'):
            output = "Good for " + cWord.replace('trans','').capitalize() + "! :)"
            options.append(output)
        if cWord.startswith('bi'):
            output = "Oh, so " + cWord.replace('bi','') + " is a bicon then." 
            options.append(output)
        # Girl Named [Blank] Bit
        if cWord == "in" or cWord.endswith('in') or cWord == "on" or cWord.endswith('on'):
            if x == len(wds)-1 and cWord.endswith('on'):
                output = cWord.replace('on','').capitalize() + " on who, now?"
            elif x == len(wds)-1 and cWord.endswith('in'):
                output = cWord.replace('in','').capitalize() + " in who, now?"
            else: 
                output = "Girl named " + wds[x+1] + "."
            options.append(output)
        elif cWord.startswith('in') or cWord.startswith('on'):
            if cWord.startswith('in'):
                output = "Girl named " + cWord.replace('in','').capitalize() + "."
            elif cWord.startswith('on'):
                output = "Girl named " + cWord.replace('on','').capitalize() + "."
            options.append(output)
        # [Blank] Her? I hardly know her! Bit
        elif cWord.endswith('er') or cWord.endswith('ir') or cWord.endswith('ur') or cWord.endswith('or'):
            output = cWord[:-2].capitalize() + " her? I hardly know her!"
            options.append(output)
    if options:
        await message.reply(random.choice(options))
    # Joaquin Hello Bit
    elif msg.startswith('hello') or msg.startswith('hi'):
        await message.reply("*in a poor imitatation of Joaquin's voice*: Hello!")
    return
client.run(token)