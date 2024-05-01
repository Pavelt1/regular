from pprint import pprint
import csv
import re

contacts=[]
duplicates={}

with open("regular/phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

for i in contacts_list:# Разлепит слипшиеся ФИО
  if " " in i[0]:
    result = i[0].split(" ")
    if len(result) == 3:
      i[0]=result[0]
      i[1]=result[1]
      i[2]=result[2]
    if len(result) == 2:
      i[0]=result[0]
      i[1]=result[1]
  if " " in i[1]:
    result = i[1].split(" ")
    if len(result) == 2:
      i[1]=result[0]
      i[2]=result[1]
  contacts.append(i)
result = []

pattern_number = r"(\+*7|8?)\s*\(*(\d{3})\)*\s*[-]*(\d{3})\s*[-]*(\d{2})\s*[-]*(\d{2})"
pattern_dob = r"\(*([а-яА-Я]{3}.)\s*(\d{4})\)*"
pattern_data = r"^([а-яА-Я]+)\s(\w+)"

for i in contacts: # Разберет дублирующие строки и объединит данные
  y =" ".join(i)
  result_list = re.findall(pattern_data,y)
  if result_list:
    last_name = result_list[0][0]
    name = result_list[0][1]
    res = f"{last_name} {name}"
    if res in duplicates:
      result.remove(duplicates[res])
      for o in range(len(duplicates[res])):
        if duplicates[res][o] == "":
          if i[o] != "":
            duplicates[res][o] = i[o]
      
      result.append(duplicates[res])
    else:
      duplicates[res] = i
      result.append(duplicates[res]) 
  else:
    result.append(i)

res = []

for i in result: # Приведение к нужному формату тел. номера и доб. номера
  i =",".join(i)
  result_list = re.sub(pattern_number,r"\1(\2)\3-\4-\5",i)
  result_list = re.sub(pattern_dob,r"\1\2.",result_list)
  result_list = result_list.split(",")
  res.append(result_list)
  
with open("regular/phonebook.csv", "a", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(res)