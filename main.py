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
                'cabin' : row.attrib['CabinType'].lower(),
                'layout' : cabin.attrib['Layout'].lower(),
                'seats' : {}
            }

            for seat in row.findall('{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo') :
                seatdata = {}
                summary = seat.find('{http://www.opentravel.org/OTA/2003/05/common/}Summary')
                features = seat.findall('{http://www.opentravel.org/OTA/2003/05/common/}Features')
                stype = []
                #find the seat type
                for x in features :
                    if x.text == 'Center' or x.text == 'Aisle' or x.text == 'Window' :
                        stype.append(x.text)
                    elif x.text == "Other_":
                        stype.append(x.attrib['extension'])

                #make it lowercase
                stype = [element.lower() for element in stype]

                seatdata['details'] = stype

                #Check if seat is available
                av = summary.attrib['AvailableInd']
                seatdata['available'] = av

                #Get price if available
                if av == "true" :
                    service = seat.find('{http://www.opentravel.org/OTA/2003/05/common/}Service')
                    curr = service[0].attrib['CurrencyCode']
                    amount = float(service[0].attrib['Amount']) + float(service[0][0].attrib['Amount'])
                    seatdata['seatPrice'] = {
                        'currencyCode' : curr.lower(),
                        'fee' : float(service[0].attrib['Amount']),
                        'tax' :  float(service[0][0].attrib['Amount']),
                        'total' : amount
                    }
                else :
                    seatdata['seatPrice'] = 'null'

                #find the seat number 
                SeatNum = summary.attrib['SeatNumber'].lower()
                output[RowNum]['seats'][SeatNum] = seatdata

    print(json.dumps(output))


#function for second xml file
def mapTwo(tree) :
    output = {}
    #move into the seatmap
    all = tree.getroot()

    seatspecs = {}

    #extract seat data into seatspecs dictionary
    datalist = all.find('{http://www.iata.org/IATA/EDIST/2017.2}DataLists')
    seatlist= datalist.find('{http://www.iata.org/IATA/EDIST/2017.2}SeatDefinitionList')
    for spec in seatlist.findall('{http://www.iata.org/IATA/EDIST/2017.2}SeatDefinition') :
        id = spec.attrib['SeatDefinitionID']
        text = spec[0][0].text.lower()
        seatspecs[id] = text

    pricespecs = {}

    #extract pricing data into pricespecs dictionary
    pricelist = all.find('{http://www.iata.org/IATA/EDIST/2017.2}ALaCarteOffer')
    for x in pricelist :
        id = x.attrib['OfferItemID']
        price = x.find('{http://www.iata.org/IATA/EDIST/2017.2}UnitPriceDetail')[0][0]
        pricespecs[id] = {
            'currencyCode' : price.attrib['Code'].lower(),
            'total' : float(price.text),
        }
    
    rows = []

    #go through every cabin in the xml file    
    for seatmap in all.findall('{http://www.iata.org/IATA/EDIST/2017.2}SeatMap') :
        cabin = seatmap[1]
        layout = cabin[0]
        lay = ""

        #extract the layout 
        for collumn in layout.findall('{http://www.iata.org/IATA/EDIST/2017.2}Columns') :
            pos = collumn.attrib['Position'].lower()
            lay += pos
        
        #store the rows in output and rownums in a list to be sorted
        for row in cabin.findall('{http://www.iata.org/IATA/EDIST/2017.2}Row') :
            rowNum = row[0].text
            rows.append(int(rowNum))
            output[rowNum] = {
                'layout' : lay,
                'seats' : {}
            }

            #loop through all the seats and find the refrences
            for seat in row.findall('{http://www.iata.org/IATA/EDIST/2017.2}Seat') :
                seatdata = {
                    'details' : [],
                    'available' : 'false',
                    'seatPrice' : 'null'
                }
                seatNum = rowNum + seat[0].text.lower()
                deets = []

                #fetch the price from the prices dictionary

                priceid = seat.find('{http://www.iata.org/IATA/EDIST/2017.2}OfferItemRefs')
                if (priceid is not None) :
                    seatdata['seatPrice'] = pricespecs[priceid.text]

                #fetch the specifications from the seat dictionary
                for ref in seat.findall('{http://www.iata.org/IATA/EDIST/2017.2}SeatDefinitionRef') :
                    reftxt = seatspecs[ref.text]
                    if reftxt == 'available' :
                        seatdata['available'] = 'true'
                    else :
                        deets.append(reftxt)

                seatdata['details'] = deets
                output[rowNum]['seats'][seatNum] = seatdata
    #sort by row
    sorted_output = {}
    
    rows.sort()
    for x in rows :
        sorted_output[str(x)] = output[str(x)]

    print(json.dumps(sorted_output['7']))

#check which xml file it is and call the appropriate function
if filename[-5] == "1" :
    mapOne(tree)
else :
    mapTwo(tree)


