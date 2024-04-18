from SOLID.SQLAlchemy.SQL_Manager import SQLManager


def main():
    sql_manager = SQLManager()
    sql_manager.get_irises()

if __name__ == "__main__":
    main()
