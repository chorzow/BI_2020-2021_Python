a, operation, b = float(input()), input(), float(input())
if (operation == '/' or operation == '%' or operation == '//') and b == 0:
    output = "Division by zero!"
elif operation == '+':
    output = a + b
elif operation == '-':
    output = a - b
elif operation == '/':
    output = a / b
elif operation == '*':
    output = a * b
elif operation == '%':
    output = a % b
elif operation == '**':
    output = a ** b
elif operation == '//':
    output = a // b
else:
    output = "Undefined operation!"
print(output)
