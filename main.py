import sys
import xml.etree.ElementTree as ET
import json

#verify the file
try:
    filename = sys.argv[1]
    tree = ET.parse(filename)
except IndexError:
    print("ERROR : Filename not found. Please pass a filename to the program")
except FileNotFoundError:
    print("FileNotFoundError: No such file: '" + filename + "'")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

def mapOne(tree) :
    output = {}
    #move into the seatmap
    seatmap = tree.getroot()[0][0][1][0][1]
    for cabin in seatmap:
        for row in cabin :
            #Fetch info about the row
            RowNum =  row.attrib['RowNumber']
            output[RowNum] = {
                'cabin' : row.attrib['CabinType'],
                'layout' : cabin.attrib['Layout'],
                'seats' : {}
            }

            for seat in row.findall('{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo') :
                seatdata = {}
                summary = seat.find('{http://www.opentravel.org/OTA/2003/05/common/}Summary')
                features = seat.findall('{http://www.opentravel.org/OTA/2003/05/common/}Features')
                stype = ""
                #find the seat type
                for x in features :
                    if x.text == 'Center' or x.text == 'Aisle' or x.text == 'Window' :
                        stype = x.text
                    elif x.text == "Other_" and x.attrib['extension'] == 'Lavatory':
                        stype = 'Lavatory'

                seatdata['type'] = stype

                #Check if seat is available
                av = summary.attrib['AvailableInd']
                seatdata['available'] = av

                #Get price if available
                if av == "true" :
                    service = seat.find('{http://www.opentravel.org/OTA/2003/05/common/}Service')
                    curr = service[0].attrib['CurrencyCode']
                    amount = int(service[0].attrib['Amount']) + int(service[0][0].attrib['Amount'])
                    seatdata['seatPrice'] = {
                        'currencyCode' : curr,
                        'fee' : int(service[0].attrib['Amount']),
                        'tax' :  int(service[0][0].attrib['Amount']),
                        'total' : amount
                    }
                else :
                    seatdata['seatPrice'] = 'null'

                #find the seat number 
                SeatNum = summary.attrib['SeatNumber']
                output[RowNum]['seats'][SeatNum] = seatdata

    print(json.dumps(output))


#function for second xml file
def mapTwo(tree) :
    output = {}
    #move into the seatmap
    seatmap = tree.getroot()
    print(seatmap.tag, seatmap.attrib)
    print(json.dumps(output))

#check which xml file it is and call the appropriate function
if filename[-5] == "1" :
    mapOne(tree)
else :
    mapTwo(tree)


