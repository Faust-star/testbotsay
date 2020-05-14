import discord
from random import randint, choice
from discord.ext import commands 
import datetime
import speech_recognition as sr 
from discord.utils import get
import asyncio
import random as r
import youtube_dl, os
import random
from random import choice
import pyowm
import requests
import json
import os
import sqlite3
import discord
import asyncio
import random
import googletrans
from bs4 import BeautifulSoup
import urllib.request


PREFIX = '!'

client = commands.Bot(command_prefix = PREFIX )
client.remove_command( 'help' )


@Bot.event
async def on_ready():
    print('Bot is ready.')

@Bot.command()
async def members_info(ctx):
    server_members = ctx.guild.members
    data = "\n".join([i.name for i in server_members])
    
    await ctx.send(data)

# калькулятор
@Bot.command(aliases = ['count', 'calc', 'вычисли', 'math'])
async def __count(ctx, *, args = None):
    text = ctx.message.content

    if args == None:
        await ctx.send(embed = discord.Embed(description = 'Please, specify expression to evaluate.', color = 0x39d0d6))
    else:
        result = eval(args)
        await ctx.send(embed = discord.Embed(description = f'Evaluation result of `{args}`: \n`{result}`', color = 0x39d0d6))

@Bot.event
async def on_message(message):

    await client.process_commands(message)

    if 'discord.gg' in message.content.lower():
        await message.delete()
        await message.channel.send(embed = discord.Embed(description = f'{message.author}, реклама запрещена.',color=0x0c0c0c)) 
        return

@Bot.event
async def on_ready():
    print('client ready')


def toggle_next():
    client.loop.call_soon_threadsafe(play_next_song.set)

@Bot.command()
async def send(ctx, member: discord.Member, *, arg):
    await member.send(embed = discord.Embed(description = f'{arg}', color=0x0c0c0c)) 
    return

#time
@Bot.command()
async def time(ctx):
    emb = discord.Embed(colour= discord.Color.green(), url= 'https://www.timeserver.ru')
    
    emb.set_author(name= client.user.name, icon_url=client.user.avatar_url)
    emb.set_footer(text= 'Если у вас время по МСК, то к этому добавляйте +1 час', icon_url=ctx.author.avatar_url)
    emb.set_thumbnail(url='https://www.worldtimeserver.com/img/dst/dst-2-3.png')

    now_date = datetime.datetime.now()
    emb.add_field(name='Time', value='{}'.format(now_date))

    await ctx.send( embed = emb ) 

@Bot.command()
@commands.has_permissions( administrator = True)
async def say(ctx, *, arg):

    await ctx.message.delete()
    await ctx.send(embed = discord.Embed(description = f'{arg}', color=0x0c0c0c))

@Bot.command()
async def ping(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    emb = discord.Embed(
        title= 'Текущий пинг',
        description= f'{client.ws.latency * 1000:.0f} ms'
    )
    await ctx.send(embed=emb)

@Bot.event
async def on_raw_reaction_add(payload):
    msgID = int(payload.message_id)
    if msgID == int(config.message_id):
        emoji = str(payload.emoji)
        member = payload.member 
        role = discord.utils.get(member.guild.roles, id=config.roles[emoji])
        await member.add_roles(role)
    else:
        pass

@Bot.event
async def on_ready(*args):
    type = discord.ActivityType.watching
    activity = discord.Activity(name = "за сервером", type = type)
    status = discord.Status.dnd
    await client.change_presence(activity = activity, status = status)

# информация сервера
@Bot.command()
async def serverinfo(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"{ctx.guild.name}", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: Сервер создали **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
        f":flag_white: Регион **{ctx.guild.region}\n\nГлава сервера **{ctx.guild.owner}**\n\n"
        f":tools: Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
        f":green_circle: Онлайн: **{online}**\n\n"
        f":black_circle: Оффлайн: **{offline}**\n\n"
        f":yellow_circle: Отошли: **{idle}**\n\n"
        f":red_circle: Не трогать: **{dnd}**\n\n"
        f":shield: Уровень верификации: **{ctx.guild.verification_level}**\n\n"
        f":musical_keyboard: Всего каналов: **{allchannels}**\n\n"
        f":loud_sound: Голосовых каналов: **{allvoice}**\n\n"
        f":keyboard: Текстовых каналов: **{alltext}**\n\n"
        f":briefcase: Всего ролей: **{allroles}**\n\n"
        f":slight_smile: Людей на сервере **{ctx.guild.member_count}\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {ctx.guild.id}")
    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)

# удаление пользователя из сервера
@Bot.command()
@commands.has_permissions( administrator = True) 
async def kick(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = client.get_channel( 709750350759854091 ) #Айди канала логов

        await member.kick( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c))
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c)) 

# Работа с ошибками кика


