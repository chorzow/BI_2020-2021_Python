a, operation, b = float(input()), input(), float(input())
if (operation == '/' or operation == 'mod' or operation == 'div') and b == 0:
    output = "Division by zero!"
elif operation == '+':
    output = a + b
elif operation == '-':
    output = a - b
elif operation == '/':
    output = a / b
elif operation == '*':
    output = a * b
elif operation == 'mod':
    output = a % b
elif operation == 'pow':
    output = a ** b
elif operation == 'div':
    output = a // b
else:
    output = "Undefined operation!"
print(output)
