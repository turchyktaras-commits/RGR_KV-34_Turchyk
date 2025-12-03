import psycopg2
from psycopg2 import errors 
from db_config import db_config
import time

class Model:
    def __init__(self):
        self.connection = None
        try:
            self.connection = psycopg2.connect(**db_config)
            self.connection.autocommit = True
        except Exception as e:
            print(f"Критична помилка підключення: {e}")

    def __del__(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None, fetch=False):
        """
        Цей метод виконує запит і ловить помилки згідно з ТЗ.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                return "Операція виконана успішно!"
        
        except errors.ForeignKeyViolation:
            if "update or delete" in query.lower() or "delete" in query.lower():
                return "ПОМИЛКА: Неможливо видалити цей запис, оскільки до нього прив'язані залежні дані (фестивалі/виступи)."
            else:
                return "ПОМИЛКА: Вказаного ID (Організатора/Фестивалю/Артиста) не існує."

        except (errors.InvalidTextRepresentation, errors.NumericValueOutOfRange, errors.DatatypeMismatch):
            return "ПОМИЛКА: Некоректний формат даних. Перевірте, чи вводите ви числа там, де це потрібно, та формат дати (YYYY-MM-DD)."

        except errors.UniqueViolation:
            return "ПОМИЛКА: Запис з такими даними вже існує (дублікат)."

        except Exception as e:
            return f"Невідома помилка: {e}"

    # --- READ (Вибірка) ---
    def get_all_artists(self):
        return self.execute_query("SELECT * FROM artists ORDER BY id;", fetch=True)

    def get_all_organizers(self):
        return self.execute_query("SELECT * FROM organizers ORDER BY id;", fetch=True)

    def get_all_festivals(self):
        return self.execute_query("SELECT * FROM festivals ORDER BY id;", fetch=True)

    def get_all_lineups(self):
        return self.execute_query("SELECT * FROM lineups ORDER BY id;", fetch=True)

    # --- CRUD: ARTISTS ---
    def add_artist(self, name, genre, country):
        return self.execute_query(
            "INSERT INTO artists (name, genre, country) VALUES (%s, %s, %s)", 
            (name, genre, country)
        )

    def update_artist(self, id, name, genre, country):
        return self.execute_query(
            "UPDATE artists SET name=%s, genre=%s, country=%s WHERE id=%s", 
            (name, genre, country, id)
        )

    def delete_artist(self, id):
        return self.execute_query("DELETE FROM artists WHERE id=%s", (id,))

    # --- CRUD: ORGANIZERS ---
    def add_organizer(self, name, email):
        return self.execute_query(
            "INSERT INTO organizers (company_name, contact_email) VALUES (%s, %s)", 
            (name, email)
        )

    def update_organizer(self, id, name, email):
        return self.execute_query(
            "UPDATE organizers SET company_name=%s, contact_email=%s WHERE id=%s", 
            (name, email, id)
        )

    def delete_organizer(self, id):
        return self.execute_query("DELETE FROM organizers WHERE id=%s", (id,))

    # --- CRUD: FESTIVALS ---
    def add_festival(self, title, city, date, org_id):
        return self.execute_query(
            "INSERT INTO festivals (title, city, event_date, organizer_id) VALUES (%s, %s, %s, %s)", 
            (title, city, date, org_id)
        )

    def update_festival(self, id, title, city, date, org_id):
        return self.execute_query(
            "UPDATE festivals SET title=%s, city=%s, event_date=%s, organizer_id=%s WHERE id=%s", 
            (title, city, date, org_id, id)
        )

    def delete_festival(self, id):
        return self.execute_query("DELETE FROM festivals WHERE id=%s", (id,))

    # --- CRUD: LINEUPS ---
    def add_lineup(self, fest_id, art_id, stage, fee):
        return self.execute_query(
            "INSERT INTO lineups (festival_id, artist_id, stage_name, fee_amount) VALUES (%s, %s, %s, %s)", 
            (fest_id, art_id, stage, fee)
        )

    def update_lineup(self, id, fest_id, art_id, stage, fee):
        return self.execute_query(
            "UPDATE lineups SET festival_id=%s, artist_id=%s, stage_name=%s, fee_amount=%s WHERE id=%s", 
            (fest_id, art_id, stage, fee, id)
        )

    def delete_lineup(self, id):
        return self.execute_query("DELETE FROM lineups WHERE id=%s", (id,))

    def generate_organizers(self, count):
        query = """
        INSERT INTO organizers (company_name, contact_email)
        SELECT 
            name, 
            lower(replace(name, ' ', '_')) || '_' || trunc(random()*1000)::text || '@' || (ARRAY['gmail.com', 'event.ua', 'music.net', 'fest.org'])[floor(random()*4 + 1)::int]
        FROM (
            SELECT 
                (ARRAY['Global', 'Star', 'Mega', 'Prime', 'First', 'Ua', 'Kyiv', 'Lviv'])[floor(random()*8 + 1)::int] || ' ' || 
                (ARRAY['Events', 'Promo', 'Music', 'Production', 'Group', 'Agency', 'Fest'])[floor(random()*7 + 1)::int] as name
            FROM generate_series(1, %s)
        ) sub
        ON CONFLICT DO NOTHING;
        """
        return self.execute_query(query, (count,))

    def generate_artists(self, count):
        query = """
        INSERT INTO artists (name, genre, country)
        SELECT 
            (ARRAY['The', 'Neon', 'Black', 'White', 'Retro', 'Cyber', 'Happy', 'Angry', 'Silent'])[floor(random()*9 + 1)::int] || ' ' || 
            (ARRAY['Cats', 'Rockets', 'Waves', 'Beats', 'Wolves', 'Stars', 'Pilots', 'Monkeys', 'Orchestra'])[floor(random()*9 + 1)::int],
            
            (ARRAY['Rock', 'Pop', 'Jazz', 'Indie', 'Metal', 'Electronic', 'Hip-Hop', 'Folk'])[floor(random()*8 + 1)::int],
            
            (ARRAY['Ukraine', 'USA', 'UK', 'Germany', 'Poland', 'France', 'Italy', 'Canada'])[floor(random()*8 + 1)::int]
        FROM generate_series(1, %s);
        """
        return self.execute_query(query, (count,))

    def generate_festivals(self, count):
        query = """
        INSERT INTO festivals (title, city, event_date, organizer_id)
        SELECT 
            (ARRAY['Atlas', 'Faine', 'Zahid', 'Respublica', 'Jazz', 'Summer', 'Winter', 'Vibe'])[floor(random()*8 + 1)::int] || ' ' || 
            (ARRAY['Weekend', 'Fest', 'Open Air', 'Live', 'Days', 'Nights'])[floor(random()*6 + 1)::int],
            
            (ARRAY['Kyiv', 'Lviv', 'Odesa', 'Kharkiv', 'Dnipro', 'Ternopil', 'Kamianets'])[floor(random()*7 + 1)::int],
            
            NOW() + (random() * (interval '365 days')),
            
            (SELECT id FROM organizers ORDER BY random() + (g.i * 0) LIMIT 1)
        FROM generate_series(1, %s) as g(i);
        """
        return self.execute_query(query, (count,))

    def generate_lineups(self, count):
        query = """
        INSERT INTO lineups (festival_id, artist_id, stage_name, fee_amount)
        SELECT 
            (SELECT id FROM festivals ORDER BY random() + (g.i * 0) LIMIT 1),
            (SELECT id FROM artists ORDER BY random() + (g.i * 0) LIMIT 1),
            
            (ARRAY['Main Stage', 'Dark Stage', 'Light Stage', 'East Stage', 'West Stage'])[floor(random()*5 + 1)::int],
            
            (random() * 50000 + 1000)::numeric(10, 2)
        FROM generate_series(1, %s) as g(i)
        ON CONFLICT (festival_id, artist_id) DO NOTHING;
        """
        return self.execute_query(query, (count,))

    def clear_all_data(self):
        query = "TRUNCATE TABLE lineups, festivals, artists, organizers RESTART IDENTITY CASCADE;"
        return self.execute_query(query)

    def search_analytics_1(self, city_pattern, min_budget, max_budget, start_date, end_date):
        """
        Запит 1: Аналіз витрат організаторів.
        Знайти організаторів, які проводили фестивалі у містах, схожих на city_pattern,
        у заданий період дат, і сумарно виплатили гонорарів у діапазоні [min, max].
        
        Таблиці: organizers -> festivals -> lineups
        Атрибути: city (LIKE), date (RANGE), fee_amount (RANGE - SUM)
        """
        query = """
        SELECT 
            o.company_name, 
            COUNT(DISTINCT f.id) as festivals_count,
            SUM(l.fee_amount) as total_fees
        FROM organizers o
        JOIN festivals f ON o.id = f.organizer_id
        JOIN lineups l ON f.id = l.festival_id
        WHERE f.city ILIKE %s 
          AND f.event_date BETWEEN %s AND %s
        GROUP BY o.id, o.company_name
        HAVING SUM(l.fee_amount) BETWEEN %s AND %s
        ORDER BY total_fees DESC;
        """
        params = (f"%{city_pattern}%", start_date, end_date, min_budget, max_budget)
        
        start_time = time.time()
        result = self.execute_query(query, params, fetch=True)
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1000
        return result, execution_time_ms

    def search_analytics_2(self, genre_pattern, min_fee, max_fee, stage_pattern):
        """
        Запит 2: Аналіз популярності жанрів та сцен.
        Знайти артистів жанру genre_pattern, які виступали на сценах, схожих на stage_pattern,
        і отримували гонорар у діапазоні [min, max]. Показати кількість таких виступів.
        
        Таблиці: artists -> lineups
        Атрибути: genre (LIKE), stage_name (LIKE), fee_amount (RANGE)
        """
        query = """
        SELECT 
            a.name, 
            a.genre,
            COUNT(l.id) as shows_count,
            AVG(l.fee_amount)::numeric(10,2) as avg_fee
        FROM artists a
        JOIN lineups l ON a.id = l.artist_id
        WHERE a.genre ILIKE %s
          AND l.stage_name ILIKE %s
          AND l.fee_amount BETWEEN %s AND %s
        GROUP BY a.id, a.name, a.genre
        ORDER BY shows_count DESC;
        """
        params = (f"%{genre_pattern}%", f"%{stage_pattern}%", min_fee, max_fee)
        
        start_time = time.time()
        result = self.execute_query(query, params, fetch=True)
        end_time = time.time()
        
        return result, (end_time - start_time) * 1000

    def search_analytics_3(self, country_pattern, start_date, end_date):
        """
        Запит 3: Географія фестивалів.
        Знайти фестивалі, що проходили у заданий період, на яких виступало 
        більше 1 артиста з країни, схожої на country_pattern.
        
        Таблиці: festivals -> lineups -> artists
        Атрибути: country (LIKE), date (RANGE)
        """
        query = """
        SELECT 
            f.title,
            f.city,
            f.event_date,
            COUNT(DISTINCT a.id) as artists_count
        FROM festivals f
        JOIN lineups l ON f.id = l.festival_id
        JOIN artists a ON l.artist_id = a.id
        WHERE a.country ILIKE %s
          AND f.event_date BETWEEN %s AND %s
        GROUP BY f.id, f.title, f.city, f.event_date
        HAVING COUNT(DISTINCT a.id) > 0
        ORDER BY f.event_date;
        """
        params = (f"%{country_pattern}%", start_date, end_date)
        
        start_time = time.time()
        result = self.execute_query(query, params, fetch=True)
        end_time = time.time()
        
        return result, (end_time - start_time) * 1000
