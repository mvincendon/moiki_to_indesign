# moiki_to_indesign

## Requirements:
- numpy
- BeautifulSoup 4
- Adobe InDesign 2020

## Workflow

*Note: All paths are considered from repository root.*

### Initial steps
- Install requirements somehow
- Open template.indd in InDesign
- Enable Data Merge panel in Window > Utility > Data Merge

### Story update process
- Export story from Moiki as json
- Download zip file into repository root
- In command line, run update.cmd script with the zip file as argument
- Run *(from repository root)* story_json_to_csv.py to create/update csv file
- If not done previously, in the Data Merge panel, select the data source as story/story.csv
- Click on *Create a merged document*
- Change **Options > Adjustement** to *Fill blocks proportionnally*
- Click ok and voilà.

## Troubleshooting
Good luck.