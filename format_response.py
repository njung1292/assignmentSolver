import xlrd, xlwt, re

## Converts the real data into a format more like Survey Monkey data

SEMINAR_LIST = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",\
                "F11", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9",\
                "S10"]
num_seminars = len(SEMINAR_LIST)

responseBk      = xlrd.open_workbook("test data/FS_response_data.xlsx")
responseSht     = responseBk.sheet_by_name("Sheet1")
surveyMonkeyBk  = xlwt.Workbook(encoding = "utf-8")
surveyMonkeySht = surveyMonkeyBk.add_sheet("Sheet1")

# Initialize surveyMonkeySht
surveyMonkeySht.write(0,0,"RespondentID")
surveyMonkeySht.write(0,1,"CollectorID")
surveyMonkeySht.write(0,2,"Start Date")
surveyMonkeySht.write(0,3,"EndDate")
surveyMonkeySht.write(0,4,"IP Address")
surveyMonkeySht.write(0,5,"Email Address")
surveyMonkeySht.write(0,6,"First Name")
surveyMonkeySht.write(0,7,"Last Name")
surveyMonkeySht.write(0,8,"Custom Data")
surveyMonkeySht.write(0,9,"Ranking results")
for i in xrange(num_seminars):
    surveyMonkeySht.write(1,9+i,SEMINAR_LIST[i])

# Get raw ranking values
num_rows = responseSht.nrows - 1
num_cols = responseSht.ncols - 1

responses = responseSht.col_values(1,start_rowx=23,end_rowx=None)
vals = []

# Put raw ranking values into arrays
p = re.compile("(\d*)[^\d]*")
for resp in responses:
    matches = [int(c) for c in p.findall(resp) if c!='']
    vals.append(matches)

# Write ranking values into spreadsheet
for i in range(len(vals)):
    surveyMonkeySht.write(2+i,0,i+1)
    for j in range(len(vals[i])):
        surveyMonkeySht.write(2+i,8+vals[i][j],j+1)

surveyMonkeyBk.save("test data/FS_response_data_formatted.xls")
