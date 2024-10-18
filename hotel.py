import time
import sys

class AVLTree:
    class AVLNode:
        def __init__(self, room_no):
            self.room_no = room_no
            self.left = None
            self.right = None
            self.height = 1

        def __str__(self):
            return str(self.room_no)

        def setHeight(self):
            self.height = 1 + max(self.getHeight(self.left), self.getHeight(self.right))

        def getHeight(self, node):
            return 0 if node is None else node.height

        def balanceValue(self):
            return self.getHeight(self.right) - self.getHeight(self.left)

    def __init__(self):
        self.root = None

    def add(self, room_no):
        result, is_duplicate = self._add(self.root, room_no)
        if is_duplicate:
            return False
        else:
            self.root = result
            return True

    def _add(self, node, room_no):
        if node is None:
            return self.AVLNode(room_no), False

        if room_no < node.room_no:
            node.left, is_duplicate = self._add(node.left, room_no)
        elif room_no > node.room_no:
            node.right, is_duplicate = self._add(node.right, room_no)
        else:
            return node, True

        node.setHeight()
        return self._rebalance(node), is_duplicate

    def _rebalance(self, node):
        balance = node.balanceValue()

        if balance > 1:
            if node.right.balanceValue() < 0:
                node.right = self.rotateRightChild(node.right)
            return self.rotateLeftChild(node)

        if balance < -1:
            if node.left.balanceValue() > 0:
                node.left = self.rotateLeftChild(node.left)
            return self.rotateRightChild(node)

        return node


    def rotateLeftChild(self, root):
        right = root.right
        root.right = right.left
        right.left = root

        root.setHeight()
        right.setHeight()

        return right

    def rotateRightChild(self, root):
        left = root.left
        root.left = left.right
        left.right = root

        root.setHeight()
        left.setHeight()

        return left

    def delete(self, room_no):
        self.root, deleted = self._delete(self.root, room_no)
        return deleted

    def _delete(self, node, room_no):
        if node is None:
            return node, False

        if room_no < node.room_no:
            node.left, deleted = self._delete(node.left, room_no)
        elif room_no > node.room_no:
            node.right, deleted = self._delete(node.right, room_no)
        else:
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            temp = self._get_min_value_node(node.right)
            node.room_no = temp.room_no
            node.right, _ = self._delete(node.right, temp.room_no)
            deleted = True
            
        node.setHeight()
        return self._rebalance(node), deleted

    def _get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search(self, room_no):
        return self._search(self.root, room_no)

    def _search(self, node, room_no):
        if node is None or node.room_no == room_no:
            return node
        if room_no < node.room_no:
            return self._search(node.left, room_no)
        return self._search(node.right, room_no)

    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node is not None:
            self._in_order(node.left, result)
            result.append(node)
            self._in_order(node.right, result)

