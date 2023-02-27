# Exercise 2 - Write a Python class which has two methods get_String and print_String. get_String accept a string from the user and print_String print the string in upper case 
class Return():
    def __init__(self) -> None:
        self.r_string = ''

    def get_String(self, n_string):
        self.r_string = n_string
    
    def print_String(self):
        print(self.r_string.upper())

test = Return()
test.get_String('bada bing')
test.print_String()