# Бан    

@Bot.command()
@commands.has_permissions( administrator = True) 
async def ban(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = client.get_channel( 709795894542729320 ) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 


@Bot.command()
@commands.has_permissions( administrator = True )
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@Bot.command()
@commands.has_permissions( administrator = True) 
async def mute(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 709813120750583808) #Айди роли
        channel_log = client.get_channel(709795894542729320) #Айди канала логов

        await member.add_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))  

# Размут

@Bot.command()
@commands.has_permissions( administrator = True) 
async def unmute(ctx,member: discord.Member = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 709813120750583808) #Айди роли
        channel_log = client.get_channel(709795894542729320) #Айди канала логов

        await member.remove_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0x0c0c0c))    

# Работа с ошибками размута

@unmute.error 
async def unmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@mute.error 
async def mute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c)) 

# выдача роли при входе 
@Bot.event
async def on_member_join( member ):
    channel = client.get_channel(709743018617471026)
    role = discord.utils.get( member.guild.roles, id = 709838029677658192)

    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'Пользователь ``{ member.name }``, присоеденился к нам!', 
                          color = 0x0c0c0c ) )

@Bot.command()
async def report(ctx,member: discord.Member = None,*,arg = None):

    channel = client.get_channel( 709696227780067479 ) #Айди канала жалоб

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif arg is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        await ctx.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}**', color=0x0c0c0c))
        await channel.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}\n:bust_in_silhouette: Автор жалобы: {ctx.author.mention}**', color=0x0c0c0c))

@Bot.command()
@commands.has_permissions( administrator = True)
async def clear(ctx,amount : int):
    
    channel_log = client.get_channel(709743018617471026) #Айди канала логов

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0x0c0c0c))
    await channel_log.send(embed = discord.Embed(description = f'**:wastebasket:  Удалено {amount} сообщений.**', color=0x0c0c0c))

# Работа с ошибками очистки чата

@clear.error 
async def clear_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name},обязательно укажите количевство сообщений.**', color=0x0c0c0c)) 

