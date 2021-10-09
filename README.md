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
+----+-----------+-----------
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
import time

def count_connections(list1: list, list2: list) -> int:
  count, start, finish = 0, 0, 0
    
  start = time.time()
  for i in list1:
    for j in list2:
      if i == j:
        count += 1
  finish = time.time()
  
  print('original: ', finish-start) 
  return count

def perfect_counter(list1: list, list2: list) -> int:
    count, start, finish = 0, 0, 0
    
    start = time.time()
    list1 = set(list1)
    list2 = set(list2)
    count = len(list1.intersection(list2))
    finish = time.time()
    
    print('my variant: ', finish-start)
    return count
    
list1 = [1, 3, 5, 2, 4, 7]
list2 = [10, 3, 7, 8, 0, 5]
count_connections(list1, list2)
perfect_counter(list1, list2)   
```
It is good for small lists

2. Given a string `s`, find the length of the longest substring without repeating characters. Analyze your solution and please provide Space and Time complexities.
## Linux Shell
