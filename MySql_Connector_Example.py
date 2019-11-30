import mysql.connector as mysql
import pandas as pd
import os

print('Instructions:')
print('-Use table ID to pull the reports from the correct platform site')
print('Specify where the files should be exported to')
print('')

#This table ID probably isn't needed, however, it was needed for the mysql database I was using.

kd = input('What is the tableID?')

#Where to put export?

destination = input('Where should I put them?')

kd = str(kd)

#Connection
#Host = environment connecting to...

db = mysql.connect(
  host="host.prod.com", user='user', password='password', port='1111'

)

cursor = db.cursor()

print('working on it')


query = '''SELECT 
TRIM(person.FirstName),
person.middleName as 'Middle Name',
person.LastName as 'Last Name',
person.suffix as 'Suffix',
person.gender as 'Gender',
person.dateOfBirth as 'Birthday',
person.preferredContactMethod as 'Preferred Contact Method',
person.marketingSource as 'Marketing Source',
email.address as 'Email Address',
email.optOut as 'Email Opt Out',
personUserRelation.userId as 'Producer ID',
personUserRelation.userId as 'Servicer ID',


from table_''' + kd + '''.person

left outer join table_''' + kd + '''.personUserRelation on personUserRelation.personId = person.id
left outer join table_''' + kd + '''.personRiskRelation on personRiskRelation.personId = person.id
left outer join table_''' + kd + '''.personEmailRelation on personEmailRelation.personId = person.id
left outer join table_''' + kd + '''.email on email.id = personEmailRelation.emailId


where businessPersonRelation.businessId is null and person.invalid=0  
'''

#I would have made aliases for the tables, however, for whatever reason I couldn't get them to work.

#Run above query

cursor.execute(query)

#Get all records
records = cursor.fetchall()

#Make into dataframe with the following column names

df = pd.DataFrame(records, columns=['First Name','Middle Name','Last Name','Suffix','Gender','Birthday','Preferred Contact Method','Marketing Source','Email Address','Email Opt Out'])

#Change working drive

os.chdir(destination)


#Export file in csv format

export = df.to_csv(destination + "\\" + 'personalextract.csv', index=None,header=True, sep=',')

