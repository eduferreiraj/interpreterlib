# Eduardo Ferreira José, 2018
#
# - Arquivo interpretador.py
# Arquivo contendo o main, para chamar a biblioteca.

from interpreterlib import Interpreter, Assertions
import sys

if __name__ == "__main__":
    Interpreter(sys.argv).execute()
