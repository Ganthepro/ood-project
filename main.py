class HilbertsHotel:
    def __init__(self):
        self.room_assignments = {}
        self.occupied_rooms = set()
        self.current_room_number = 1

    def check_in_existing(self, existing_guests):
        for i in range(1, existing_guests + 1):
            self.room_assignments[i] = f"Guest {i}"
            self.occupied_rooms.add(i)
        self.current_room_number = existing_guests + 1 

    def generate_room_number(self):
        room_number = self.current_room_number
        self.current_room_number += 1
        return room_number

    def check_in_incoming_guests(self, spaceships, ships, buses, persons):
        for spaceship in range(spaceships):
            for ship in range(ships):
                for bus in range(buses):
                    for person in range(persons):
                        room_number = self.generate_room_number()
                        guest_info = {
                            'spaceship': spaceship + 1,
                            'ship': ship + 1,
                            'bus': bus + 1,
                            'person': person + 1
                        }
                        self.room_assignments[room_number] = guest_info
                        self.occupied_rooms.add(room_number)
                        print(f"Set {guest_info} to room {room_number}")

    def manual_add_room(self, room_number, guest_info):
        if room_number not in self.occupied_rooms:
            self.room_assignments[room_number] = guest_info
            self.occupied_rooms.add(room_number)
            print(f"Manual Add room {room_number} to {guest_info}.")
        else:
            print(f"Room {room_number} is already occupied.")

    def manual_delete_room(self, room_number):
        if room_number in self.occupied_rooms:
            del self.room_assignments[room_number]
            self.occupied_rooms.remove(room_number)
            print(f"Room {room_number} has been deleted.")
        else:
            print(f"Room {room_number} is not occupied.")

    def sort_rooms(self):
        print(f"Sorted room numbers: {self.occupied_rooms}")
        return self.occupied_rooms
    
    def search_room(self, room_number):
        if room_number in self.occupied_rooms:
            guest_info = self.room_assignments[room_number]
            print(f"Room {room_number} is occupied.")
            print(f"User Info: Spaceship {guest_info['spaceship']}, Ship {guest_info['ship']}, Bus {guest_info['bus']}, Person {guest_info['person']}")
            return True
        else:
            print(f"Room {room_number} is not occupied.")
            return False

    def find_missing_rooms(self):
        if not self.occupied_rooms:
            print("No rooms are occupied.")
            return []

        min_room_number = min(self.occupied_rooms)
        max_room_number = max(self.occupied_rooms)
        all_rooms = set(range(min_room_number, max_room_number + 1))
        missing_rooms = sorted(all_rooms - self.occupied_rooms)
        print(f"Missing rooms: {missing_rooms}")
        return missing_rooms

    def count_guests_per_channel(self):
        channel_count = [0, 0, 0, 0]  # Assuming 4 channels (0 to 3)
        for room_number in self.occupied_rooms:
            channel = room_number // (3 * 2 * 1)
            channel_count[channel] += 1

        for i, count in enumerate(channel_count):
            print(f"Channel {i} has {count} guests.")
        return channel_count


if __name__ == "__main__":
    input_string = input("Enter the input in the format a/b/c/d/e: ")
    a, b, c, d, e = map(int, input_string.split("/"))

    hotel = HilbertsHotel()

    hotel.check_in_existing(a)

    hotel.check_in_incoming_guests(b, c, d, e)

    hotel.manual_add_room(100, "Manual Guest")

    hotel.manual_delete_room(100)

    hotel.sort_rooms()

    hotel.search_room(1)

    hotel.find_missing_rooms()
