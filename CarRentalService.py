# PWP Assignment
# ONG LIT TSEN
# NG ZHI YAO


# Import library
import datetime


# ---------------------------- Mix Functionalities----------------------------
# Login to access system for customers & admin
def users_login():
    # Initialise list and variables
    user_data = []
    userid = None
    login = False
    list_counter = 0

    # Get user input for ID
    print("~ Enter 0 to register for an account / Enter -1 to exit ~")
    user_input = input("ID: ")

    # Detect exit status and registration
    if user_input == "-1":
        return None
    elif user_input == "0":
        userid = registration()
        return userid

    # Loop over all line in user file and append into list
    with open("users.txt", "r") as users_file:
        for line in users_file:
            user_data.append(line)

    # Check for user input in each string of list
    for item in user_data:
        if user_input in item:
            # Ask for password
            user_password = input("Password: ")

            real_password_line = user_data[list_counter + 2]
            real_password = real_password_line[real_password_line.find("-") + 2: real_password_line.find("\n")]

            # Check for user input if in password line
            if user_password == real_password:
                username_line = user_data[list_counter + 1]
                username = username_line[username_line.find("-") + 2: username_line.find("\n")]
                userid = user_input

                print("Welcome back" + "! " + username)
                login = True
            else:
                print("Wrong Password!\n")
                userid = users_login()
                return userid

            # Prevent further looping over all lines and error
            break

        # Determine list position
        list_counter += 1

    # Wrong ID terminate program
    if not login:
        print("Wrong ID!\n")
        userid = users_login()

    return userid


# Luhn algorithm is applied to check for fraud card, the algorithm is divided into two part
def validate_credit_card(card_no):
    # First part: Check for total sum in card number
    # Initialise variable
    sum_num = 0
    card_position = 0
    tmp = int(card_no)

    # Create loop to add up every no in credit card. The loop start from last digit of credit card number
    while tmp > 0:
        remainder = tmp % 10
        tmp = tmp // 10

        # Card no require *2 if not divisible by 2
        if card_position % 2 != 0:
            remainder *= 2
            remainder_string = str(remainder)
            for no in range(len(remainder_string)):
                sum_num += int(remainder_string[no])
        else:
            sum_num += remainder

        # Increment on card position
        card_position += 1

        # Check if total sum divisible by 10, valid if can
    if sum_num % 10 != 0:
        return False

    # Second part: Check for card length
    # Initialise and convert credit card no into string type
    card_length = len(str(card_no))
    tmp = int(card_no)

    # Get the first two digit of credit card
    while tmp > 100:
        tmp //= 10

    # Visa and Mastercard
    if card_length == 13 or card_length == 16:
        if 51 <= tmp <= 55:
            return True
        else:
            tmp //= 10

            if tmp == 4:
                return True

    return False


# View available car
def view_car_available(user_id):
    # Initialise
    car_data = []
    list_counter = 0
    car_amount = 0

    # Copy data into list
    with open("cars.txt", "r") as car_file:
        for line in car_file:
            car_data.append(line)

    print("\nCars available: ")

    # Loop every car in list and display
    for item in car_data:
        if "True" in item:
            line_car_type = car_data[list_counter - 6]
            car_type = line_car_type[line_car_type.find("-") + 2: line_car_type.find("\n")]

            line_car_brand = car_data[list_counter - 8]
            car_brand = line_car_brand[line_car_brand.find("-") + 2: line_car_brand.find("\n")]

            car_amount += 1
            print(f"\t{car_amount}. {car_type} ({car_brand})")

        # Increment counter
        list_counter += 1

    if user_id is not None:
        view_car_detail(user_id, car_data)
        return

    else:
        option = input("Would you like to login to check for car details? (Y/N): ")

        if option.upper() == "Y":
            user_id = users_login()

            if user_id is not None:
                member_menu(user_id)
            return

        elif option.upper() == "N":
            return
        else:
            print("Invalid option. Returning to menu...")
            return


