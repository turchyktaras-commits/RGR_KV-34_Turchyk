from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice = self.view.show_menu()
            if choice == '1':
                self.manage_artists()
            elif choice == '2':
                self.manage_organizers()
            elif choice == '3':
                self.manage_festivals()
            elif choice == '4':
                self.manage_lineups()
            elif choice == '5':
                self.manage_generation()
            elif choice == '6':
                confirm = input("УВАГА! Це видалить ВСІ дані з усіх таблиць і скине ID. Продовжити? (y/n): ")
                if confirm.lower() == 'y':
                    msg = self.model.clear_all_data()
                    self.view.show_message(msg)
                else:
                    self.view.show_message("Операцію скасовано.")
            elif choice == '7': 
                self.manage_search()
            elif choice == '0':
                self.view.show_message("Exit.")
                break
            else:
                self.view.show_message("Invalid choice.")

    def manage_artists(self):
        while True:
            choice = self.view.show_crud_menu("ARTISTS")
            if choice == '1':
                self.view.show_artists(self.model.get_all_artists())
            elif choice == '2':
                n, g, c = self.view.get_artist_inputs()
                msg = self.model.add_artist(n, g, c)
                self.view.show_message(msg)
            elif choice == '3':
                id = self.view.get_id()
                n, g, c = self.view.get_artist_inputs()
                msg = self.model.update_artist(id, n, g, c)
                self.view.show_message(msg)
            elif choice == '4':
                id = self.view.get_id()
                msg = self.model.delete_artist(id)
                self.view.show_message(msg)
            elif choice == '0':
                break

    def manage_organizers(self):
        while True:
            choice = self.view.show_crud_menu("ORGANIZERS")
            if choice == '1':
                self.view.show_organizers(self.model.get_all_organizers())
            elif choice == '2':
                n, e = self.view.get_organizer_inputs()
                msg = self.model.add_organizer(n, e)
                self.view.show_message(msg)
            elif choice == '3':
                id = self.view.get_id()
                n, e = self.view.get_organizer_inputs()
                msg = self.model.update_organizer(id, n, e)
                self.view.show_message(msg)
            elif choice == '4':
                id = self.view.get_id()
                msg = self.model.delete_organizer(id)
                self.view.show_message(msg)
            elif choice == '0':
                break

    def manage_festivals(self):
        while True:
            choice = self.view.show_crud_menu("FESTIVALS")
            if choice == '1':
                self.view.show_festivals(self.model.get_all_festivals())
            elif choice == '2':
                t, c, d, oid = self.view.get_festival_inputs()
                msg = self.model.add_festival(t, c, d, oid)
                self.view.show_message(msg)
            elif choice == '3':
                id = self.view.get_id()
                t, c, d, oid = self.view.get_festival_inputs()
                msg = self.model.update_festival(id, t, c, d, oid)
                self.view.show_message(msg)
            elif choice == '4':
                id = self.view.get_id()
                msg = self.model.delete_festival(id)
                self.view.show_message(msg)
            elif choice == '0':
                break

    def manage_lineups(self):
        while True:
            choice = self.view.show_crud_menu("LINEUPS")
            if choice == '1':
                self.view.show_lineups(self.model.get_all_lineups())
            elif choice == '2':
                fid, aid, s, f = self.view.get_lineup_inputs()
                msg = self.model.add_lineup(fid, aid, s, f)
                self.view.show_message(msg)
            elif choice == '3':
                id = self.view.get_id()
                fid, aid, s, f = self.view.get_lineup_inputs()
                msg = self.model.update_lineup(id, fid, aid, s, f)
                self.view.show_message(msg)
            elif choice == '4':
                id = self.view.get_id()
                msg = self.model.delete_lineup(id)
                self.view.show_message(msg)
            elif choice == '0':
                break

    def manage_generation(self):
        while True:
            choice = self.view.show_generation_menu()
            
            if choice == '0':
                break
            
            count_str = self.view.get_count_input()
            if not count_str.isdigit():
                self.view.show_message("Будь ласка, введіть число!")
                continue
            
            count = int(count_str)
            
            if choice == '1':
                msg = self.model.generate_artists(count)
                self.view.show_message(msg)
            elif choice == '2':
                msg = self.model.generate_organizers(count)
                self.view.show_message(msg)
            elif choice == '3':
                msg = self.model.generate_festivals(count)
                self.view.show_message(msg)
            elif choice == '4':
                msg = self.model.generate_lineups(count)
                self.view.show_message(msg)
            else:
                self.view.show_message("Невірний вибір.")

    def manage_search(self):
        while True:
            choice = self.view.show_search_menu()
            
            if choice == '0':
                break
                
            elif choice == '1':
                city, min_b, max_b, d1, d2 = self.view.get_search_1_inputs()
                try:
                    data, time_ms = self.model.search_analytics_1(city, float(min_b), float(max_b), d1, d2)
                    self.view.show_search_results(['Organizer', 'Festivals Count', 'Total Budget'], data, time_ms)
                except ValueError:
                    self.view.show_message("Помилка: Введіть коректні числа/дати.")

            elif choice == '2':
                genre, min_f, max_f, stage = self.view.get_search_2_inputs()
                try:
                    data, time_ms = self.model.search_analytics_2(genre, float(min_f), float(max_f), stage)
                    self.view.show_search_results(['Artist', 'Genre', 'Shows Count', 'Avg Fee'], data, time_ms)
                except ValueError:
                    self.view.show_message("Помилка: Введіть коректні числа.")

            elif choice == '3':
                country, d1, d2 = self.view.get_search_3_inputs()
                try:
                    data, time_ms = self.model.search_analytics_3(country, d1, d2)
                    self.view.show_search_results(['Festival', 'City', 'Date', 'Artists from Country'], data, time_ms)
                except ValueError:
                    self.view.show_message("Помилка: Введіть коректні дати.")
            
            else:
                self.view.show_message("Невірний вибір.")
