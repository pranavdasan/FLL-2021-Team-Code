#!/usr/bin/env python3
import init
import message

# Main program
def main():

    # Menu items
    list = init.main_menu

    # Load the main menu on the console
    message.display_menu(list)

if __name__ == "__main__":
    main()