class Hotel:
    def __init__(self):
        self.people_distribution = []
        self.total_room = 0
        self.manual_rooms = AVLTree()
    
    def manual_add(self, room_no):
        if room_no > self.total_room and self.manual_rooms.add(room_no):
            return f"room {room_no} added"
        else:
            return f"room {room_no} already exists"   

    def manual_delete(self, room_no):
        if room_no > self.total_room and self.manual_rooms.delete(room_no):
            return f"room {room_no} deleted"
        else:
            return f"room {room_no} is not manual room"

    def sort_rooms(self):
        print(self.total_room)
        for i in range(1, self.total_room + 1):
            print(i, end = " ")
        for i in self.manual_rooms.in_order():
            print(i, end = " ")

    def search_room(self, room_no):
        if room_no > self.total_room and self.manual_rooms.search(room_no):
            return f"Manual add"
        else:
            people_distribution = self.people_distribution + [0] * (5 - len(self.people_distribution))
            people_in_channel_1 = people_distribution[0]
            people_in_channel_2 = people_distribution[1] * 2
            people_in_channel_3 = people_distribution[2] * 8
            people_in_channel_4 = people_distribution[3] * 64
            people_in_channel_5 = people_distribution[4] * 1024
            
            previous_people = 0
            
            if room_no <= people_in_channel_1:
                return f'no_{room_no}'
            
            previous_people += people_in_channel_1
            if room_no <= previous_people + people_in_channel_2:
                person_in_motorcycle = room_no - previous_people
                bike_number = (person_in_motorcycle - 1) // 2 + 1
                person_on_bike = (person_in_motorcycle - 1) % 2 + 1
                return f'no_{person_on_bike}_{bike_number}'
            
            previous_people += people_in_channel_2
            if room_no <= previous_people + people_in_channel_3:
                person_in_truck = room_no - previous_people
                truck_number = (person_in_truck - 1) // 8 + 1
                remaining_people_in_truck = (person_in_truck - 1) % 8
                bike_number = (remaining_people_in_truck // 2) + 1
                person_on_bike = (remaining_people_in_truck % 2) + 1
                return f'no_{person_on_bike}_{bike_number}_{truck_number}'
            
            previous_people += people_in_channel_3
            if room_no <= previous_people + people_in_channel_4:
                person_in_plane = room_no - previous_people
                plane_number = (person_in_plane - 1) // 64 + 1
                remaining_people_in_plane = (person_in_plane - 1) % 64
                truck_number = (remaining_people_in_plane // 8) + 1
                remaining_people_in_truck = remaining_people_in_plane % 8
                bike_number = (remaining_people_in_truck // 2) + 1
                person_on_bike = (remaining_people_in_truck % 2) + 1
                return f'no_{person_on_bike}_{bike_number}_{truck_number}_{plane_number}'
            
            previous_people += people_in_channel_4
            if room_no <= previous_people + people_in_channel_5:
                person_in_ship = room_no - previous_people
                ship_number = (person_in_ship - 1) // 1024 + 1
                remaining_people_in_ship = (person_in_ship - 1) % 1024
                plane_number = (remaining_people_in_ship // 64) + 1
                remaining_people_in_plane = remaining_people_in_ship % 64
                truck_number = (remaining_people_in_plane // 8) + 1
                remaining_people_in_truck = remaining_people_in_plane % 8
                bike_number = (remaining_people_in_truck // 2) + 1
                person_on_bike = (remaining_people_in_truck % 2) + 1
                return f'no_{person_on_bike}_{bike_number}_{truck_number}_{plane_number}_{ship_number}'
            
        return "Not found"
    
    def start(self):
        print()
        people_input = input("Enter Airplane carrier, Airplane, Truck, Motorcycle, Guest (split by ' '): ")
        start_time = time.time()
        self.people_distribution = list(map(int, people_input.split()))
        self.total_room = sum([
            self.people_distribution[0],
            self.people_distribution[1] * 2,
            self.people_distribution[2] * 8,
            self.people_distribution[3] * 64,
            self.people_distribution[4] * 1024
        ])
        end_time = time.time()
        print(f"Run time : {end_time - start_time:.20f} seconds")
        
    def write_to_file(self):
        print()
        filename = input("Enter file name (ex.'room.txt') : ")
        with open(filename, 'w', encoding='utf-8') as file:
            for room_no in range(1, self.total_room + 1):
                result = self.search_room(room_no)
                file.write(f'Room {room_no} : {result}\n')
            for room_no in self.manual_rooms.in_order():
                file.write(f'Room {room_no} : Manual add\n')
        print(f"All room have been written to {filename}")
    
    def memory_usage(self):
        total_size = sys.getsizeof(self)
        total_size += sys.getsizeof(self.people_distribution)
        total_size += sys.getsizeof(self.total_room)
        total_size += sys.getsizeof(self.manual_rooms)
        total_size += self._memory_usage_of_avl_tree(self.manual_rooms.root)

        print(f"Total memory usage of Hotel : {total_size} bytes")
    
    def _memory_usage_of_avl_tree(self, node):
        if node is None:
            return 0
        return (sys.getsizeof(node) + 
                self._memory_usage_of_avl_tree(node.left) + 
                self._memory_usage_of_avl_tree(node.right))

hotel = Hotel()
hotel.start()

while True:
    print()
    print("--- Hotel Command Menu ---")
    print("1 : Manual add room")
    print("2 : Manual delete room")
    print("3 : Sort rooms")
    print("4 : Search room by number")
    print("5 : Show free rooms")
    print("6 : Write to file")
    print("7 : Show memory usage")
    print("8 : Exit")
    
    command = input("Enter command : ")

    if command == "1":
        room_no = int(input("Enter room number to add : "))
        print()
        start_time = time.time()
        print(hotel.manual_add(room_no))
        end_time = time.time()
        print(f"Run time : {end_time - start_time:.20f} seconds")
    elif command == "2":
        room_no = int(input("Enter room number to delete : "))
        print()
        start_time = time.time()
        print(hotel.manual_delete(room_no))
        end_time = time.time()
        print(f"Run time : {end_time - start_time:.20f} seconds")
    elif command == "3":
        print()
        start_time = time.time()
        hotel.sort_rooms()
        end_time = time.time()
        print(f"\nRun time : {end_time - start_time:.20f} seconds")
    elif command == "4":
        room_no = int(input("Enter room number to search : "))
        print()
        start_time = time.time()
        result = hotel.search_room(room_no)
        print(f"Room {room_no} : {result}")
        end_time = time.time()
        print(f"Run time : {end_time - start_time:.20f} seconds")
    elif command == "5":
        print()
        start_time = time.time()
        print(f"Free room : {None}")
        end_time = time.time()
        print(f"Run time : {end_time - start_time:.20f} seconds")
    elif command == "6":
        start_time = time.time()
        hotel.write_to_file()
        end_time = time.time()
        print(f"Run time : {end_time - start_time:.20f} seconds")
    elif command == "7":
        print()
        hotel.memory_usage()
    elif command == "8":
        print()
        print("Exit the program !")
        print()
        break
    else:
        print()
        print("Wrong command ! please select 1 - 8")