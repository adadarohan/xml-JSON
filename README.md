# XML to JSON

XML to JSON converts the given seatmaps into json files with the same format. It differentiates between the 2 files using the filename and coverts the following properties - 
- Seat type (Center, Window, Aisle, Bathroom etc.)
- Details (Limited recline, Quiet zone etc.)
- Seat number
- Price (Fee, Tax, Total and Currency Code)
- Cabin Class (Omitted in seatmap2 as no cabin is specified)
- Availibility (True/False)
- Row Layout

## Usage

Download the python program from the repository and run it from the command line while passing the filename using the following command. Replace `[FILENAME]` with the path to your file.

 ```bash
 python main.py [FILENAME]
 ```

## Output

The program outputs a new json file with the name `[FILENAME]_parsed.json` which contains the parsed json. All strings in the json file are lower case and sorted by row and class. The details are stored in a list and the price is an object. Below is an example of how the output would look.


```json
{
    "1":{
        "cabin":"first",
        "layout":"ab ef",
        "seats":{
            "1a":{
                "details":[
                    "window"
                ],
                "available":"false",
                "seatPrice":"null"
            },
            "1b":{
                "details":[
                    "aisle"
                ],
                "available":"false",
                "seatPrice":"null"
            },
            "1e":{
                "details":[
                    "aisle"
                ],
                "available":"false",
                "seatPrice":"null"
            },
            "1f":{
                "details":[
                    "window"
                ],
                "available":"false",
                "seatPrice":"null"
            }
        }
    },
    "2":{
        "cabin":"first",
        "layout":"ab ef",
        "seats":{
            "2a":{
                "details":[
                    "window"
                ],
                "available":"false",
                "seatPrice":"null"
            },
            "2b":{
                "details":[
                    "aisle"
                ],
                "available":"false",
                "seatPrice":"null"
            },
            "2e":{
                "details":[
                    "aisle"
                ],
                "available":"false",
                "seatPrice":"null"
            },
            "2f":{
                "details":[
                    "window"
                ],
                "available":"false",
                "seatPrice":"null"
            }
        }
    }
}
```
