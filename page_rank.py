from random import choice
import sys
import os
import time
import argparse
import networkx as nx


def load_graph(args):

    G = nx.DiGraph()
    # Iterate through the file line by line
    for line in args.datafile:
        # And split each line into two URLs
        node, target = line.split()

        # add an edge to the graph
        G.add_edge(node, target)
        # Return the NetworkX graph
    return G


def print_stats(graph):


    print(f'Number of Nodes: {graph.number_of_nodes()}')
    print(f'Number of Edges: {graph.number_of_edges()}')


def stochastic_page_rank(graph, args):


    # Initialize hit_count dictionary with 0 for all nodes
    hit_count = {node: 0 for node in graph.nodes}
    # adding a new variable
    list_graph_nodes = list(graph.nodes)

    # choose a starting node randomly
    current_node = choice(list_graph_nodes)
    hit_count[current_node] += 1

    for n in range(args.repeats):

        # checking if the current node has any out edges
        if graph.out_degree(current_node) == 0:

            # choosing another random node
            current_node = choice(list_graph_nodes)
        else:
            # choose one out edge of the current node randomly
            node1, target = choice(list(graph.out_edges(current_node)))
            current_node = target
        # increase the number of hits for the final node After n_steps
        hit_count[current_node] += 1
    return hit_count


def distribution_page_rank(graph, args):

    # initialize node_prob with 1/(number of nodes) for all nodes
    node_prob = {node: 1 / graph.number_of_nodes() for node in graph.nodes}

    for n in range(args.steps):
        # initialize next_prob 0 for all nodes
        next_prob = {node: 0 for node in graph.nodes}
        for node in graph.nodes:

            p = node_prob[node] / graph.out_degree(node)
            for n, target in graph.out_edges(node):
                next_prob[target] += p

        node_prob = next_prob

    return node_prob


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")

if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100 * v:.2f}\t{k}' for k, v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
