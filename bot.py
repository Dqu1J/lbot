import discord
import os
from discord.ext import tasks

client = discord.Client()
admin = "🍀 • Лакич"
channels = ["798454449697325066", "775292935948075008", "804080163826040842"]
reacts = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

@tasks.loop(seconds=300)
async def update_stats():
    for i in range(3):
        cid = int( channels[i] )
        channel = client.get_channel(cid)
        guild = channel.guild
        if i == 0:
            value = str(guild.member_count)
            await channel.edit(name=f"Участники: {value}")
        elif i == 1:
            value = str(guild.premium_subscription_count)
            await channel.edit(name=f"Бустеры: {value}")
        else:
            value = 0
            for member in guild.members:
                if str(member.status) == "online":
                    value += 1
            value = str(value)
            await channel.edit(name=f"Онлайн: {value}")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='ваши %команды'))
    update_stats.start()
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("%ютуб"):
        await message.channel.send("https://www.youtube.com/channel/UCS943x0zbAvopIVsdTXkLjg")
        return
    
    if message.content.startswith("%привет"):
        await message.channel.send("И тебе привет!")
        return
    
    if message.content.startswith("%лаки"):
        await message.channel.send("Лаки - крутой чувак!")
        return

    if message.content.startswith("%инфо"):
        await message.channel.send("Я - ЛакиБот. Я умею много чего (в разработке)! Такой же фортовый как и Лаки.")
        return

    if message.content.startswith("%команды"):
        await message.channel.send("Вот мое мастерство:\n \n- %ютуб\n- %привет\n- %лаки\n- %инфо\n- %команды")
        return
    
    if message.content.startswith("%отправить embed"):
        if message.author.top_role.name == admin:
            rawmsg = message.content
            msg = rawmsg[17:]
            msgspl = msg.split(";")
            if len(msgspl) < 2:
                await message.channel.send("Неверная команда!")
                return
            embed = discord.Embed(title=msgspl[0], description=msgspl[1])
            await message.channel.send(embed=embed)
            await message.delete()
        else:
            await message.channel.send("Ты не можешь использовать эту команду!")
        return

    if message.content.startswith("%отправить"):
        if message.author.top_role.name == admin:
            msg = message.content
            await message.channel.send(msg[11:])
            await message.delete()
        else:
            await message.channel.send("Ты не можешь использовать эту команду!")
        return

    if message.content.startswith("%опрос"):
        if message.author.top_role.name == admin:
            rawmsg = message.content
            msg = rawmsg[7:]
            msgspl = msg.split(";")
            if len(msgspl) < 3 or len(msgspl) > 11:
                await message.channel.send("Неверная команда!")
                return
            pollmsg = f"{msgspl[0]}\n \n"
            for i in range(len(msgspl)-1):
                pollmsg += f"{reacts[i]} - {msgspl[i+1]}\n"
            poll = await message.channel.send(pollmsg)
            for i in range(len(msgspl)-1):
                await poll.add_reaction(reacts[i])
            await message.delete()
        else:
            await message.channel.send("Ты не можешь использовать эту команду!")
        return

client.run(os.getenv("TOKEN"))