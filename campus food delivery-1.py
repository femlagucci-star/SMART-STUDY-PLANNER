# Campus Food Delivery and Order Management System

import json
import os

menu = {
    "Meals": {
        1: {"name": "Chicken & Chips", "price": 12000},
        2: {"name": "Beef and Rice", "price": 8000}, 
        3: {"name": "Posho and Beans", "price": 3000},
        4: {"name": "Matooke and G nuts", "price": 5000}
    },

    "Drinks": {
        5: {"name": "Soda", "price": 3000},
        6: {"name": "Rwenzori Water", "price": 1000},
        7: {"name": "Mango Juice", "price": 4000},
        8: {"name": "Milkshake", "price": 5000}
    },

    "Snacks": {
        9: {"name": "Samosa", "price": 1000},
        10: {"name": "Chapati", "price": 2000},
        11: {"name": "Doughnut", "price": 500},
        12: {"name": "Mandazi", "price": 500}
    }
}

riders = {
    "Ephraim": "Available",
    "Emmauel": "Available",
    "Musa": "Available",
    "Trevor": "Available"
}

orders = []
next_order_id = 1
LOG_FILE = "orders_log.json"


def show_menu():
    print("\n===== CAMPUS FOOD MENU =====")

    for category, items in menu.items():
        print(f"\n{category}")

        for number, item in items.items():
            print(
                f"{number}. {item['name']} - "
                f"UGX {item['price']:,}"
            )


def calculate_delivery_fee(subtotal):
    if subtotal >= 50000:
        return 0
    elif subtotal >= 30000:
        return 2000
    else:
        return 3000


def calculate_distance_fee(distance):
    if distance <= 1:
        return 1000
    elif distance <= 3:
        return 2000
    elif distance <= 6:
        return 4000
    else:
        return 6000


def get_delivery_fee(subtotal):
    print("\nDelivery fee")
    print("1. Based on order value")
    print("2. Based on distance")

    while True:
        choice = input("Choose 1 or 2: ")

        if choice == "1":
            return calculate_delivery_fee(subtotal)

        elif choice == "2":
            distance = input("Enter distance in km: ")

            try:
                distance = float(distance)

                if distance < 0:
                    print("Distance cannot be negative.")
                    continue

                return calculate_distance_fee(distance)

            except ValueError:
                print("Please enter a valid distance.")

        else:
            print("Please choose 1 or 2.")


def take_order():
    global next_order_id

    customer = input("\nEnter customer name: ")

    while customer == "":
        print("Customer name cannot be empty.")
        customer = input("Enter customer name: ")

    show_menu()

    items = []
    subtotal = 0

    while True:
        choice = input("\nEnter item number or 'done': ")

        if choice.lower() == "done":
            break

        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        item_number = int(choice)
        selected_item = None

        for category in menu:
            if item_number in menu[category]:
                selected_item = menu[category][item_number]
                break

        if selected_item is None:
            print("Item not found.")
            continue

        quantity = input("Enter quantity: ")

        if not quantity.isdigit() or int(quantity) <= 0:
            print("Please enter a valid quantity.")
            continue

        quantity = int(quantity)
        total = selected_item["price"] * quantity
        subtotal += total

        items.append({
            "name": selected_item["name"],
            "price": selected_item["price"],
            "quantity": quantity,
            "total": total
        })

        print("Item added successfully.")

    if len(items) == 0:
        print("No items were added.")
        return

    delivery_fee = get_delivery_fee(subtotal)
    total = subtotal + delivery_fee

    order_id = f"ORD{next_order_id:03d}"

    order = {
        "id": order_id,
        "customer": customer,
        "items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "rider": None,
        "status": "Pending"
    }

    orders.append(order)
    next_order_id += 1

    print("\n===== ORDER SUMMARY =====")
    print(f"Order ID: {order_id}")
    print(f"Customer: {customer}")

    for item in items:
        print(
            f"{item['name']} x {item['quantity']} "
            f"= UGX {item['total']:,}"
        )

    print(f"Subtotal: UGX {subtotal:,}")

    if delivery_fee == 0:
        print("Delivery fee: FREE")
    else:
        print(f"Delivery fee: UGX {delivery_fee:,}")

    print(f"Total: UGX {total:,}")
    print("Status: Pending")
    print("Order recorded successfully.")