# userinfo
@Bot.command()
async def userinfo(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"Имя: {Member.name}\n\n"
                                                                                      f"Никнейм: {Member.nick}\n\n"
                                                                                      f"Статус: {Member.status}\n\n"
                                                                                      f"ID: {Member.id}\n\n"
                                                                                      f"Высшая роль: {Member.top_role}\n\n"
                                                                                      f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

# Command help
@Bot.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def help( ctx ):
    emb = discord.Embed( title = 'Навигация по командам' )

    emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистка чата!' )
    emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Удаление участника с сервера!' )
    emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Ограничение доступа к серверу!' )
    emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Удаление ограничения к серверу!' )
    emb.add_field( name = '{}mute'.format( PREFIX ), value = 'Ограничение доступа к чату сервера!' )
    emb.add_field( name = '{}umute'.format( PREFIX ), value = 'Удаление ограничения к чату сервера!' )
    emb.add_field( name = '{}userinfo'.format( PREFIX ), value = 'Информация об участнике!' )
    emb.add_field( name = '{}report'.format( PREFIX ), value = 'Жалоба на участника!' )
    emb.add_field( name = '{}serverinfo'.format( PREFIX ), value = 'Информация о сервере!' )
    emb.add_field( name = '{}ping'.format( PREFIX ), value = 'Пинг!' )
    emb.add_field( name = '{}time'.format( PREFIX ), value = 'Узнать текущее время!' )
    emb.add_field( name = '{}say'.format( PREFIX ), value = 'Отправлять сообщения от имени бота!' )
    emb.add_field( name = '{}roles'.format( PREFIX ), value = 'Показывает сколько ролей действует на сервере!' )
    emb.add_field( name = '{}event_roles'.format( PREFIX), value = 'Розыгрыш ролей!' )
    emb.add_field( name = '{}temp_add_role'.format( PREFIX ), value = 'Временная роль!')
    emb.add_field( name = '{}suggest'.format( PREFIX ), value = 'Предложение идей!' )
    emb.add_field( name = '{}botinfo'.format( PREFIX ), value = 'Информация о боте!' )
    emb.add_field( name = '{}dice'.format( PREFIX ), value = 'Игра в кубики!' )
    emb.add_field( name = '{}avatar'.format( PREFIX ), value = 'Показывает аватар пользователя!' )
    emb.add_field( name = '{}кино'.format( PREFIX ), value = 'Начинает поиск нужного фильма!')
    emb.add_field( name = '{}зайцы'.format( PREFIX ), value = 'Начинает поиск нужной музыки на "Зайцев.net"')
    emb.add_field( name = '{}wiki'.format( PREFIX ), value = 'Начинает поиск на "wikipedia"')
    emb.add_field( name = '{}ямузыка'.format( PREFIX ), value = 'Начинает поиск музыки на "Я.музыка"')
    emb.add_field( name = '{}meme'.format( PREFIX ), value = 'Отправляет мемы в чат.')
    

    await ctx.send( embed = emb )

@Bot.command()
async def roles(ctx, role: discord.Role = None):
    if not role:
        description = f''
        guild = ctx.guild
        for i in guild.roles:
            description += f'{i.mention} \n\n'
        await ctx.send(embed = discord.Embed(description = description))
    else:
        await ctx.send(embed = discord.Embed(description = f'**Участников с этой ролью:** {len(role.members)}'))


# временная роль
@Bot.command()
@commands.has_permissions(administrator = True)
async def temp_add_role(ctx, amount : int, member: discord.Member = None, role: discord.Role = None):

    try:

        if member is None:

            await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

        elif role is None:

            await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: роль!**'))

        else:

            await discord.Member.add_roles(member, role)
            await ctx.send(embed = discord.Embed(description = f'**Роль успешна выдана на {amount} секунд!**'))
            await asyncio.sleep(amount)
            await discord.Member.remove_roles(member, role)

    except:
        
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: Не удалось выдать роль.**', color=0x0c0c0c))

ev_player = [''] #игроки в розыгрыше
start_ev = 0 #перемычка

# розыгрыш ролей
@Bot.command()
async def event_roles(stx, role: discord.Role = None, member: discord.Member = None):
    global ev_player
    global start_ev
    general = client.get_channel(709698803543965746)
    if role is None:
        await stx.send('**Упомяните роль для розыгрыша.**' '\n' '`!event_roles [role]`')
        return
    ev_role = role
    start_ev = 1
    await general.send(f'Технический администратор запустил розыгрыш роли {role.mention}. Для участия пропишите `!mp`.' '\n' f'**Розыгрыш состоится через 1 минуту.**')
    await asyncio.sleep(60)
    ev_win = r.choice(ev_player)
    member = ev_win
    await general.send(f'**Поздравляем {ev_win.mention}! Он выигрывает в розыгрыше и получает роль {role.mention}.**')
    await ev_win.add_roles(role)
    ev_player = ['']
    start_ev = 0

@Bot.command()
async def mp(stx):
    global ev_player
    global start_ev
    author = stx.message.author
    if start_ev == 0:
        await stx.send('**Сейчас нету розыгрыша ролей!**')
        return
    if author in ev_player:
        await stx.send('Вы уже приняли участие в этом розыгрыше!')
        return
    else:
        ev_player.append(author)
        print(f'Игрок {author} принял участие в розыгрыши роли.')
        await stx.send(embed = discord.Embed(description = f'**{author.mention}, Вы успешно приняли участие в розыгрыши роли!**', color = 0xee3131))
        print('Розыгрыш роли завершен.')

# предложение пользователей
@Bot.command( pass_context = True, aliases = [ "Предложить", "предложить", "предложка", "Предложка", "Suggest" ])

async def suggest( ctx , * , agr ):
    suggest_chanell = client.get_channel( 709699128803721309 ) #Айди канала предложки
    embed = discord.Embed(title=f"{ctx.author.name} Предложил :", description= f" {agr} \n\n")

    embed.set_thumbnail(url=ctx.guild.icon_url)

    message = await suggest_chanell.send(embed=embed)
    await message.add_reaction('✅')
    await message.add_reaction('❎')


@Bot.command()
async def dice(ctx, od: int = None, ot: int = None):
    if od and ot:
        b = random.randint(od, ot)
        a = random.randint(od, ot)
        if b > a:
            await ctx.send(embed = discord.Embed(description = f'Ты проиграл! Боту выпало {b}, а тебе {a}. '))
        else:
            await ctx.send(embed=discord.Embed(description=f'Ты выиграл! Тебе выпало {a} а боту {b}'))
    else:
        await ctx.send(embed=discord.Embed(description='Укажите номера! (!dice 1 12)'))

@dice.error
async def dice_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send(embed = discord.Embed(description = f'Ошибка, вы неправильно указали номера!'))

#Застрелить
@Bot.command()
async def kill(  ctx, member: discord.Member ):
    await ctx.send( f"{ctx.author.mention} Достает дробовик... \n https://tenor.com/view/eyebrow-raise-smile-prepared-ready-loaded-gif-15793001" )
    await asyncio.sleep( 3 )
    await ctx.send( f"{ctx.author.mention} Направляет дробовик на {member.mention}... \n https://tenor.com/view/aim-point-gun-prepared-locked-and-loaded-gif-15793489" )
    await asyncio.sleep( 2 )
    await ctx.send( f"{ctx.author.mention} Стреляет в {member.mention}... \n https://media.discordapp.net/attachments/690222948283580435/701494203607416943/tenor_3.gif" )
    await asyncio.sleep( 2 )
    await ctx.send( f"{member.mention} истекает кровью..." )
    await asyncio.sleep( 3 )
    await ctx.send( f"{member.mention} погиб..." )


@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален')
    except PermissionError:
        print('[log] Не удалось удалить файл')

    await ctx.send('Пожалуйста ожидайте')

    voice = get(client.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'[log] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила свое проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас проигрывает музыка: {song_name[0]}')


@Bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@Bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()

@Bot.command() # Декоратор команды
async def avatar(ctx, member : discord.Member = None): # Название команды и аргументы
    user = ctx.message.author if member == None else member # 
    emb = discord.Embed( 
        title=f'Аватар пользователя {user}', 
        description= f'[Ссылка на изображение]({user.avatar_url})', 
        color=user.color #
    )
    emb.set_image(url=user.avatar_url) 
    await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def profile(ctx):
    roles = ctx.author.roles
    role_list = ""
    for role in roles:
        role_list += f"<@&{role.id}> "
    emb = discord.Embed(title='Profile', colour = discord.Colour.purple())
    emb.set_thumbnail(url=ctx.author.avatar_url)
    emb.add_field(name='Никнэйм', value=ctx.author.mention)
    emb.add_field(name="Активность", value=ctx.author.activity)
    emb.add_field(name='Роли', value=role_list)
    if 'online' in ctx.author.desktop_status:
        emb.add_field(name="Устройство", value=":computer:Компьютер:computer:")
    elif 'online' in ctx.author.mobile_status:
        emb.add_field(name="Устройство", value=":iphone:Телефон:iphone:")
    elif 'online' in ctx.author.web_status:
        emb.add_field(name="Устройство", value=":globe_with_meridians:Браузер:globe_with_meridians:")
    emb.add_field(name="Статус", value=ctx.author.status)
    emb.add_field(name='Id', value=ctx.author.id)
    await ctx.channel.purge(limit=1)
    await ctx.send(embed = emb)



#Инфо о боте
@Bot.command()
async def botinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}", description= "Бота создал : **Say**\n\n"
                                                              "Помог в создании: **✘Ⲙⲁⲧⲟ✘**\n\n"
                                                              "Бот создан на : **Discord.py**\n\n"
                                                              "Версия бота : **18.4**\n\n")

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text="© Copyright 2020 Say-BOT - Все права защищены!")

    await ctx.send(embed=embed)

