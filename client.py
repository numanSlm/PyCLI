import re
import socket
import os

def display_menu():
    return input("\n".join([
        "Customer Management Menu",
        "1. Find customer",
        "2. Add customer",
        "3. Delete customer",
        "4. Update customer age",
        "5. Update customer address",
        "6. Update customer phone",
        "7. Print report",
        "8. Exit",
        "Select: "
    ]))

def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(request.encode())
        response = sock.recv(1024).decode()
    return response
def clear_screen():
    os.environ['TERM'] = 'xterm'  # Set TERM to 'xterm' or another appropriate terminal type
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_validated_input(prompt, validation_func):
    while True:
        value = input(prompt).strip()
        if validation_func(value):
            return value
        print("Invalid input. Please try again.")

def validate_name(name):
    return bool(name.strip())

def validate_age(age):
    return age.isdigit() and 1 <= int(age) <= 120

def validate_address(address):
    return all(c.isalnum() or c in ' .-' for c in address)

def validate_phone(phone):
    return not phone or re.match(r'^\d{3} \d{3}-\d{4}$', phone) or re.match(r'^\d{3}-\d{4}$', phone)
def main(host, port):
    while True:
        clear_screen()
        choice = display_menu()

        if choice == '1':
            name = get_validated_input("Enter customer name to find: ", validate_name)
            request = f"find|{name}"
            print(send_request(host, port, request))
        elif choice == '2':
            name = get_validated_input("Enter customer name: ", validate_name)
            age = get_validated_input("Enter customer age: ", validate_age)
            address = get_validated_input("Enter customer address: ", validate_address)
            phone = get_validated_input("Enter customer phone: ", validate_phone)
            request = f"add|{name}|{age}|{address}|{phone}"
            print(send_request(host, port, request))
        elif choice == '3':
            name = get_validated_input("Enter customer name to delete: ", validate_name)
            request = f"delete|{name}"
            print(send_request(host, port, request))
        elif choice == '4':
            name = get_validated_input("Enter customer name to update age: ", validate_name)
            age = get_validated_input("Enter new age: ", validate_age)
            request = f"update_age|{name}|{age}"
            print(send_request(host, port, request))
        elif choice == '5':
            name = get_validated_input("Enter customer name to update address: ", validate_name)
            address = get_validated_input("Enter new address: ", validate_address)
            request = f"update_address|{name}|{address}"
            print(send_request(host, port, request))
        elif choice == '6':
            name = get_validated_input("Enter customer name to update phone: ", validate_name)
            phone = get_validated_input("Enter new phone: ", validate_phone)
            request = f"update_phone|{name}|{phone}"
            print(send_request(host, port, request))

        elif choice == '7':
            request = "report"
            print(send_request(host, port, request))
        elif choice == '8':
            print("Good Bye...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 9999
    main(HOST, PORT)