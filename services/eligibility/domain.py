from math import isfinite


def nonnegative(value):
    return type(value) in (int, float) and isfinite(value) and value >= 0


def operation(data, _):
    cold, radius, partners = data["cold"], data["radiusKm"], data["partners"]
    if type(cold) is not bool or not nonnegative(radius) or not isinstance(partners, list):
        raise ValueError("Expected cold, radiusKm and partners")
    sites, seen = [], set()
    for partner in partners:
        site, distance, capacity, refrigerated = (partner[key] for key in ("id", "distanceKm", "capacity", "refrigeration"))
        if (not isinstance(site, str) or not site.strip() or site in seen or not nonnegative(distance)
                or type(capacity) is not int or not 0 <= capacity <= 2**53 - 1 or type(refrigerated) is not bool):
            raise ValueError("Invalid partner data or duplicate ID")
        seen.add(site)
        if distance <= radius and (not cold or refrigerated):
            sites.append({"id": site, "distanceKm": distance, "capacity": capacity})
    return {"sites": sorted(sites, key=lambda item: (item["distanceKm"], item["id"]))}
