import sys
import os
import random
from collections import Counter

class MetaPathGenerator:
    def __init__(self):
        self.id_User = dict()
        self.id_IpAddress = dict()
        self.id_Movie = dict()
        self.id_Genre = dict()
        self.User_IpAddresslist = dict()
        self.IpAddress_Userlist = dict()
        self.Movie_Genrelist = dict()
        self.Genre_Movielist = dict()
        self.User_Movielist = dict()
        self.Movie_Userlist = dict()

    def read_data(self, dirpath):
        with open(dirpath + "/id_User.txt", encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                # if len(toks) == 2:
                self.id_User[toks[0]] = toks[1].replace(" ", "")
        print(self.id_User)

        with open(dirpath + "/id_IpAddress.txt", encoding='ISO-8859-1') as bdictfile:
            for line in bdictfile:
                toks = line.strip().split("\t")
                # if len(toks) == 2:
                self.id_IpAddress[toks[0]] = toks[1].replace(" ", "")
        print(self.id_IpAddress)

        with open(dirpath + '/id_Movie.txt', encoding='ISO-8859-1') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                # if len(toks) == 2:
                self.id_Movie[toks[0]] = toks[1].replace(" ", "")
        print(self.id_Movie)

        with open(dirpath + '/id_Genre.txt', encoding='ISO-8859-1') as ddictfile:
            for line in ddictfile:
                toks = line.strip().split("\t")
                # if len(toks) == 2:
                self.id_Genre[toks[0]] = toks[1].replace(" ", "")
        print(self.id_Genre)

        with open(dirpath + "/User_IpAddress.txt", encoding='ISO-8859-1') as abfile:
            for line in abfile:
                toks = line.strip().split("\t")
                a, p = toks[0], toks[1]
                if a not in self.User_IpAddresslist:
                    self.User_IpAddresslist[a] = []
                self.User_IpAddresslist[a].append(p)
                if p not in self.IpAddress_Userlist:
                    self.IpAddress_Userlist[p] = []
                self.IpAddress_Userlist[p].append(a)
        print(self.User_IpAddresslist)
        print(self.IpAddress_Userlist)

        with open(dirpath + "/Movie_Genre.txt", encoding='ISO-8859-1') as cdfile:
            for line in cdfile:
                toks = line.strip().split("\t")
                a, p = toks[0], toks[1]
                if a not in self.Movie_Genrelist:
                    self.Movie_Genrelist[a] = []
                self.Movie_Genrelist[a].append(p)
                if p not in self.Genre_Movielist:
                    self.Genre_Movielist[p] = []
                self.Genre_Movielist[p].append(a)
        print(self.Movie_Genrelist)
        print(self.Genre_Movielist)

        with open(dirpath + "/User_Movie.txt", encoding='ISO-8859-1') as acfile:
            for line in acfile:
                toks = line.strip().split("\t")
                a, p = toks[0], toks[1]
                if a not in self.User_Movielist:
                    self.User_Movielist[a] = []
                self.User_Movielist[a].append(p)
                if p not in self.Movie_Userlist:
                    self.Movie_Userlist[p] = []
                self.Movie_Userlist[p].append(a)
        print(self.User_Movielist)
        print(self.Movie_Userlist)

    def generate_random_GMUIUMG(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding='utf-8')
        for genre in self.Genre_Movielist:
            genre0 = genre
            for i in range(0, numwalks):
                outline = self.id_Genre[genre0]
                for j in range(0, walklength):
                    movies = self.Genre_Movielist[genre]
                    numa = len(movies)
                    movieid = random.randrange(numa)
                    movie = movies[movieid]
                    while movie not in self.Movie_Userlist:
                        movieid = random.randrange(numa)
                        movie = movies[movieid]
                    outline += " " + self.id_Movie[movie]
                    users = self.Movie_Userlist[movie]
                    numb = len(users)
                    userid = random.randrange(numb)
                    user = users[userid]
                    while user not in self.User_IpAddresslist:
                        userid = random.randrange(numb)
                        user = users[userid]
                    outline += " " + self.id_User[user]
                    ipaddresss = self.User_IpAddresslist[user]
                    numc = len(ipaddresss)
                    ipaddressid = random.randrange(numc)
                    ipaddress = ipaddresss[ipaddressid]
                    while ipaddress not in self.IpAddress_Userlist:
                        ipaddressid = random.randrange(numc)
                        ipaddress = ipaddresss[ipaddressid]
                    outline += " " + self.id_IpAddress[ipaddress]
                    users = self.IpAddress_Userlist[ipaddress]
                    numd = len(users)
                    userid = random.randrange(numd)
                    user = users[userid]
                    while user not in self.User_Movielist:
                        userid = random.randrange(numd)
                        user = users[userid]
                    outline += " " + self.id_User[user]
                    movies = self.User_Movielist[user]
                    nume = len(movies)
                    movieid = random.randrange(nume)
                    movie = movies[movieid]
                    while movie not in self.Movie_Genrelist:
                        movieid = random.randrange(numa)
                        movie = movies[movieid]
                    outline += " " + self.id_Movie[movie]
                    genres = self.Movie_Genrelist[movie]
                    numf = len(genres)
                    genreid = random.randrange(numf)
                    genre = genres[genreid]
                    outline += " " + self.id_Genre[genre]
                outfile.write(outline + "\n")
        outfile.close()

    def generate_random_UMGMU(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding='utf-8')
        for user in self.User_Movielist:
            user0 = user
            for i in range(0, numwalks):
                outline = self.id_User[user0]
                for j in range(0, walklength):
                    movies = self.User_Movielist[user]
                    numa = len(movies)
                    movieid = random.randrange(numa)
                    movie = movies[movieid]
                    while movie not in self.Movie_Genrelist:
                        movieid = random.randrange(numa)
                        movie = movies[movieid]
                    outline += " " + self.id_Movie[movie]
                    genres = self.Movie_Genrelist[movie]
                    numb = len(genres)
                    genreid = random.randrange(numb)
                    genre = genres[genreid]
                    while genre not in self.Genre_Movielist:
                        genreid = random.randrange(numb)
                        genre = genres[genreid]
                    outline += " " + self.id_Genre[genre]
                    movies = self.Genre_Movielist[genre]
                    numc = len(movies)
                    movieid = random.randrange(numc)
                    movie = movies[movieid]
                    while movie not in self.Movie_Userlist:
                        movieid = random.randrange(numc)
                        movie = movies[movieid]
                    outline += " " + self.id_Movie[movie]
                    users = self.Movie_Userlist[movie]
                    numd = len(users)
                    userid = random.randrange(numd)
                    user = users[userid]
                    while user not in self.User_Movielist:
                        userid = random.randrange(numd)
                        user = users[userid]
                    outline += " " + self.id_User[user]
                outfile.write(outline + "\n")
        outfile.close()

    def generate_random_IUMUI(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding='utf-8')
        for ipaddress in self.IpAddress_Userlist:
            ipaddress0 = ipaddress
            for i in range(0, numwalks):
                outline = self.id_IpAddress[ipaddress0]
                for j in range(0, walklength):
                    users = self.IpAddress_Userlist[ipaddress]
                    numa = len(users)
                    userid = random.randrange(numa)
                    user = users[userid]
                    while user not in self.User_Movielist:
                        userid = random.randrange(numa)
                        user = users[userid]
                    outline += " " + self.id_User[user]
                    movies = self.User_Movielist[user]
                    numb = len(movies)
                    movieid = random.randrange(numb)
                    movie = movies[movieid]
                    while movie not in self.Movie_Userlist:
                        movieid = random.randrange(numb)
                        movie = movies[movieid]
                    outline += " " + self.id_Movie[movie]
                    users = self.Movie_Userlist[movie]
                    numc = len(users)
                    userid = random.randrange(numc)
                    user = users[userid]
                    while user not in self.User_IpAddresslist:
                        userid = random.randrange(numc)
                        user = users[userid]
                    outline += " " + self.id_User[user]
                    ipaddresss = self.User_IpAddresslist[user]
                    numd = len(ipaddresss)
                    ipaddressid = random.randrange(numd)
                    ipaddress = ipaddresss[ipaddressid]
                    while ipaddress not in self.IpAddress_Userlist:
                        ipaddressid = random.randrange(numd)
                        ipaddress = ipaddresss[ipaddressid]
                    outline += " " + self.id_IpAddress[ipaddress]
                outfile.write(outline + "\n")
        outfile.close()

    def generate_random_MGM(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding='utf-8')
        for movie in self.Movie_Genrelist:
            movie0 = movie
            for i in range(0, numwalks):
                outline = self.id_Movie[movie0]
                for j in range(0, walklength):
                    genres = self.Movie_Genrelist[movie]
                    numa = len(genres)
                    genreid = random.randrange(numa)
                    genre = genres[genreid]
                    outline += " " + self.id_Genre[genre]
                    movies = self.Genre_Movielist[genre]
                    numb = len(movies)
                    movieid = random.randrange(numb)
                    movie = movies[movieid]
                    outline += " " + self.id_Movie[movie]
                outfile.write(outline + "\n")
        outfile.close()

    def generate_random_UIU(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding='utf-8')
        for user in self.User_IpAddresslist:
            user0 = user
            for i in range(0, numwalks):
                outline = self.id_User[user0]
                for j in range(0, walklength):
                    ipaddresss = self.User_IpAddresslist[user]
                    numa = len(ipaddresss)
                    ipaddressid = random.randrange(numa)
                    ipaddress = ipaddresss[ipaddressid]
                    outline += " " + self.id_IpAddress[ipaddress]
                    users = self.IpAddress_Userlist[ipaddress]
                    numb = len(users)
                    userid = random.randrange(numb)
                    user = users[userid]
                    outline += " " + self.id_User[user]
                outfile.write(outline + "\n")
        outfile.close()

    def generate_random_UMU(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding='utf-8')
        for user in self.User_Movielist:
            user0 = user
            for i in range(0, numwalks):
                outline = self.id_User[user0]
                for j in range(0, walklength):
                    movies = self.User_Movielist[user]
                    numa = len(movies)
                    movieid = random.randrange(numa)
                    movie = movies[movieid]
                    outline += " " + self.id_Movie[movie]
                    users = self.Movie_Userlist[movie]
                    numb = len(users)
                    userid = random.randrange(numb)
                    user = users[userid]
                    outline += " " + self.id_User[user]
                outfile.write(outline + "\n")
        outfile.close()


numwalks = int(100)
walklength = int(100)

dirpath = "network"
outfilename = "ER.GMUIUMG.w100.l100.txt"

def main():
    mpg = MetaPathGenerator()
    mpg.read_data(dirpath)
    mpg.generate_random_GMUIUMG(outfilename, numwalks, walklength)


if __name__ == "__main__":
    main()
