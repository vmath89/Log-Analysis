#! Python3
import psycopg2
from datetime import datetime

"""
    This function searches for the 3 most popular articles which have been
    accessed and presents this list information with the
    most popular article on the top.
"""
def popular_articles():
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    cursor.execute(
        'Select title, count(*) as count '
        'from articles, log '
        'where log.path like concat(\'%\', articles.slug) '
        'group by title '
        'order by count limit 3')
    result = cursor.fetchall()
    print('Most popular 3 articles:')
    for row in result:
        print('\"' + row[0] + '\"' + ' — ' + str(row[1]) + ' views')
    conn.close()


"""
    This function searches for the authors who gets the most page
    views and present this as a sorted list with the
    most popular author at the top.
"""
def popular_authors():
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    cursor.execute(
        'Select name, count(*) as count '
        'from articles, log, authors '
        'where authors.id = articles.author '
        'and log.path like concat(\'%\', articles.slug) '
        'group by name '
        'order by count desc')
    result = cursor.fetchall()
    print('Most popular article authors of all time:')
    for row in result:
        print(row[0] + ' — ' + str(row[1]) + 'views')
    conn.close()


"""
    This function prints the days on which more than 1%
    of the requests lead to errors.
"""
def most_error():
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    cursor.execute(
        'select date(time) as date, count(*) as count, status '
        'from log where status=\'404 NOT FOUND\' '
        'or status=\'200 OK\' '
        'group by date, status '
        'order by date desc')
    result = cursor.fetchall()
    # This will get the status 200 OK and status 404 NOT FOUND rows
    # alternating for each date.
    for i in range(0, len(result) - 1, 2):
        OK_requests = result[i][1]
        # Moving to the next row returned by the database because the next row
        # is status 404 NOT FOUND row.
        i += 1
        ERROR_requests = result[i][1]
        # Finding the total number of requests for any day.
        total_requests = OK_requests + ERROR_requests
        percentage = (ERROR_requests / total_requests) * 100
        if percentage > 1:
            # Converting the date format from yyyy-mm-dd to name-of-month
            # date-of-month, year format.
            d = datetime.strptime(str(result[i][0]), "%Y-%m-%d")
            print(d.strftime("%B %d, %Y") + ' — ' + '%.2f' %
                  percentage + '% errors')
    conn.close()


def options():
    print('Welcome to reporting tool:')
    print('Press 1 if you want to know the most popular 3 articles.')
    print('Press 2 if you want to know the most '
          'popular article authors of all time.')

    print('Press 3 if you want to know on which days did '
          'more than 1 % of the requests lead to error.')

    print('Press 4 for exit.\n')
    option = int(input("Waiting for your input - "))
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


options()
