from program import Program
from ui import UI

ui = UI()
prog = Program(ui)
ui.program = prog
prog.start()
