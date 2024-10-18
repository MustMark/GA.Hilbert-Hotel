import time
from concurrent.futures import ThreadPoolExecutor

class HilbertsHotelMath:
    def __init__(self, max_rooms=10**6):
        self.max_rooms = max_rooms  # โรงแรมมีจำนวนห้องทั้งหมดที่กำหนดไว้
        self.guest_details = {}  # เก็บรายละเอียดแขกในแต่ละห้อง

    # ฟังก์ชันคำนวณห้องที่แขกเข้าพักจากลำดับแขกที่เข้ามา
    def room_number(self, guest_number):
        return guest_number * 2  # ใช้สูตรคำนวณหมายเลขห้องที่ต้องการ (เปลี่ยนสูตรได้ตามต้องการ)

    # ฟังก์ชันเพิ่มหมายเลขห้อง
    def add_room(self, guest_number, details):
        room_number = self.room_number(guest_number)
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
        all_rooms = set(range(1, self.max_rooms + 1, 2))  # สมมติว่าห้องทุกห้องเป็นเลขคี่
        empty_rooms = sorted(all_rooms - occupied_rooms)  # ห้องที่ว่าง
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

# การจัดการแขกด้วย Multi-threading เพื่อความเร็ว
def handle_guests_multithreaded(hotel, guests_input):
    current_guest = 1
    with ThreadPoolExecutor() as executor:
        futures = []
        for num_guests in guests_input:
            for guest in range(1, num_guests + 1):
                details = f"Guest {current_guest}"
                futures.append(executor.submit(hotel.add_room, current_guest, details))
                current_guest += 1
        for future in futures:
            future.result()

# ตัวอย่างการใช้งาน
def main_menu():
    hotel = HilbertsHotelMath(max_rooms=10**6)  # โรงแรมมี 1 ล้านห้อง

    # รับ input ทีเดียว
    print("กรุณาป้อนจำนวนแขกในแต่ละช่องทาง (แยกด้วยเว้นวรรค เช่น '1 2 3 4 5'):")
    guests_input = list(map(int, input().split()))

    # เริ่มนับเวลา
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
