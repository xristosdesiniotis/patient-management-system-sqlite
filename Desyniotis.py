import sqlite3
from datetime import datetime

class Patient:
    def __init__(self, amka: str, first_name: str, last_name: str):
        self.amka = amka
        self.first_name = first_name
        self.last_name = last_name
    
    def __str__(self):
        return f"{self.amka} - {self.first_name} {self.last_name}"
        
class Examination:
    def __init__(self, amka: str, date: str, shift: str,
                 pressure: float, pulses: int, temperature: float, oxygen: int):
        self.amka = amka
        self.date = date
        self.shift = shift
        self.pressure = pressure
        self.pulses = pulses
        self.temperature = temperature
        self.oxygen = oxygen

    def __str__(self):
        return (f"{self.date} [{self.shift}] "
                f"pressure={self.pressure}, pulses={self.pulses}, "
                f"temp={self.temperature}, oxygen={self.oxygen}")

class ClinicApp:
    def __init__(self, db_path: str = "clinic.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            amka TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS examinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amka TEXT NOT NULL,
            date TEXT NOT NULL,
            shift TEXT NOT NULL CHECK(shift IN ('m','a','e')),
            pressure REAL NOT NULL,
            pulses INTEGER NOT NULL,
            temperature REAL NOT NULL,
            oxygen INTEGER NOT NULL,
            UNIQUE(amka, date, shift),
            FOREIGN KEY (amka) REFERENCES patients(amka) ON DELETE CASCADE
        );
        """)

        self.conn.commit()
        
    def register_patient(self):
      amka = input("Εισάγετε το ΑΜΚΑ(11 ψηφία): ").strip()

      if len(amka) == 11 and amka.isdigit():
         first_name = input("Εισάγετε όνομα ").strip()
         last_name = input("Εισάγετε επίθετο ").strip()

         cur = self.conn.cursor()
         cur.execute("SELECT * FROM patients WHERE amka = ?", (amka,))
         row = cur.fetchone()

         if row is None:
             cur.execute(
                "INSERT INTO patients (amka, first_name, last_name) VALUES (?, ?, ?)",
                 (amka, first_name, last_name)
             )
             self.conn.commit()
             print("Ο ασθενής καταχωρήθηκε επιτυχώς στο σύστημα.")
         else:
             choice = input("Θέλετε ενημέρωση στοιχείων;(ναι,όχι). ").strip().lower()
             if choice == "ναι":
                 cur.execute(
                    "UPDATE patients SET first_name = ?, last_name = ? WHERE amka = ?",
                    (first_name, last_name, amka)
                 )
                 self.conn.commit()
                 print("Τα στοιχεία ενημερώθηκαν.")
             else:
                 print("Δεν άλλαξαν τα στοιχεία.")
      else:
          print("Λάθος ΑΜΚΑ, πρέπει να είναι συνολικά 11 ψηφία.")
          

    def add_daily_examinations(self):
    
      amka = input("Εισάγετε το ΑΜΚΑ(11 ψηφία): ").strip()

      if len(amka) == 11 and amka.isdigit():
          cur = self.conn.cursor()

          cur.execute("SELECT 1 FROM patients WHERE amka = ?;", (amka,))
          if cur.fetchone() is None:
              print("Δεν βρέθηκε ασθενής με το ΑΜΚΑ που εισάγατε.")
              return

          date = datetime.now().strftime("%Y-%m-%d")

          shift = input("Εισάγετε βάρδια εξέτασης(m/a/e): ").strip().lower()
          if shift not in ("m", "a", "e"):
              print("Λάθος βάρδια.")
              return

          # Ζητά αρτηριακή πίεση με έλεγχο εγκυρότητας
          try:
              pressure = float(input("Εισάγετε αρτηριακή πίεση(float): "))
          except ValueError: 
              print("Λάθος τιμή")
              return
          
          # Ζητά παλμούς με έλεγχο εγκυρότητας
          try:
              pulses = int(input("Εισάγετε παλμούς(integer): "))
          except ValueError: 
              print("Λάθος τιμή")
              return
          
          # Ζητά θερμοκρασία με έλεγχο εγκυρότητας
          try:
              temperature = float(input("Εισάγετε θερμοκρασία(float): "))
          except ValueError: 
               print("Λάθος τιμή")
               return
           
          # Ζητά κορεσμό οξυγόνου με έλεγχο εγκυρότητας
          try:
              oxygen = int(input("Εισάγετε κορεσμό οξυγόνου(integer): "))
          except ValueError: 
              print("Λάθος τιμή")
              return
          

          exam = Examination(
              amka, date, shift,
              pressure, pulses, temperature, oxygen
        )

          try:
              cur.execute(
                  "INSERT INTO examinations (amka, date, shift, pressure, pulses, temperature, oxygen) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (exam.amka, exam.date, exam.shift,
                   exam.pressure, exam.pulses, exam.temperature, exam.oxygen)
              )
              self.conn.commit()
              print("Η εξέταση καταχωρήθηκε.")
          except sqlite3.IntegrityError:
              print("Υπάρχει ήδη εξέταση για αυτή τη βάρδια σήμερα.")

      else:
          print("Λάθος ΑΜΚΑ (πρέπει να είναι 11 ψηφία).")
        
        
    def patients_list(self):
        cur = self.conn.cursor()

        cur.execute("SELECT amka, first_name, last_name FROM patients;")
        rows = cur.fetchall()

        if len(rows) == 0:
            print("Δεν βρέθηκαν ασθενείς στο σύστημα.")
            return

        print("\n--- Λίστα Ασθενών ---")
        for row in rows:
            amka = row[0]
            first_name = row[1]
            last_name = row[2]

            p = Patient(amka, first_name, last_name)
            print(p)

 
    def patient_history(self):
        amka = input("Εισάγετε ΑΜΚΑ: ").strip()

        if len(amka) == 11 and amka.isdigit():
            cur = self.conn.cursor()

            # Έλεγχος ότι υπάρχει ο ασθενής
            cur.execute("SELECT first_name, last_name FROM patients WHERE amka = ?;", (amka,))
            patient_row = cur.fetchone()

            if patient_row is None:
                print("Δεν βρέθηκε ασθενής με αυτό το ΑΜΚΑ.")
                return

            first_name = patient_row[0]
            last_name = patient_row[1]

            print(f"\nΙστορικό εξετάσεων για: {first_name} {last_name} ({amka})")

            # Φέρνουμε όλες τις εξετάσεις του
            cur.execute("""
                SELECT date, shift, pressure, pulses, temperature, oxygen
                FROM examinations
                WHERE amka = ?
                ORDER BY date, shift;
            """, (amka,))

            rows = cur.fetchall()

            if len(rows) == 0:
                print("Δεν υπάρχουν καταχωρημένες εξετάσεις για αυτόν τον ασθενή.")
                return

            print("\n--- Εξετάσεις ---")
            for row in rows:
                date = row[0]
                shift = row[1]
                pressure = row[2]
                pulses = row[3]
                temperature = row[4]
                oxygen = row[5]

                exam = Examination(amka, date, shift, pressure, pulses, temperature, oxygen)
                print(exam)

        else:
            print("Λάθος ΑΜΚΑ (πρέπει να είναι 11 ψηφία).")


    def delete_patient(self):
        amka = input("Εισάγετε ΑΜΚΑ για διαγραφή: ").strip()

        if len(amka) == 11 and amka.isdigit():
            cur = self.conn.cursor()

            # έλεγχος αν υπάρχει ασθενής
            cur.execute("SELECT 1 FROM patients WHERE amka = ?;", (amka,))
            if cur.fetchone() is None:
                print("Δεν βρέθηκε ασθενής με αυτό το ΑΜΚΑ.")
                return

            print("Ο ασθενής βρέθηκε και θα πραγματοποιηθεί διαγραφή")

            cur.execute("DELETE FROM patients WHERE amka = ?;", (amka,))
            self.conn.commit()

            print("Η καρτέλα του ασθενή διαγράφηκε από το σύστημα.")
        else:
            print("Λάθος ΑΜΚΑ (πρέπει να είναι 11 ψηφία).")

    def menu(self):
        while True:
            print("\n--- Σύστημα Διαχείρισης Ασθενών ---")
            print("1. Εγγραφή νέου ασθενή")
            print("2. Καταχώριση ημερήσιων εξετάσεων")
            print("3. Λίστα ασθενών")
            print("4. Ιστορικό ασθενή")
            print("5. Διαγραφή ασθενή")
            print("0. Έξοδος")

            choice = input("Επιλογή: ").strip()

            if choice == "1":
                self.register_patient()
            elif choice == "2":
                self.add_daily_examinations()
            elif choice == "3":
                self.patients_list()
            elif choice == "4":
                self.patient_history()
            elif choice == "5":
                self.delete_patient()
            elif choice == "0":
                print("Έξοδος από το σύστημα.")
                break
            else:
                print("Μη έγκυρη επιλογή.")



    def close(self):
        self.conn.close()


if __name__ == "__main__":
    app = ClinicApp()
    app.create_tables()
    app.menu()
    app.close()
