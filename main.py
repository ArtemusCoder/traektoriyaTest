from vehicle_manager import VehicleManager, Vehicle

manager = VehicleManager(url="https://test.tspb.su/test-task")

print(manager.get_vehicles())

print(manager.filter_vehicles(params={"color": "red"}))

print(manager.get_vehicle(vehicle_id=1))

print(manager.add_vehicle(
    vehicle=Vehicle
    (name='Toyota',
     model='Camry',
     year=2021,
     color='red',
     price=21000,
     latitude=55.753215,
     longitude=37.620393
     )
)
)

print(manager.update_vehicle(
    vehicle=Vehicle(
        id=1,
        name='Toyota',
        model='CAMRY',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
)
)

print(manager.delete_vehicle(id=1))

print(manager.get_distance(id1=1, id2=2))

print(manager.get_nearest_vehicle(id=1))