# View car specification in detail
def view_car_detail(userid, car_data):
    # Initialise variable
    car_number = 1
    list_counter = 0
    car_id = None
    car_name = None
    cost_per_hour = None
    cost_per_day = None
    cost_per_week = None
    mileage = None
    car_status = False

    # Validate integer is being input
    try:
        car_option = int(input("Enter a number to view car details, 0 to exit : "))
    except:
        print("Invalid option. Please try again.\n")
        view_car_available(userid)
        return

    # Exit function
    if car_option == 0:
        return

    print("\n--------------------")

    for item in car_data:
        # Check for car available status True
        if "True" in item:
            # Display only the car details depend on user input
            if car_option == car_number:
                # Set flag on car_status
                car_status = True

                # Display 9 lines of car details
                for count in range(9, 0, -1):
                    car_detail_line = car_data[list_counter - count]
                    print(car_detail_line.rstrip("\n"))
                print("--------------------")

                # Transfer value into variables
                id_line = car_data[list_counter - 9]
                car_id = id_line[id_line.find("-") + 2: id_line.find("\n")]

                car_type_line = car_data[list_counter - 6]
                car_type = car_type_line[car_type_line.find("-") + 2: car_type_line.find("\n")]

                car_brand_line = car_data[list_counter - 8]
                car_brand = car_brand_line[car_brand_line.find("-") + 2: car_brand_line.find("\n")]
                car_name = "{} ({})".format(car_type, car_brand)

                cost_hour_line = car_data[list_counter - 4]
                cost_per_hour = int(cost_hour_line[cost_hour_line.find("M") + 1: cost_hour_line.find("\n")])

                cost_day_line = car_data[list_counter - 3]
                cost_per_day = int(cost_day_line[cost_day_line.find("M") + 1: cost_day_line.find("\n")])

                cost_week_line = car_data[list_counter - 2]
                cost_per_week = int(cost_week_line[cost_week_line.find("M") + 1: cost_week_line.find("\n")])

                mileage_line = car_data[list_counter - 1]
                mileage = int(mileage_line[mileage_line.find("-") + 2: mileage_line.find("\n")])
                break
            else:
                car_number += 1

        # Increment counter
        list_counter += 1

    # Check for car status
    if not car_status:
        print("Car is not in the list. Please try again...")
        view_car_available(userid)
        return

    # No booking available for admin
    if userid == "A001":
        view_car_available(userid)
        return

    # Booking option
    booking_option = input("\nEnter 1 to book the car, other keys to back to previous page: ")
    print("")

    if booking_option == "1":
        print("The minimum rental duration is 3hours ('h' for hours, 'd' for days, 'w' for weeks)")
        print("*Eg: 1d3h = 1days 3hours*")

        # Input duration and calculate total cost
        try:
            week = 0
            day = 0
            hour = 0
            week_status = False
            day_status = False
            hour_status = False

            rent_duration = input("Enter the rental duration (Minimum three hours): ")

            for count in range(len(rent_duration)):
                if rent_duration[count].lower() == "w" and week_status is False:
                    week = int(rent_duration[: rent_duration.find("w")])
                    week_status = True

                elif rent_duration[count].lower() == "d" and day_status is False:
                    day = int(rent_duration[count - 1])
                    day_status = True

                    if rent_duration[count - 2].isnumeric():
                        print("Invalid day. Please follow the format ~\n")
                        view_car_available(userid)
                        return

                elif rent_duration[count].lower() == "h" and hour_status is False:
                    if rent_duration[count - 3].isnumeric() and count-3 >= len(rent_duration):
                        print("Invalid hours. Please follow the format ~\n")
                        view_car_available(userid)
                        return
                    elif rent_duration[count - 2].isnumeric() and count-2 >= len(rent_duration):
                        hour = (int(rent_duration[count - 2]) * 10) + int(rent_duration[count - 1])
                    else:
                        hour = int(rent_duration[count - 1])
                    hour_status = True
                elif rent_duration[count].lower().isalpha():
                    print("Invalid character. Returning to previous page...")
                    view_car_available(userid)
                    return
        except:
            print("Invalid duration. Returning to previous page...\n")
            view_car_available(userid)
            return

        total_cost = (week * cost_per_week) + (day * cost_per_day) + (hour * cost_per_hour)
        payment_status = payment(total_cost)

        # If success payment
        if payment_status:
            rental_id = create_booking(userid, car_id, car_name, rent_duration, total_cost, mileage)
            print("Rental ID: " + str(rental_id))
            print("Have a Nice Day!")
            return

        else:
            print("Payment terminated. Return to previous page...")
            view_car_available(userid)
            return

    # Return to view car if no book
    view_car_available(userid)
    return


