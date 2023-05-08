import socket
import os
from _thread import *
import requests
from bs4 import BeautifulSoup
from xlwt import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345

ThreadCount = 0
try:
    s.bind((host, port))
except socket.error as e:
    print(e)

print('Waitiing for a Connection..')
s.listen(5)

def get_imdb_top250():
    url = "https://www.imdb.com/chart/top"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    movie_tags = soup.select("td.titleColumn")
    movies = []
    for movie_tag in movie_tags:
        # Extract movie title, year, and link
        title_tag = movie_tag.a
        title = title_tag.text
        year = movie_tag.span.text.strip("()")
        link = "https://www.imdb.com" + title_tag.get("href")

        movie = {
            "title": title,
            "year": year,
            "link": link,
        }
        movies.append(movie)
    return movies


def get_books():
    url = "https://www.cosmopolitan.com/entertainment/books/g42557681/best-books-2023/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    book_tags = soup.select("h2.css-1ms88rh.e8seki10")
    books = []
    for book_tag in book_tags:
        # Extract movie title, year, and link
        title = book_tag.text

        book = {
            "title": title,
        }
        books.append(book)
    return books


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))
    while True:
        data = connection.recv(2048)
        print('Received from client' + str(ThreadCount)+' : ' + data.decode())
        if data == b"IMDB":
            movies = get_imdb_top250()
            for movie in movies:
                connection.sendall(str(movie).encode())
                connection.send(b'\n') # add newline separator between each movie
            connection.send(b'Done') # indicate end of data
        elif data == b"COSMOPOLITAN":
            books = get_books()
            for book in books:
                connection.sendall(str(book).encode())
                connection.send(b'\n') # add newline separator between each movie
            connection.send(b'Done') # indicate end of data
        else:
            connection.sendall(b'Unknown command\n')
    connection.close()




while True:
    Client, address = s.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
s.close()