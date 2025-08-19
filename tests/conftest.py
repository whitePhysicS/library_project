import sys, pathlib
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
p = str(PROJECT_ROOT)
if p not in sys.path:
    sys.path.insert(0, p)
