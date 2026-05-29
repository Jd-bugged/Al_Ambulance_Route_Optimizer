import heapq

# =========================
# LOCATIONS
# =========================

locations = [
    "St. Vincent",
    "Garcia Hospital",
    "St. Victoria",
    "SDS Medical",
    "Amang",
    "Marikina Valley",
    "St. Anthony",
    "Concepcion Uno",
    "Parang",
    "Malanday",
    "Santo Niño",
    "Lilac St.",
    "E. Santos St.",
    "Katipunan St.",
]

# =========================
# GRAPH
# Format:
# location: [(neighbor, distance, risk), ...]
# Risk scale:
# 2-4 = Low Risk
# 5-7 = Medium Risk
# 8-10 = High Risk
# =========================

graph = {
    "St. Vincent": [
        ("Garcia Hospital", 8, 7),
        ("St. Victoria", 11, 5),
        ("SDS Medical", 13, 6),
        ("Amang", 12, 4),
        ("Marikina Valley", 18, 3),
        ("St. Anthony", 19, 2),
    ],
    "Garcia Hospital": [
        ("Concepcion Uno", 7, 3),
        ("Parang", 9, 4),
    ],
    "St. Victoria": [
        ("Malanday", 8, 5),
    ],
    "SDS Medical": [
        ("Lilac St.", 7, 7),
    ],
    "Amang": [
        ("Santo Niño", 3, 7),
    ],
    "Marikina Valley": [
        ("E. Santos St.", 10, 3),
    ],
    "St. Anthony": [
        ("Katipunan St.", 9, 5),
    ],
    "Concepcion Uno": [
        ("Parang", 10, 2),
        ("Malanday", 8, 4),
    ],
    "Parang": [
        ("Concepcion Uno", 10, 2),
        ("Katipunan St.", 8, 3),
    ],
    "Malanday": [
        ("Concepcion Uno", 8, 4),
        ("Lilac St.", 12, 2),
    ],
    "Lilac St.": [
        ("Malanday", 12, 2),
        ("Santo Niño", 11, 3),
    ],
    "Santo Niño": [
        ("Lilac St.", 11, 3),
        ("E. Santos St.", 4, 5),
    ],
    "E. Santos St.": [
        ("Santo Niño", 4, 5),
        ("Katipunan St.", 11, 2),
    ],
    "Katipunan St.": [
        ("E. Santos St.", 11, 2),
        ("Parang", 8, 3),
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
    if risk <= 4:
        return "Low Risk"
    if risk <= 7:
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
    print(f"Total Time: {distance} minutes")
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
