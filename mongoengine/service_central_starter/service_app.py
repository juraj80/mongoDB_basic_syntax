import nosql.mongo_setup as mongo_setup

from nosql.car import Car


def main():
    print_header()
    config_mongo()
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


def user_loop():
    while True:
        print("Available actions:")
        print(" * [a]dd car")
        print(" * [l]ist cars")
        print(" * [f]ind car")
        print(" * perform [s]ervice")
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
        elif not ch or ch == 'x':
            print("Goodbye")
            break


def add_car():
    model = input('What is the model?')
    make = input('What is the make?')
    year = int(input('Year built?'))
    # mileage = float(input('Mileage?'))
    # vin = input('VIN? ')

    car = Car()
    car.model = model
    car.make = make
    car.year = year
    # car.mileage = mileage
    # car.vi_number = vin

    car.save()   # in order to insert it to db in active record style, where we work with a single document



def list_cars():
    print("TODO: list_cars")


def find_car():
    print("TODO: find_car")


def service_car():
    print("TODO: service_car")


if __name__ == '__main__':
    main()
