from dbManager import DBManager


def main():
    manager = DBManager("127.0.0.1", "27017", "VacuumWorld", "states", "actions")
    # TODO: do whatever is needed here.
    manager.close_connection()

if __name__ == "__main__":
    main()
