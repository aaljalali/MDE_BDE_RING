import Add_user
import BDE_MDE_APP
if __name__ == "__main__":
    choice = input("Enter 1 to run the first program or 2 to run the second program: ")

    if choice == "1":
        BDE_MDE_APP.main()
    elif choice == "2":
        Add_user.main()
    else:
        print("Invalid choice. Please enter 1 or 2.")
