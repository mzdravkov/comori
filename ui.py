# from program import Program
from ui_interface import UIInterface
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
import sys

class MyApp(ShowBase):
    pass


class EventHandler(DirectObject.DirectObject):
    def __init__(self, program):
        self.program = program
        self.accept('mouse1', program.handle, ['left_click'])
        self.accept('wheel_up', program.handle, ['wheel_up'])
        self.accept('wheel_down', program.handle, ['wheel_down'])
        self.accept('arrow_up', program.handle, ['up'])
        self.accept('arrow_down', program.handle, ['down'])
        self.accept('enter', program.handle, ['enter'])


class UI(UIInterface):
    def start(self):
        self.app = MyApp()
        self.eventHandler = EventHandler(self.program)
        self.app.run()

    def exit(self):
        sys.exit()
