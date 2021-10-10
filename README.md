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
SELECT id 
FROM users

SELECT user_id
FROM departments
WHERE department_id = 1

INNER JOIN id AND user_id
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
select * from salary
group by salary
order by salary desc limit 1,1;

select id, MAX(salary) as salary
from salary
where salary in 
(select salary from salary MINUS select MAX(salary)
 from salary);
 
 select id, max(salary)as salary
 from salary
 where salary <> (select max(salary)
 from salary);
 
SELECT id, salary
FROM salary A
WHERE 2 = (SELECT count(n-2) 
             FROM salary B 
             WHERE B.salary>A.salary)
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

def count_connections2(list1, list2) -> int:
    count, start, finish = 0, 0, 0

    start = time.time()
    for i in list1:
        for j in list2:
            if i == j:
                count += 1
    time.sleep(1)
    finish = time.time()

    print('original: ', finish - start)
    return count


def perfect_counter2(list1: list, list2: list) -> int:
    count, start, finish = 0, 0, 0

    start = time.time()
    list1 = set(list1)
    list2 = set(list2)
    count = len(list1.intersection(list2))
    time.sleep(1)
    finish = time.time()

    print('my variant: ', finish - start)
    return count


def count_connections(list1, list2):
    count, start, finish = 0, 0, 0

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
    count, start, finish = 0, 0, 0

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
    list2 = sort(list2)
    count, r = 0, len(list2)-1
    start = datetime.datetime.now()
    for i in list1:
        count += binarySearch(list2,0, r, i)
    time.sleep(1)
    finish = datetime.datetime.now()
    print('my_new: ', (finish-start).microseconds)
    return count



if __name__ == '__main__':
    list1 = [1, 3, 5, 2, 4, 7, 11000, 1242143, 214124, 1241, 214214, 125354, 15234, 15243, 125434154, 15423, 5123,
             51243234, 5124312, 521434, 154233254623, 3246356345]
    list2 = [10, 3, 7, 8, 0, 5, 1254326, 4563476, 7684586, 3254452, 1525422431, 32454236, 546437, 265342, 51435151,
             6315, 2456223, 2412425, 3425, 1243, 353526]
    count_connections(list1, list2)
    perfect_counter(list1, list2)
    my2(list1, list2)   
```

It is good for small lists

2. Given a string `s`, find the length of the longest substring without repeating characters. Analyze your solution and please provide Space and Time complexities.
## Linux Shell
