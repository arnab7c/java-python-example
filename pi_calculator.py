"""""
Problem Title :: Find PI to the Nth Digit 
Problem Description :: Enter a number and have the program generate PI up to that many decimal places. 
Keep a limit to how far the program will go.
"""""

v_number = input("Enter number ::")


print("Input number is " + v_number)

if v_number.isdigit() is False:
    print("Input has to be integer")
    exit(1)

if int(v_number) > 15:
    print("Maximum float can be 15")
    v_number=15

v_val = round(22 / 7,int(v_number))

print ("Pi value till %s digit is %s" %(v_number, v_val) )
