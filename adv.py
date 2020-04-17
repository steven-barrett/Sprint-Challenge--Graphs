from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Helper function to pick out an unexplored rooom
def pick_unexplored_room(room):
    # Using a fixed order, return a room's first unexplored direction
    directions = ['n', 's', 'e', 'w']  # Createa fixed order
    random.shuffle(directions)  # randomly select it
    # Loop on each direction 
    for direction in directions:
        explored = room.get(direction)
        if explored == '?':
            return direction
    return None

def find_unexplored_room(room, graph):    
    # Look for closest unexplored exit and return a path to it
    # Create a queue...
    qq = []

    # Add a path to the room_id to the queue
    qq.append([room])

    # Create an empty set to store visited rooms
    visited = set()

    # While the queue is not empty...
    while qq:
        # Dequeue the first path
        path = qq.pop(0)

        # grab the last room from the path
        room = path[-1]

        # If last room has an unexplored exit, return the path
        # Hopefully my nested loop isn't too slow... :/
        if pick_unexplored_room(graph[room]):
            rewind = []
            for i in range(1, len(path)):
                for room_direction, room_id in graph[path[i-1]].items():
                    if room_id == path[i]:
                        rewind.append(room_direction)
                        break
            return rewind

        # If it has not been visited
        if room not in visited:
            # Mark it as visited
            visited.add(room)
            # Then add a path to all unvisited rooms to the back of the queue
            for next_room in graph[room].values():
                if next_room not in visited:
                    q.append(path + [next_room])
    return None

def explore_rooms(player, traversal_path):    
    # add first room to graph and initialize exits
    reverse_d = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}     
    graph = {player.current_room.id: {}}
    for exits in player.current_room.get_exits():
        graph[player.current_room.id][exits] = '?'

    # enter a room in an unexplored direction
    direction = pick_unexplored_room(graph[player.current_room.id])
    if direction is None:
        print("Help, I am trapped in a room with no exits!")
        return -1

    # make a previous_room variable and save the last room
    prev_room = player.current_room

    # append the direction to the traversal path
    player.travel(direction)
    traversal_path.append(direction)

    # constant loop While True:
    while True:
        # if new room, add to graph and initialize exits
        if player.current_room.id not in graph:
            graph[player.current_room.id] = {}
            for exits in player.current_room.get_exits():  # Loop through all the exits and initialize them
                graph[player.current_room.id][exits] = '?'

        # if entered from an unexplored direction, make connections between the new room and the previous room
        if graph[player.current_room.id][reverse_d[direction]] == '?':
            graph[player.current_room.id][reverse_d[direction]] = prev_room.id
            graph[prev_room.id][direction] = player.current_room.id

        

# Call the function to start the exploring!!                            
explore_rooms(player, traversal_path)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
