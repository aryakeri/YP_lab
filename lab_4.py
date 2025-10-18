"""Simple transport class hierarchy for Lab 4."""


class Transport:
    """Базовый класс для транспортных средств."""

    def __init__(self, brand: str, speed: int):
        self.brand = brand
        self.speed = speed

    def move(self) -> None:
        print(f"Transport is moving at {self.speed} km/h")

    def __str__(self) -> str:
        return f"Transport: {self.brand}, Speed: {self.speed}"


class Car(Transport):
    """Класс автомобиля"""

    def __init__(self, brand: str, speed: int, seats: int):
        super().__init__(brand, speed)
        self.seats = seats

    def move(self) -> None:
        print(f"Car {self.brand} is driving at {self.speed} km/h")

    def honk(self) -> None:
        print("Beep beep!")

    def __str__(self) -> str:
        return f"Car: {self.brand}, Speed: {self.speed}, Seats: {self.seats}"

    def __len__(self) -> int:
        return self.seats

    def __eq__(self, other) -> bool:
        if isinstance(other, Car):
            return self.speed == other.speed
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Car):
            return self.speed + other.speed
        return NotImplemented


class Bike(Transport):
    """Класс велосипеда."""

    def __init__(self, brand: str, speed: int, bike_type: str):
        super().__init__(brand, speed)
        self.type = bike_type

    def move(self) -> None:
        print(f"Bike {self.brand} is cycling at {self.speed} km/h")

    def __str__(self) -> str:
        return f"Bike: {self.brand}, Speed: {self.speed}, Type: {self.type}"


if __name__ == "__main__":
    base_transport = Transport("Generic", 40)
    car1 = Car("Toyota", 80, 5)
    car2 = Car("Tesla", 90, 4)
    bike = Bike("Giant", 25, "mountain")

    print(base_transport)
    print(car1)
    print(car2)
    print(bike)

    base_transport.move()
    car1.move()
    car1.honk()
    bike.move()

    print(f"Number of seats in {car1.brand}: {len(car1)}")
    print(f"car1 == car2: {car1 == car2}")
    print(f"car1 + car2: {car1 + car2}")

    try:
        print(car1 + bike)
    except TypeError as error:
        print(f"car1 + bike вызвало ошибку: {error}")

    vehicles_uniq = [base_transport, car1, car2, bike]
    for vehicle in vehicles_uniq:
        vehicle.move()
