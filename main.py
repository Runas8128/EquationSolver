import os
import psutil
import threading

import time
import math

import sympy

x = sympy.Symbol('x')

def elapsed_since(start: float) -> str:
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))

def get_process_memory() -> int:
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

class taskSolve(threading.Thread):
    def __init__(self, tarFunc: sympy.Expr, tarY: float, tarVar: sympy.Symbol):
        self.tarFunc = tarFunc
        self.tarY    = tarY
        self.tarVar  = tarVar
    
    def run(self, *args, **kwargs):
        sol = sympy.solve(tarFunc - tarY, tarVar)
        print(f"Solve End! Solution: {sol}")

class taskTracker(threading.Thread):
    def __init__(self, trackThread: threading.Thread):
        self.t         = trackThread
        self.startTime = 0
        self.startMem  = 0

    def run(self, *args, **kwargs):
        self.startTime = time.time()
        self.startMem  = get_process_memory()

        while self.t.is_alive():
            timeElapse = elapsed_since(self.startTime)
            memUsage = get_process_memory() - self.startMem
            print(f"Thread `{self.t.getName()}`: memUsage: {memUsage/1024:.2f}MB, exec time: {timeElapse}")

tSolve = taskSolve(
    tarFunc =
        -0.91345 * (math.e ** (-x / 11.63286)) + \
        -0.91354 * (math.e ** (-x / 14.21794)) + \
        1.82708,\
    tarY    = 0.01,
    tarVar  = x
)

tTrack = taskTracker(
    trackThread=tSolve
)

tSolve.start()
tTrack.start()
