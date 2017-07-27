#!/usr/bin/python3
import psycopg2
from datetime import datetime

""" This function searches for the 3 most popular articles which have been
accessed and presents this list information with the
most popular article on the top.
"""


def popular_articles():
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    cursor.execute(
        'SELECT title, count(*) AS views '
        'FROM articles, log '
        'WHERE log.path = concat(\'/article/\', articles.slug) '
        'GROUP BY title '
        'ORDER BY views DESC LIMIT 3')
    result = cursor.fetchall()
    print('Most popular 3 articles:')
    for row in result:
        print('     \"' + row[0] + '\"' + ' — ' + str(row[1]) + ' views')
    conn.close()
    ask_for_more_report()


""" This function searches for the authors who gets the most page
views and present this as a sorted list with the
most popular author at the top.
"""


def popular_authors():
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    cursor.execute(
        'SELECT name, count(*) AS count '
        'FROM articles, log, authors '
        'WHERE authors.id = articles.author '
        'AND log.path = concat(\'/article/\', articles.slug) '
        'GROUP BY name '
        'ORDER BY count DESC')
    result = cursor.fetchall()
    print('Most popular article authors of all time:')
    for row in result:
        print('     ' + row[0] + ' — ' + str(row[1]) + ' views')
    conn.close()
    ask_for_more_report()


""" This function prints the days on which more than 1%
of the requests lead to errors.
"""


def most_error():
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    cursor.execute(
        'select date, error_percentage from'
        '(select date(time) as date, '
        '100.0 * sum(case when status != \'200 OK\' then 1 else 0 end) /'
        'count(*) as error_percentage '
        'from log '
        'group by date(time) '
        'order by date(time)) as daily_error_rates '
        'where error_percentage > 1')
    result = cursor.fetchall()
    # Converting the date format from yyyy-mm-dd to name-of-month
    # date-of-month, year format.
    for row in result:
        d = datetime.strptime(str(row[0]), "%Y-%m-%d")
        print('     ' + d.strftime("%B %d, %Y") + ' — ' + '%.2f' %
              row[1] + '% errors')
    conn.close()
    ask_for_more_report()


def options():
    print('Welcome to reporting tool:')
    print('Press 1 if you want to know the most popular 3 articles.')
    print('Press 2 if you want to know the most '
          'popular article authors of all time.')

    print('Press 3 if you want to know on which days did '
          'more than 1 % of the requests lead to error.')

    print('Press 4 for exit.\n')
    option = int(input("Waiting for your input — "))
    if option == 1:
        print('Processing... Please wait...')
        popular_articles()
    if option == 2:
        print('Processing... Please wait...')
        popular_authors()
    if option == 3:
        print('Processing... Please wait...')
        most_error()
    if option == 4:
        exit(0)


def ask_for_more_report():
    while True:
        print('')
        more_report = input('Do you want to look at some more reports (Y/N)?')
        if more_report == 'Y' or more_report == 'y':
            options()
        elif more_report == 'N' or more_report == 'n':
            exit(0)
        else:
            print('I did not understand the input.. Please enter a valid input.')


options()
