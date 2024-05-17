from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSController
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI

import random
# Import random because randomness in quantum process

# Rectilinear and Diagonal refer to two different polarization states

RECTILINEAR = '+'
DIAGONAL = 'x'

# Generate list of random bits (0 or 1) and random bases and return 2 lists
def generate_bits_and_bases(length):
bits = [random.randint(0, 1) for _ in range(length)]
bases = [random.choice([RECTILINEAR, DIAGONAL]) for _ in range(length)]
return bits, bases


# Pairs each bit with its corresponding base in the list
def encode_bits(bits, bases):
return[(bit, base) for bit, base in zip(bits, bases)]


# Eve intercepts and measures using guessed bases (attack simulation)
def intercept_and_measure(encoded_bits):

# This is how Alice and Bob choose their bases
guessed_bases = [random.choice([RECTILINEAR, DIAGONAL]) for _ in encoded_bits]
# compare the guessed_bases list with the actual bases list to simulate an attack
measured_bits = []
for (bit, base), guessed_base in zip(encoded_bits, guessed_bases):
# Attacker in middle "EVE" has 50% chance to guess the correct base
if base == guessed_base:
# if the bit is right then we append the correct bits to the measured array
measured_bits.append(bit)
else:
# if the bits are wrong then we just append a random guess in between 0 and 1
measured_bits.append(random.randint(0, 1)) 
return measured_bits, guessed_bases


# Bob measures his bits and only adds them to the list if it's right
def measure_bits(encoded_bits, bob_bases):
bob_measured_bits = []
# bob's base measuring idea is the same as eve's but he doesn't append random guesses to his bits
for (bit, base), bob_base in zip(encoded_bits, bob_bases):
if base == bob_base:
bob_measured_bits.append(bit)
else:
bob_measured_bits.append(None)
return bob_measured_bits


#qkd simulation with the attack
def qkd_simulation(length = 10):
# Generates bits and bases for alice and encode them
alice_bits, alice_bases = generate_bits_and_bases(length)
encoded_bits = encode_bits(alice_bits, alice_bases)
# Eve intercepts the bases
eve_bits, eve_bases = intercept_and_measure(encoded_bits)
# Bob generates his bases and measures the bits sent by alice
bob_bases = [random.choice([RECTILINEAR, DIAGONAL]) for _ in range(length)]
bob_measured_bits = measure_bits(encoded_bits, bob_bases)
# Alice and Bob perform key sifting, discards bits where they don't match, secret key is created
sifting_indices = [i for i in range(length) if alice_bases[i] == bob_bases[i]]
alice_key = [alice_bits[i] for i in sifting_indices]
bob_key = [bob_measured_bits[i] for i in sifting_indices if bob_measured_bits[i]]


return alice_key, bob_key, eve_bits

alice_key, bob_key, eve_bits = qkd_simulation()

print("Alice Key: ", alice_key)
print("Bob key: ", bob_key)
print("Eve bits: ", eve_bits)
