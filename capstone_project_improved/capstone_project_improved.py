# Import libraries
import sqlite3
import string

# Connect to ebookstore db
db = sqlite3.connect('data/ebookstore.db')
cursor = db.cursor()

# Declare Book class
class Book():
    # Initialise instance variables
    def __init__(self, title, author, qty):
        self.title = title
        self.author = author
        self.qty = qty

    # Define class functions (methods)
    # Each executes its own SQL as well as additional
    # logic for the task chosen by the user
    def add(self):
        if self.qty < 1:
            return print('\nSorry, you cannot add nil or negative stock.')
        cursor.execute(''' 
        INSERT INTO books(title, author, qty)
        VALUES(?,?,?)''', (self.title, self.author, self.qty))
        db.commit()
        if self.qty > 1:
            return print(f'\n{str(self.qty)} copies of \'{self.title}\' by \'{self.author}\' have been added.')
        elif self.qty == 1:
            return print(f'\n{str(self.qty)} copy of \'{self.title}\' by \'{self.author}\' has been added.')

    def update_title(self, new_title, id):
        cursor.execute('''UPDATE books SET title = ? WHERE id = ?''', 
                       (new_title, id))
        db.commit()
        if self.title == new_title:
            return print(f'\nThe book with ID={str(id)} already has the title \'{new_title}\'.')
        else:
            return print(f'\nThe title of the book with ID={str(id)} has been updated from \'{self.title}\' to \'{new_title}\'.')
         
    def update_author(self, new_author, id):
        cursor.execute('''UPDATE books SET author = ? WHERE id = ?''', 
                       (new_author, id))
        db.commit()
        if self.author == new_author:
            return print(f'\nThe book with ID={str(id)} already has the author \'{new_author}\'.')
        else:
            return print(f'\nThe title of the book with ID={str(id)} has been updated from \'{self.author}\' to \'{new_author}\'.')

    def update_qty(self, new_qty, id):
        updated_qty = self.qty + new_qty
        cursor.execute('''UPDATE books SET qty = ? WHERE id = ?''', 
                       (updated_qty, id))
        db.commit()
        if updated_qty < 0:
            return print('\nYou cannot have negative stock. Please try again.')
        else:
            return print(f'\nNumber of books with ID={str(id)} has been updated from \'{self.qty}\' to \'{updated_qty}\'.')
    
    def delete(self, id):
        print(f'\nAre you sure you wish to delete \'{self.title}\' by \'{self.author}\'?')
        while True:
            answer = input('Yes/No: ').strip().capitalize()
            if answer == 'Yes':
                cursor.execute('''DELETE FROM books WHERE id = ?''', (id,))
                db.commit()
                return print(f'\n\'{self.title}\' by \'{self.author}\' has been deleted.')
            elif answer == 'No':
                return print('\nDelete operation cancelled.')
            else:
                print('\nSorry, please answer \'Yes\' or \'No\'.')

# Create table called book with fields id, title, author, qty
# Try-Except block to catch error if table has already been created
try:
    cursor.execute('''
        CREATE TABLE books(id INTEGER PRIMARY KEY,
                            title TEXT,
                            author TEXT,
                            qty INTEGER)
    ''')
    db.commit()

    # Add initial values to table
    initial_books = [(3001, "A Tale of Two Cities", "Charles Dickens", 30), 
                    (3002, "Harry Potter and the Philosopher\'s Stone", "J.K. Rowling", 40), 
                    (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25), 
                    (3004, "The Lord of the Rings", "J.R.R Tolkien", 37), 
                    (3005, "Alice in Wonderland", "Lewis Carroll", 12)]

    cursor.executemany('''
        INSERT INTO books(id, title, author, qty)
        VALUES(?,?,?,?)''', (initial_books))
    db.commit()
    print('\nWelcome! This is your eBookStore Programme to easily add, update and take stock of your bookshop inventory.\nIf you ever want to return to the main menu, simply enter \'\\\' into the terminal no matter where you are in the programme.')

except sqlite3.OperationalError:
    # 'Go Back' feature implemented throughout programme
    # Just enter '\' in the terminal to go back to the main menu
    print('\nWelcome Back! Remember, to go back to the main menu at any point just enter \'\\\'.')

