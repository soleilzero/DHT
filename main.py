import simpy
from node import Node
from ring import Ring
from message import Message

# Simulation
env = simpy.Environment()
ring = Ring(env)

# Creating and adding nodes to the ring
node1 = Node(env, 1)
node2 = Node(env, 2)
node3 = Node(env, 3)
node4 = Node(env, 4)

ring.add_node(node1)
ring.add_node(node2)
ring.add_node(node3)
ring.add_node(node4)

#message
message1 = Message(node1, node3, "Hi node3, its node1")
message1.send()
message2 = Message(node4, node2, "Hi node 2, its the new node 4")
message2.send()

# Simulating the removal of a node
ring.remove_node(node2)

# Simulation running for 100 time units
env.run(until=100)
