import socket

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

def main(host, port):
    while True:
        choice = display_menu()

        if choice == '1':
            name = input("Enter customer name to find: ").strip()
            request = f"find|{name}"
            print(send_request(host, port, request))
        elif choice == '2':
            name = input("Enter customer name: ").strip()
            age = input("Enter customer age: ").strip()
            address = input("Enter customer address: ").strip()
            phone = input("Enter customer phone: ").strip()
            request = f"add|{name}|{age}|{address}|{phone}"
            print(send_request(host, port, request))
        elif choice == '3':
            name = input("Enter customer name to delete: ").strip()
            request = f"delete|{name}"
            print(send_request(host, port, request))
        elif choice == '4':
            name = input("Enter customer name to update age: ").strip()
            age = input("Enter new age: ").strip()
            request = f"update_age|{name}|{age}"
            print(send_request(host, port, request))
        elif choice == '5':
            name = input("Enter customer name to update address: ").strip()
            address = input("Enter new address: ").strip()
            request = f"update_address|{name}|{address}"
            print(send_request(host, port, request))
        elif choice == '6':
            name = input("Enter customer name to update phone: ").strip()
            phone = input("Enter new phone: ").strip()
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