# ----------------------------Functionalities of Admin----------------------------
# Add cars to be rented out
def add_car():
    # Generate ID counter
    with open("cars.txt", "r") as file:
        data = file.read()
        car_id = str(data.count("Car ID - ") + 1)

    # Input car specification
    car_brand = input("Car Brand: ")
    year_made = input("Year made: ")
    car_type = input("Car type: ")
    gear = input("Gear: ")
    cost_per_hour = input("Cost per hour: ")
    cost_per_day = input("Cost per day: ")
    cost_per_week = input("Cost per week: ")
    mileage = input("Mileage: ")
    available_status = input("Available status: ")

    # Write car specification into file
    with open("cars.txt", "a") as f:
        f.write("Car ID - " + car_id.zfill(4) + "\n")
        f.write("Car Brand - " + car_brand + "\n")
        f.write("Year made - " + year_made + "\n")
        f.write("Car type - " + car_type + "\n")
        f.write("Gear - " + gear + "\n")
        f.write("Cost per hour - " + cost_per_hour + "\n")
        f.write("Cost per day - " + cost_per_day + "\n")
        f.write("Cost per week - " + cost_per_week + "\n")
        f.write("Mileage - " + mileage + "\n")
        f.write("Available status - " + available_status + "\n")
        f.write("# ------------------------------------\n")
    print("Car successfully add!!")


# Remove car from renting
def remove_car():
    # Initialise list and variable
    car_data = []
    list_counter = 0
    available_status = False

    # Copy every line into list
    with open("cars.txt", "r") as car_file:
        for line in car_file:
            car_data.append(line)

    while True:
        # Ask for car to be remove
        print("Enter 0 to exit")
        car_id = input("Enter carID to be removed: ")

        if car_id == "0":
            return
        # Check for position of car to be removed
        for item in car_data:
            if "Car ID" in item:
                if car_id in item:
                    available_status = True
                    break
            list_counter += 1

        # Return error if no cars found
        if not available_status:
            print("No records found on specific carID.")
            continue

        # Pop every item for the car. Require a loop due to special design
        for counter in range(11):
            car_data.pop(list_counter)

        # Rewriting the file
        with open("cars.txt", "w") as car_file:
            for item in car_data:
                car_file.write(item)
        print("Remove Car Success!!")
        return


