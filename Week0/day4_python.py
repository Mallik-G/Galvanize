import psycopg2
from datetime import datetime

conn = psycopg2.connect(dbname='socialmedia', user='postgres', host='/tmp')
c = conn.cursor()

today = '2014-08-14'

timestamp = datetime.strptime(today, '%Y-%m-%d').strftime('%Y%m%d')


#Create a table of users who have logged in at least one day of the past
#7 days... counting the number of days
c.execute(
    '''
    SELECT userid, COUNT(DISTINCT date_part('day', tmstmp)) AS cnt, timestamp %(timestamp)s AS date_7d
    INTO TEMPORARY TABLE logins_7d
    FROM logins
    WHERE logins.tmstmp > timestamp %(timestamp)s - interval '7 days'
    GROUP BY userid;
    ''', {'timestamp': timestamp}


)
conn.commit()


#Q1 Create a pipeline like the example above that has the userid, registration
#date and the last login date.
c.execute(
    '''
    SELECT logins.userid, registrations.tmstmp AS reg_date,
           MAX(logins.tmstmp) AS last_login
    INTO TEMPORARY TABLE last_login
    FROM logins
    JOIN registrations
        ON logins.userid = registrations.userid
    GROUP BY logins.userid, registrations.tmstmp;
    '''

)
conn.commit()

#Create a temp table of userids and registration times
#that we will join to the logins_7d table
c.execute(
    '''
    SELECT userid, tmstmp as reg_date
    INTO TEMPORARY TABLE reg_table
    FROM registrations;
    '''
    )
conn.commit()


#Create another temp table that now has reg_date, last login and the count
#of the number of days in the past week a user has logged in
c.execute(
    '''
    SELECT reg.userid, reg.reg_date, last_login.last_login,
           logins_7d.cnt as logins_7d
    INTO TEMPORARY TABLE logins_prev7d
    FROM reg_table reg
    LEFT JOIN logins_7d
        ON reg.userid=logins_7d.userid
    LEFT JOIN last_login
        ON last_login.userid = reg.userid;
    '''
)
conn.commit()



#Create yet another temp table that includes the number of times a user has
#logged in using mobile

c.execute(
    '''
    SELECT userid, COUNT(DISTINCT date_part('day', tmstmp)) AS cnt, timestamp %(timestamp)s AS date_7d
    INTO TEMPORARY TABLE logins_7d_mobile
    FROM logins
    WHERE logins.tmstmp > timestamp %(timestamp)s - interval '7 days' and
        type='mobile'
    GROUP BY userid;
    ''', {'timestamp': timestamp}
)
conn.commit()




#Create again a temp table that includes the number of times a user has
#logged in using web


c.execute(
    '''
    SELECT userid, COUNT(DISTINCT date_part('day', tmstmp)) AS cnt, timestamp %(timestamp)s AS date_7d
    INTO TEMPORARY TABLE logins_7d_web
    FROM logins
    WHERE logins.tmstmp > timestamp %(timestamp)s - interval '7 days' and
        type='web'
    GROUP BY userid;
    ''', {'timestamp': timestamp}
)
conn.commit()




#Create a table of all users with 0 for not optout and 1 for optout
c.execute(
    '''
    SELECT reg.userid, COUNT(optout.userid) as cnt
    INTO TEMPORARY TABLE optout_total_users
    FROM reg_table reg
    LEFT JOIN optout
        ON reg.userid = optout.userid
    GROUP BY reg.userid;
    '''
)
conn.commit()


#Final grouping - create the user table pulling all the data together:
#userid, registration date, last login, logins over the past 7 days (count of
#days), web/mobile logins over past 7 days (count of days), opt out (0 for no,
#1 for yes)

c.execute(
    '''
    CREATE TABLE users_20140814 AS
    SELECT reg.userid, reg.reg_date, last_login.last_login,
           logins_7d.cnt as logins_7d, logins_7d_mobile.cnt as mobile_logins,
           logins_7d_web.cnt as web_logins, optout_total_users.cnt as optout
    FROM reg_table reg
    LEFT JOIN logins_7d
        ON reg.userid=logins_7d.userid
    LEFT JOIN last_login
        ON last_login.userid = reg.userid
    LEFT JOIN logins_7d_mobile
        ON logins_7d_mobile.userid = reg.userid
    LEFT JOIN logins_7d_web
        ON logins_7d_web.userid = reg.userid
    LEFT JOIN optout_total_users
        ON optout_total_users.userid = reg.userid;
    '''
)
conn.commit()



#Close the connection
conn.close()















#
