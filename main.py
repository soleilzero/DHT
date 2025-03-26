import simpy
from node import Node
from ring import Ring


def main():
    # Création de l'environnement de simulation
    env = simpy.Environment()
    ring = Ring(env)

    # Création et ajout de nœuds à l'anneau
    print("\n")
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

    # Afficher la table de routage initiale
    display_routing_table(ring.nodes)

    # Test de l'envoi de messages
    node1.send_message(node5.node_id, "Salut, Node 1000!")
    node1.send_message(node3.node_id, "Bonjour, Node 500!")
    print("\n")

    # Test des raccourcis pour un routage plus efficace
    node3.send_message(node1.node_id, "Message pour Node 100!")
    print("\n")

    # Afficher la table de routage après l'ajout des liens longs
    display_routing_table(ring.nodes)
    
    # Test du stockage et de la récupération des données
    node1.put_data("user1", {"name": "Daniel", "x": "123", "y": "123"})
    node1.get_data("user1")
    print("\n")

    # Test de la suppression des nœuds et de la réplication des données
    ring.remove_node(node3)
    ring.remove_node(node2)
    ring.remove_node(node4)
    print("\n")

    # Tentative de récupération des données après suppression
    node1.get_data("user1")
    print("\n")

    # Exécuter la simulation
    env.run(until=100)


def display_routing_table(nodes):
    print("\n# Tables de Routage:")
    for node in nodes:
        print(f"Node {node.node_id}: {list(node.routing_table.keys())}")
    print("\n")


if __name__ == "__main__":
    main()