# Modify car details
def modify_car():
    # Initialise variable
    modify_status = False

    # Open file as read mode
    file = open("cars.txt", "r")

    # Option for modification
    modify_details = input("Do you wish to modify car details?(Yes/No): ")

    # Continue if want to modify
    if modify_details.lower() == "yes":
        # Initialise variable and list
        list_counter = 0
        temp_car_id = None
        car_data = []
        print("You are currently requesting to modify car details!")

        # Read car_id
        car_id = input("Enter Car ID: ")

        # Loop over file and check for car_id
        for line in file:
            # Copy the line into list
            car_data.append(line)

            # Check for car_id
            if "Car ID" in line:
                temp_car_id = car_data[list_counter]
                temp_car_id = temp_car_id[temp_car_id.find("-") + 2: temp_car_id.find("\n")]
                if car_id == temp_car_id:
                    modify_status = True
                    break

            list_counter += 1

        # Print if car available, else input car_id again
        if modify_status:
            print("\nYou have selected this car!")
        else:
            print("Please enter a valid Car ID!")
            modify_car()
            return

        # Do-while loop to check for only 3 input enter
        while True:
            # Initialise list and reset file pointer
            content = []
            file.seek(0)

            # Ask for specification to edit
            print("1.Gear")
            print("2.Cost")
            print("3.Mileage")
            editing = input("Please choose which criteria to edit: ")

            # Editing gear
            if editing == "1":
                # Input old info and new info
                gear = input("Enter current gear: ")
                new_gear = input("Enter new gear: ")

                # Loop over file
                for line in file:
                    # Update file pointer on car
                    if "Car ID" in line:
                        temp_car_id = line[line.find("-") + 2: line.find("\n")]

                    # Update gear
                    if gear in line:
                        if car_id == temp_car_id:
                            print("Gear successfully changed!")
                            line = line.replace(gear, new_gear)
                        content.append(line)
                    else:
                        content.append(line)
                break
            # Editing cost
            elif editing == "2":
                # Input car detail
                cost_per_hour = input("Enter current cost per hour: ")
                new_cost_per_hour = input("Enter new cost per hour: ")
                cost_per_day = input("\nEnter current cost per day: ")
                new_cost_per_day = input("Enter new cost per day: ")
                cost_per_week = input("\nEnter current cost per week: ")
                new_cost_per_week = input("Enter new cost per week: ")

                for line in file:
                    # Update file pointer on car
                    if "Car ID" in line:
                        temp_car_id = line[line.find("-") + 2: line.find("\n")]

                    # Update cost on specific car
                    if cost_per_hour in line:
                        if car_id == temp_car_id:
                            print("Cost per hour successfully changed!")
                            line = line.replace(cost_per_hour, new_cost_per_hour)
                        content.append(line)
                    elif cost_per_day in line:
                        if car_id == temp_car_id:
                            print("Cost per day successfully changed!")
                            line = line.replace(cost_per_day, new_cost_per_day)
                        content.append(line)
                    elif cost_per_week in line:
                        if car_id == temp_car_id:
                            print("Cost per week successfully changed!")
                            line = line.replace(cost_per_week, new_cost_per_week)
                        content.append(line)
                    else:
                        content.append(line)
                break
            # Editing mileage
            elif editing == "3":
                mileage = input("Enter current mileage: ")
                new_mileage = input("Enter new mileage: ")

                for line in file:
                    # Update file pointer on car
                    if "Car ID" in line:
                        temp_car_id = line[line.find("-") + 2: line.find("\n")]

                    if mileage in line:
                        if car_id == temp_car_id:
                            print("Mileage successfully changed!")
                            line = line.replace(mileage, new_mileage)
                        content.append(line)
                    else:
                        content.append(line)
                break
            # Prompt again if invalid option
            else:
                print("Invalid option, please try again.")

        # Open f as write mode
        f = open("cars.txt", "w")
        for count in content:
            f.write(count)

        # Close file
        file.close()
        f.close()

    # Return to menu if no modify
    elif modify_details.lower() == "no":
        print("Kindly proceed to next part!")
    else:
        print("Invalid option, please try again!")
        modify_car()


# Display all records of cars rented out
def display_car_rented():
    # Initialise list and variable
    car_data = []
    list_counter = 0
    car_amount = 0

    # Copy data into list
    with open("cars.txt", "r") as car_file:
        for line in car_file:
            car_data.append(line)

    print("Cars rented out:\n")

    # Loop every car in list and display
    for item in car_data:
        if "False" in item:
            # Increment on car_amount
            car_amount += 1

            # Due to text file format, assign value to a value and print
            line_car_type = car_data[list_counter - 6]
            car_type = line_car_type[line_car_type.find("-") + 2: line_car_type.find("\n")]

            line_car_brand = car_data[list_counter - 8]
            car_brand = line_car_brand[line_car_brand.find("-") + 2: line_car_brand.find("\n")]

            # Print car rented out, eg: "1. SUV (BMW)"
            print(f"{car_amount}. {car_type} ({car_brand})")

        # Increment list counter
        list_counter += 1


# Display all records of customer booking
def display_booking():
    # Open a file named rental.txt
    infile = open("rental.txt", "r")

    # Read the file's content
    file_content = infile.read()

    # Print the data
    print(file_content)

    # Close the file
    infile.close()


#  Display all records of customer Payment for a specific time duration
def display_booking_time():
    # Initialise variable
    rental_data = []
    list_counter = 0
    rent_status = False

    # Do-while loop and prompt for a correct time range
    while True:
        # Get time_range input
        print("* Range: YYYY/MM/DD - Today *")
        starting_date = input("Enter the starting range (YYYY/MM/DD): ")
        print()

        # Check for valid date, any error in try part will prompt for new input
        try:
            year, month, day = starting_date.split("/")
            starting_date = datetime.date(int(year), int(month), int(day))
            break
        except:
            print("Please follow the date format. Eg: 2021/6/2\n")
            continue

    # Open rental file and copy everything into list
    with open("rental.txt", "r") as rental_file:
        for line in rental_file:
            rental_data.append(line)

    for item in rental_data:
        # Find line with "Date -"
        if "Date -" in item:
            file_date = item[item.find("-") + 2: item.find("\n")]
            year, month, day = file_date.split("-")

            file_date = datetime.date(int(year), int(month), int(day))
            # Print booking if bigger than
            if file_date >= starting_date:
                rent_status = True
                for line_counter in range(list_counter - 3, list_counter + 5):
                    print(rental_data[line_counter].rstrip("\n"))
                print()
        # Increment on list_counter
        list_counter += 1

    if not rent_status:
        print("No record found in the time range.")
    return


