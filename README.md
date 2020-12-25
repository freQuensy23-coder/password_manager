# Password maneger
Symple console password maneger using MySQL Database

# Installing 
```
pip install-r requirements
Buy server with mysql database
python3 pm.py
```

### Add password
```
Welcome back Alex
What should we do?
+-----+-------------------------+
| key |          action         |
+-----+-------------------------+
|  1  |     Add new password    |
|  2  |   Search for password   |
|  3  |     Import from csv     |
|  4  |      Export to csv      |
|  5  | Show obsolete passwords |
|  6  |    Get password by id   |
|  7  |   Print all passwords   |
+-----+-------------------------+

1
Login: freQuensy23-coder
Password (leave empty for autogen): 
Description: github work accaunt
url: github.com
TTL (in month):12
```

### Print all pass in db
```
+----+-------------------+-------------+-------------------------+------------+
| id |        name       |   password  |       description       |    url     |
+----+-------------------+-------------+-------------------------+------------+
| 7  | freQuensy23-coder | obdezJKHBRW |   github work accaunt   | github.com |
+----+-------------------+-------------+-------------------------+------------+
```

### Print all "old" password
```
+----+------+----------+-------------+---------+------+
| id | name | password | description |   url   | logo |  
+----+------+----------+-------------+---------+------+
| 4  | haus |   123456 |  habe forum | habr.ru | None | 
+----+------+----------+-------------+---------+------+
```