# Create menu containing different user options
# Try-Except blocks used throughout programme to prevent ValueErrors
# when user is inputting integers
while True:
    # Variable to be updated when user enters '\' to go back
    go_back = False
    while True:
        try:
            menu = int(input('''\nSelect one of the following options:
1. Add a book
2. Update a book
3. Delete a book
4. Search books
5. Show inventory
0. Exit
'''))
            break
        except ValueError:
            print('\nSorry, please enter a number from the options given.')

    # Add book
    # Inputs capitalised to prevent duplicate records
    # If record already exists, quantity is added to existing record's qty
    if menu == 1:
        while True:
            try:
                while True:
                    print('\nEnter the details for the book you wish to add')
                    title = string.capwords(input('Title: ')).strip()
                    if title == '\\':
                        go_back = True
                        break

                    author = string.capwords(input('Author: ')).strip()
                    if author == '\\':
                        go_back = True
                        break

                    qty_str = input('Quantity: ').strip()
                    if qty_str == '\\':
                        go_back = True
                        break
                    else:
                        qty = int(qty_str)

                    if title == ''or author == '':
                        print('\nSorry, none of the fields can be empty.')
                    else:
                        break

                if go_back == True:
                    break

                cursor.execute('''SELECT * FROM books WHERE title = ? and author = ? ''', 
                              (title, author))
                exists = cursor.fetchone()

                if exists is not None:
                    # Update existing record (add qty to existing qty)
                    id = exists[0]
                    Book(title, author, qty).update_qty(qty, id)
                else:    
                    Book(title, author, qty).add()
                break

            except ValueError:
                print('\nSorry, please enter a valid integer for the quantity.')

    # Update book
    # Use id to find record with SQL
    # If exists, request what field user wants to update
    elif menu == 2:
        while True:
            while True:
                try:
                    print('\nEnter the ID of the book you wish to update')
                    id_str = input('ID: ').strip()
                    if id_str == '\\':
                        go_back = True
                        break
                    else:
                        id = int(id_str)
                        break
                except ValueError:  
                    print('\nSorry, please enter a valid ID.') 

            if go_back == True:
                break

            cursor.execute('''SELECT title, author, qty FROM books WHERE id = ?''', 
                        (id,))
            record_to_update = cursor.fetchone()
            if record_to_update is not None:
                while go_back == False:
                    try:
                        menu_str = input('''
1. Update Title
2. Update Author
3. Update Quantity
''').strip()
                        if menu_str == '\\':
                            go_back = True
                        else:
                            menu = int(menu_str)

                        if menu == 1:
                            while True:
                                new_title = string.capwords(input('\nEnter the updated title: ')).strip()
                                if new_title == '':
                                    print('\nSorry, this field cannot be empty.')
                                elif new_title == '\\':
                                    go_back = True
                                    break
                                else:
                                    break

                            if go_back == True:
                                break
                            else:
                                Book(record_to_update[0], record_to_update[1], record_to_update[2]).update_title(new_title, id)
                                break
                        
                        elif menu == 2:
                            while True:
                                new_author = string.capwords(input('\nEnter the updated author: ')).strip()
                                if new_author == '':
                                    print('\nSorry, this field cannot be empty.')
                                elif new_author == '\\':
                                    go_back = True
                                    break
                                else:
                                    break
                            if go_back == True:
                                break
                            else:
                                Book(record_to_update[0], record_to_update[1], record_to_update[2]).update_author(new_author, id)
                                break
                        
                        elif menu == 3:
                            while True:
                                try:
                                    new_qty_str = input('\nEnter the number of books you wish to add: ').strip()
                                    if new_qty_str == '\\':
                                        break
                                    else:
                                        new_qty = int(new_qty_str)
                                        Book(record_to_update[0], record_to_update[1], record_to_update[2]).update_qty(new_qty, id)
                                        break
                                except ValueError:
                                    print('\nSorry, please enter a valid integer.')
                            break
                        else:
                            print('\nSorry, please enter a number from the options given.')

                    except ValueError:
                        print('\nSorry, please enter a number from the options given.')
                break
            else:
                print('\nA record with that ID does not exist.')
                break
    
    # Delete book
    # Request ID of record to delete
    # If exists, delete record
    elif menu == 3:
        while True:
            while True:
                try:
                    print('\nEnter the ID of the book you wish to delete')
                    id_str = input('ID: ').strip()
                    if id_str == '\\':
                        go_back = True
                        break
                    else:
                        id = int(id_str)
                        break
                except ValueError:  
                        print('\nSorry, please enter a valid ID.')
            
            if go_back == True:
                break

            cursor.execute('''SELECT title, author, qty FROM books WHERE id = ?''', 
                            (id,))
            record_to_delete = cursor.fetchone()
            if record_to_delete is not None:
                Book(record_to_delete[0],record_to_delete[1],record_to_delete[2]).delete(id)
                break
            else:
                print('\nA record with that ID does not exist.')
                break
    
    # Search books
    # Request what field user wants to search with
    # If exists, display all records with corresponding field info
    # When searching title or author, searches whole table for 
    # each record containing searched word
    # Display all records containing searched word
    elif menu == 4:
        while True:
            try:
                menu_str = input('''
Search by:
1. ID
2. Title
3. Author
''').strip()
                if menu_str == '\\':
                    break
                else:
                    menu = int(menu_str)

                if menu == 1:
                    while True:
                        try:
                            print('\nEnter the ID of the record you wish to search')
                            id_str = input('ID: ').strip()

                            if id_str == '\\':
                                go_back = True
                                break
                            else:
                                id = int(id_str)
                                break

                        except ValueError:
                            print('Sorry, please enter a valid ID.')
                    
                    if go_back == True:
                        break

                    cursor.execute('''SELECT * FROM books WHERE id = ?''', 
                                    (id,))
                    record_to_search = cursor.fetchone()

                    if record_to_search is not None:
                        print('\nSearch Results (ID, Title, Author, Quantity):')
                        print(record_to_search)
                        break
                    else:
                        print('\nA record with that ID does not exist.')

                elif menu == 2:
                    print('\nEnter a keyword or the title you wish to search')
                    title_input = input('Search: ')
                    
                    if title_input == '\\':
                        break
                    else:
                        title = "%" + string.capwords(title_input).strip() + "%"

                    cursor.execute('''SELECT * FROM books WHERE title LIKE ? ''', (title,))
                    record_to_search = cursor.fetchall()

                    if record_to_search:
                        print('\nSearch Results (ID, Title, Author, Quantity):')
                        i = 0
                        for i in range(len(record_to_search)):
                            print(record_to_search[i])
                            i += 1
                    else:
                        print('\nNo results found.')
                    break

                elif menu == 3:
                    print('\nEnter a keyword or the author you wish to search')
                    author_input = input('Search: ')

                    if author_input == '\\':
                        break
                    else:
                        author = "%" + string.capwords(author_input).strip() + "%"

                    cursor.execute('''SELECT * FROM books WHERE author LIKE ? ''', (author,))
                    record_to_search = cursor.fetchall()

                    if record_to_search:
                        print('\nSearch Results (ID, Title, Author, Quantity):')
                        i = 0
                        for i in range(len(record_to_search)):
                            print(record_to_search[i])
                            i += 1
                    else:
                        print('\nNo results found.')
                    break
                else:
                    print('\nSorry, please enter a number from the options given.')

            except ValueError:
                print('\nSorry, please enter a number from the options given.')

    # Show Inventory
    # Display all records in books table
    # Each record printed on its own line
    elif menu == 5:
        cursor.execute('''SELECT * FROM books''')
        all_records = cursor.fetchall()
        i = 0
        total_chars = []
        for i in range(len(all_records)):
            total_chars.append(sum(len(str(x)) for x in all_records[i]))
            i += 1
        print('\nINVENTORY')
        print('-' * max(total_chars) + '------------')
        for i in range(len(all_records)):
            print(all_records[i])
            i += 1
        print('-' * max(total_chars) + '------------')

    # Exit
    elif menu == 0:
        print('\nGoodbye :)\n')
        exit()
    
    else:
        print('\nSorry, please enter a number from the options given.')