def assign_rider():
    if len(orders) == 0:
        print("There are no orders.")
        return

    print("\n===== ASSIGN RIDER =====")

    for order in orders:
        if order["rider"] is None:
            print(
                f"{order['id']} - "
                f"{order['customer']} - "
                f"{order['status']}"
            )

    order_id = input("Enter order ID: ").upper()

    selected_order = None

    for order in orders:
        if order["id"] == order_id:
            selected_order = order
            break

    if selected_order is None:
        print("Order not found.")
        return

    if selected_order["rider"] is not None:
        print("This order already has a rider.")
        return

    available_riders = []

    for rider, status in riders.items():
        if status == "Available":
            available_riders.append(rider)

    if len(available_riders) == 0:
        print("No riders are available.")
        return

    print("\nAvailable riders:")

    for number, rider in enumerate(available_riders, start=1):
        print(f"{number}. {rider}")

    choice = input("Choose rider: ")

    if not choice.isdigit():
        print("Please enter a valid number.")
        return

    choice = int(choice)

    if choice < 1 or choice > len(available_riders):
        print("Invalid rider choice.")
        return

    rider = available_riders[choice - 1]

    selected_order["rider"] = rider
    riders[rider] = "Busy"

    print(f"{rider} assigned to {order_id}.")


def update_status():
    if len(orders) == 0:
        print("There are no orders.")
        return

    print("\n===== UPDATE ORDER STATUS =====")

    for order in orders:
        print(
            f"{order['id']} - "
            f"{order['customer']} - "
            f"{order['status']}"
        )

    order_id = input("Enter order ID: ").upper()

    selected_order = None

    for order in orders:
        if order["id"] == order_id:
            selected_order = order
            break

    if selected_order is None:
        print("Order not found.")
        return

    if selected_order["status"] == "Pending":

        if selected_order["rider"] is None:
            print("Assign a rider first.")
            return

        selected_order["status"] = "Out for Delivery"

    elif selected_order["status"] == "Out for Delivery":

        selected_order["status"] = "Delivered"

        rider = selected_order["rider"]

        if rider in riders:
            riders[rider] = "Available"

        save_order(selected_order)

    else:
        print("This order is already delivered.")
        return

    print(
        f"Order {order_id} is now "
        f"{selected_order['status']}."
    )


def view_orders():
    if len(orders) == 0:
        print("There are no orders.")
        return

    print("\n===== ALL ORDERS =====")

    for order in orders:

        if order["rider"] is None:
            rider = "Not assigned"
        else:
            rider = order["rider"]

        print(
            f"\nOrder: {order['id']}"
            f"\nCustomer: {order['customer']}"
            f"\nTotal: UGX {order['total']:,}"
            f"\nRider: {rider}"
            f"\nStatus: {order['status']}"
        )


def sales_report():
    if len(orders) == 0:
        print("There are no orders.")
        return

    revenue = 0
    item_sales = {}

    for order in orders:
        revenue += order["total"]

        for item in order["items"]:
            name = item["name"]

            if name in item_sales:
                item_sales[name] += item["quantity"]
            else:
                item_sales[name] = item["quantity"]

    best_item = max(item_sales, key=item_sales.get)

    print("\n===== SALES REPORT =====")
    print(f"Total orders: {len(orders)}")
    print(f"Total revenue: UGX {revenue:,}")
    print(
        f"Best-selling item: {best_item} "
        f"({item_sales[best_item]} sold)"
    )


def save_order(order):
    data = []

    if os.path.exists(LOG_FILE):

        try:
            with open(LOG_FILE, "r") as file:
                data = json.load(file)

        except:
            data = []

    data.append(order)

    with open(LOG_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_orders():
    global next_order_id

    if not os.path.exists(LOG_FILE):
        return

    try:
        with open(LOG_FILE, "r") as file:
            data = json.load(file)

        for order in data:
            orders.append(order)

            number = int(order["id"][3:])

            if number >= next_order_id:
                next_order_id = number + 1

    except:
        pass


def main():

    load_orders()

    while True:

        print("\n===== CAMPUS FOOD DELIVERY =====")
        print("1. View Menu")
        print("2. Take Order")
        print("3. Assign Rider")
        print("4. Update Order Status")
        print("5. View Orders")
        print("6. Sales Report")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_menu()

        elif choice == "2":
            take_order()

        elif choice == "3":
            assign_rider()

        elif choice == "4":
            update_status()

        elif choice == "5":
            view_orders()

        elif choice == "6":
            sales_report()

        elif choice == "7":
            print("Thank you for using Campus Food Delivery.")
            break

        else:
            print("Invalid choice.")


main()