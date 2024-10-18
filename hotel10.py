import time
from concurrent.futures import ThreadPoolExecutor

class HilbertsHotelMath:
    def __init__(self, max_rooms):
        self.max_rooms = max_rooms  # กำหนดจำนวนห้องทั้งหมด
        self.guest_details = {}  # เก็บรายละเอียดแขกในแต่ละห้อง

    # ฟังก์ชันเพิ่มหมายเลขห้องตามลำดับ
    def add_room(self, guest_number, details):
        room_number = guest_number  # ใช้เลขที่ของแขกเป็นเลขที่ห้อง
        if room_number in self.guest_details:
            pass  # ห้องนี้มีแขกแล้ว
        else:
            self.guest_details[room_number] = details  # เก็บรายละเอียดแขกในห้องนี้

    # ฟังก์ชันลบหมายเลขห้อง
    def remove_room(self, room_number):
        if room_number in self.guest_details:
            del self.guest_details[room_number]  # ลบรายละเอียดแขกในห้องนี้

    # ฟังก์ชันแสดงหมายเลขห้องที่มีแขกเข้าพัก
    def sort_rooms(self):
        return sorted(self.guest_details.keys())  # คืนค่าเฉพาะหมายเลขห้องที่มีแขกเข้าพัก

    # ฟังก์ชันค้นหาหมายเลขห้องและแสดงรายละเอียดแขก
    def find_room(self, room_number):
        if room_number in self.guest_details:
            return f"Room {room_number} is occupied by: {self.guest_details[room_number]}"
        else:
            return f"Room {room_number} is empty"

    # ฟังก์ชันแสดงจำนวนห้องที่ว่าง
    def show_empty_rooms(self):
        occupied_rooms = set(self.guest_details.keys())
        all_rooms = set(range(1, self.max_rooms + 1))
        empty_rooms = sorted(all_rooms - occupied_rooms)
        return empty_rooms

    # ฟังก์ชันแสดงเวลาที่ใช้สำหรับการทำงานแต่ละฟังก์ชัน
    def timed_execution(self, func, *args):
        start_time = time.time_ns()
        result = func(*args)
        if isinstance(result, list):
            print(f"Rooms result: {result}")
        else:
            print(result)
        end_time = time.time_ns()
        execution_time = (end_time - start_time) / 1_000_000_000  # แปลงจากนาโนวินาทีเป็นวินาที
        print(f"\nExecution time for {func.__name__}: {execution_time:.15f} seconds")
        return result

# ฟังก์ชันคำนวณจำนวนแขกทั้งหมดตามช่องทางการเดินทาง
def calculate_total_guests(guests_input):
    total_guests = guests_input[0]  # จำนวนคน (ช่องทางที่ 1)
    total_guests += guests_input[1] * 2  # จากรถมอเตอร์ไซค์ (2 คน)
    total_guests += guests_input[2] * 4 * 2  # จากรถกระบะ (4 มอเตอร์ไซค์ = 8 คน)
    total_guests += guests_input[3] * 8 * 4 * 2  # จากเครื่องบิน (8 รถกระบะ = 64 คน)
    total_guests += guests_input[4] * 16 * 8 * 4 * 2  # จากเรือบรรทุกเครื่องบิน (16 เครื่องบิน = 1024 คน)
    return total_guests

