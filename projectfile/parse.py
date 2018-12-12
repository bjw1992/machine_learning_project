import csv
import codecs

def parse(filename):
  '''
  takes a filename and returns attribute information and all the data in array of dictionaries
  '''
  # initialize variables

  out = []
  csvfile = open(filename,'r',encoding='UTF-8')
  fileToRead = csv.reader(csvfile)
  headers = next(fileToRead)
  length=len(headers)
  for i in range(length):
    if headers[i]=='Rating':
      headers[i]='Class'

  # iterate through rows of actual data
  for row in fileToRead:
    if len(row)!=len(headers) or row[2]=='NaN':
      continue
    row[2]=float(row[2])
    row[3] = int(row[3])
    row[5] = row[5].replace('+', '') if '+' in str(row[3]) else row[3]
    row[5] = row[5].replace(',', '') if ',' in str(row[3]) else row[3]
    row[4] = row[4].replace('M', '') if 'M' in str(row[4]) else row[4]
    row[4] = row[4].replace('Varies with device', 'NaN') if 'Varies with device' in str(row[4]) else row[4]
    row[4] = float(row[4].replace('k', ''))/1000 if 'k' in str(row[4]) else row[4]
    row[7] = row[7].replace('$', '') if '$' in str(row[7]) else row[7]
    #Varies with device
    row[4] = float(row[4])
    row[5] = int(row[5])
    row[7] = float(row[7])
    out.append(dict(zip(headers, row)))
  return out