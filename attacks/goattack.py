"""
@author: azseza
HTTP flood attack declared in go file as a shared library
"""
import multiprocessing
import requests

class HttpGoFood(multiprocessing.Process):
    """
     httpFlood demo
    """
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.target = ""
        self.numberOfBots = 50
        self.headers = {'Headless' : ''}
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
            },
            {
                'type': 'list',
                'name': 'headers',
                'message': 'Choose A header Flavor :) '
                'choices':['Headless', 'one_header', ' mixed_header']
            }
        ]
        answers = prompt(questions, style=style)
        self.target = answers.get("target")
        self.numberOfBots = answers.get("nob")
        choice = self.headers[answers.get("headers")]
        if choice == 'sokcet':
            # raw socket flooding sequence
            pass
        elif choice == '':
    def run(self):
        try:
            file = pathlib.Path(gofile)
            if file.exists():
                lib = cdll.LoadLibrary('./httpflood.so')
                lib(self.target, self.numberOfBots)
            else:
                raise FileNotFoundError
        except BrokenGoFile:
            log("something went wrong with the Go interpreter", color="red")
        except FileNotFoundError:
            log("Did You make the project ? Go executable not found!", color="red")
        except NameError:
            log("Go object shared library not found, Did You make the project ? ", color="red")