# การจัดการแขกด้วย Multi-threading เพื่อความเร็ว
def handle_guests_multithreaded(hotel, guests_input):
    current_guest = 1  # เริ่มที่แขกคนแรก
    with ThreadPoolExecutor() as executor:
        futures = []
        
        # ช่องทางที่ 1: คน
        for person in range(1, guests_input[0] + 1):
            details = f"Guest {current_guest} (person)"
            futures.append(executor.submit(hotel.add_room, current_guest, details))
            current_guest += 1

        # ช่องทางที่ 2: รถมอเตอร์ไซค์ (2 คนต่อคัน)
        for motorcycle in range(1, guests_input[1] + 1):
            for person in range(1, 3):
                details = f"Guest {current_guest} (motorcycle {motorcycle} person {person})"
                futures.append(executor.submit(hotel.add_room, current_guest, details))
                current_guest += 1

        # ช่องทางที่ 3: รถกระบะ (4 มอเตอร์ไซค์ = 8 คนต่อคัน)
        for truck in range(1, guests_input[2] + 1):
            for motorcycle in range(1, 5):
                for person in range(1, 3):
                    details = f"Guest {current_guest} (truck {truck}, motorcycle {motorcycle} person {person})"
                    futures.append(executor.submit(hotel.add_room, current_guest, details))
                    current_guest += 1

        # ช่องทางที่ 4: เครื่องบิน (8 รถกระบะ = 64 คนต่อเครื่องบิน)
        for airplane in range(1, guests_input[3] + 1):
            for truck in range(1, 9):
                for motorcycle in range(1, 5):
                    for person in range(1, 3):
                        details = f"Guest {current_guest} (airplane {airplane}, truck {truck}, motorcycle {motorcycle} person {person})"
                        futures.append(executor.submit(hotel.add_room, current_guest, details))
                        current_guest += 1

        # ช่องทางที่ 5: เรือบรรทุกเครื่องบิน (16 เครื่องบิน = 1024 คนต่อเรือ)
        for ship in range(1, guests_input[4] + 1):
            for airplane in range(1, 17):
                for truck in range(1, 9):
                    for motorcycle in range(1, 5):
                        for person in range(1, 3):
                            details = f"Guest {current_guest} (ship {ship}, airplane {airplane}, truck {truck}, motorcycle {motorcycle} person {person})"
                            futures.append(executor.submit(hotel.add_room, current_guest, details))
                            current_guest += 1

        # รอให้ทุก thread ทำงานเสร็จ
        for future in futures:
            future.result()

# ตัวอย่างการใช้งาน
def main_menu():
    print("กรุณาป้อนจำนวนแขกในแต่ละช่องทาง (แยกด้วยเว้นวรรค เช่น '1 2 3 4 5'):")
    guests_input = list(map(int, input().split()))  # รับ input จำนวนแขกในแต่ละช่องทาง

    total_guests = calculate_total_guests(guests_input)
    print(f"จำนวนแขกทั้งหมด: {total_guests}")

    hotel = HilbertsHotelMath(max_rooms=total_guests)  # จำนวนห้องสูงสุดเท่ากับจำนวนแขกทั้งหมด

    hotel.timed_execution(handle_guests_multithreaded, hotel, guests_input)

    while True:
        print("\n--- เมนู ---")
        print("1: แสดงหมายเลขห้องที่มีแขกอยู่")
        print("2: แสดงห้องที่ว่าง")
        print("3: ค้นหาหมายเลขห้อง")
        print("4: เพิ่มหมายเลขห้องแบบ manual")
        print("5: ลบหมายเลขห้องแบบ manual")
        print("6: ออกจากโปรแกรม")
        
        choice = input("เลือกคำสั่ง: ")

        if choice == '1':
            hotel.timed_execution(hotel.sort_rooms)
        elif choice == '2':
            hotel.timed_execution(hotel.show_empty_rooms)
        elif choice == '3':
            room_number = int(input("กรุณาป้อนหมายเลขห้องที่ต้องการค้นหา: "))
            hotel.timed_execution(hotel.find_room, room_number)
        elif choice == '4':
            guest_number = int(input("กรุณาป้อนหมายเลขแขกที่ต้องการเพิ่ม: "))
            details = input("กรุณาป้อนรายละเอียดแขก: ")
            hotel.timed_execution(hotel.add_room, guest_number, details)
        elif choice == '5':
            room_number = int(input("กรุณาป้อนหมายเลขห้องที่ต้องการลบ: "))
            hotel.timed_execution(hotel.remove_room, room_number)
        elif choice == '6':
            print("ออกจากโปรแกรม")
            break
        else:
            print("คำสั่งไม่ถูกต้อง กรุณาลองใหม่")

# เรียกใช้เมนูหลัก
main_menu()
