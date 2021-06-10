import pymongo as pm
from decouple import config

class Database:
    def __init__(self):
        try:
            self.cluster = pm.MongoClient("mongodb+srv://danger-ahead:"
            +config('MONGO')+"@cluster0.z0zou.mongodb.net/test")

            self.db = self.cluster["roBOT"]
            self.collection = self.db["user_score"]
            self.collection2 = self.db["servers"]
            print('Running: Database module [database.py]')       #prints the message after successfully initializing the connection with mongoDB
        except:
            print('Failed to run Database module [database.py]\n')

    async def score_up(self, message, client):     #increases the score of the user
        score = -1
        query = {"_id": message.author.id}
        user = self.collection.find(query)
        for result in user:
            score = result["score"]

        if score > 0:
            score = score + 1
            self.collection.update_one({"_id":message.author.id}, {"$set":{"score":score}})

            if score%15 == 0:  #user levels up every 15 points
                user = self.collection2.find({"_id":message.guild.id})
                for result in user:
                    channell = result["channel"]

                chanell = client.get_channel(channell)
                await chanell.send(message.author.mention+', you\'re my level '
                +str(int(score/15))+ ' friend now!')
        else:
            self.collection.insert_one({"_id":message.author.id, "score":1})   #if the user has interacted for the 1st time, sets the user's score to 1

    async def rank_query(self, message):   #searches and messages rank of the user
        query = {"_id": message.author.id}
        user = self.collection.find(query)
        for result in user:
            score = result["score"]
        await message.channel.send(message.author.mention+', you\'re my level '
        +str(int(score/15))+ ' friend!')

    async def server_config(self, server, message):    #sets the channel for roBOT's admin commands, also initializes the confess key with 0
        channell = ''
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            channell = result["channel"]

        if channell != '':
            await message.channel.send('I\'m already configured on <#'+str(channell)+'>')
        else:
            self.collection2.insert_one({"_id":server, "channel":message.channel.id, "confess":0})
            await message.channel.send('I just got configured!')

    async def server_deconfig(self, server, message):      #deletes the discord server's details
        channell = ''
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            channell = result["channel"]

        if channell == message.channel.id:
            self.collection2.delete_one({"_id": server})
            await message.channel.send('I\'ve been deconfigured!')
        elif channell == '':
            await message.channel.send('Configure me first!')
        elif channell != message.channel.id:
            await message.channel.send('I\'m configured on <#'
            +str(channell)+'> \nI can\'t deconfigure here!')

    async def confess_config(self, server, message):       #configures the confession channel
        confess = 0
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            confess = result["confess"]
            channell = result["channel"]

        if confess != 0:
            await message.channel.send('I\'m already configured on <#'+str(confess)+'>')
        else:
            self.collection2.update_one({"_id" : server},
            {"$set" : {"_id" : server, "channel" : channell, "confess":message.channel.id}})
            await message.channel.send('I just got the confession channel configured!')

    async def confess_deconfig(self, server, message):     #sets the confession channel's id to 0
        confess = 0
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            confess = result["confess"]
            channell = result["channel"]

        if confess == message.channel.id:
            self.collection2.update_one({"_id" : server},
            {"$set" : {"_id" : server, "channel" : channell, "confess":0}})
            await message.channel.send('My confession channel has been deconfigured!')
        elif confess == 0:
            await message.channel.send('Configure my confession channel first!')
        elif confess != message.channel.id:
            await message.channel.send('My confession channel is configured on <#'
            +str(confess)+'> \nI can\'t deconfigure here!')

    async def leave_server(self, server, message):     #function for leaving the server on command from pre-configured channel
        channell = ''
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            channell = result["channel"]

        if channell == message.channel.id:
            await message.channel.send('Don\'t want me? Fine!')
            await message.guild.leave()
        elif channell == '':
            await message.channel.send('Configure me first!')
        else:
            await message.channel.send('I\'ll only leave if instructed from <#'+str(channell)+'>')

    async def confess(self, client, discord, confession, message):      #function for forwarding the confession
        channell = 0
        user = self.collection2.find({"_id":message.guild.id})
        for result in user:
            channell = result["confess"]

        if channell != 0:
            embed=discord.Embed(title='Someone just confessed:',
            description=confession, color=discord.Color.blue())
            await client.get_channel(channell).send(embed=embed)
        else:
            await message.channel.send('My confession channel hasn\'t been configured!')
