from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
working_dir = os.path.dirname(os.path.abspath(__file__))


# lista książek
@app.route('/book/', methods=['GET'])
def list_of_books():
    query = 'SELECT book.id, book.title, book.cover_image, publisher.name \
    FROM book, publisher WHERE book.publisher_id=publisher.id;'
    info = jsonify(mysql_db_connection(query))
    image_path = f"{working_dir}/static/468561.jpg"

    return info


# pojedyncza książka
@app.route('/book/<pk>/', methods=['GET'])
def one_book_info(pk):
    query = f"SELECT book.id, book.title, author.firstname, author.lastname, publisher.name, book.pages_num, \
    book.cover_image FROM book, publisher, author, book_author WHERE book.id = '{pk}' \
    AND book.publisher_id=publisher.id AND book_author.book_id = book.id AND book_author.author_id = author.id;"
    info = jsonify(mysql_db_connection(query))

    return info


# tworzy obiekt książki
@app.route('/book/', methods=['POST'])
def create_book_object():
    content_body = request.get_json()
    print("get_json() content: " + str(content_body))

    # parse received JSON:
    for key in content_body:
        print(f"{key}: {content_body[key]}")

        if str(key).lower() == "title":
            title = content_body[key]
        if str(key).lower() == "publisher_id":
            publisher_id = content_body[key]
        if str(key).lower() == "pages_num":
            pages_num = content_body[key]
        if str(key).lower() == "cover_image":
            cover_image = content_body[key]

    info = add_book(title, publisher_id, pages_num, cover_image)

    if info is "success":
        return "Book added, success!"
    else:
        return "Error, post failed: " + info


# edytuje książkę o podanym ID
@app.route('/book/<pk>/', methods=['PUT'])
def edit_book_object(pk):
    content_body = request.get_json()
    print("get_json() content: " + str(content_body))

    # parse received JSON:
    for key in content_body:
        print(f"{key}: {content_body[key]}")

        if str(key).lower() == "title":
            title = content_body[key]
        if str(key).lower() == "publisher_id":
            publisher_id = content_body[key]
        if str(key).lower() == "pages_num":
            pages_num = content_body[key]
        if str(key).lower() == "cover_image":
            cover_image = content_body[key]

    info = edit_book(pk, title, publisher_id, pages_num, cover_image)

    if info is "success":
        return "Book added, success!"
    else:
        return "Error, post failed: " + info


# add book to db
def add_book(title, publisher_id, pages_num, cover_image):
    query = "INSERT INTO book(title, publisher_id, pages_num, cover_image)" \
            "VALUES(%s,%s,%s,%s)"
    args = (title, publisher_id, pages_num, cover_image)

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='books_db',
                                             user='root',
                                             password='1test_task')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print(f"Connected to MySQL database... MySQL Server version on: {db_Info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"Connected to: {record}")

            cursor.execute(query, args)
            connection.commit()  # apply changes

            info = "success"

    except Error as error:
        info = str(error)
        print(f"Error with MySQL: {error}")
    finally:
        # closing database connection.
        if connection.is_connected():
            cursor.close()
            connection.close()

    return info


# edytuje książkę:
def edit_book(pk, title, publisher_id, pages_num, cover_image):
    query = f"UPDATE book SET 'title'={title}, 'publisher_id'={publisher_id}, \
            'pages_num'={pages_num}, 'cover_image'={cover_image} WHERE 'id'={pk}"


    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='books_db',
                                             user='root',
                                             password='1test_task')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print(f"Connected to MySQL database... MySQL Server version on: {db_Info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"Connected to: {record}")

            cursor.execute(query)
            connection.commit()  # apply changes

            info = "success"

    except Error as error:
        info = str(error)
        print(f"Error with MySQL: {error}")
    finally:
        # closing database connection.
        if connection.is_connected():
            cursor.close()
            connection.close()

    return info

# database connection:
def mysql_db_connection(query):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='books_db',
                                             user='root',
                                             password='1test_task')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print(f"Connected to MySQL database... MySQL Server version on: {db_Info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"Connected to: {record}")

            cursor.execute(query)
            records = cursor.fetchall()

            info = records

    except Error as error:
        info = str(error)
        print(f"Error with MySQL: {error}")
    finally:
        # closing database connection.
        if connection.is_connected():
            cursor.close()
            connection.close()

    return info


if __name__ == '__main__':
   app.run(debug=True)
