import math
import locale
import os.path

locale.setlocale(locale.LC_ALL, '')

def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Error: Please enter a positive value.")
            else:
                return value
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Error: Please enter a positive integer.")
            else:
                return value
        except ValueError:
            print("Error: Invalid input. Please enter an integer.")

def save_result_to_file(filename, result):
    with open(filename, "a") as file:
        file.write(result + "\n\n")
    return filename

def calculate_stock_return(initial_price, number_of_shares, selling_price, dividends):
    total_investment = initial_price * number_of_shares
    total_return = (selling_price * number_of_shares) + dividends
    return_on_investment = ((total_return - total_investment) / total_investment) * 100
    return total_investment, total_return, return_on_investment

def calculate_bond_return(principal_amount, coupon_rate, years_to_maturity, market_interest_rate):
    present_value = principal_amount
    total_return = present_value * (1 + (coupon_rate / 100)) ** years_to_maturity
    return_on_investment = ((total_return - present_value) / present_value) * 100
    return present_value, total_return, return_on_investment

def calculate_mutual_fund_return(initial_investment, annual_contribution, years_investing, interest_rate):
    total_investment = initial_investment + (annual_contribution * years_investing)
    total_return = total_investment * (1 + (interest_rate / 100)) ** years_investing
    return_on_investment = ((total_return - total_investment) / total_investment) * 100
    return total_investment, total_return, return_on_investment

def calculate_mortgage(monthly_interest_percentage, loan_amount, years_repaying):
    monthly_interest = monthly_interest_percentage / 100 / 12  # Divide by 100 and 12 to get the monthly interest rate
    num_payments = years_repaying * 12
    monthly_repayment = loan_amount * (monthly_interest * math.pow(1 + monthly_interest, num_payments)) / (math.pow(1 + monthly_interest, num_payments) - 1)
    return monthly_repayment

def save_amortization_schedule(filename, house_value, deposit, months_repaying, formatted_monthly_repayment, amortization_schedule):
    with open(filename, "w") as file:
        file.write(f"Your mortgage for {locale.currency(house_value, grouping=True)}, with a deposit of {locale.currency(deposit, grouping=True)} will be repaid over {months_repaying} months, at {formatted_monthly_repayment} per month.\n\n")
        file.write("Month\tPrincipal Payment\tInterest Payment\tRemaining Balance\n")
        for month, principal_payment, interest_payment, remaining_balance in amortization_schedule:
            file.write(f"{month}\t{locale.currency(principal_payment, grouping=True)}\t\t\t{locale.currency(interest_payment, grouping=True)}\t\t{locale.currency(remaining_balance, grouping=True)}\n")

    print(f"\nAmortization schedule saved to {filename}.")

def get_compound_frequency_factor(frequency):
    if frequency == 'annually':
        return 1
    elif frequency == 'semi-annually':
        return 2
    elif frequency == 'quarterly':
        return 4
    elif frequency == 'monthly':
        return 12
    elif frequency == 'weekly':
        return 52
    elif frequency == 'daily':
        return 365

def handle_inner_menu():
    while True:
        print("\n1. Return to the main menu")
        print("2. Exit\n")

        inner_choice = input("Please enter your choice (1 or 2): ")

        if inner_choice == "1":
            return # This will go back to the main menu
        elif inner_choice == "2":
            print("Thank you for using the finance calculator. Goodbye!")
            exit() # This will exit the program
        else:
            print("Invalid choice. Please select a valid option.")

