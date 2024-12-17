class Employee:
    def __init__(self, employee_id, name, address, contact_details, employment_type):
        self.employee_id = employee_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.employment_type = employment_type

    def update_record(self, attribute, new_value):
        if attribute == 'name':
            self.name = new_value
        elif attribute == 'address':
            self.address = new_value
        elif attribute == 'contact_details':
            self.contact_details = new_value
        elif attribute == 'employment_type':
            self.employment_type = new_value

    def delete_record(self):
        pass

class FullTimeEmployee(Employee):
    def __init__(self, employee_id, name, address, contact_details, annual_salary):
        super().__init__(employee_id, name, address, contact_details, 'Full-time')
        self.annual_salary = annual_salary 

    def compute_monthly_salary(self):
        return self.annual_salary / 12


class PartTimeEmployee(Employee):
    def __init__(self, employee_id, name, address, contact_details, hourly_rate, hours_worked_per_month):
        super().__init__(employee_id, name, address, contact_details, 'Part-time')
        self.hourly_rate = hourly_rate 
        self.hours_worked_per_month = hours_worked_per_month

    def compute_monthly_salary(self):
        return self.hourly_rate * self.hours_worked_per_month


class TaxCalculator: 
    def __init__(self, tax_brackets, deductions):
        self.tax_brackets = tax_brackets
        self.deductions = deductions

    def compute_tax(self, employee):
        if isinstance(employee, FullTimeEmployee):
            tax_rate = 0.15  
        elif isinstance(employee, PartTimeEmployee):
            tax_rate = 0.20 

        taxable_income = employee.compute_monthly_salary() * 12
        tax = taxable_income * tax_rate

        for bracket, rate in self.tax_brackets.items():
            if taxable_income > bracket:
                tax += (taxable_income - bracket) * rate

        tax = self.apply_deductions(tax)
        return tax

    def apply_deductions(self, tax_amount):
        for deduction in self.deductions.values():
            tax_amount -= deduction
        return max(0, tax_amount)


def load_employees():
    try:
        with open("employees.txt", "r") as file:
            lines = file.readlines()
            employees = []
            for line in lines:
                data = line.strip().split(",")
                employee_id, name, address, contact_details, employment_type = data[:5]
                if employment_type == 'Full-time':
                    annual_salary = float(data[5])
                    employee = FullTimeEmployee(employee_id, name, address, contact_details, annual_salary)
                elif employment_type == 'Part-time':
                    hourly_rate = float(data[5])
                    hours_worked_per_month = float(data[6])
                    employee = PartTimeEmployee(employee_id, name, address, contact_details, hourly_rate, hours_worked_per_month)
                employees.append(employee)
            return employees
    except FileNotFoundError:
        return []

def save_employees(employees):
    with open("employees.txt", "w") as file:
        for employee in employees:
            if isinstance(employee, FullTimeEmployee):
                file.write(f"{employee.employee_id},{employee.name},{employee.address},{employee.contact_details},{employee.employment_type},{employee.annual_salary}\n")
            elif isinstance(employee, PartTimeEmployee):
                file.write(f"{employee.employee_id},{employee.name},{employee.address},{employee.contact_details},{employee.employment_type},{employee.hourly_rate},{employee.hours_worked_per_month}\n")
def add_employee(employees, employee):
    employees.append(employee)
    save_employees(employees) 
    print("Employee Added Successfully!")


def update_employee_record(employees, employee_id, attribute, new_value): 
    for employee in employees:
        if employee.employee_id == employee_id:
            employee.update_record(attribute, new_value)
            print("Employee Record Updated Successfully!")
            return
    print("Employee ID not found.")


def delete_employee_record(employees, employee_id): 
    for employee in employees:
        if employee.employee_id == employee_id:
            employees.remove(employee)
            print("Employee Record Deleted Successfully!")
            return
    print("Employee ID not found.")


