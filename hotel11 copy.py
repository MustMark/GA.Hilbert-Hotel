import time

# Function to calculate the exact position of the person
def find_position(person_number, people_distribution):
    # Ensure that people_distribution has exactly 5 values (filling missing ones with 0)
    people_distribution += [0] * (5 - len(people_distribution))
    
    # Extracting the number of people in each channel from the input
    people_in_channel_1 = people_distribution[0]  # คนเดินเท้า
    people_in_channel_2 = people_distribution[1] * 2  # มอเตอร์ไซค์ (2 คนต่อมอเตอร์ไซค์)
    people_in_channel_3 = people_distribution[2] * 8  # รถกระบะ (8 คนต่อคัน)
    people_in_channel_4 = people_distribution[3] * 64  # เครื่องบิน (64 คนต่อเครื่องบิน)
    people_in_channel_5 = people_distribution[4] * 1024  # เรือ (1024 คนต่อเรือ)
    
    # Total people in the channels before the ship
    previous_people = 0
    
    # Check if the person is in channel 1 (คนเดินเท้า)
    if person_number <= people_in_channel_1:
        return f'คนเดินเท้าคนที่ {person_number}'
    
    # Update total people and check channel 2 (มอเตอร์ไซค์)
    previous_people += people_in_channel_1
    if person_number <= previous_people + people_in_channel_2:
        person_in_motorcycle = person_number - previous_people
        bike_number = (person_in_motorcycle - 1) // 2 + 1  # Adjusted to correctly handle bike numbering
        person_on_bike = (person_in_motorcycle - 1) % 2 + 1
        return f'มอไซคันที่ {bike_number} คนที่ {person_on_bike}'
    
    # Update total people and check channel 3 (รถกระบะ)
    previous_people += people_in_channel_2
    if person_number <= previous_people + people_in_channel_3:
        person_in_truck = person_number - previous_people
        truck_number = (person_in_truck - 1) // 8 + 1  # Adjusted to handle truck numbering
        remaining_people_in_truck = (person_in_truck - 1) % 8
        bike_number = (remaining_people_in_truck // 2) + 1
        person_on_bike = (remaining_people_in_truck % 2) + 1
        return f'กระบะคันที่ {truck_number} มอไซคันที่ {bike_number} คนที่ {person_on_bike}'
    
    # Update total people and check channel 4 (เครื่องบิน)
    previous_people += people_in_channel_3
    if person_number <= previous_people + people_in_channel_4:
        person_in_plane = person_number - previous_people
        plane_number = (person_in_plane - 1) // 64 + 1  # Corrected plane numbering
        remaining_people_in_plane = (person_in_plane - 1) % 64
        truck_number = (remaining_people_in_plane // 8) + 1
        remaining_people_in_truck = remaining_people_in_plane % 8
        bike_number = (remaining_people_in_truck // 2) + 1
        person_on_bike = (remaining_people_in_truck % 2) + 1
        return f'เครื่องบินลำที่ {plane_number} กระบะคันที่ {truck_number} มอไซคันที่ {bike_number} คนที่ {person_on_bike}'
    
    # Update total people and check channel 5 (เรือ)
    previous_people += people_in_channel_4
    if person_number <= previous_people + people_in_channel_5:
        person_in_ship = person_number - previous_people
        ship_number = (person_in_ship - 1) // 1024 + 1  # Corrected ship numbering
        remaining_people_in_ship = (person_in_ship - 1) % 1024
        plane_number = (remaining_people_in_ship // 64) + 1
        remaining_people_in_plane = remaining_people_in_ship % 64
        truck_number = (remaining_people_in_plane // 8) + 1
        remaining_people_in_truck = remaining_people_in_plane % 8
        bike_number = (remaining_people_in_truck // 2) + 1
        person_on_bike = (remaining_people_in_truck % 2) + 1
        return f'เรือลำที่ {ship_number} เครื่องบินลำที่ {plane_number} กระบะคันที่ {truck_number} มอไซคันที่ {bike_number} คนที่ {person_on_bike}'
    
    # If the person_number exceeds the total number of people
    return 'ไม่พบ'

# Function to get input and run the calculation
def run_calculation():
    # Get user input for number of guests in each channel
    people_input = input("กรุณาป้อนจำนวนแขกในแต่ละช่องทาง (แยกด้วยเว้นวรรค เช่น '1 2 3 4 5'): ")
    
    # Convert the input into a list of integers
    people_distribution = list(map(int, people_input.split()))
    
    return people_distribution
    
def write_people_details_to_file(people_distribution):
    filename = input("กรุณาป้อนชื่อไฟล์ที่ต้องการบันทึก (เช่น 'people_details.txt'): ")
    # Calculate the total number of people
    total_people = sum([
        people_distribution[0],  # คนเดินเท้า
        people_distribution[1] * 2,  # มอเตอร์ไซค์ (2 คนต่อคัน)
        people_distribution[2] * 8,  # รถกระบะ (8 คนต่อคัน)
        people_distribution[3] * 64,  # เครื่องบิน (64 คนต่อเครื่องบิน)
        people_distribution[4] * 1024  # เรือ (1024 คนต่อเรือ)
    ])
    
    # Open the file for writing
    with open(filename, 'w', encoding='utf-8') as file:
        # Loop through all people and find their position
        for room_number in range(1, total_people + 1):
            result = find_position(room_number, people_distribution)
            # Write the result to the file
            file.write(f'Room {room_number}: {result}\n')
    
    print(f'All people details have been written to {filename}')
    

def main_menu():

    total_guests = run_calculation()

    while True:
        print("\n--- เมนู ---")
        print("1: เพิ่มหมายเลขห้องแบบ manual")
        print("2: ลบหมายเลขห้องแบบ manual")
        print("3: การจัดเรียงลำดับหมายเลขห้อง")
        print("4: การค้นหาหมายเลขห้อง")
        print("5: การแสดงจำนวนหมายเลขห้องที่ไม่มีแขกเข้าพัก")
        print("6: เขียนผลลัพธ์เป็นไฟล์")
        print("7: ออกจากโปรแกรม")
        
        choice = input("เลือกคำสั่ง: ")

        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            person_number = int(input("Enter Room number to find: "))
            result = find_position(person_number, total_guests)
            print(f"ข้อมูลของห้องหมายเลข {person_number} : ",end ="")
            print(result)
        elif choice == '5':
            print("[]")
        elif choice == '6':
            write_people_details_to_file(total_guests)
        elif choice == '7':
            print("ออกจากโปรแกรม")
            break
        else:
            print("คำสั่งไม่ถูกต้อง กรุณาลองใหม่")

main_menu()