while True:
    print("\n----- Finance Calculator -----\n"
          "\n1. Investment  - to calculate the amount of interest you'll earn on your investment\n"
          "2. Stock       - to calculate the return on a stock investment\n"
          "3. Bond        - to calculate the reurn on a bond investment\n"
          "4. Mutual Fund - to calculate the return on a mutual fund investment\n"
          "5. Mortgage    - to calculate the amount you'll have to pay on a home loan\n"
          "6. Exit\n")
    
    choice = input("Please enter your choice (1-6): ")

    if choice == "6":
        print("Thank you for using the finance calculator. Goodbye!")
        break

    elif choice == "1":
        deposit = get_float_input("Please enter the deposit amount: ")
        interest_rate = get_float_input("Please enter the interest rate as a percentage: ")
        years_investing = get_int_input("Please enter the number of years you plan on investing for: ")

        valid_interest_type = False
        while not valid_interest_type:
            interest = input("Please enter the interest type (simple/compound): ").lower()

            if interest == 'simple':
                total_return = deposit * (1 + (interest_rate / 100) * years_investing)
                return_on_investment = ((total_return - deposit) / deposit) * 100
                result = "Deposit: {}\nInterest Rate: {:.2f}%\nYears Investing: {}\nInterest Type: {}\nTotal Amount: {}\nTotal Profit: {}".format(
                    locale.currency(deposit, grouping=True),
                    interest_rate,
                    years_investing,
                    interest.capitalize(),
                    locale.currency(total_return, grouping=True),
                    locale.currency(total_return - deposit, grouping=True)
                )
            elif interest == 'compound':
                while True:
                    frequency = input("Please enter the compounding frequency (annually/semi-annually/quarterly/monthly/weekly/daily): ").lower()
                    compound_frequency_factor = get_compound_frequency_factor(frequency)
                    if compound_frequency_factor is not None:
                        break
                    else:
                        print("Error: Invalid compounding frequency. Please try again.")

                total_return = deposit * (1 + (interest_rate / 100) / compound_frequency_factor) ** (
                            compound_frequency_factor * years_investing)
                return_on_investment = ((total_return - deposit) / deposit) * 100
                result = "Deposit: {}\nInterest Rate: {:.2f}%\nYears Investing: {}\nInterest Type: {}\nCompound Frequency: {}\nTotal Amount: {}\nTotal Profit: {}".format(
                    locale.currency(deposit, grouping=True),
                    interest_rate,
                    years_investing,
                    interest.capitalize(),
                    frequency.capitalize(),
                    locale.currency(total_return, grouping=True),
                    locale.currency(total_return - deposit, grouping=True)
                )
            else:
                print("Error: Invalid interest type. Please try again.")
                continue

            filename = save_result_to_file("investment_results.txt", result)
            print("")
            print(result)
            print(f"\nSuccess! Calculation saved to {filename}")

            break

        handle_inner_menu()

    elif choice == "2":
        initial_price = get_float_input("Please enter the initial price per share: ")
        number_of_shares = get_int_input("Please enter the number of shares purchased: ")
        selling_price = get_float_input("Please enter the selling price per share: ")
        dividends = get_float_input("Please enter the total dividends received: ")

        total_investment, total_return, return_on_investment = calculate_stock_return(initial_price, number_of_shares, selling_price, dividends)

        result = "Initial Price per Share: {}\nNumber of Shares Purchased: {}\nSelling Price per Share: {}\nTotal Dividends Received: {}\nTotal Investment: {}\nTotal Return: {}\nReturn on Investment: {:.2f}%".format(
            locale.currency(initial_price, grouping=True),
            number_of_shares,
            locale.currency(selling_price, grouping=True),
            locale.currency(dividends, grouping=True),
            locale.currency(total_investment, grouping=True),
            locale.currency(total_return, grouping=True),
            return_on_investment
        )

        filename = save_result_to_file("stock_investment_results.txt", result)
        print("")
        print(result)
        print(f"\nSuccess! Calculation saved to {filename}")

        handle_inner_menu()

    elif choice == "3":
        principal_amount = get_float_input("Please enter the principal amount: ")
        coupon_rate = get_float_input("Please enter the coupon rate as a percentage: ")
        years_to_maturity = get_int_input("Please enter the number of years to maturity: ")
        market_interest_rate = get_float_input("Please enter the market interest rate as a percentage: ")

        present_value, total_return, return_on_investment = calculate_bond_return(principal_amount, coupon_rate, years_to_maturity, market_interest_rate)

        result = "Principal Amount: {}\nCoupon Rate: {:.2f}%\nYears to Maturity: {}\nMarket Interest Rate: {:.2f}%\nPresent Value: {}\nTotal Return: {}\nReturn on Investment: {:.2f}%".format(
            locale.currency(principal_amount, grouping=True),
            coupon_rate,
            years_to_maturity,
            market_interest_rate,
            locale.currency(present_value, grouping=True),
            locale.currency(total_return, grouping=True),
            return_on_investment
        )

        filename = save_result_to_file("bond_investment_results.txt", result)
        print("")
        print(result)
        print(f"\nSuccess! Calculation saved to {filename}")

        handle_inner_menu()

    elif choice == "4":
        initial_investment = get_float_input("Please enter the initial investment amount: ")
        annual_contribution = get_float_input("Please enter the annual contribution amount: ")
        years_investing = get_int_input("Please enter the number of years you plan on investing for: ")
        interest_rate = get_float_input("Please enter the interest rate as a percentage: ")

        total_investment, total_return, return_on_investment = calculate_mutual_fund_return(initial_investment, annual_contribution, years_investing, interest_rate)

        result = "Initial Investment: {}\nAnnual Contribution: {}\nYears Investing: {}\nInterest Rate: {:.2f}%\nTotal Investment: {}\nTotal Return: {}\nReturn on Investment: {:.2f}%".format(
            locale.currency(initial_investment, grouping=True),
            locale.currency(annual_contribution, grouping=True),
            years_investing,
            interest_rate,
            locale.currency(total_investment, grouping=True),
            locale.currency(total_return, grouping=True),
            return_on_investment
        )

        filename = save_result_to_file("mutual_fund_investment_results.txt", result)
        print("")
        print(result)
        print(f"\nSuccess! Calculation saved to {filename}")

        handle_inner_menu()
        

    elif choice == "5":
        house_value = get_float_input("Please enter the house value: ")
        deposit = get_float_input("Please enter the deposit amount: ")
        loan_amount = house_value - deposit
        monthly_interest_percentage = get_float_input("Please enter the monthly interest rate as a percentage: ")
        years_repaying = get_int_input("Please enter the number of years you plan on repaying the mortgage: ")

        monthly_repayment = calculate_mortgage(monthly_interest_percentage, loan_amount, years_repaying)

        result = "House Value: {}\nDeposit: {}\nLoan Amount: {}\nMonthly Interest Rate: {:.2f}%\nYears Repaying: {}\nMonthly Repayment: {}".format(
            locale.currency(house_value, grouping=True),
            locale.currency(deposit, grouping=True),
            locale.currency(loan_amount, grouping=True),
            monthly_interest_percentage,
            years_repaying,
            locale.currency(monthly_repayment, grouping=True)
        )

        filename = save_result_to_file("mortgage_results.txt", result)
        print("")
        print(result)
        print(f"\nSuccess! Calculation saved to {filename}")

        generate_schedule = input("\nWould you like to generate an amortization schedule? (yes/no): ").lower()
        while generate_schedule not in ["yes", "no"]:
            generate_schedule = input("Error, your input was invalid. Please enter either 'yes' or 'no': ").lower()

        if generate_schedule == "yes":
            principal = loan_amount
            remaining_balance = principal
            interest_rate_monthly = monthly_interest_percentage / 100 / 12

            amortization_schedule = []

            for month in range(1, years_repaying * 12 + 1):
                interest_payment = remaining_balance * interest_rate_monthly
                principal_payment = monthly_repayment - interest_payment
                remaining_balance -= principal_payment

                amortization_schedule.append((month, principal_payment, interest_payment, remaining_balance))

            while True:
                filename = input("Please enter the filename for the amortization schedule (without file extension): ")
                filename += ".txt"

                if not os.path.exists(filename):
                    break
                else:
                    print("Error: The file already exists. Please enter a different filename.")

            save_amortization_schedule(filename, house_value, deposit, years_repaying, monthly_repayment, amortization_schedule)

        else:
            print("Amortization schedule generation skipped.")

        handle_inner_menu()

    else:
        print("Invalid choice. Please select a valid option.")