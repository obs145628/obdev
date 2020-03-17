import os
import sys

OBTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../obts/python"))
sys.path.append(OBTS_DIR)
from obts.tsauto import TSAuto

OUTPUT_DIR = os.getenv("OBTS_OUTPUT_DIR")
BUILD_DIR = os.getenv("OBTS_BUILD_DIR")
BINARY_DIR = os.getenv("OBTS_BINARY_DIR")

root = sys.argv[1]
ts = TSAuto(root, output_dir=OUTPUT_DIR, build_dir=BUILD_DIR, binary_dir=BINARY_DIR)
res = ts.run()
sys.exit(res)
