import time
import os

def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Enter a number.")
       continue
    else:
       return userInput 
       break

def progress(total,goal):
  print(f"Total: {total} / {goal}")
  percent = round((total/goal)*100,1)
  print("▓" * int(int(percent)/10) + " " * (10-int(int(percent)/10)) + str(percent) + "%")
  
#MAIN PROGRAM STARTS HERE:
goal = inputNumber("Goal: ")
total = 0
start = time.time()


while total != goal:
  # Do this every time
  #os.system("clear")
  print("Rep Counter")
  progress(total, goal)
  # If reps is less than goal keep looping
  if total >= goal:
    break
  else:
    reps = inputNumber("Reps: ")
    total += reps
  # Show the duration at program end
  if total >= goal:
    end = time.time()
    print(time.strftime("%H:%M:%S", time.gmtime(end - start)))

# Print the last progress bar at 100% or more
if total <= goal:
  progress(total,goal)
