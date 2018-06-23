# Eduardo Ferreira José, 2018
#
# - Arquivo interpretador.py
# Arquivo contendo o main, e as funções com as regras de negócio do
# interpretador. Onde a magia acontece!

from interpreterlib import Interpreter, Assertions
import sys

if __name__ == "__main__":
    Interpreter(sys.argv).execute()
