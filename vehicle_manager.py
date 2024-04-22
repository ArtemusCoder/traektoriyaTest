from typing import Optional
import json
import requests
from dataclasses import dataclass
from math import sin, cos, atan2, radians, sqrt


@dataclass
class Vehicle:
    name: str
    model: str
    year: int
    color: str
    price: int
    latitude: float
    longitude: float
    id: Optional[int] = 0

    def to_json(self):
        return {"id": self.id, "name": self.name, "model": self.model, "year": self.year, "color": self.color,
                "price": self.price, "latitude": self.latitude, "longitude": self.longitude}


class VehicleManager:
    def __init__(self, url: str) -> None:
        self.url = url

    def get_vehicles(self):
        response = requests.get(self.url + "/vehicles").json()
        vehicles = []
        for vehicle in response:
            vehicles.append(Vehicle(**vehicle))
        return vehicles

    def filter_vehicles(self, params: dict):
        response = requests.get(self.url + "/vehicles").json()
        vehicles = []
        for vehicle in response:
            for key, value in params.items():
                if vehicle[key] == value:
                    vehicles.append(Vehicle(**vehicle))
        return vehicles

    def get_vehicle(self, vehicle_id: int):
        response = requests.get(self.url + f"/vehicles/{vehicle_id}").json()
        vehicle = Vehicle(**response)
        return vehicle

    def add_vehicle(self, vehicle: Vehicle):
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url + "/vehicles", data=json.dumps(vehicle.to_json()), headers=headers)
        return Vehicle(**response.json())

    def update_vehicle(self, vehicle: Vehicle):
        headers = {"Content-Type": "application/json"}
        response = requests.put(self.url + f"/vehicles/{vehicle.id}", data=json.dumps(vehicle.to_json()),
                                headers=headers)
        return Vehicle(**response.json())

    def delete_vehicle(self, id: int):
        response = requests.delete(self.url + f"/vehicles/{id}")
        return response.status_code

    def get_distance(self, id1: int, id2: int):
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)

        lat1 = vehicle1.latitude
        lon1 = vehicle1.longitude
        lat2 = vehicle2.latitude
        lon2 = vehicle2.longitude

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        R = 6371000

        distance = R * c

        return distance

    @staticmethod
    def get_distance_formula(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        R = 6371000

        distance = R * c

        return distance

    def get_nearest_vehicle(self, id: int):
        vehicle_main = self.get_vehicle(id)
        vehicles = self.get_vehicles()
        distances = {}
        for vehicle in vehicles:
            if vehicle_main.id != vehicle.id:
                distance = self.get_distance_formula(vehicle_main.latitude, vehicle_main.longitude,
                                                     vehicle.latitude, vehicle.longitude)
                distances[vehicle.id] = distance
        nearest_vehicle = min(distances, key=distances.get)
        for vehicle in vehicles:
            if vehicle.id == nearest_vehicle:
                return vehicle
