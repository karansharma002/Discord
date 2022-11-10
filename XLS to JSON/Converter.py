import pyexcel_xlsx as px
import json
import tkinter.filedialog as fd
import tkinter
import time
import sys

root = tkinter.Tk()
root.withdraw()
file = fd.askopenfilename(parent=root, title='Choose a XLSX File')
workbook = px.get_data(file)
try:
    data = json.dumps(workbook)
    data = json.loads(data)
    data['variable'].pop(0)
    data['constant'].pop(0)

    new_data = {}

    for x,y in zip(data['variable'],data['constant']):
        new_data[x[0]] = {}
        new_data[x[0]][y[0]] = x[1]
        new_data[x[0]][y[3]] = {}
        new_data[x[0]][y[3]][y[4]] = {}
        new_data[x[0]][y[3]][y[4]][y[1]] = x[2] 
        new_data[x[0]][y[3]][y[4]][y[2]] = x[3]

    with open('Converted_File.json','w') as f:
        json.dump(new_data,f,indent = 2)

except Exception as e:
    print(f'ERROR: {e}')
    time.sleep(5)
    sys.exit()

print('File has been Converted. (Converted_File.json)')
time.sleep(5)