# Search specific record of customer booking
def search_booking():
    # Create a boolean variable as flag
    found = False

    # Get the rent ID to search
    search = input("Enter a rent ID to search for: ")

    # Open the rental.txt
    rentals_file = open("rental.txt", "r")

    # Read the first record
    rent_id = rentals_file.readline()

    # Read the customer ID
    customer_id = rentals_file.readline()

    # Strip
    rent_id = (rent_id.rstrip())

    # Read the remaining data
    while rent_id != "":
        # Strip
        customer_id = (customer_id.rstrip())

        # Check the record matches search value
        if search in rent_id:
            # Display record
            print(rent_id)
            print(customer_id)
            print()
            # Set the found flag
            found = True
        else:
            for i in range(8):
                rentals_file.readline()

        # Read next record
        rent_id = rentals_file.readline().rstrip()
        customer_id = rentals_file.readline()

    # End of loop

    # Close the file
    rentals_file.close()

    # If not found
    if not found:
        print("The item is unavailable")


# Search specific record of customer payment
def search_payment():
    # Create a boolean variable as flag
    found = False

    # Get the rent ID to search
    search = input("Enter a rent ID to search for: ")

    # Open the rental.txt
    rentals_file = open("rental.txt", "r")

    # Read once rent id
    rent_id = rentals_file.readline()

    # Read the remaining data
    while rent_id != "":
        # Read customer id record
        customer_id = rentals_file.readline()

        # Skip 3 line
        for i in range(3):
            rentals_file.readline()

        # Read the car type
        car_type = rentals_file.readline()

        # Skip one line
        rentals_file.readline()

        # Read totalCost
        total_cost = rentals_file.readline()

        # Skip two line
        for i in range(2):
            rentals_file.readline()

        # Strip
        rent_id = (rent_id.rstrip())
        customer_id = (customer_id.rstrip())
        car_type = (car_type.rstrip())
        total_cost = (total_cost.rstrip())

        # Check the record matches search value
        if search in rent_id:
            # Display record
            print(rent_id)
            print(customer_id)
            print(car_type)
            print(total_cost)
            print()
            # Set the found flag
            found = True
        # Determine whether EOF (End of file)
        rent_id = rentals_file.readline()

    # End of loop

    # Close the file
    rentals_file.close()

    # If not found
    if not found:
        print("The item is unavailable")


# Return a rented car
def return_car():
    # Initialise variable
    car_data = []
    list_counter = 0
    temp_car_id = None
    flag = False

    # Create file as read mode
    file = open("cars.txt", "r")

    # Read car_id to be returned
    car_id = input("Enter Car ID: ")

    # Loop over file
    for line in file:
        car_data.append(line)
        if "Car ID" in line:
            temp_car_id = car_data[list_counter]
            temp_car_id = temp_car_id[temp_car_id.find("-") + 2: temp_car_id.find("\n")]
            if car_id == temp_car_id:
                flag = True
                break

        list_counter += 1

    # Check for flag status, prompt again if invalid car ID
    if flag:
        print("\nCurrently returning a rented car")
    else:
        print("Please enter a valid Car ID")
        file.close()
        return_car()
        return

    print("Choice = Yes or No")
    returning = input("Please enter a choice: ")

    # returning a rented car
    if returning.lower() == "yes":
        content = []
        file.seek(0)
        for line in file:
            # Update file pointer in car
            if "Car ID" in line:
                temp_car_id = line[line.find("-") + 2: line.find("\n")]

            # Update available status
            if "False" in line:
                if car_id == temp_car_id:
                    print("Available Status changed, car is returned!")
                    line = line.replace("False", "True")
                content.append(line)
            else:
                content.append(line)
    elif returning.lower() == "no":
        print("Returning to previous page")
        file.close()
        return
    else:
        print("Invalid!")
        file.close()
        return

    # Open f as write mode and write list into file
    f = open("cars.txt", "w")
    for count in content:
        f.write(count)

    # Close file
    file.close()
    f.close()


