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
    
    # Get user input for the person number to find
    person_number = int(input("Enter the person number to find: "))
    
    # Find the position of the person
    result = find_position(person_number, people_distribution)
    
    # Print the result
    print(result)



# Uncomment the line below to run the function when using in a terminal
run_calculation()
