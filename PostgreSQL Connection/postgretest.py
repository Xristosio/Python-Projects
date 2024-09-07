import psycopg2

conn = psycopg2.connect(database = "", 
                        user = "", 
                        host= '',
                        password = "",
                        port = )
cur = conn.cursor()

class Person:
  def __init__(self, firstName, lastName, birthYear, id):
    self.id = id
    self.firstName = firstName
    self.lastName = lastName
    self.birthYear = birthYear

persons=[]
query = 'SELECT * FROM ...;'
cur.execute(query)

results = cur.fetchall()  # Παίρνει όλα τα αποτελέσματα
x = len(results)  # Πλήθος των γραμμών

persons = []  # Δημιουργία κενής λίστας για τα άτομα

for i in range(x):
    # Δημιουργία ενός αντικειμένου Person για κάθε γραμμή αποτελέσματος
    person = Person(results[i][0], results[i][1], results[i][2], results[i][3])
    persons.append(person)  # Προσθήκη του αντικειμένου στη λίστα

# Εκτύπωση πχ
print(persons[0].firstName)

conn.commit()
conn.close()