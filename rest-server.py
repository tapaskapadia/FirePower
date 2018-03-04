#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
from requests.utils import quote

import MySQLdb
import sys
import csv
import requests 
import json
app = Flask(__name__, static_url_path="")


USERNAME = 'root'
PASSWORD = 'blahblahblah'
DB_NAME = 'crime'
#Insert host url from RDS
connect = MySQLdb.connect (	host = "",
                        	user = USERNAME,
                        	passwd = PASSWORD,
                        	db = DB_NAME, 
				port = 3306
						)

conn  = connect.cursor()



@app.route('/', methods=['GET'])
def getHome():
    return render_template('index.html')





@app.route('/heat', methods=['GET'])
def getHeat():
    conn  = connect.cursor()
    conn.execute( """SELECT state,year,SUM(response) 
                FROM ( SELECT state, year, response FROM q1
                    UNION ALL
                    SELECT state, year, response FROM q2
                    UNION ALL
                    SELECT state, year, response FROM q3
                    UNION ALL
                    SELECT state, year, response FROM q4
                    UNION ALL
                    SELECT state, year, response FROM q5
                    UNION ALL
                    SELECT state, year, response FROM q6
                    UNION ALL
                    SELECT state, year, response FROM q7
                    UNION ALL
                    SELECT state, year, response FROM q8
                    UNION ALL
                    SELECT state, year, response FROM q9
                    UNION ALL
                    SELECT state, year, response FROM q10
                    UNION ALL
                    SELECT state, year, response FROM q11
                    )a
                GROUP BY state,year;
                """)
    results = conn.fetchall()
   # c = csv.writer(open("./templates/test.csv","wb"))
   # c.writerow(['state','year','score'])
   # for row in results:
   #     c.writerow(row)
   # conn.close()  
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }    
    count = 0
    writeRow = []
    conn.close()       
    c = csv.writer(open("./static/test.csv","wb"))
    c.writerow(['state', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']) 
    for row in results: 
        if (count == 0):
            writeRow.append(states[row[0]])
            writeRow.append(row[2])
            count = count +1
        elif (count == 27):
            writeRow.append(row[2]) 
            c.writerow(writeRow) 
            count = 0  
            writeRow = []
            print(writeRow)
        else: 
            writeRow.append(row[2])
            count = count + 1
    return render_template('heatmap.html')

@app.route('/bills', methods=['GET'])
def getBill():
    HEADERS = {
        "X-API-Key":"",
        "user-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }
    SearchAPI = "https://api.propublica.org/congress/v1/bills/search.json?query=firearm"
    response=requests.get(SearchAPI, headers=HEADERS).json()
    picList = ["http://image.nj.com/home/njo-media/width620/img/politics_impact/photo/screen-shot-2017-10-28-at-114911-pmpng-109d38eea9f506c8.png","https://dallasnews.imgix.net/1517022644-gun_ammunition2(Tom-Fox).JPG?auto=format%2Cenhance&crop=faces%2Centropy&fit=crop&q=40&or=0&w=1024&h=543","http://pixel.nymag.com/imgs/daily/intelligencer/2016/11/11/magazine/11-guns.w512.h600.2x.jpg","https://static.seattletimes.com/wp-content/uploads/2016/06/a1db598a-3cb1-11e6-ad3b-ad62395918a6-780x520.jpg","http://affinitymagazine.us/wp-content/uploads/2017/06/o-GUN-VIOLENCE-facebook.jpg","https://publichealthwatch.files.wordpress.com/2014/05/gun_violence.jpeg","http://www.sbhny.org/wp-content/uploads/2016/04/Gun-city-540x360.jpg","https://media.npr.org/assets/img/2015/12/06/176636323_sq-0b2c12714f9964835092a49c4e2c2e112907502c-s300-c85.jpg","https://gunnewsdaily.com/wp-content/uploads/2017/05/Darmstadter-gun-control-constitutionality.jpg","http://lawcenter.giffords.org/wp-content/uploads/2013/09/PublicSafetyScale.jpg","https://i0.wp.com/altoday.com/wp-content/uploads/2016/01/Second-Amendment-gun.jpg?fit=3872%2C2592","https://orig00.deviantart.net/f4ca/f/2015/140/2/c/ak47_by_cjustusmig-d8u3hqe.jpg","http://mediad.publicbroadcasting.net/p/wxxi/files/styles/x_large/public/201405/gun_crimes.jpeg","http://www.abc.net.au/news/image/3769268-3x2-940x627.jpg","http://www.p6firearmstraining.com/wp-content/uploads/2017/02/cropped-shooting-range-for-slider.jpg","https://www.concealedcarryofillinois.com/media/chicago-il-nra-basic-pistol-safety-class1.jpg","https://media.wired.com/photos/59d5030537e70007e32cc66a/master/w_2400,c_limit/RifflesCSA-TA-97235390.jpg","https://www.motherjones.com/wp-content/uploads/gunmap_1lead630.jpg?w=990","https://www.gannett-cdn.com/-mm-/96038deab84fc0df4a8f6cebc1dd7953f6ba372d/c=167-0-2647-1865&r=x404&c=534x401/local/-/media/2017/04/06/SiouxFalls/SiouxFalls/636270953107830683-GettyImages-140443836.jpg","http://pepperdine-graphic.com/wp-content/uploads/2016/10/gun-laws-3.jpg"]
    return render_template('carddeck.html',results=response['results'][0]['bills'], pics=picList)



@app.route('/shooting', methods=['GET'])
def getShootings():
    conn  = connect.cursor()
    conn.execute("SELECT state,COUNT(killed) FROM shooting GROUP BY state");
    results = conn.fetchall()
    shootingData=[]
    for item in results:
        shot={}
        shot['key'] = item[0]
        shot['value'] = int(item[1])
        shootingData.append(shot)
    conn.close()
    print(shootingData)
    return render_template('updatingbarchart.html', shootingData=shootingData)

@app.route('/reps', methods=['GET', 'POST'])
def getRepresentativeInformation(): 
    if request.method == 'POST': 
        searchLocation = request.form['location'] 
        params = {"address":searchLocation, "levels":"administrativeArea1"}
        civicsURL = "https://www.googleapis.com/civicinfo/v2/representatives?key="
        response = requests.get(civicsURL, params=params).json()
        try:
            officials = response['officials']
        except: 
            return render_template('representatives.html')
        returnData = []
        city = officials[0]['address'][0]['city']
        state = officials[0]['address'][0]['state']
        zipcode = officials[0]['address'][0]['zip']
        line1 = officials[0]['address'][0]['line1']
        line1 = quote(line1, safe='')
        for official in officials: 
            officialData = {};
            officialData['name'] = official['name']
            officialData['party'] = official['party']
            officialData['website'] = official['urls'][0]
            officialData['phone'] = official['phones'][0]
            returnData.append(officialData)
        mapsURL = "https://www.google.com/maps/embed/v1/place?key==" + line1 + "," + city + "+" + state + "," + zipcode
        return render_template('representatives.html', reps=returnData, map=mapsURL)
    else: 
        return render_template('representatives.html') 

@app.route('/scatter', methods=['GET', 'POST'])
def getScatterPlot(): 
    drop = [2014, 2015, 2016]
    if request.method == 'POST': 
        year = request.form['year']
        return render_template('scatter.html', years=drop, file=year)

    else: 
        return render_template('scatter.html', years=drop)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=3001)
    
