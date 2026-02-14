import json
import os

DATA_FILE = "tickets.json"


# ---------------- FILE HANDLING ---------------- #

def load_tickets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_tickets(tickets):
    with open(DATA_FILE, "w") as file:
        json.dump(tickets, file, indent=4)


# ---------------- TICKET OPERATIONS ---------------- #

def create_ticket():
    tickets = load_tickets()

    ticket_id = len(tickets) + 1
    title = input("Enter issue title: ")
    priority = input("Priority (Low/Medium/High): ")

    ticket = {
        "id": ticket_id,
        "title": title,
        "priority": priority,
        "status": "Open"
    }

    tickets.append(ticket)
    save_tickets(tickets)

    print(f"Ticket {ticket_id} created successfully!")


def view_tickets():
    tickets = load_tickets()

    if not tickets:
        print("No tickets found.")
        return

    for t in tickets:
        print("\n-------------------")
        print(f"ID: {t['id']}")
        print(f"Title: {t['title']}")
        print(f"Priority: {t['priority']}")
        print(f"Status: {t['status']}")


def search_ticket():
    tickets = load_tickets()
    tid = int(input("Enter Ticket ID: "))

    for t in tickets:
        if t["id"] == tid:
            print("\nTicket Found")
            print(t)
            return

    print("Ticket not found.")


def update_status():
    tickets = load_tickets()
    tid = int(input("Enter Ticket ID: "))

    for t in tickets:
        if t["id"] == tid:
            new_status = input("New Status (Open/In Progress/Closed): ")
            t["status"] = new_status
            save_tickets(tickets)
            print("Ticket updated.")
            return

    print("Ticket not found.")


def delete_ticket():
    tickets = load_tickets()
    tid = int(input("Enter Ticket ID to delete: "))

    updated = [t for t in tickets if t["id"] != tid]

    if len(updated) == len(tickets):
        print("Ticket not found.")
        return

    save_tickets(updated)
    print("Ticket deleted.")


# ---------------- MENU ---------------- #

def menu():
    while True:
        print("\n===== SUPPORT TICKET SYSTEM =====")
        print("1. Create Ticket")
        print("2. View Tickets")
        print("3. Search Ticket")
        print("4. Update Status")
        print("5. Delete Ticket")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == "1":
            create_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            search_ticket()
        elif choice == "4":
            update_status()
        elif choice == "5":
            delete_ticket()
        elif choice == "6":
            break
        else:
            print("Invalid option")


menu()
