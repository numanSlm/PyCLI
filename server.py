# Name - Numan Salim Shaikh
# SID - 40266934
# Course - COMP 6411
# Assignment 1

import socketserver
import os
import re

def load_database():
    db = []
    name_set = set()

    if os.path.exists('data.txt'):
        with open('data.txt', 'r') as file:
            for line in file:
                parts = line.strip().split('|')

                if len(parts) < 4:
                    print(f"Record skipped [missing field(s)]: {line.strip()}")
                    continue

                name = parts[0].strip().lower()
                if not name:
                    print(f"Record skipped [empty name field]: {line.strip()}")
                    continue

                if name in name_set:
                    print(f"Record skipped [customer already exists]: {line.strip()}")
                    continue

                age = parts[1].strip()
                if age and (not age.isdigit() or not (1 <= int(age) <= 120)):
                    print(f"Record skipped [invalid age field]: {line.strip()}")
                    continue

                address = parts[2].strip()
                if not all(c.isalnum() or c in ' .-' for c in address):
                    print(f"Record skipped [invalid address field]: {line.strip()}")
                    continue

                phone = parts[3].strip()
                if phone and not (re.match(r'^\d{3} \d{3}-\d{4}$', phone) or re.match(r'^\d{3}-\d{4}$', phone)):
                    print(f"Record skipped [invalid phone field]: {line.strip()}")
                    continue

                db.append((name, age, address, phone))
                name_set.add(name)

    #print(f"Database loaded with {len(db)} record(s) \n\nPython Server is now running...")
    print("\nPython Server is now running...")
    return db

class DatabaseRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip().decode()
        command, *params = self.data.split('|')
        response = ""

        if command == "find":
            response = self.find_customer(params[0])
        elif command == "add":
            response = self.add_customer(*params)
        elif command == "delete":
            response = self.delete_customer(params[0])
        elif command == "update_age":
            response = self.update_customer_age(params[0], params[1])
        elif command == "update_address":
            response = self.update_customer_address(params[0], params[1])
        elif command == "update_phone":
            response = self.update_customer_phone(params[0], params[1])
        elif command == "report":
            response = self.print_report()

        self.request.sendall(response.encode())

    def find_customer(self, name):
        for customer in self.server.database:
            if customer[0] == name.lower():
                return f"{customer[0]}|{customer[1]}|{customer[2]}|{customer[3]}"
        return "Customer not found"

    def validate_customer(self, name, age=None, address=None, phone=None):
        if not name.strip():
            return "Invalid name"
        if age and (not age.isdigit() or not (1 <= int(age) <= 120)):
            return "Invalid age"
        if address and not all(c.isalnum() or c in ' .-' for c in address):
            return "Invalid address"
        if phone and not (re.match(r'^\d{3} \d{3}-\d{4}$', phone) or re.match(r'^\d{3}-\d{4}$', phone)):
            return "Invalid phone"
        return "Valid"

    def add_customer(self, name, age, address, phone):
        name = name.lower().strip()
        validation = self.validate_customer(name, age, address, phone)
        if validation != "Valid":
            return validation
        if any(customer[0] == name for customer in self.server.database):
            return "Customer already exists"
        self.server.database.append((name, age, address, phone))
        return "Customer added"

    def delete_customer(self, name):
        name = name.lower().strip()
        if any(customer[0] == name for customer in self.server.database):
            self.server.database = [customer for customer in self.server.database if customer[0] != name]
            return "Customer deleted"
        return "Customer does not exist"

    def update_customer_age(self, name, age):
        name = name.lower().strip()
        validation = self.validate_customer(name, age)
        if validation != "Valid":
            return validation
        for i, customer in enumerate(self.server.database):
            if customer[0] == name:
                self.server.database[i] = (customer[0], age, customer[2], customer[3])
                return "Customer age updated"
        return "Customer not found"

    def update_customer_address(self, name, address):
        name = name.lower().strip()
        validation = self.validate_customer(name, address=address)
        if validation != "Valid":
            return validation
        for i, customer in enumerate(self.server.database):
            if customer[0] == name:
                self.server.database[i] = (customer[0], customer[1], address, customer[3])
                return "Customer address updated"
        return "Customer not found"

    def update_customer_phone(self, name, phone):
        name = name.lower().strip()
        validation = self.validate_customer(name, phone=phone)
        if validation != "Valid":
            return validation
        for i, customer in enumerate(self.server.database):
            if customer[0] == name:
                self.server.database[i] = (customer[0], customer[1], customer[2], phone)
                return "Customer phone updated"
        return "Customer not found"

    def print_report(self):
        report = "\n".join(f"{customer[0]}|{customer[1]}|{customer[2]}|{customer[3]}" for customer in sorted(self.server.database))
        return f"** Database contents **\n{report}\n\n"
        #return f"** Database contents **\n{report}\n\nTotal records: {len(self.server.database)}\n" if report else "Database is empty\n\n"

class DatabaseServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.database = load_database()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with DatabaseServer((HOST, PORT), DatabaseRequestHandler) as server:
        server.serve_forever()
