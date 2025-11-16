#1
def Q1():
    name = input("Enter your name : ")
    age = input("Enter your age : ")
    print(f"Hello {name} you are {age} old." )

#2, 3, 4
def Q2():
    firstNumber = int(input("Enter first number: "))
    secondNumber = int(input("Enter second number: "))
    Operation = input("Enter desired Operation (+,-,/,*, E): ")
    match Operation:
        case "+":
            result = firstNumber + secondNumber
        case "-":
            result = firstNumber - secondNumber
        case "/":
            result = firstNumber/secondNumber
        case "*":
            result = firstNumber * secondNumber
        case "E":
            result = (float(firstNumber) + float(secondNumber)) / 2
        case _:
            print("Uknown Operation. Use +, -, * or /, E")
    print(result)

#5
def Q5():
    x = 10+3*2**2
    print(x)

###Explanation
#Exponentiation (` `)**: 2**2 is evaluated first, resulting in 4
#Multiplication (*): 3 * 4 is evaluated next, resulting in 12.
#Addition (+): 10 + 12 is evaluated last, resulting in 22

#6
def Q6():
    x = 10
    y= 112
    print(f"Orignal x:{x} y:{y}")
    t = x
    x=y
    y=t
    print(f"swapped x:{x} y:{y}")

#7
def Q7():
    temp_celsius = input("Enter temperature in Celsius: ")
    temp_fahrenheit = (float(temp_celsius) * (9/5))+32
    print(f"The tempurature {temp_celsius}C in Fahrenheit is {temp_fahrenheit}F")

#8
def Q8():
    radius= input("Enter radius: ")
    print(f"The area of the circle with radius {radius} is {3.144 * (float(radius)**2)}")

#9
def Q9():
    principal = float(input("Enter Principal amount: "))
    rate = float(input("Enter rate of interest: "))
    time = float(input("Enter duration of loan: "))
    si = (principal*rate* time)/100
    print(f"the simple interest for the above loan is {si}")

#10
def Q10():
    from fractions import Fraction
    import math
    value = float(input("Enter a decimal number: "))

    value_parts = str(value).split('.')
    fractional_float, integer_float = math.modf(value)
    integeral_float, fraction_float = divmod(value, 1)

    print(f"Using String Splitter\n - integral part : {value_parts[0]} \nfractional part : {value_parts[1]}")
    print(f"Using Math modf()\n - integral part : {integer_float} \nfractional part : {fractional_float}")
    print(f"Using math divmod()\n - integral part : {integeral_float} \nfractional part : {round(fraction_float,3)})")
q = 1
while q !=0:
    q = int(input("Enter Q number 1-10 (0 to exit): "))
    match q:
        case 0:
            break
        case 1:
            Q1()
        case 2,3,4:
            if(q==2):
                Q2()
            elif(q==3):
                Q3()
            elif(q==4):
                Q4()
        case 5:
            Q5()
        case 6:
            Q6()
        case 7:
            Q7()
        case 8:
            Q8()        
        case 9:
            Q9()
        case 10:
            Q10()
        case _: 
            print("Invalid Q number.Enter 0 to exit.")