def admin_menu(user_id):
    while True:
        # Print and ask for option
        print("\nADMIN MODE: ")
        print("\t1. Add new car")
        print("\t2. Remove car")
        print("\t3. Modify car details")
        print("\t4. Display car that rented out")
        print("\t5. Display car available for rent")
        print("\t6. Display all customer bookings")
        print("\t7. Display customer bookings in a time range")
        print("\t8. Search customer's booking")
        print("\t9. Search customer payment")
        print("\t10. Return a rented car")
        print("\t0. Exit")

        option = input("Please select an option to continue: ")
        print()

        # Add car
        if option == "1":
            add_car()
        # Remove car
        elif option == "2":
            remove_car()
        # Modify car detail
        elif option == "3":
            modify_car()
        # Display car rented out
        elif option == "4":
            display_car_rented()
        elif option == "5":
            view_car_available(user_id)
        elif option == "6":
            display_booking()
        elif option == "7":
            display_booking_time()
        elif option == "8":
            search_booking()
        elif option == "9":
            search_payment()
        elif option == "10":
            return_car()
        elif option == "0":
            return
        else:
            print("Invalid option. Please try again...")


# ---------------------------Functionalities of Member---------------------------
# Register for membership
def registration():
    # Registration start
    print("\n--------------------------Registration--------------------------")
    username = input("Username: ")

    # Validate for confirm password
    password = input("Password: ")
    confirm_password = input("Confirm password: ")
    if password != confirm_password:
        print("Different password detected. Please try again.")
        username = registration()
        return username

    # Validate for invalid email
    email = input("Email address: ")
    if "@" in email and ".com" in email:
        pass
    else:
        print("Invalid email address. Please try again.")
        username = registration()
        return username

    # Validate for invalid phone number. Assume Malaysian only
    contact_number = input("Contact Number (exclude hyphen): ")
    if len(contact_number) != 10 and len(contact_number) != 11:
        print("Invalid phone number. Please try again.")
        username = registration()
        return username

    # Validate for IC No / ID
    ic_number = input("Identity card number (exclude hyphen): ")
    if len(ic_number) != 12:
        print("Invalid identity card number. Please try again.")
        username = registration()
        return username

    # Write info into text file
    with open("users.txt", "a") as f:
        f.write("ID - " + ic_number + "\n")
        f.write("username - " + username + "\n")
        f.write("password - " + password + "\n")
        f.write("email - " + email + "\n")
        f.write("contact number - " + contact_number + "\n")
        f.write("# ----------------------------------------\n")

    # Display success notification
    print("\n -----------------------Registration Success-----------------------")
    print("* Please be noted that your IC number will be used for loginID *")

    # IC as ID, unique key
    return ic_number


