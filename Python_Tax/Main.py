class Person():
    def __init__(self,first_name,last_name):
        self.first_name = first_name
        self.last_name = last_name

    def full_name(self):
        print(self.first_name + ' ' + self.last_name)

class Employee(Person):
    def __init__(self,first_name, last_name, basic_salary, deductions):
        Person.__init__(self, first_name, last_name)
        self.basic_salary = basic_salary
        self.deductions = deductions

    def calc_net_salary(self):
        if self.basic_salary <= 30000:
            net_salary = self.basic_salary - self.deductions
            print(net_salary)
        
        elif self.basic_salary >= 30001 and self.basic_salary <= 75000:
            tax_1 = 0
            tax_2 = (self.basic_salary - 30000) * 0.1
            total_tax = round(tax_1 + tax_2)
            net_salary = self.basic_salary - total_tax - self.deductions
            print(net_salary)

        elif self.basic_salary > 75000:
            tax_1 = 0
            tax_2 = (75000 - 30000) * 100
            tax_3 = (self.basic_salary - 75000) * 0.3
            total_tax = round(tax_1 + tax_2 + tax_3)
            net_salary = self.basic_salary - total_tax - self.deductions
            print(net_salary)


a = Employee('Sofia', 'Howard', 31000, 7500)
a.calc_net_salary()
a.full_name()
