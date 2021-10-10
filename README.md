# This repository is for tasks that need to be done before the interview
In the internship folder you can find folders named as `level1`, `level2` and `level3`. In each folder I tried to accomplish the task outlined [here](https://github.com/provectus/internship/tree/main/dataeng). Task description, solution and faced problems are provided in each folder by README file.

Here I would like to show my solution of __Coding Tasks for Data Engineers__.

# Coding Tasks for Data Engineers
* [SQL](#sql)
* [Algorithms and Data Structures](#algorithms-and-data-structures)
* [Linux Shell](#linux-shell)

## SQL
1. Rewrite this SQL without subquery:
```
SELECT id
FROM users
WHERE id NOT IN (
	SELECT user_id
	FROM departments
	WHERE department_id = 1
);
```
My solution:
```
CREATE TABLE tbl AS
SELECT user_id
FROM departments
WHERE department_id = 1


SELECT id 
FROM users, tbl
where id = tbl.user_id
```
2. Write a SQL query to find all duplicate lastnames in a table named user
```sql
+----+-----------+----------+
| id | firstname | lastname |
+----+-----------+----------+
| 1  | Ivan      | Sidorov  |
| 2  | Alexandr  | Ivanov   |
| 3  | Petr      | Petrov   |
| 4  | Stepan    | Ivanov   |
+----+-----------+----------+
```
```
SELECT lastname, COUNT(lastname)
FROM user
GROUP BY lastname
HAVING COUNT(lastname) > 1
```
3. Write a SQL query to get a username from user table with the second highest salary from tables. Show the username and it's salary in the result.
```sql
+---------+--------+
| user_id | salary |
+----+--------+----+
| 1       | 1000   |
| 2       | 1100   |
| 3       | 900    |
| 4       | 1200   |
+---------+--------+
```
```sql
+---------+--------+
| id | username    |
+----+--------+----+
| 1  | Alex       |
| 2  | Maria      |
| 3  | Bob        |
| 4  | Sean       |
+---------+-------+
```
My solution:
```sql
select first_name, salary
from users, salaries
where users.id = salaries.id
group by users.id, salary
order by salary desc
limit 1
offset 1;
```

## Algorithms and Data Structures
1. Optimise execution time of this Python code snippet:
```
def count_connections(list1: list, list2: list) -> int:
  count = 0
  
  for i in list1:
    for j in list2:
      if i == j:
        count += 1
  
  return count
```
My solution:
```
import datetime, time

def count_connections(list1, list2):
    count = 0
    start = datetime.datetime.now()
    for i in list1:
        for j in list2:
            if i == j:
                count += 1
    time.sleep(1)
    finish = datetime.datetime.now()

    delta = finish - start
    print('original: ', delta.microseconds)
    return count

def perfect_counter(list1, list2):
    start = datetime.datetime.now()
    list1 = set(list1)
    list2 = set(list2)
    count = len(list1.intersection(list2))
    time.sleep(1)
    finish = datetime.datetime.now()

    print('my variant: ', (finish - start).microseconds)
    return count

def sort(array):
    less = []
    equal = []
    greater = []
    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)
        return sort(less)+equal+sort(greater)
    else:
        return array

def binarySearch(arr, l, r, x):
    if r >= l:
        mid = l + (r - l) // 2
        if arr[mid] == x:
            return 1
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        return 0

def my2(list1, list2):
    start = datetime.datetime.now()
    list2 = sort(list2)
    count, r = 0, len(list2)-1
    for i in list1:
        count += binarySearch(list2, 0, r, i)
    time.sleep(1)
    finish = datetime.datetime.now()
    print('my_new: ', (finish-start).microseconds)
    return count


if __name__ == '__main__':
    list1 = [1, 3, 5, 2, 4, 7, 11000, 1242143, 214124, 1241, 214214, 125354, 15234, 15243, 125434154, 15423, 5123,
             51243234, 5124312, 521434, 154233254623, 3246356345]
    list2 = [10, 3, 7, 8, 0, 5, 1254326, 4563476, 7684586, 3254452, 1525422431, 32454236, 546437, 265342, 51435151,
             6315, 2456223, 2412425, 3425, 1243, 353526]
    print(count_connections(list1, list2))
    time.sleep(2)
    print(perfect_counter(list1, list2))
    time.sleep(2)
    print(my2(list1, list2))
```
I obtained such results:
```
original:  10989
my variant:  3367
my_new:  15101
```
looks like variant with set intersections works fine, but I didn't use big list. I think for big lists variant with binary search will show better results. Shortly, how `my2` function works, it sorts one list with quicksort and then applies binary search for each value in unsorted list.

2. Given a string `s`, find the length of the longest substring without repeating characters. Analyze your solution and please provide Space and Time complexities.
```
string = list(input())
temp_string = []
sub_string = []

for i in string:
    if i in temp_string:
        if len(temp_string)>len(sub_string):
            sub_string = temp_string
            temp_string = []
            temp_string.append(i)
        else:
            temp_string = []
	    temp_string.append(i)
    else:
        temp_string.append(i)

print(len(sub_string))
```
This solution takes O(n) because converting input string to list of characters take max O(n), then we have a loop with 2 conditions. Taking to consideration 'aaaaa' and 'abdegsq' cases, we can find what they take same time. So, therefore this solution takes O(n).

3. Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.
Solution: (input should be provided in form: nums = [1,3,5,6], target = 5)
```
list = input().split(' ')
array = [int(i) for i in list[2][1:-2].split(',')]
target = int(list[5])

for i in range(len(array)):
    if target == array[i]:
        print(i)
        break
    elif target < array[i]:
        print(i)
        break
```
## Linux Shell
1. `netstat -aon | find ":443"`
then `netstat -aon | find ":80"`
2. create `pidp.sh` script (by cat for example:
```sh
#!/bin/bash

# reads the user input

echo "Enter the process PID: "
read pid
echo "here is the result: "
cat /proc/$pid/environ | tr '\0' '\n'
```
then run it:
`sh ./pidp.sh`

Another variant:
```
read -p "PID:" pid_val
cat /proc/$pid_val/environ
```
3. Solution:
`python3 my_program.py &`
then look to backround processes:
`jobs`
and choose\kill needed one by `kill %(interested_process)`
