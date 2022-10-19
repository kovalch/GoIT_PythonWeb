from src.methods import remove_by_id, create, find_by_id, create_note, find_note_by_id, remove_note_by_id

def main():
    while True:
        print('Menu:',
              '1. AddressBook',
              '2. NoteBook',
              '3. Close program', sep='\n')
        user_command = input('Press menu button: >>> ')
        if user_command == '1':
            print('*'*60, 'AddressBook Manager', '*'*60, sep='\n')
            print('What are you going to do:',
              '1. Add new record to the AddressBook',
              '2. Check a record by id',
              '3. Remove a record by id', sep='\n')
            user_method = input('Press give a method: >>> ')
            if user_method == '1':
                result = create()
            elif user_method == '2':
                result = find_by_id()
            elif user_method == '3':
                result = remove_by_id()

            if result == 'Exit':
                continue
        elif user_command == '2':
            print('*'*60, 'NoteBook Manager', '*'*60, sep='\n')
            print('What are you going to do:',
              '1. Add new note to the NoteBook',
              '2. Check a note by id',
              '3. Remove a note by id', sep='\n')
            user_method = input('Press give a method: >>> ')
            if user_method == '1':
                result = create_note()
            elif user_method == '2':
                result = find_note_by_id()
            elif user_method == '3':
                result = remove_note_by_id()

            if result == 'Exit':
                continue
        elif user_command == '3':
            print('Good bye!')
            break


if __name__ == '__main__':
    main()