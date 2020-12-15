import re
import pdfplumber
import csv

#every loaded page will be stored in RAM, so when the lap count is achieved, the file will be closed and reopened
lap = 200


ano_loa = '2021'
arquivo = 'LOA ' + ano_loa + '.pdf'
output = 'LOA_PRECS_' + ano_loa + '.csv'
a = len(pdfplumber.open(arquivo).pages)
n_laps = a // lap + 1
tribunal = ""
devedor = ""

for b in range (0,n_laps):
    if b*lap<a:
        csv_writer=[]

        with pdfplumber.open(arquivo) as pdf:
            for i in range(lap*b,min(lap*(b+1),a)):
                page = pdf.pages[i]
                text = page.extract_text()
                for line in text.split('\n'):
                    if line[:15] == 'UO CADASTRADORA':
                        tribunal = line.split(' ',3)
                    if line[:11] == 'UO DEVEDORA':
                        devedor = line.split(' ',3)
                    if line[:2] == '20':
                        info = line.rsplit(' ',1)
                        info[0] = info[0].split(' ',2)
                        csv_writer.append([ano_loa, info[0][0], tribunal[2], tribunal[3], devedor[2], devedor[3], info[0][1], info[0][2], info[1]])

            with open(output,'a',newline='', encoding='utf-8') as f:
                thewriter = csv.writer(f, delimiter=';')
                for c in range(0,len(csv_writer)):
                    thewriter.writerow(csv_writer[c])
