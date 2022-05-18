import os
import subprocess
import csv
import pandas as pd
import argparse

#extract SaaS key from CSV file
def getSAASkey(csvFile):
    with open(csvFile, newline='') as f:
        reader = csv.reader(f)
        SaaSkey = next(reader)[1]  # gets the SaaS key from first row of the CSV file
    return SaaSkey    

#get images from RAIC
def RAICcsv2Files(csvFile,outDir):
    SASkey=getSAASkey(csvFile)
    df=pd.read_csv(csvFile,skiprows=1) 
    i=0
    for index, row in df.iterrows():
        try:
            file_path = (os.path.join(outDir,str(row['category'])))
            if not os.path.exists(file_path):
                    os.makedirs(file_path)
            full_link = ('"'+row['url'] + SASkey + '"')
            processcmd="azcopy cp "+full_link+" "+file_path
            #print(processcmd)
            transfer = subprocess.call(processcmd, stderr=subprocess.STDOUT)
            #rename image in case they are same
            downloadedName=str(row['url']).split('/')[len(str(row['url']).split('/'))-1]
            newName="image_"+str(i)+".jpg"
            os.rename(os.path.join(file_path,downloadedName), os.path.join(file_path,newName))
        except EOFError as error:
            #Output for EOF error, would be caused by missing SAS
            print('Error with SAS')
        except Exception as e:
            #When an unexpected error has occured.
            print(str(e) + 'Unknown error has occured')
        i+=1

parser = argparse.ArgumentParser()
   
parser.add_argument('-i', '--input',  required=True, help="CSV file downloaded from RAIC portal")
parser.add_argument('-o', '--outdir', required=True , help="output directory for downlaoded images")

args = parser.parse_args()

RAICcsv2Files(args.input,args.outdir)
