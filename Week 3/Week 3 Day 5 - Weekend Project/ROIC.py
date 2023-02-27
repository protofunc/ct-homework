# ROI Calculator

class ROIC():
    def __init__(self):
        self.expenses = {}
        self.income = {}

    def quitQuery(self, flag):
        '''Ask if user wants to continue in existing loop'''
        if flag == 1:
            quit = input("Would you like to add more income streams? (Y/N): ")
        elif flag == 2:
            quit = input("Would you like to add more expenses? (Y/N): ")
        elif flag == 3:
            quit = input("Would you like to remove more income streams? (Y/N): ")
        elif flag == 4:
            quit = input("Would you like to remove more expenses? (Y/N): ")
        elif flag == 5:
            quit = input("Would you like to remove income streams? (Y/N): ")
        elif flag == 6:
            quit = input("Would you like to remove expenses? (Y/N): ")

        if quit.lower() == 'y':
            return False
        else:
            return True

    def addIncome(self):
        '''Add line items to the income dict'''
        quit = False
        while quit == False:
            new_category = input("Enter income category (rent, laundry, etc.): ")
            new_income = int(input("Enter monthly income amount: "))
            self.income[new_category.title()] = new_income
            quit = self.quitQuery(1)

    def addExpense(self):
        '''Add line items to the expense dict'''
        quit = False
        while quit == False:
            new_category = input("Enter expense category (utilities, mortgage, etc.): ")
            new_expense = int(input("Enter monthly expense amount: "))
            self.expenses[new_category.title()] = new_expense
            quit = self.quitQuery(2)

    def delIncome(self):
        '''Remove income streams from the income dict'''
        quit = False
        while quit == False:
            del_category = input("Enter income category you would like to remove: ")
            del self.income[del_category.title()]
            quit = self.quitQuery(3)

    def delExpense(self):
        '''Remove expenses from expense dict'''
        quit = False
        while quit == False:
            del_category = input("Enter expense category you would like to remove: ")
            del self.expenses[del_category.title()]
            quit = self.quitQuery(4)

    def getIncome(self):
        '''Display list of existing income categories'''
        print("\nIncome Streams:")
        for k,v in self.income.items():
            print(f"{k} - ${v}")
        print()

    def getExpense(self):
        '''Display list of existing expenses'''
        print("\nExpenses:")
        for k,v in self.expenses.items():
            print(f"{k} - ${v}")
        print()

    def calcROI(self):
        '''Calculate ROI'''
        # Total income and expense
        t_income = 0
        t_expense = 0
        for i in self.income.values():
            t_income += i
        for e in self.expenses.values():
            t_expense += e
        # Prompt user for total investment and run calculation on ROI
        t_investment = int(input("Enter the total investment amount put into this property: "))
        roi = round(((((t_income - t_expense) * 12) / t_investment)) * 100, 2)
        
        print(
            f'\nTotal Income: ${t_income}'
            f'\nTotal Expenses: ${t_expense}'
            f'\nTotal Investment: ${t_investment}'
            f'\nROI: {roi}%'
            )

    def runner(self):
        print("\nWelcome to the Return on Investment (ROI) Calculator\n***")
        self.addIncome()
        self.addExpense()
        self.getExpense()
        self.getIncome()
        if self.quitQuery(5) == False:
            self.delIncome()
            self.getIncome()
        if self.quitQuery(6) == False:
            self.delExpense()
            self.getExpense()
        self.calcROI()

# Test it bb
tester = ROIC()
tester.runner()