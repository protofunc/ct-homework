# Dan's parking garage code.
class Garage():
    def __init__(self):
        self.tickets = 3
        self.parkingSpot = {
            1: {
                "open":True,
                "paid":False,
            },
            2: {
                "open":True,
                "paid":False,
            },
            3: {
                "open":True,
                "paid":False,
            }
        }

    def takeTicket(self):
        '''This function assigns an open parking spot if it's available.'''
        for spot in self.parkingSpot.keys():
            if self.parkingSpot[spot]["open"] == True:
                self.parkingSpot[spot]["open"] = False
                print(f"Please park in parking spot number {spot}.")
                self.tickets -= 1
                break
            elif self.tickets == 0:
                print("There are no available parking spaces.")
                break

    def getSpot(self):
        '''Return the parking spot used by each individual customer.'''
        while True:
            spotNum = int(input("\nEnter your parking spot number (type '9' to quit): "))
            if spotNum == 9:
                print("Thank you, have a nice day.")
                exit() # Exit program when done testing
            if spotNum <= 0 or spotNum > 3:
                print("Invalid input (parking spot doesn't exist)")
            elif self.parkingSpot[spotNum]["open"] == True:
                print(f"Parking spot number {spotNum} is not in use.", end=" ")
            else:
                break
        return spotNum

    def parkingPayment(self, spotNum, exitPay=False):
        '''This function closes out payment with customer and resets parking spot availability.'''
        # Cost of parking set to $5
        balance = 5 
        
        # If paid, allow exit. If not, process payment.
        if self.parkingSpot[spotNum]["paid"] == True:
            self.resetSpot(spotNum)
        else:
            while self.parkingSpot[spotNum]["paid"] == False:
                payment = round(float(input(f"Your balance is ${balance}. Enter payment: ")), 2)
                balance -= payment
                round(float(balance), 2)
                if balance > 0:
                    print(f"Your remaining balance is ${balance}.")
                elif balance < 0:
                    print("Invald payment amount (overpayment)")
                    balance += payment
                elif balance == 0 and exitPay == True:
                    print("Payment complete.", end=" ")
                    self.resetSpot(spotNum)
                    self.tickets += 1
                    break
                else: 
                    print("Payment complete. You have 15 minutes to leave.")
                    self.parkingSpot[spotNum]["paid"] = True

    def leaveGarage(self):
        '''Customer is leaving garage. Process payment and/or exit.'''
        wherePay = int(input('\nAre you paying at the kiosk or the gate?\n1 - Kiosk\n2 - Gate\n3 - Already Paid\nEnter selection here: '))
        if wherePay == 1 or wherePay == 3:
            self.parkingPayment(self.getSpot(), False)
        elif wherePay == 2:
            self.parkingPayment(self.getSpot(), True)


    def resetSpot(self, spotNum):
        '''Resets all the values in ea dictionary item.'''
        self.parkingSpot[spotNum]["open"] = True
        self.parkingSpot[spotNum]["paid"] = False
        self.parkingSpot[spotNum]["exitPay"] = True
        print("Thank you, have a nice day.\n")


    def runner(self):
        '''Runner func. NOTE: Program can be exited in line 38.'''
        print('Welcome to the parking garage.')
        # Test taking all the tickets. Also test taking more than available tickets.
        for i in range(4):
            self.takeTicket()

        # Test payment:
        while True:
            self.leaveGarage()
            quit = input('Continue? Y/N ')
            if quit.lower() == 'n':
                break

            

# Test class.
iParked = Garage()
iParked.runner()