# Modify member info
def modify_info(userid):
    # Initialise variable
    user_data = []
    rental_data = []
    list_counter = 0

    # Open file and read all data into list
    with open("users.txt", "r") as user_file:
        for line in user_file:
            user_data.append(line)
    with open("rental.txt", "r") as rental_file:
        for line in rental_file:
            rental_data.append(line)

    # Count Username line in file
    for line in user_data:
        if userid in line:
            break
        list_counter += 1

    # Display option for modification
    print("\n1. Username")
    print("2. Password")
    print("3. Email Address")
    print("4. Contact Number")
    option = input("Select an information to modify (0 to exit): ")
    print()

    # Exit
    if option == "0":
        return

    # Username
    elif option == "1":
        temp_line = user_data[list_counter + 1]
        old_info = temp_line[temp_line.find("-") + 2: temp_line.find("\n")]

        print(f"Existing username: {old_info}")
        new_info = input("Enter your new username: ")

    # Password
    elif option == "2":
        temp_line = user_data[list_counter + 2]
        old_info = temp_line[temp_line.find("-") + 2: temp_line.find("\n")]

        new_info = input("Enter your new password: ")
        confirm_password = input("Enter again new password for confirmation: ")

        # Check for new password if same
        if new_info != confirm_password:
            print("Password not same! Please try again.")
            modify_info(userid)

            user_file.close()
            rental_file.close()
            return

    # Email address
    elif option == "3":
        temp_line = user_data[list_counter + 3]
        old_info = temp_line[temp_line.find("-") + 2: temp_line.find("\n")]

        print(f"Existing email address: {old_info}")
        new_info = input("Enter your new email address: ")
        if "@" and ".com" in new_info:
            pass
        else:
            print("Invalid email address! Please try again.")
            modify_info(userid)
            return

    # Contact number
    elif option == "4":
        temp_line = user_data[list_counter + 4]
        old_info = temp_line[temp_line.find("-") + 2: temp_line.find("\n")]

        print(f"Existing contact number: {old_info}")
        new_info = input("Enter your new contact number: ")

        if len(new_info) != 10 and len(new_info) != 11:
            print("Invalid contact number. Please try again.")
            modify_info(userid)
            return

    # Other option
    else:
        print("Invalid option. Please try again.")
        modify_info(userid)
        return

    # Initialise list counter
    list_counter = 0
    id_position = None

    # Replacing data in user_file
    for item in user_data:
        if "ID" in item:
            id_position = user_data[list_counter]
            id_position = id_position[id_position.find("-") + 2: id_position.find("\n")]

        # Prevent changing multiple data
        if old_info in item:
            if userid == id_position:
                user_data[list_counter] = item.replace(old_info, new_info)
                print("----------Modify Success!----------\n")
                break

        # Increment on counter
        list_counter += 1

    list_counter = 0
    # Replacing data in rental file
    for item in rental_data:
        if "ID" in item:
            id_position = rental_data[list_counter]
            id_position = id_position[id_position.find("-") + 2: id_position.find("\n")]

            # Prevent changing multiple data
        if old_info in item:
            if userid == id_position:
                rental_data[list_counter] = item.replace(old_info, new_info.rstrip("\n"))
                break

        # Increment on counter
        list_counter += 1

    # Open file as write mode. Rewrite file with list
    with open("users.txt", "w") as f:
        with open("rental.txt", "w") as file:
            for item in user_data:
                f.write(item)
            for items in rental_data:
                file.write(items)

    # Exit
    exit_status = input("Would you wish to continue modifying info? (Y/N): ")

    if exit_status.upper() == "Y":
        modify_info(userid)
        return
    elif exit_status.upper() == "N":
        return
    else:
        print("Invalid option. Returning to menu...")
        return


# Check personal rental history
def display_rental(userid):
    # Initialise
    rental_data = []
    list_counter = 0
    user_status = False

    # Open file and read into list
    with open("rental.txt", "r") as rental_file:
        for line in rental_file:
            rental_data.append(line)

    # Search for specific user and display his records
    for item in rental_data:
        if userid in item:
            # Check for no record users
            user_status = True
            # Date
            date_line = rental_data[list_counter + 2]
            date = date_line[date_line.find("-") + 2: date_line.find("\n")]

            # Rental ID
            rental_id_line = rental_data[list_counter - 1]
            rental_id = rental_id_line[rental_id_line.find("-") + 2: rental_id_line.find("\n")]
            print(f"{date} ({rental_id})")

            # Loop to print other details
            for loop_counter in range(3, 8):
                print(rental_data[list_counter + loop_counter], end="")
            print()
        # Increment counter
        list_counter += 1

    # Check status if have rental record
    if not user_status:
        print("No rentals record found.")

    return


# Create rental booking after payment success
def create_booking(userid, car_id, car_name, rent_duration, total_cost, mileage):
    # Initialise
    list_counter = 0
    car_list_counter = 0
    user_data = []
    car_data = []
    rental_info = []

    # Read content from car_file and copy into list
    with open("cars.txt", "r") as car_file:
        for line in car_file:
            car_data.append(line)

    # Modify car status in list
    for item in car_data:
        if car_id in item:
            car_data[car_list_counter + 9] = "Available status - False\n"
            break
        car_list_counter += 1

    # Rewrite car file
    with open("cars.txt", "w") as car_write:
        for item in car_data:
            car_write.write(item)

    # Rent ID
    id_counter = 1
    with open("rental.txt", "r") as rental_file:
        for line in rental_file:
            if "Rent ID" in line:
                id_counter += 1

        id_counter = "A" + str(id_counter)
        rental_info.append("Rent ID - " + id_counter)

    # Customer_id
    rental_info.append("Customer ID - " + userid)

    # Username
    with open("users.txt", "r") as users_file:
        for line in users_file:
            user_data.append(line)

    for item in user_data:
        if userid in item:
            customer_name_line = user_data[list_counter + 1]
            rental_info.append("Customer name - " + customer_name_line[customer_name_line.find("-") + 2:
                                                                       customer_name_line.find("\n")])

        list_counter += 1

    # Date
    rental_info.append("Date - " + str(datetime.date.today()))

    # Car
    rental_info.append("Car ID - " + car_id)
    rental_info.append("Car type - " + car_name)

    # Rent duration
    rental_info.append("Rent days - " + rent_duration)

    # Total Cost
    rental_info.append("Total cost - RM" + str(total_cost))

    # Mileage
    rental_info.append("Trip mileage - " + str(mileage))

    # Update file with new booking
    with open("rental.txt", "a") as file:
        for item in rental_info:
            file.write(item + "\n")
        file.write("# -------------------------------------------\n")

    # Return
    return id_counter


