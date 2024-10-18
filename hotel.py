import time

class Hotel:
    def __init__(self):
        self.last_room = 0
        self.manual_rooms = {}
    
    def add_guest(self, guest):
        self.rooms.append(guest)
    
    def automatic_add(self, airplane_carrier, airplane, truck, motorcycle, guest):
        count = airplane_carrier * airplane * truck * motorcycle * guest
        self.last_room = count
        # for a in range(1, airplane_carrier+1):
        #     for b in range(1, airplane+1):
        #         for c in range(1, truck+1):
        #             for d in range(1, motorcycle+1):
        #                 for e in range(1, guest+1):
        #                     self.add_guest(f"no.{a}_{b}_{c}_{d}_{e}")
    
    # def automatic_add(self, airplane_carrier, airplane, truck, motorcycle, guest):
    #     for i in range(count):
    #         a = (i // (airplane * truck * motorcycle * guest)) % airplane_carrier + 1
    #         b = (i // (truck * motorcycle * guest)) % airplane + 1
    #         c = (i // (motorcycle * guest)) % truck + 1
    #         d = (i // guest) % motorcycle + 1
    #         e = i % guest + 1
    #         hotel.add_guest(f"no.{a}_{b}_{c}_{d}_{e}")

    def manual_add(self, room, guest):
        if room > self.last_room:
            self.last_room = room
            self.manual_rooms[room] = guest
            print(f"room {room} added")
        else:
            print(f"room {room} already exists")

    def manual_delete(self, room):
        if room in self.manual_rooms:
            self.manual_rooms.pop(room)
        else:
            print(f"room {room} is not manual room")
    
    def sort_room(self):
        print(self.last_room)
        for i in range(1, self.last_room + 1):
            print(i)


airplane_carrier, airplane, truck, motorcycle, guest = [int(i) for i in input("Enter 1, 2, 3, 4, 5 : ").split()]

hotel = Hotel()

hotel.automatic_add(airplane_carrier, airplane, truck, motorcycle, guest)
hotel.sort_room()
