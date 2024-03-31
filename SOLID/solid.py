from SOLID.SQL_Manager import SQLManager


def main():
    sql_manager = SQLManager()
    sql_manager.post_manager.add_post()


if __name__ == "__main__":
    main()