# Payment for renting car
def payment(total_cost):
    # Interface
    print("Payment method:")
    print("\t1. Debit/Credit card")
    print("\t2. TNG")
    payment_option = input("Please select a payment method: ")

    # Due to to privacy issue, no real payment info will be saved into file.
    # Debit/Credit Card
    if payment_option == "1":
        card_no = input("\nEnter your debit/credit card no: ")
        owner_name = input("Owner name: ")
        expiration_date = input("Expiration Date(MM/YY): ")
        bank = input("Issue bank: ")

        # Validate expiration date
        date_today = str(datetime.datetime.today())
        tmp_year, tmp_month, tmp_day = date_today.split("-")
        month, year = expiration_date.split("/")
        year = "20" + year
        try:
            if int(year) < int(tmp_year):
                print("Expired card. Payment terminated...")
                return False
            elif int(year) == int(tmp_year):
                if int(month) < int(tmp_month):
                    print("Expired card. Payment terminated...")
                    return False
        except:
            print("Invalid expiration date. Payment terminated...")
            return False

        # Luhn algorithm is applied to check for valid credit_card number
        # References: https://www.geeksforgeeks.org/luhn-algorithm/
        card_status = validate_credit_card(card_no)

        # Return error if invalid card number.
        if not card_status:
            print("This card does not exist. Payment terminated...")
            return False

    elif payment_option == "2":
        tng_id = input("\nEnter your TNG username: ")
        tng_pass = input("Password: ")

    else:
        print("Invalid option. Payment terminated.")
        return False

    # Proceed with charges
    print("\nThe total cost is RM", total_cost)
    confirm_payment = input("Enter Y to proceed with payment: ")

    if confirm_payment.upper() != "Y":
        return False

    # End transaction
    print("Processing.....")
    print("\n-------------Success!-------------")
    return True


def member_menu(user_id):
    while True:
        # Print and ask for option
        print("\nMEMBER MODE: ")
        print("\t1. Modify personal details")
        print("\t2. View personal rental history")
        print("\t3. View cars to be rented out")
        print("\t0. Exit")

        option = input("Please select an option to continue: ")
        print()

        # Modify personal info
        if option == "1":
            modify_info(user_id)
        # View personal booking
        elif option == "2":
            display_rental(user_id)
        # View car available and details
        elif option == "3":
            view_car_available(user_id)
        # Exit
        elif option == "0":
            return
        else:
            print("Invalid option. Please try again...")


# ---------------------------Main Program---------------------------
def main():
    # Initialise variable
    user_id = None

    # Welcome user and prompt for member
    print(
        "//////////////////////////////////////////////////////\n\n\tWELCOME TO SUPER RENTAL CAR SERVICES\n\n//////////////////////////////////////////////////////")

    option = input("Do you have a member? (Y/N): ")
    if option.lower() == "y":
        user_id = users_login()

        # Admin
        if user_id == "A001":
            admin_menu(user_id)
        # Member
        elif user_id is not None:
            member_menu(user_id)
        else:
            view_car_available(user_id)

    elif option.lower() == "n":
        registration_opt = input("Would you like to register for a member? (Y/N): ")

        if registration_opt.lower() == "y":
            user_id = registration()
        else:
            print("~ Showing car to be rented ~")

        view_car_available(user_id)

    # Exit status
    print("\n''''''''''''''''''''''''''''''''''''''''''''''''''''''\n\n\t\tThanks for visiting SCRS application ~~\n\n "
          "''''''''''''''''''''''''''''''''''''''''''''''''''''''")


# Call main function
main()
