import nosql.mongo_setup as mongo_setup

from nosql.car import Car

from nosql.engine import Engine

from nosql.servicehistory import ServiceHistory


def main():
    print_header()
    config_mongo()
 #   update_doc_versions()
    user_loop()


def print_header():
    print('----------------------------------------------')
    print('|                                             |')
    print('|           SERVICE CENTRAL v.02              |')
    print('|               demo edition                  |')
    print('|                                             |')
    print('----------------------------------------------')
    print()

def config_mongo():
    mongo_setup.global_init()

def update_doc_versions():
    for car in Car.objects():
        car._mark_as_changed('vi_number')
        car.save()


def user_loop():
    while True:
        print("Available actions:")
        print(" * [a]dd car")
        print(" * [l]ist cars")
        print(" * [f]ind car")
        print(" * perform [s]ervice")
        print(" * [p]oorly serviced cars")
        print(" * e[x]it")
        print()
        ch = input("> ").strip().lower()
        if ch == 'a':
            add_car()
        elif ch == 'l':
            list_cars()
        elif ch == 'f':
            find_car()
        elif ch == 's':
            service_car()
        elif ch == 'p':
            show_poorly_serviced_cars()
        elif not ch or ch == 'x':
            print("Goodbye")
            break


def add_car():
    model = input('What is the model? ')
    make = input('What is the make? ')
    year = int(input('Year built? '))
    # mileage = float(input('Mileage? '))
    # vin = input('VIN? ')

    car = Car()
    car.model = model
    car.make = make
    car.year = year
    # car.mileage = mileage
    # car.vi_number = vin

    engine = Engine()
    engine.horsepower = 600
    engine.mpg = 20
    engine.liters = 5.0

    car.engine = engine  # equals to an object

    car.save()   # in order to insert it to db in active record style, where we work with a single document



def list_cars():
    cars = Car.objects().order_by("-year") # query of objects ordered by year
    for car in cars:
        print("{} -- {} with vin {} (year {})".format(car.make, car.model, car.vi_number, car.year))
        print("{} of service records".format(len(car.service_history)))
        for s in car.service_history:
            print("  * ${:,.0f} {}".format(s.price, s.description))
    print()

def find_car():
    print("TODO: find_car")


def service_car():
    vin = input("What is the VIN of the car to service? ")
    service = ServiceHistory()
    service.price = float(input("What is the price of service? "))
    service.description = input("What type of service is this? ")
    service.customer_rating = int(input("How happy is our customer? [1-5] "))

    updated = Car.objects().filter(vi_number=vin).update_one(push__service_history=service) # it does update the doc, if
    # it finds it, will return 1, if not returns 0.
    if updated == 0:
        print("Car with VIN {} not found!".format(vin))
        return


def show_poorly_serviced_cars():
    level = int(input("What max level of satisfaction are we looking for? [1-5]"))
    # { "service_history.customer_rating" : {$lte: level}}
    cars = Car.objects().filter(service_history__customer_rating__lte=level)
    for car in cars:
        print("{} -- {} with vin {} (year {})".format(car.make, car.model, car.vi_number, car.year))
        print("{} of service records".format(len(car.service_history)))
        for s in car.service_history:
            print("  * Satisfaction: {} ${:,.0f} {}".format(s.customer_rating, s.price, s.description))
    print()

if __name__ == '__main__':
    main()
