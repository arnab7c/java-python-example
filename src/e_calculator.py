""""
Problem Title :: Find e to the Nth Digit 
Problem Description :: Enter a number and have the program generate e up to that many decimal places. 
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

v_num=int(v_number)

v_val = round(pow((1 + 1 / (v_num)),v_num),v_num)

print ("Pi value till %s digit is %s" %(v_number, v_val) )
