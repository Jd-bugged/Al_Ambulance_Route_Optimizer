import heapq

# =========================
# LOCATIONS
# =========================

locations = [
    "St. Vincent",
    "Cpt Cip",
    "St. Lucia",
    "SDS Medical",
    "Amang",
    "Marikina Valley",
    "St. Anthony",
    "Concepcion Uno",
    "Parang",
    "Nangka",
    "Lilac St.",
    "Santo Niño",
]

# =========================
# GRAPH
# Format:
# location: [(neighbor, distance, risk), ...]
# Risk scale:
# 1-3 = Low Risk
# 4-6 = Medium Risk
# 7-10 = High Risk
# =========================

graph = {
    "St. Vincent": [
        ("Cpt Cip", 8, 3),
        ("St. Lucia", 11, 4),
        ("SDS Medical", 13, 5),
        ("Amang", 12, 6),
        ("Marikina Valley", 18, 7),
        ("St. Anthony", 19, 8),
    ],
    "Cpt Cip": [
        ("St. Vincent", 8, 3),
        ("Concepcion Uno", 7, 4),
        ("Parang", 9, 5),
    ],
    "St. Lucia": [
        ("St. Vincent", 11, 4),
        ("Nangka", 8, 4),
    ],
    "SDS Medical": [
        ("St. Vincent", 13, 5),
        ("Lilac St.", 7, 3),
    ],
    "Amang": [
        ("St. Vincent", 12, 6),
        ("Santo Niño", 3, 2),
    ],
    "Marikina Valley": [
        ("St. Vincent", 18, 7),
    ],
    "St. Anthony": [
        ("St. Vincent", 19, 8),
    ],
    "Concepcion Uno": [
        ("Cpt Cip", 7, 4),
    ],
    "Parang": [
        ("Cpt Cip", 9, 5),
    ],
    "Nangka": [
        ("St. Lucia", 8, 4),
    ],
    "Lilac St.": [
        ("SDS Medical", 7, 3),
    ],
    "Santo Niño": [
        ("Amang", 3, 2),
    ],
}


# =========================
# DISPLAY LOCATIONS
# =========================

def show_locations():
    print("\nAvailable Locations:")
    for i, location in enumerate(locations):
        print(f"{i}. {location}")


# =========================
# GET USER LOCATION CHOICE
# =========================

def get_location_choice(message):
    while True:
        try:
            choice = int(input(message))

            if 0 <= choice < len(locations):
                return locations[choice]

            print("Invalid number. Please choose from the list.")

        except ValueError:
            print("Please enter a valid number.")


# =========================
# RISK LABEL
# =========================

def get_risk_label(risk):
    if risk <= 3:
        return "Low Risk"
    if risk <= 6:
        return "Medium Risk"
    return "High Risk"


# =========================
# DIJKSTRA WITH ROUTE BLOCKING
# =========================

def dijkstra(start, destination, blocked_routes=None):
    if blocked_routes is None:
        blocked_routes = []

    queue = [(0, 0, start, [start])]
    visited = set()

    while queue:
        total_distance, total_risk, current, path = heapq.heappop(queue)

        if current == destination:
            return total_distance, total_risk, path

        if current in visited:
            continue

        visited.add(current)

        for neighbor, distance, risk in graph[current]:
            route_key = tuple(sorted([current, neighbor]))

            if route_key in blocked_routes:
                continue

            if neighbor not in visited:
                heapq.heappush(
                    queue,
                    (
                        total_distance + distance,
                        total_risk + risk,
                        neighbor,
                        path + [neighbor],
                    ),
                )

    return None


# =========================
# ROUTE SUMMARY
# =========================

def show_route(distance, risk, path):
    print("\nBest Route Found:")
    print(" -> ".join(path))
    print(f"Total Distance: {distance}")
    print(f"Total Risk Score: {risk}")
    print(f"Risk Level: {get_risk_label(risk)}")


# =========================
# MAIN ROUTE SYSTEM
# =========================

def route_system():
    current_location = None

    while True:
        show_locations()

        if current_location is None:
            current_location = get_location_choice(
                "\nWhere are you right now? Choose number: "
            )
        else:
            print(f"\nCurrent Location: {current_location}")

        destination = get_location_choice("Where do you want to go? Choose number: ")

        if current_location == destination:
            print("\nYou are already in that location.")
            continue

        blocked_routes = []

        while True:
            result = dijkstra(current_location, destination, blocked_routes)

            if result is None:
                print("\nNo more available alternate routes.")
                break

            distance, risk, path = result
            show_route(distance, risk, path)

            if risk >= 7:
                print("\nWarning: This route has high risk.")
            elif risk >= 4:
                print("\nNotice: This route has medium risk.")
            else:
                print("\nThis route has low risk.")

            decision = input("\nAre you willing to take this route? (yes/no): ").lower()

            if decision == "yes":
                print(f"\nYou traveled from {current_location} to {destination}.")
                print(f"You have arrived at {destination}.")

                current_location = destination

                next_action = input(
                    "\nDo you want to end here or go to another location? (end/go): "
                ).lower()

                if next_action == "end":
                    print("\nNavigation ended. Stay safe!")
                    return
                if next_action == "go":
                    break

                print("\nInvalid choice. Navigation will continue.")
                break

            if decision == "no":
                print("\nFinding the next best alternate route...")

                for i in range(len(path) - 1):
                    route_key = tuple(sorted([path[i], path[i + 1]]))
                    blocked_routes.append(route_key)
            else:
                print("Please answer only yes or no.")


# =========================
# RUN PROGRAM
# =========================

if __name__ == "__main__":
    route_system()
