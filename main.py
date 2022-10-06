import os
import requests
import websocket
import threading
import subprocess

errorCache = {}

def newError(name: str):
    if name in errorCache:
        return errorCache[name]
    error = type(name, (Exception, object), {})
    errorCache[name] = error
    return error

class Discord:
    discordRunning = False
    websocketDebuggerUrl = None
    port = None

    @classmethod
    def openDiscord(cls, discordLocation: str, port: int):
        if not os.path.isfile(discordLocation):
            raise newError('DiscordNotFound')
        tasks = subprocess.Popen('tasklist', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tasklist = tasks.communicate()[0].lower()
        if b'discord.exe' in tasklist:
            subprocess.Popen(['taskkill', '/f', '/im', 'Discord.exe'])

        def openDiscordThread():
            def openDiscordLoop():
                subprocess.Popen([f'"{discordLocation}"' if ' ' in discordLocation else discordLocation, f'--remote-debugging-port={port}'])
                cls.discordRunning = True
                while True: pass
            return threading.Thread(target=openDiscordLoop, daemon=True).start()

        return openDiscordThread()

    @classmethod
    def fetchDebuggerUrl(cls):
        raise NotImplementedError
