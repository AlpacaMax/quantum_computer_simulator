import numpy as np 
import math
import random

#All quantum logic gates
ONE = np.array([1], complex)

IDENTITY = np.array(
    [[1, 0],
     [0, 1]], complex
)

PAULI_X = np.array(
    [[0, 1],
     [1, 0]], complex
)

H = (1/math.sqrt(2)) * np.array(
    [[1, 1],
     [1,-1]], complex
)

PAULI_Y = np.array(
    [[0,-1j],
     [1j, 0]], complex
)

PAULI_Z = np.array(
    [[1, 0],
     [0,-1]], complex
)

SWAP = np.array(
    [[1, 0, 0, 0],
     [0, 0, 1, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 1]], complex
)

CNOT = np.array(
    [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 1],
     [0, 0, 1, 0]], complex
)

class Circuit:
    def __init__(self, n):
        self.numQubits = n

        self.qubits = None
        self.collapse(0)

        self.isCollapsed = True

    def __repr__(self):
        if not self.isCollapsed:
            self.measure()

        return self.toString()

    def __getitem__(self, ind):
        if not self.isCollapsed:
            self.measure()
        
        recovered = self.recoverQubits()
        return recovered[ind]
    
    def recoverQubits(self):
        temp = list(self.qubits)

        try:
            deci = temp.index(ONE)
        except:
            raise ValueError("You have to measure the circuit")

        qState = list(bin(deci))[2:]
        qState += ['0'] * (self.numQubits - len(qState))

        return qState
        
    def measure(self):
        #print("Measuring")

        vDie = random.random()
        temp = 0
        collapState = None

        for i in range(len(self.qubits)):
            temp += self.qubits[i][0] ** 2
            if temp > vDie:
                collapState = i
                break
        
        self.collapse(collapState)

    def collapse(self, ind):
        #print("Collapsing")

        self.qubits = np.zeros((2 ** self.numQubits, 1), complex)
        self.qubits[ind][0] = 1

        self.isCollapsed = True

    def applyGate(self, ind, gate, name='GATE'):
        self.isCollapsed = False

        #print("Applying " + name)
        shape = gate.shape
        step = int(math.log(shape[0], 2))

        GATE = ONE
        index = 0
        while index < self.numQubits:
            if index == ind:
                GATE = np.kron(GATE, gate)
                index += step
            else:
                GATE = np.kron(GATE, IDENTITY)
                index += 1
        
        self.qubits = np.dot(GATE, self.qubits)
    
    def toString(self):
        qState = self.recoverQubits()
        qState.reverse()

        mathRepr = '|' + ''.join(qState) + '>'
        return mathRepr