def compute_salary(employee_id, employees): 
    for employee in employees:
        if employee.employee_id == employee_id:
            monthly_salary = employee.compute_monthly_salary()
            print(f"Monthly Salary: ${monthly_salary}")
            return
    print("Employee ID not found.")


def compute_tax(employee_id, employees, tax_calculator):
    for employee in employees:
        if employee.employee_id == employee_id:
            tax_amount = tax_calculator.compute_tax(employee)
            print(f"Tax Amount: ${tax_amount}")
            return
    print("Employee ID not found.")


def view_employee_information(employee_id, employees):
    for employee in employees:
        if employee.employee_id == employee_id:
            print("Employee Information:")
            print(f"ID: {employee.employee_id}")
            print(f"Name: {employee.name}")
            print(f"Address: {employee.address}")
            print(f"Contact Details: {employee.contact_details}")
            print(f"Employment Type: {employee.employment_type}")
            compute_salary(employee_id, employees)
            return
    print("Employee ID not found.")


def generate_reports(employees, tax_calculator):
    employees = load_employees()
    print("Generate Reports")
    print("1. Employee List")
    print("2. Tax Report")

    option = input("Enter an option: ")

    if option == '1':
        print("Employee List:")
        for employee in employees:
            print(f"{employee.name} ({employee.employee_id}) - {employee.employment_type}")
    elif option == '2':
        print("Tax Report:")
        for employee in employees:
            tax_amount = tax_calculator.compute_tax(employee)
            print(f"{employee.name} ({employee.employee_id}) - Tax Amount: ${tax_amount}")
    else:
        print("Invalid option.")

employees = load_employees()
tax_calculator = TaxCalculator(tax_brackets={}, deductions={})

while True:
    print("\nPayroll and HRIS System")
    print("1. Add New Employee")
    print("2. Update Employee Record")
    print("3. Delete Employee Record")
    print("4. Compute Salary")
    print("5. Compute Taxes")
    print("6. View Employee Information")
    print("7. Generate Reports")
    print("8. Exit")

    option = input("Please select an option (1-8): ")

    if option == '1':
        employee_id = input("Enter Employee ID: ")
        name = input("Name: ")
        address = input("Address: ")
        contact_details = input("Contact Details: ")
        employment_type = input("Employment Type (Full-time/Part-time): ")
        if employment_type.lower() == 'full-time':
            annual_salary = float(input("Annual Salary: "))
            employee = FullTimeEmployee(employee_id, name, address, contact_details, annual_salary)
        elif employment_type.lower() == 'part-time':
            hourly_rate = float(input("Hourly Rate: "))
            hours_worked_per_month = float(input("Hours Worked Per Month: "))
            employee = PartTimeEmployee(employee_id, name, address, contact_details, hourly_rate,
                                         hours_worked_per_month)
        else:
            print("Invalid employment type.")
            continue
        add_employee(employees, employee)

    elif option == '2':
        employee_id = input("Enter Employee ID: ")
        attribute = input(
            "Choose Attribute to Update:\n1. Name\n2. Address\n3. Contact Details\n4. Employment Type\nEnter Option: ")
        new_value = input("Enter New Value: ")
        update_employee_record(employees, employee_id, attribute, new_value)

    elif option == '3':
        employee_id = input("Enter Employee ID: ")
        delete_employee_record(employees, employee_id)

    elif option == '4':
        employee_id = input("Enter Employee ID: ")
        compute_salary(employee_id, employees)

    elif option == '5':
        employee_id = input("Enter Employee ID: ")
        compute_tax(employee_id, employees, tax_calculator)

    elif option == '6':
        employee_id = input("Enter Employee ID: ")
        view_employee_information(employee_id, employees)

    elif option == '7':
        generate_reports(employees, tax_calculator)

    elif option == '8':
        print("Exiting Payroll and HRIS System. Goodbye!")
        break

    else:
        print("Invalid option. Please choose a number between 1 and 8.")

