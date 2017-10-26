
#Program created by Maximilian Krochman
#October 26th 2017

#Main function
#1. Gathering Temp data from sensors
#2. Convert data if needed
#3. Store data in predefined table for later use
#4. Loops every 5 mins

#Pratical application for my Aquariums so I can monitor the water temps
# over a long period of time against the temps of the room they are in.
#


#Imports
import MySQLdb
import os
import time

#Nessary mods for One-Wire functions(for the temp probes)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Location of Tempsensor One-Wire File
temp_sensor = '/sys/bus/w1/devices/28-051684383cff/w1_slave'

#Reading temp data object
def temp_raw():
        f = open(temp_sensor, 'r')
        lines = f.readlines()
        f.close()
        return lines

#Takes raw string input from temp data object and cuts down to var data
# converts fron Celsius to Fahrenheit (For us dim folk across the pond) :P
def read_temp():
        lines = temp_raw()
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = temp_raw()
        temp_output = lines[1].find('t=')
        if temp_output != -1:
                temp_string = lines[1].strip()[temp_output+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                #In this case only returning the Fahrenheit temps
                return temp_f

#Main loop
#
while True:
        #Set temp var as a float(just incase)
        Temp = float(read_temp())
        ##print(Temp)
        #Connecting to DB where temp data is stored
        db = MySQLdb.connect(host="DB-IP Address", user="UserName", passwd="Password", db="DB-Name")
        cur = db.cursor()

        #Testing to see how many rows exist already for ID count
        cur.execute("SELECT COUNT(*) FROM AquariumDataBase.SmallTank;")

        #Left over from testing
        for row in cur.fetchall():
                ##print(row[0])

        #I had some confusion with Python assumptions on data types and the
        # mysql Python connector doing the same thing. Forced an Int conversion just incase
        rowNum = row[0]
        rowNum = int(rowNum)
        rowNum = rowNum + 1
        ##print(rowNum)

        #Inserting the new Temp and its row ID, Date-Time is defaulted to system time of MySQL server
        cur.execute("INSERT INTO AquariumDataBase.SmallTank (id,InternalTemp) Values(%s,%s)", (rowNum, Temp))
        #Saving changes to Table
        db.commit()
        #Closing DB connection
        db.close()
        #Sleep for 5 mins (300 seconds)
        time.sleep(300)
