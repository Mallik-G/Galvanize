SELECT COUNT(userid), date_part('day', tmstmp)
FROM registrations
GROUP BY date_part('day', tmstmp)
ORDER BY date_part('day', tmstmp);



SELECT COUNT(userid), EXTRACT(DOW FROM tmstmp) as DOW
FROM registrations
GROUP BY DOW
ORDER BY DOW;



SELECT logins.userid FROM logins
WHERE logins.tmstmp < '2014-08-14' and logins.tmstmp > '2014-08-06'
EXCEPT SELECT optout.userid FROM optout;



SELECT R1.userid, COUNT(R2.userid)
FROM registrations R1, registrations R2
WHERE date_part('day', R1.tmstmp) = date_part('day', R2.tmstmp)
GROUP BY R1.userid;


#test for above
SELECT R1.userid, R2.userid
FROM registrations R1, registrations R2
WHERE date_part('day', R1.tmstmp) = date_part('day', R2.tmstmp)
   and R1.userid = '27';


SELECT userid FROM logins
WHERE (SELECT COUNT(type) FROM logins WHERE type='web') <
      (SELECT COUNT(type) FROM logins WHERE type='mobile')

EXCEPT SELECT userid FROM test_group WHERE grp = 'CONTROL';

#include this for a test of redundancy
#ORDER BY userid;



CREATE TABLE temp1 as (
SELECT sender, recipient, COUNT(message)
FROM messages
GROUP BY sender, recipient
UNION SELECT recipient, sender, COUNT(message)
FROM messages
GROUP BY recipient, sender);

CREATE TABLE temp12 as (
SELECT sender, recipient
FROM (
    SELECT sender, recipient,
        rank() OVER (PARTITION BY recipient
                     ORDER BY sum(count)) as rank
    FROM (SELECT sender, recipient, COUNT(message)
          FROM messages
          GROUP BY sender, recipient
          UNION SELECT recipient, sender, COUNT(message)
          FROM messages
          GROUP BY recipient, sender) as alias2
    GROUP BY sender, recipient
  ) as alias
WHERE rank = 1
ORDER BY sender, recipient);




CREATE TABLE temp2 as (
SELECT sender, recipient, SUM(length(message)) as msg_sum
FROM messages
GROUP BY sender, recipient
UNION SELECT recipient, sender, SUM(length(message)) as msg_sum
FROM messages
GROUP BY recipient, sender);


CREATE TABLE temp13 as (
SELECT sender, recipient
FROM (
    SELECT sender, recipient,
        rank() OVER (PARTITION BY recipient
                     ORDER BY sum(msg_sum)) as rank
    FROM (SELECT sender, recipient, SUM(length(message)) as msg_sum
          FROM messages
          GROUP BY sender, recipient
          UNION SELECT recipient, sender, SUM(length(message)) as msg_sum
          FROM messages
          GROUP BY recipient, sender) as alias3
    GROUP BY sender, recipient
  ) as alias
WHERE rank = 1
ORDER BY sender, recipient);









SELECT temp12.*, temp13.*
FROM temp12
JOIN temp13
    ON temp13.sender = temp12.sender;
