num1, operation, num2 = float(input("Enter a number: ")), input("Enter an operand: "), float(input("Enter a number: "))
if (operation == '/' or operation == '%' or operation == '//') and num2 == 0:
    output = "Division by zero!"
elif operation == '+':
    output = num1 + num2
elif operation == '-':
    output = num1 - num2
elif operation == '/':
    output = num1 / num2
elif operation == '*':
    output = num1 * num2
elif operation == '%':
    output = num1 % num2
elif operation == '**':
    output = num1 ** num2
elif operation == '//':
    output = num1 // num2
else:
    output = "Undefined operand!"
print(output)
