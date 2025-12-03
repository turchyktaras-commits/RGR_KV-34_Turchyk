class View:
    def show_menu(self):
        print("\n--- ГОЛОВНЕ МЕНЮ ---")
        print("1. Керування Artists")
        print("2. Керування Organizers")
        print("3. Керування Festivals")
        print("4. Керування Lineups")
        print("5. Генерація даних (Random)")
        print("6. ОЧИСТИТИ ВСЮ БАЗУ (Видалити все)")
        print("7. ПОШУК І АНАЛІТИКА (Query 1-3)")
        print("0. Вихід")
        return input("Оберіть пункт: ")

    def show_artists(self, artists):
        print("\n--- Artists ---")
        if not artists:
            print("No data.")
        elif isinstance(artists, str):
            print(artists)
        else:
            print(f"{'ID':<5} {'Name':<25} {'Genre':<15} {'Country':<15}")
            print("-" * 65)
            for row in artists:
                print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<15}")

    def show_organizers(self, organizers):
        print("\n--- Organizers ---")
        if not organizers:
            print("No data.")
        elif isinstance(organizers, str):
            print(organizers)
        else:
            print(f"{'ID':<5} {'Company Name':<30} {'Email':<30}")
            print("-" * 70)
            for row in organizers:
                print(f"{row[0]:<5} {row[1]:<30} {row[2]:<30}")

    def show_festivals(self, festivals):
        print("\n--- Festivals ---")
        if not festivals:
            print("No data.")
        elif isinstance(festivals, str):
            print(festivals)
        else:
            print(f"{'ID':<5} {'Title':<30} {'City':<15} {'Date':<12} {'OrgID':<5}")
            print("-" * 75)
            for row in festivals:
                print(f"{row[0]:<5} {row[1]:<30} {row[2]:<15} {str(row[3]):<12} {row[4]:<5}")

    def show_lineups(self, lineups):
        print("\n--- Lineups ---")
        if not lineups:
            print("No data.")
        elif isinstance(lineups, str):
            print(lineups)
        else:
            print(f"{'ID':<5} {'FestID':<8} {'ArtID':<8} {'Stage':<20} {'Fee':<10}")
            print("-" * 60)
            for row in lineups:
                print(f"{row[0]:<5} {row[1]:<8} {row[2]:<8} {row[3]:<20} {row[4]:<10}")

    def show_message(self, message):
        print(f"\n>>> {message}")

    def show_crud_menu(self, table_name):
        print(f"\n--- УПРАВЛІННЯ: {table_name} ---")
        print("1. Показати всі")
        print("2. Додати новий")
        print("3. Редагувати")
        print("4. Видалити")
        print("0. Назад")
        return input("Ваш вибір: ")

    def get_id(self):
        return input("Введіть ID запису: ")

    def get_artist_inputs(self):
        return input("Name: "), input("Genre: "), input("Country: ")

    def get_organizer_inputs(self):
        return input("Company Name: "), input("Email: ")

    def get_festival_inputs(self):
        print("Формат дати: YYYY-MM-DD")
        return input("Title: "), input("City: "), input("Date: "), input("Organizer ID: ")

    def get_lineup_inputs(self):
        return input("Festival ID: "), input("Artist ID: "), input("Stage: "), input("Fee: ")

    def show_generation_menu(self):
        print("\n--- ГЕНЕРАЦІЯ ДАНИХ (RANDOM) ---")
        print("1. Згенерувати Артистів")
        print("2. Згенерувати Організаторів")
        print("3. Згенерувати Фестивалі (потребує Організаторів!)")
        print("4. Згенерувати Виступи/Лайнап (потребує Артистів та Фестивалі!)")
        print("0. Назад")
        return input("Оберіть таблицю: ")

    def get_count_input(self):
        return input("Введіть кількість записів для генерації (наприклад, 1000): ")

    def show_search_menu(self):
        print("\n--- АНАЛІТИКА ТА ПОШУК ---")
        print("1. Організатори: Витрати у містах за період (Range + Like + Date)")
        print("2. Артисти: Жанри та гонорари на сценах (Range + Like)")
        print("3. Фестивалі: Пошук за країною артистів та датою (Date + Like + Group)")
        print("0. Назад")
        return input("Оберіть запит: ")

    def get_search_1_inputs(self):
        print("\n--- Параметри пошуку організаторів ---")
        return (
            input("Частина назви міста (Like): "),
            input("Мін. сумарний бюджет (Range Start): "),
            input("Макс. сумарний бюджет (Range End): "),
            input("Дата початку (YYYY-MM-DD): "),
            input("Дата кінця (YYYY-MM-DD): ")
        )

    def get_search_2_inputs(self):
        print("\n--- Параметри пошуку артистів ---")
        return (
            input("Частина жанру (Like): "),
            input("Мін. гонорар за виступ: "),
            input("Макс. гонорар за виступ: "),
            input("Частина назви сцени (Like): ")
        )

    def get_search_3_inputs(self):
        print("\n--- Параметри пошуку фестивалів ---")
        return (
            input("Країна артиста (Like, напр. Ukraine): "),
            input("Дата початку періоду: "),
            input("Дата кінця періоду: ")
        )

    def show_search_results(self, columns, data, time_ms):
        print(f"\n--- Результати пошуку ({time_ms:.4f} ms) ---")
        if isinstance(data, str): 
            print(data)
            return

        if not data:
            print("Нічого не знайдено.")
            return

        header = " | ".join([f"{col:<20}" for col in columns])
        print(header)
        print("-" * len(header))
        
        for row in data:
            print(" | ".join([f"{str(item):<20}" for item in row]))
