# Exercise 1 - Turn shopping cart into class.
# Ask the user four bits of input: Do you want to : Show/Add/Delete or Quit?

class NewCart():
    def __init__(self):
        self.this_cart = []
        self.empty_cart = 0

    def add_item(self):
        '''This function adds new items to the shopping cart.'''
        item = input('\nType in the item you would like to add to your cart: ')
        self.this_cart.append(item)
        self.empty_cart+=1

    def del_item(self):
        '''This function removes items from the shopping cart.'''
        self.get_cart()
        try:
            if self.empty_cart == 0:
                print('There are no items to remove.')
            else:
                index = int(input('\nEnter the item # you would like to remove: '))-1
                print(f"You've removed {self.this_cart[index].title()} from your shopping cart.")
                del self.this_cart[index]
                self.empty_cart-=1
        except:
            print('Invalid input.')
            self.del_item()

    def get_cart(self):
        '''This function displays contents in shoping cart.'''
        print("\nShopping Cart:") 
        if self.empty_cart == 0:
            print('Empty')
        else:
            for i in range(len(self.this_cart)):
                print(f'{i+1} - {self.this_cart[i].title()}')

    def runner(self):
        '''This functions runs each function within the class.'''
        options = {'Shop': 1, 'View Cart': 2, 'Remove Item': 3, 'Quit': 4}
        while True:
            print("\nType the number for the action you'd like to take.")
            for k,v in options.items():
                print(f" {v} - {k} ", end= " | ")
            try:
                select = int(input('Enter selection here: '))
            except:
                print('Invalid input. Type in a number.')
                self.runner()
            if select == options['Shop']:
                self.add_item()
            elif select == options['View Cart']:
                self.get_cart()
            elif select == options['Remove Item']:
                self.del_item()
            elif select == options['Quit']:
                break
            else:
                print('Invalid input. Select an option in the menu.')

# Run the code in the class
target = NewCart()
target.runner()