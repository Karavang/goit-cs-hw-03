import random
import psycopg2
from faker import Faker

fake = Faker()

conn = psycopg2.connect(
    dbname="mydb", user="user", password="123456", host="localhost", port="5432"
)
cur = conn.cursor()

existing_statuses = set()
cur.execute("SELECT name FROM status")
for row in cur.fetchall():
    existing_statuses.add(row[0])

statuses = ["To Do", "In Progress", "Done", "On Hold", "Cancelled"]
for status in statuses:
    if status not in existing_statuses:
        cur.execute("INSERT INTO status (name) VALUES (%s) RETURNING id", (status,))


user_ids = []
for _ in range(10):
    fullname = fake.name()
    email = fake.unique.email()
    cur.execute(
        "INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id",
        (fullname, email),
    )
    user_ids.append(cur.fetchone()[0])


cur.execute("SELECT id FROM status")
status_ids = [row[0] for row in cur.fetchall()]


for _ in range(50):
    title = fake.sentence(nb_words=4)
    description = fake.text(max_nb_chars=200)
    status_id = random.choice(status_ids)
    user_id = random.choice(user_ids)
    cur.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
        (title, description, status_id, user_id),
    )

conn.commit()
cur.close()
conn.close()

print("✅ Seed completed with 50 new tasks and 10 new users")
