from library import Library, Book, EBook,AudioBook, Member
from typing import Literal
from colorama import Fore, Style, init
init(autoreset=True)

def main():
    my_library = Library(name="Mew's Library")


    while True:
        print(Fore.GREEN + "--- Welcome to Mew's Library System v0.2 ---")
        print("1. Add by ISBN (OpenLibrary)") #OpenLibrary aracılığıyla ISBN kodu girerek kütüphaneye kitap ekle.
        print("2. Add Book")   #Kitap Ekle.
        print("3. Delete Book")   #Kitap Sil.
        print("4. List Books")   #Kitapları Listele.
        print("5. Search Book")  #Kütüphaneden Kitap Arat.
        print("6. Borrow Book") #Kitap Ödünç Al.
        print("7. Return Book") #Kitap İade Et.
        print("8. List Members") #Üyeleri Listele.
        print("9. Add Member") #Üye ekle.
        print("10. Delete Member") #Üye Sil.
        print("11. Who has this ISBN") # ISBN ile kitaba sahip kişiyi bulma.
        print("12. Exit")  #Sistemden Çıkış Yap.


        choice = input("Please enter your choice: ").strip()
##-----------------Add Book by ISBN---------------------
        if choice == "1":
           isbn = input("Enter ISBN to fetch from OpenLibrary: ").strip()
           kind = input("Type? (b=book, e=ebook, a=audiobook) [b]: ").strip().lower() or "b"

           if kind == "e":
               file_format = input("File format (e.g., EPUB/PDF) [EPUB]: ").strip() or "EPUB"
               ok = my_library.add_book_by_isbn(isbn, kind="ebook", file_format=file_format)
           elif kind == "a":
               duration = input("Duration in minutes (e.g., 780): ").strip()
               duration = int(duration or 0)
               ok = my_library.add_book_by_isbn(isbn, kind="audiobook", duration_in_minutes=duration)
           else:
               ok = my_library.add_book_by_isbn(isbn, kind="book")

           if ok:
               print(Fore.GREEN + "Book added via OpenLibrary.")
           else:
               print(Fore.RED + "Could not add book (not found or network error).")

##-----------------Add Book---------------------
        elif choice == "2":
            title = input("Book title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            page_count = input("Page count: ").strip()

            kind = input("Book Type? (b=book, e=ebook, a=audiobook) [b]: ").strip().lower() or "b"
            if kind == "e":
                file_format = input("File format (e.g., EPUB/PDF): ").strip() or "EPUB"
                book = EBook(title, author, isbn, file_format, page_count)
            elif kind == "a":
                duration = input("Duration in minutes: ").strip()
                duration = int(duration or 0)
                book = AudioBook(title, author, isbn, duration, page_count)
            else: book = Book(title, author, isbn, page_count)

            my_library.add_book(book)
            print(Fore.GREEN + f"'{title}' has been added as {book.__class__.__name__}.")
##-----------------Delete Book---------------------
        elif choice == "3":
            isbn = input("Enter ISBN to remove a book. ").strip()
            removed = my_library.remove_book(isbn)
            if removed:
                print(Fore.GREEN + f"Book with ISBN {isbn} has been removed. ")

            else:
                print(Fore.RED + f"No book found with ISBN {isbn}. ")

##-----------------List Book---------------------
        elif choice == "4":
            books = my_library.list_books()
            if not books:
                print(Fore.RED + "The Mew's Library is empty. ")

            else:
                print(Fore.CYAN + f"Total: {len(books)}")                
                for b in books:                   
                    status = "Borrowed" if b.is_borrowed else "Available"
                    status_color = Fore.RED if status == "Borrowed" else Fore.GREEN
                    type_color = Fore.YELLOW if b.__class__.__name__ == "EBook" else (Fore.MAGENTA if b.__class__.__name__ == "AudioBook" else Fore.WHITE)
                    tname = b.__class__.__name__
                    print(type_color + b.display_info() + " " + status_color + f"[{status}]")
##-----------------Search Book---------------------
        elif choice == "5":
            title = input("Enter title to search a book: ").strip()
            found = my_library.find_book(title)
            if found:
               status = "Borrowed" if found.is_borrowed else "Available"
               status_color = Fore.RED if status == "Borrowed" else Fore.GREEN
               type_color = Fore.YELLOW if found.__class__.__name__ == "EBook" else (
               Fore.MAGENTA if found.__class__.__name__ == "AudioBook" else Fore.WHITE
                  )
               print(type_color + found.display_info() + " " + status_color + f"[{status}]")
            else:
              print(Fore.RED + f"No book found with title '{title}'.")

##-----------------Borrow Book---------------------
        elif choice =="6":
            mid = input("Please enter Member ID: ").strip()
            isbn = input("Please enter ISBN to borrow a book. ").strip()
            try:
                mid_int = int(mid)
            except ValueError:
                print(Fore.RED + "Member ID must be a number.")
            else:
                ok = my_library.borrow_for_member(mid_int, isbn)
                if ok:
                    print(Fore.GREEN + "Borrowed successfully for the member.")
                else:
                    print(Fore.RED + "Cannot borrow (member/book not found or already borrowed).")
            
##-----------------Return Book---------------------
        elif choice =="7":
            mid = input("Please enter Member ID: ").strip()
            isbn = input("Please enter ISBN to return a book. ").strip()
            try:
                mid_int = int(mid_int)
            except ValueError:
                print(Fore.RED + "Member ID must be a number.")

            else:
                ok = my_library.return_for_member(mid_int, isbn)
                if ok:
                    print(Fore.GREEN + "Returned successfully for the member. ")
                else:
                    print(Fore.RED + "Cannot return (member/book not found or member doesn't have this book).")
         
##-----------------List Members---------------------
        elif choice =="8":
            members = my_library.list_members()
            if not  members:
                print(Fore.RED + "There are no members yet. ")
            else:
                print(Fore.CYAN + f"Members: {len(members)}")
                for m in members:
                    borrowed_count = len(getattr(m, "borrowed_books", []))
                    print(f" - {m.name} (ID:{Fore.GREEN}{m.member_id}{Fore.WHITE})  [Borrowed: {borrowed_count}]")


##-----------------Add Member---------------------
        elif choice =="9":
            name = input("Member name: ").strip()
            mid = input("Member ID (number): ").strip()
            try:
                mid_int = int(mid)
            except ValueError:
                print(Fore.RED + "Member ID must be a number. ")
            else:
                ok = my_library.add_member(Member(name=name, member_id=mid_int))
                print((Fore.GREEN + "Member added.") if ok else (Fore.RED + "Member ID already Exist"))

##-----------------Delete Member--------------------
        elif choice =="10":
            mid = input("Enter Member ID to delete: ").strip()
            try:
                mid_int = int(mid)
            except ValueError:
                print(Fore.RED + "Member ID must be a number.")
            else:
                removed = my_library.remove_member(mid_int)
                if removed:
                    print(Fore.GREEN + f"Member with ID {mid_int} has been removed.")
                else:
                    print(Fore.RED + f"No member found with ID {mid_int}.")

##-----------------Who has this ISBN---------------------
        elif choice =="11":
            isbn = input("ISBN: ").strip()
            owner = my_library.who_has_isbn(isbn)
            if owner is None:
                print(Fore.YELLOW + "No member currently holds this book.")
            else:
                print(Fore.CYAN + f"This book is currently borrowed by member ID {owner}.")

##-----------------Exit---------------------
        elif choice == "12":
            print(Fore.RED + "Exiting...")
            break

        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
            