@Bot.command()
async def google(ctx, *, question): # погуглить
    # сам сайт
    url = 'https://google.gik-team.com/?q=' + str(question).replace(' ', '+')
    await ctx.send(f'Так как кое кто не умеет гуглить, я сделал это за него.\n{url}')

@Bot.command(pass_context = True,alieses=['вики']) #!wiki 
async def wiki( ctx, *, amount: str):
    if not amount:
        await ctx.send("Пожалуйста, используйте такую констркуцию: `!wiki [wiki запрос]`")
    a = '_'.join(amount.split())
    await ctx.send(f'https://ru.wikipedia.org/wiki/{a}')

@Bot.command()
async def ямузыка(ctx, *, question):
    url = "https://music.yandex.ru/search?text=" + str(question).replace(" ", "%20")
    await ctx.send(f"Музыку захотел послушать? ок лови\n{url}")

@Bot.command()
async def зайцы(ctx, *, question):
    url = "https://zaycev.net/search.html?query_search=" + str(question).replace(" ", "+")
    await ctx.send(f"Музыку захотел послушать? ок лови\n{url}")

@Bot.command()
async def кино(ctx, *, question):
    url = "https://kinopoisk.ru/index.php?kp_query" + str(question).replace(" ", "+")
    await ctx.send(f"Кино? Ок\n{url}")

def random_meme():
    with open('memes_data.txt', 'r') as file:
        memes = file.read().split(',')
    picked_meme = random.choice(memes)
    return picked_meme

@Bot.command()
async def meme(ctx):
    emb = discord.Embed(description = 'Вот подобраный мем.', color = 0x00ffff)
    emb.set_image(url = random_meme())
    await ctx.send(embed=emb)

@Bot.command()
async def status(ctx):
    r = (0xcc29a9, 0x0c0c0c, 0x004B3EE1, 0x00C8E14B, 0x00E15239, 0x00E116D3, 0x002CE141, 0x0023C5E1, 0x00E116E1)
    rd = random.choice(r)
    emb = discord.Embed(title="Baned",color = int(rd), description = f'[SYSTEM] Bot online!\n[SYSTEM] Name - {client.user}\n[SYSTEM] ID - {client.user.id}\n[SYSTEM] Token - ')
    await ctx.send(embed=emb)
    print("1")

token = os.environ.get("BOT_TOKEN")

bot.run(str(token))
