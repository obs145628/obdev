import os
import sys

OBTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../obts/python"))
sys.path.append(OBTS_DIR)
from obts.tsauto import TSAuto

OBCONTROL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../obcontrol/python"))
sys.path.append(OBCONTROL_DIR)
from obcontrol.controlapp import ControlApp

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/obcontrol"))

app = ControlApp(data_dir=DATA_DIR)
res = app.run()
sys.exit(res)
