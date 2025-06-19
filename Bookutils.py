import mysql.connector

mydb = mysql.connector.connect(host="127.0.0.1", user="root", passwd="taolao", database="Library")
mycursor = mydb.cursor()

def searchBookByNameOrAuthor():
    while True:
        print("\nSEARCH BOOKS")
        print("1. By Book Name")
        print("2. By Author Name")
        print("3. Return to Previous Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter book name: ")
            query = "SELECT * FROM BookRecord WHERE BookName LIKE %s"
            mycursor.execute(query, ("%" + name + "%",))
        elif choice == "2":
            author = input("Enter author name: ")
            query = "SELECT * FROM BookRecord WHERE Author LIKE %s"
            mycursor.execute(query, ("%" + author + "%",))
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        results = mycursor.fetchall()
        if results:
            for row in results:
                print("\n==============================")
                print("Book ID    :", row[0])
                print("Book Name  :", row[1])
                print("Author     :", row[2])
                print("Publisher  :", row[3])
        else:
            print("No books found matching your search.")

def bookStatistics():
    print("\nBOOK STATISTICS")

    mycursor.execute("SELECT COUNT(*) FROM BookRecord")
    total_books = mycursor.fetchone()[0]

    mycursor.execute("SELECT COUNT(BookID) FROM UserRecord WHERE BookID IS NOT NULL")
    borrowed_books = mycursor.fetchone()[0]

    available_books = total_books - borrowed_books

    print(f"Total books       : {total_books}")
    print(f"Borrowed books    : {borrowed_books}")
    print(f"Available books   : {available_books}")
