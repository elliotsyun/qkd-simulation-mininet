from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSController
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI

import random

# BB84 Quantum Key Distribution Functions
RECTILINEAR = '+'
DIAGONAL = 'x'

def generate_bits_and_bases(length):
    bits = [random.randint(0, 1) for _ in range(length)]
    bases = [random.choice([RECTILINEAR, DIAGONAL]) for _ in range(length)]
    return bits, bases

def encode_bits(bits, bases):
    return [(bit, base) for bit, base in zip(bits, bases)]

def intercept_and_measure(encoded_bits):
    guessed_bases = [random.choice([RECTILINEAR, DIAGONAL]) for _ in encoded_bits]
    measured_bits = []
    for (bit, base), guessed_base in zip(encoded_bits, guessed_bases):
        if base == guessed_base:
            measured_bits.append(bit)
        else:
            measured_bits.append(random.randint(0, 1))
    return measured_bits, guessed_bases

def measure_bits(encoded_bits, bob_bases):
    bob_measured_bits = []
    for (bit, base), bob_base in zip(encoded_bits, bob_bases):
        if base == bob_base:
            bob_measured_bits.append(bit)
        else:
            bob_measured_bits.append(None)
    return bob_measured_bits

def qkd_simulation(length=10):
    alice_bits, alice_bases = generate_bits_and_bases(length)
    encoded_bits = encode_bits(alice_bits, alice_bases)
    eve_bits, eve_bases = intercept_and_measure(encoded_bits)
    bob_bases = [random.choice([RECTILINEAR, DIAGONAL]) for _ in range(length)]
    bob_measured_bits = measure_bits(encoded_bits, bob_bases)
    sifting_indices = [i for i in range(length) if alice_bases[i] == bob_bases[i]]
    alice_key = [alice_bits[i] for i in sifting_indices]
    bob_key = [bob_measured_bits[i] for i in sifting_indices if bob_measured_bits[i] is not None]
    return alice_key, bob_key, eve_bits

class MyTopo(Topo):
    def build(self):
        alice = self.addHost('alice')
        bob = self.addHost('bob')
        switch = self.addSwitch('s1')
        self.addLink(alice, switch)
        self.addLink(bob, switch)

def run():
    topo = MyTopo()
    net = Mininet(topo=topo, controller=OVSController, link=TCLink)
    net.start()
    alice, bob = net.get('alice', 'bob')
    alice_key, bob_key, eve_bits = qkd_simulation()
    print("Alice Key: ", alice_key)
    print("Bob Key: ", bob_key)
    print("Eve Bits: ", eve_bits)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
