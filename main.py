import simpy
from node import Node
from ring import Ring

# Simulation
env = simpy.Environment()
ring = Ring(env)

# Creating and adding nodes to the ring
node1 = Node(env, 100)
node2 = Node(env, 250)
node3 = Node(env, 500)
node4 = Node(env, 750)
node5 = Node(env, 1000)

ring.add_node(node1)
ring.add_node(node2)
ring.add_node(node3)
ring.add_node(node4)
ring.add_node(node5)

# Store data
node1.put_data("user1", {"prenom": "Daniel", "x": "123", "y": "123"})
node1.put_data("user2", {"prenom": "Sol", "x": "123", "y": "123"})

ring.remove_node(node3)

# Retrieve data
print(node2.get_data("user1"))

# Run the simulation
env.run(until=100)
