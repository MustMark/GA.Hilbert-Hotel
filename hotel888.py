import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class HilbertsHotel:
    def __init__(self, max_rooms=10**6):  # สมมติว่าโรงแรมมี 1 ล้านห้อง
        self.rooms = np.zeros(max_rooms, dtype=bool)  # ใช้ NumPy array เพื่อเก็บสถานะห้อง (True = มีแขก, False = ว่าง)
        self.guest_details = {}  # เก็บรายละเอียดแขกในแต่ละห้อง

    # ฟังก์ชันเพิ่มหมายเลขห้อง
    def add_room(self, room_number, details):
        if self.rooms[room_number]:
            pass  # ห้องนี้มีแขกแล้ว
        else:
            self.rooms[room_number] = True
            self.guest_details[room_number] = details  # เก็บรายละเอียดแขกในห้องนี้

    # ฟังก์ชันลบหมายเลขห้อง
    def remove_room(self, room_number):
        if room_number in self.guest_details:
            del self.guest_details[room_number]  # ลบรายละเอียดแขกในห้องนี้
        self.rooms[room_number] = False

    # ฟังก์ชันจัดเรียงหมายเลขห้องที่มีแขกเข้าพัก พร้อมแสดงรายละเอียดแขก
    def sort_rooms(self):
        occupied_rooms = np.where(self.rooms == True)[0]  # ห้องที่มีแขกเข้าพัก
        return {room: self.guest_details[room] for room in occupied_rooms}  # คืนค่าหมายเลขห้องและรายละเอียดแขก

    # ฟังก์ชันค้นหาหมายเลขห้องและแสดงรายละเอียดแขก
    def find_room(self, room_number):
        if self.rooms[room_number]:
            return f"Room {room_number} is occupied by: {self.guest_details[room_number]}"
        else:
            return f"Room {room_number} is empty"

    # ฟังก์ชันแสดงจำนวนหมายเลขห้องที่ไม่มีแขกเข้าพัก รวมถึงห้องที่ยังไม่ได้ถูกใช้งาน
    def show_empty_rooms(self):
        max_used_room = np.max(np.where(self.rooms == True)[0]) if np.any(self.rooms) else 0  # หาเลขห้องสูงสุดที่ถูกใช้
        all_rooms = set(range(1, max_used_room + 1))  # ห้องทั้งหมดตั้งแต่ 1 ถึงหมายเลขห้องสูงสุด
        occupied_rooms = set(np.where(self.rooms == True)[0])  # ห้องที่ถูกใช้งาน
        empty_rooms = sorted(all_rooms - occupied_rooms)  # ห้องที่ว่าง
        return empty_rooms

    # ฟังก์ชันแสดงเวลาที่ใช้สำหรับการทำงานแต่ละฟังก์ชัน
    def timed_execution(self, func, *args, print_details=False):
        start_time = time.time_ns()
        result = func(*args)
        if print_details and isinstance(result, dict):  # แสดงรายละเอียดห้องพักและแขกในกรณีที่เป็น dict
            for room, details in result.items():
                print(f"ห้อง {room}: {details}")
        elif isinstance(result, list):  # แสดงห้องที่ว่าง
            print("ห้องที่ว่าง:", result)
        else:
            print(result)  # แสดงผลลัพธ์ในกรณีที่เป็น string เช่น การค้นหาหมายเลขห้อง
        end_time = time.time_ns()
        execution_time = (end_time - start_time) / 1_000_000_000  # แปลงจากนาโนวินาทีเป็นวินาที
        print(f"Execution time for {func.__name__}: {execution_time:.15f} seconds")
        return result

# ฟังก์ชันคำนวณจำนวนแขกจากข้อมูลการเดินทาง
def calculate_total_guests(guests_input):
    total_guests = guests_input[0]  # จากคน (ช่องทางที่ 1)
    total_guests += guests_input[1] * 2  # จากรถมอเตอร์ไซค์ (ช่องทางที่ 2)
    total_guests += guests_input[2] * 4 * 2  # จากรถกระบะ (ช่องทางที่ 3)
    total_guests += guests_input[3] * 8 * 4 * 2  # จากเครื่องบิน (ช่องทางที่ 4)
    total_guests += guests_input[4] * 16 * 8 * 4 * 2  # จากเรือบรรทุกเครื่องบิน (ช่องทางที่ 5)
    return total_guests

