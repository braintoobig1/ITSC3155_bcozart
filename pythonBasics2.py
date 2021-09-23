# Python Activity
#
# Fill in the code for the functions below.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code. Make sure to add what is going to be returned.


# Part A. count_threes
# Define a function count_threes(n) that takes an int and
# returns the number of multiples of 3 in the range from 0
# to n (including n).

def count_threes(n):
 answer=0
  
 if n<=0:
  answer= 0
 if n<0:
  answer= 0
 if n>2:
  answer= n//3
 
 
 return answer
  





# Part B. longest_consecutive_repeating_char
# Define a function longest_consecutive_repeating_char(s) that takes
# a string s and returns the character that has the longest consecutive repeat.
def longest_consecutive_repeating_char(s):
  # YOUR CODE HERE
  j = 0
  x = 0
  dumb = 1
  count = 0
  contest = 0
  store = ""
  multi = 2
  for i in s:
    
    while j < len(s):
      
      if x == len(s):
        break
      if i == s[x]:
        count = count + 1*multi
        multi = multi + 1
      else:
        multi = 1
        count = count - 1
      j = j + 1
      x = x + 1
    if count > contest:
     contest = count
     store = i
    
    j=0
    x=0+dumb
    dumb=dumb+1
    count=0
  return store
     
  

    


  

  

  return 


# Part C. is_palindrome
# Define a function is_palindrome(s) that takes a string s
# and returns whether or not that string is a palindrome.
# A palindrome is a string that reads the same backwards and
# forwards. Treat capital letters the same as lowercase ones
# and ignore spaces (i.e. case insensitive).
def is_palindrome(s):
  # YOUR CODE HERE
  s=s.lower()
  s=s.replace(" ", "")
  j=len(s)
  answer = True
  reverse=""
  for i in s:
    reverse=reverse+s[j-1]
    j=j-1

  if s == reverse:
    answer = True
  else:
    answer = False

  
  
  return answer
