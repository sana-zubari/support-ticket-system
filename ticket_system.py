import json
import os
from datetime import datetime, timedelta

DATA_FILE = "tickets.json"
LOG_FILE = "activity.log"

# ---------------- FILE HANDLING ---------------- #

def load_tickets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_tickets(tickets):
    with open(DATA_FILE, "w") as file:
        json.dump(tickets, file, indent=4)

def write_log(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} : {message}\n")        

# ---------------- SLA LOGIC ---------------- #

def check_sla(ticket):
    created = datetime.fromisoformat(ticket["created_at"])

    if ticket["priority"] == "High":
        limit = timedelta(hours=4)
    elif ticket["priority"] == "Medium":
        limit = timedelta(hours=8)
    else:
        limit = timedelta(hours=24)
    
    if datetime.now() - created > limit and ticket["status"] != "Closed":
        return "BREACHED"
    return "OK"

def get_escalation(ticket):
    created = datetime.fromiosformat(ticket["created_at"])
    age = datetime.now() - created

    if ticket["priority"] == "High" and age > timedelta(hours=2):
        return "LEVEL 2"
    elif ticket["priority"] == "Medium" and age > timedelta(hours=6):
        return "LEVEL 1"
    return "Normal"


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
        "status": "Open",
        "created_at": datetime.now().isoformat(),
        "history": ["Created"]
    }

    tickets.append(ticket)
    save_tickets(tickets)

    write_log(f"Ticket {ticket_id} created")

    print(f"Ticket {ticket_id} created successfully!")


def view_tickets():
    tickets = load_tickets()

    if not tickets:
        print("No tickets found.")
        return

    for t in tickets:
        sla = check_sla(t)
        esc = get_escalation(t)

        print("\n-------------------")
        print(f"ID: {t['id']}")
        print(f"Title: {t['title']}")
        print(f"Priority: {t['priority']}")
        print(f"Status: {t['status']}")
        print(f"SLA: {sla}")
        print(f"Escalation: {esc}")


def update_status():
    tickets = load_tickets()
    tid = int(input("Ticket ID: "))

    for t in tickets:
        if t["id"] == tid:
            new_status = input("New Status (In Progress/Closed): ")
            t["status"] = new_status
            t["history"].append(new_status)
            save_tickets(tickets)
            write_log(f"Ticket {tid} status changed to {new_status}")
            print("Updated.")
            return

    print("Ticket not found.")


def search_priority():
    tickets = load_tickets()
    p = input("Priority to filter: ")
    
    for t in tickets:
        if t["priority"].lower() == p.lower():
            print(f"nID {t['id']} - {t['title']} - {t['status']}")

def ticket_history():
    tickets = load_tickets()
    tid = int(input("Ticket ID: "))

    for t in tickets:
        if t["id"] == tid:
            print("History:")
            for h in t["history"]:
                print("-", h)
            return
    
    print("Ticket not found.")


def dashboard():
    tickets = load_tickets()

    open_count = 0
    breached = 0
    high_priority = 0

    for t in tickets:
        if t["status"] != "Closed":
            open_count =+ 1
        if check_sla(t) == "BREACHED":
            breached += 1
        if t["priority"] == "High":
            high_priority += 1

    print("\n===== SYSTEM DASHBOARD =====")
    print(f"Open Tickets: {open_count}")
    print(f"SLA Breached: {breached}")
    print(f"High Priority: {high_priority}")

def view_logs():
    if not os.path.exists(LOG_FILE):
        print("No logs yet.")
        return
    with open(LOG_FILE, "r") as file:
        print("\n===== ACTIVITY LOG =====")
        print(file.read())


# ---------------- MENU ---------------- #

def menu():
    while True:
        print("\n===== INCIDENT MANAGEMENT SYSTEM =====")
        print("1. Create Ticket")
        print("2. View Tickets")
        print("3. Update Status")
        print("4. Filter by Priority")
        print("5. View Ticket History")
        print("6. Dashboard")
        print("7. View Logs")
        print("8. Exit")


        choice = input("Option: ")

        if choice == "1":
            create_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            update_status()
        elif choice == "4":
            search_priority()
        elif choice == "5":
            ticket_history()
        elif choice == "6":
            dashboard()
        elif choice == "7":
            view_logs()
        elif choice == "8":
            break
        else:
            print("Invalid option")


menu()