# การจัดการแขกด้วย Multi-threading เพื่อความเร็ว
def handle_guests_multithreaded(hotel, guests_input):
    current_room = 1
    with ThreadPoolExecutor() as executor:
        futures = []
        for i, num_guests in enumerate(guests_input):
            if i == 0:  # ช่องทางที่ 1: คน
                for person in range(1, num_guests + 1):
                    details = f"คนที่ {person}"
                    futures.append(executor.submit(hotel.add_room, current_room, details))
                    current_room += 1
            elif i == 1:  # ช่องทางที่ 2: รถมอเตอร์ไซค์ (2 คน)
                for motorcycle in range(1, num_guests + 1):
                    for person in range(1, 3):
                        details = f"มอไซคันที่ {motorcycle} คนที่ {person}"
                        futures.append(executor.submit(hotel.add_room, current_room, details))
                        current_room += 1
            elif i == 2:  # ช่องทางที่ 3: รถกระบะ (4 รถมอเตอร์ไซค์ = 8 คน)
                for truck in range(1, num_guests + 1):
                    for motorcycle in range(1, 5):
                        for person in range(1, 3):
                            details = f"รถกระบะคันที่ {truck} มอไซคันที่ {motorcycle} คนที่ {person}"
                            futures.append(executor.submit(hotel.add_room, current_room, details))
                            current_room += 1
            elif i == 3:  # ช่องทางที่ 4: เครื่องบิน (8 รถกระบะ = 64 คน)
                for airplane in range(1, num_guests + 1):
                    for truck in range(1, 9):
                        for motorcycle in range(1, 5):
                            for person in range(1, 3):
                                details = f"เครื่องบินลำที่ {airplane} รถกระบะคันที่ {truck} มอไซคันที่ {motorcycle} คนที่ {person}"
                                futures.append(executor.submit(hotel.add_room, current_room, details))
                                current_room += 1
            elif i == 4:  # ช่องทางที่ 5: เรือบรรทุกเครื่องบิน (16 เครื่องบิน = 1024 คน)
                for ship in range(1, num_guests + 1):
                    for airplane in range(1, 17):
                        for truck in range(1, 9):
                            for motorcycle in range(1, 5):
                                for person in range(1, 3):
                                    details = f"เรือลำที่ {ship} เครื่องบินลำที่ {airplane} รถกระบะคันที่ {truck} มอไซคันที่ {motorcycle} คนที่ {person}"
                                    futures.append(executor.submit(hotel.add_room, current_room, details))
                                    current_room += 1
        # รอให้ทุก thread ทำงานเสร็จ
        for future in futures:
            future.result()

# ตัวอย่างการใช้งาน
def main_menu():
    hotel = HilbertsHotel(max_rooms=10**6)  # สมมติว่าโรงแรมมี 1 ล้านห้อง

    # รับ input ทีเดียว
    print("กรุณาป้อนจำนวนแขกในแต่ละช่องทาง (แยกด้วยเว้นวรรค เช่น '1 2 3 4 5'):")
    guests_input = list(map(int, input().split()))

    # เริ่มนับเวลา
    hotel.timed_execution(handle_guests_multithreaded, hotel, guests_input)

    # เมนูรอป้อนคำสั่งใหม่
    while True:
        print("\n--- เมนู ---")
        print("1: แสดงหมายเลขห้องทั้งหมดพร้อมรายละเอียดแขก")
        print("2: แสดงห้องที่ว่าง")
        print("3: ค้นหาหมายเลขห้อง")
        print("4: เพิ่มหมายเลขห้องแบบ manual")
        print("5: ลบหมายเลขห้องแบบ manual")
        print("6: ออกจากโปรแกรม")
        
        choice = input("เลือกคำสั่ง: ")

        if choice == '1':
            # แสดงเวลาที่ใช้ในการทำงานพร้อมการพิมพ์รายละเอียด
            hotel.timed_execution(hotel.sort_rooms, print_details=True)
        elif choice == '2':
            # แสดงห้องที่ว่าง
            hotel.timed_execution(hotel.show_empty_rooms)
        elif choice == '3':
            room_number = int(input("กรุณาป้อนหมายเลขห้องที่ต้องการค้นหา: "))
            hotel.timed_execution(hotel.find_room, room_number)
        elif choice == '4':
            room_number = int(input("กรุณาป้อนหมายเลขห้องที่ต้องการเพิ่ม: "))
            details = input("กรุณาป้อนรายละเอียดแขก: ")
            hotel.timed_execution(hotel.add_room, room_number, details)
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