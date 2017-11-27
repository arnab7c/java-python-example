""""
Problem Title :: Fibonacci Sequence
Problem Description :: Enter a number and have the program generate the Fibonacci sequence to that number or to the Nth number.
"""""

v_number = input("Enter number ::")
v_fib_num = 0
v_init_num=1
counter = 1

print("Input number is " + v_number)

if v_number.isdigit() is False:
    print("Input has to be integer")
    exit(1)


while counter <= int(v_number):
    v_prev_num = v_init_num
    v_init_num = v_fib_num
    v_fib_num = v_prev_num + v_init_num
    print("{0}+{1}={2}".format(str(v_prev_num), str(v_init_num), str(v_fib_num)))
    counter += 1

