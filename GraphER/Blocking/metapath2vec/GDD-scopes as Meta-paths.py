import sys
import os
import random
from collections import Counter

class MetaPathGenerator:
	def __init__(self):
		self.id_author = dict()
		self.id_conf = dict()
		self.author_coauthorlist = dict()
		self.conf_authorlist = dict()
		self.author_conflist = dict()
		self.paper_author = dict()
		self.author_paper = dict()
		self.conf_paper = dict()
		self.paper_conf = dict()

	def read_data(self, dirpath):
		with open(dirpath + "/id_author.txt",encoding='ISO-8859-1') as adictfile:
			for line in adictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					self.id_author[toks[0]] = toks[1].replace(" ", "")

		#print "#authors", len(self.id_author)

		with open(dirpath + "/id_conf.txt",encoding='ISO-8859-1') as cdictfile:
			for line in cdictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					newconf = toks[1].replace(" ", "")
					self.id_conf[toks[0]] = newconf

		#print "#conf", len(self.id_conf)

		with open(dirpath + "/paper_author.txt",encoding='ISO-8859-1') as pafile:
			for line in pafile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					p, a = toks[0], toks[1]
					if p not in self.paper_author:
						self.paper_author[p] = []
					self.paper_author[p].append(a)
					if a not in self.author_paper:
						self.author_paper[a] = []
					self.author_paper[a].append(p)

		with open(dirpath + "/paper_conf.txt",encoding='ISO-8859-1') as pcfile:
			for line in pcfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					p, c = toks[0], toks[1]
					self.paper_conf[p] = c 
					if c not in self.conf_paper:
						self.conf_paper[c] = []
					self.conf_paper[c].append(p)

		sumpapersconf, sumauthorsconf = 0, 0
		conf_authors = dict()
		for conf in self.conf_paper:
			papers = self.conf_paper[conf]
			sumpapersconf += len(papers)
			for paper in papers:
				if paper in self.paper_author:
					authors = self.paper_author[paper]
					sumauthorsconf += len(authors)

		print("#citys  ", len(self.conf_paper))
		print("#addresses ", sumpapersconf, "#addresses per city ", sumpapersconf / len(self.conf_paper))
		print("#restaurants", sumauthorsconf, "#restaurants per city", sumauthorsconf / len(self.conf_paper))

	def generate_random_aca(self, outfilename, numwalks, walklength):
		for conf in self.conf_paper:
			self.conf_authorlist[conf] = []
			for paper in self.conf_paper[conf]:
				if paper not in self.paper_author: continue
				for author in self.paper_author[paper]:
					self.conf_authorlist[conf].append(author)
					if author not in self.author_conflist:
						self.author_conflist[author] = []
					self.author_conflist[author].append(conf)
		#print "author-conf list done"

		outfile = open(outfilename, 'w', encoding='utf-8')
		for conf in self.conf_authorlist:
			conf0 = conf
			#print(self.id_conf.keys())
			for j in range(0, numwalks ): #wnum walks
				outline = self.id_conf[conf0]
				for i in range(0, walklength):
					authors = self.conf_authorlist[conf]
					numa = len(authors)
					authorid = random.randrange(numa)
					author = authors[authorid]
					outline += " " + self.id_author[author]
					confs = self.author_conflist[author]
					numc = len(confs)
					confid = random.randrange(numc)
					conf = confs[confid]
					outline += " " + self.id_conf[conf]
				outfile.write(outline + "\n")
		outfile.close()


#python py4genMetaPaths.py 1000 100 net_aminer output.aminer.w1000.l100.txt
#python py4genMetaPaths.py 1000 100 net_dbis   output.dbis.w1000.l100.txt

#dirpath = "net_aminer"
# OR 
#dirpath = "net_dbis"
dirpath = ""

numwalks = int(1000)
walklength = int(100)

dirpath = ""
outfilename = ""

def main():
	mpg = MetaPathGenerator()
	mpg.read_data(dirpath)
	mpg.generate_random_aca(outfilename, numwalks, walklength)


if __name__ == "__main__":
	main()





























