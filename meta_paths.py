import sys
import os
import random
from collections import Counter

class MetaPathGenerator:
    def __init__(self):
        self.id_restaurant = dict()
        self.id_address = dict()
        self.id_city = dict()
        self.restaurant_address = dict()
        self.address_restaurant = dict()
        self.address_city = dict()
        self.city_address = dict()
        self.path = dict()


    def read_data(self, dirpath):
        with open(dirpath + "/restaurant.txt", encoding='ISO-8859-1') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                # if len(toks) == 2:
                self.id_restaurant[toks[0]] = toks[1].replace(" ", "")
        # print(self.id_restaurant)

        with open(dirpath + "/address.txt", encoding='ISO-8859-1') as bdictfile:
            for line in bdictfile:
                toks = line.strip().split("\t")
                # if len(toks) == 2:
                self.id_address[toks[0]] = toks[1].replace(" ", "")
        # print(self.id_address)

        with open(dirpath + "/city.txt", encoding='ISO-8859-1') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                # if len(toks) == 2:
                self.id_city[toks[0]] = toks[1].replace(" ", "")
        # print(self.id_city)


        with open(dirpath + "/restaurant-address.txt", encoding='ISO-8859-1') as abfile:
            for line in abfile:
                toks = line.strip().split("\t")
                a, p = toks[0], toks[1]
                if a not in self.restaurant_address:
                    self.restaurant_address[a] = []
                self.restaurant_address[a].append(p)
                if p not in self.address_restaurant:
                    self.address_restaurant[p] = []
                self.address_restaurant[p].append(a)
        # print(self.restaurant_address)
        # print(self.address_restaurant)

        with open(dirpath + "/address-city.txt", encoding='ISO-8859-1') as abfile:
            for line in abfile:
                toks = line.strip().split("\t")
                a, p = toks[0], toks[1]
                if a not in self.address_city:
                    self.address_city[a] = []
                self.address_city[a].append(p)
                if p not in self.city_address:
                    self.city_address[p] = []
                self.city_address[p].append(a)
        # print(self.address_city)
        # print(self.city_address)

    def generate_random_RACAR(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding='utf-8')
        for restaurant in self.restaurant_address:
            restaurant0 = restaurant
            for i in range(0, numwalks):
                outline = self.id_restaurant[restaurant0]
                for j in range(0, walklength):
                    addresss = self.restaurant_address[restaurant]
                    numa = len(addresss)
                    addressid = random.randrange(numa)
                    address = addresss[addressid]
                    outline += " " + self.id_address[address]
                    citys = self.address_city[address]
                    numb = len(citys)
                    cityid = random.randrange(numb)
                    city = citys[cityid]
                    outline += " " + self.id_city[city]
                    addresss = self.city_address[city]
                    numc = len(addresss)
                    addressid = random.randrange(numc)
                    address = addresss[addressid]
                    outline += " " + self.id_address[address]
                    restaurants = self.address_restaurant[address]
                    numd = len(restaurants)
                    restaurantid = random.randrange(numd)
                    restaurant = restaurants[restaurantid]
                    outline += " " + self.id_restaurant[restaurant]
                outfile.write(outline + "\n")
        outfile.close()

    def generate_random_RAR(self, outfilename, numwalks, walklength):
        outfile = open(outfilename, 'w', encoding='utf-8')
        for restaurant in self.restaurant_address:
            restaurant0 = restaurant
            for i in range(0, numwalks):
                outline = self.id_restaurant[restaurant0]
                for j in range(0, walklength):
                    addresss = self.restaurant_address[restaurant]
                    numa = len(addresss)
                    addressid = random.randrange(numa)
                    address = addresss[addressid]
                    outline += " " + self.id_address[address]
                    restaurants = self.address_restaurant[address]
                    numb = len(restaurants)
                    restaurantid = random.randrange(numb)
                    restaurant = restaurants[restaurantid]
                    outline += " " + self.id_restaurant[restaurant]
                outfile.write(outline + "\n")
        outfile.close()

def sentence_generation(dirpath, metapath, outfilename, numwalks, walklength):
    mpg = MetaPathGenerator()
    mpg.read_data(dirpath)
    if metapath == 'RACAR':
        mpg.generate_random_RACAR(outfilename, numwalks, walklength)
    elif metapath == 'RAR':
        mpg.generate_random_RAR(outfilename, numwalks, walklength)
    else:
        print("Need to add the meta-path function")

