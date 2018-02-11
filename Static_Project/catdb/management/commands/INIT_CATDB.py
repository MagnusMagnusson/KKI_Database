# -*- coding: utf-8 -*-
import csv
import os
from sets import Set
from django.core.management.base import BaseCommand, CommandError
from catdb.models import *
from django.utils import timezone
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


class Command(BaseCommand):    
	
	def add_arguments(self, parser):
		parser.add_argument('Action', nargs='+', type=str)
	def handle(self, *args, **options):

		print("Initializing constant data")
		act = options['Action'][0]
		if(act == "cert" or act == "all"):
			self.cert_fill()
		if(act == "judge" or act == "all"):
			self.judge_fill()

	def judge_fill(self):
		print("== STARTING JUDGE FILL ==")
		Length = 1
		with open('KKIDB_exports/Judges.csv', 'rb') as lengthfile:
			lengthreader =  unicode_csv_reader(lengthfile, quotechar='"')
			Length = sum(1 for row in lengthreader)
			print("Length recorded as " + str(Length))
		lengthfile.close()

		with open('KKIDB_exports/Judges.csv', 'rb') as csvfile:
			spamreader = unicode_csv_reader(csvfile, quotechar='"')
			first = True
			print("loaded")
			done = 0
			lastpercent = 0.05
			Cprev = None
			for row in spamreader:
				print(row)
				if(first):
					first = False
				else:
					J = judge()
					J.name = row[2]
					J.country = row[4]
					J.save()
			print("judge import done.")
			csvfile.close()

	def cert_fill(self):
		print("== STARTING CERTIFICATE FILL ==")
		Length = 1
		with open('KKIDB_exports/certificates.csv', 'rb') as lengthfile:
			lengthreader =  unicode_csv_reader(lengthfile, quotechar='"')
			Length = sum(1 for row in lengthreader)
			print("Length recorded as " + str(Length))
		lengthfile.close()

		with open('KKIDB_exports/certificates.csv', 'rb') as csvfile:
			spamreader = unicode_csv_reader(csvfile, quotechar='"')
			first = True
			print("loaded")
			done = 0
			lastpercent = 0.05
			Cprev = None
			for row in spamreader:
				print(row)
				if(first):
					first = False
				else:
					C = cert()
					C.certName = row[0]
					C.certRank = row[1]
					C.predecessor = Cprev
					C.neutered = int(row[2]) == 1
					Cprev = C if (Cprev == None or C.neutered == Cprev.neutered) else None
					C.save()
			print("cert import done.")
			csvfile.close()


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, delimiter = ',',**kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [str(cell) for cell in row]



def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.decode('latin_1').encode('utf-8')
