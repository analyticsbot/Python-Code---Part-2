from unidecode import unidecode
table = [[u'B00CH08M0G', u'Sony DSCHX50 Compact Digital Camera - Black (20.4MP, 30x Optical Zoom) 3 inch LCD', u'http://ecx.images-amazon.com/images/I/41RbnhizpbL._AA160_.jpg', '6184', 179.99, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00BHXVX3M', u'Sony DSCHX300V Digital Compact Bridge Camera with High Quality Lens (Electronic View Finder, 20.4 MP, 50x Optical...', u'http://ecx.images-amazon.com/images/I/51YmG1sV5L._AA160_.jpg', '2795', 189.0, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00IGL9SLW', u'Sony DSCWX220 Digital Compact Camera with Wi-Fi and NFC (18.2 MP, 10x Optical Zoom) - Black', u'http://ecx.images-amazon.com/images/I/41ziw6JlWBL._AA160_.jpg', '5659', 109.0, 157.41, 'NA', 179.45, 190.18, 0.0,4], [u'B00KW3BJ1Y', u'Sony DSCRX100M3 Advanced Digital Compact Premium Camera with Large 1-inch Sensor, Bright High Quality Lens and...', u'http://ecx.images-amazon.com/images/I/41N9s54kYNL._AA160_.jpg', '14778', 569.0, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00IE9X HE0', u'Sony ILCE6000LB Compact System Camera with SELP1650 Lens Kit (Fast Auto Focus, 24.3 MP, Electronic View Finder...', u'http://ecx.images-amazon.com/image s/I/411b0fwXcPL._AA160_.jpg', '7031', 489.0, 459.21, 451.77, 463.85, 459.55, 8.24, 6], [u'B00IGL9PJC', u'Sony DSCHX400V Digital Compact Bridge Camera with High Quality Lens (Electronic View Finder, 20.4 MP, 50x Optical...', u'http://ecx.ima ges-amazon.com/images/I/519vhRU+hOL._AA160_.jpg', '4759', 287.0, 283.79, 'NA', ' NA', 'NA', 1.13, 5], [u'B00BHXVWVU', u'Sony Alpha A58 Translucent Mirror Interch angeable Lens Camera with 18-55mm Lens (20MP)', u'http://ecx.images-amazon.com/i mages/I/5136KbAqI0L._AA160_.jpg', '2471', 294.9, 271.35, 284.76, 293.0, 289.13, 8.68, 5], [u'B00HR30ZQW', u'Sony DSCW830 Digital Compact Camera - Black (20.1MP, 8x Optical Zoom) 2.7 inch LCD', u'http://ecx.images-amazon.com/images/I/41Vyu8B k12L._AA160_.jpg', '6961', 77.89, 92.5, 92.5, 92.5, 92.5, 0.0, 4], [u'B00MTZI4Y8 ', u'Sony ILCE5100L Compact System Camera with 16-50 Lens (24.3 MP, 180 Degrees Tiltable LCD, Fast Hybrid Auto Focus...', u'http://ecx.images-amazon.com/images/ I/41lZIaql15L._AA160_.jpg', '7157', 391.99, 407.34, 442.2, 439.11, 385.77, 1.61, 8], [u'B010X7TG0Y', u'Sony DSCRX100M4 Advanced Digital Compact Premium Camera w ith High Speed Shutter, 4K Recording and Super Slow Motion...', u'http://ecx.ima ges-amazon.com/images/I/41eW0C302jL._AA160_.jpg', '15164', 749.0, 'NA', 'NA', 'N A', 'NA', 0.0, 4], [u'B008CNMZDW', u'Sony DSCRX100 Advanced Digital Compact Prem ium Camera with Large 1-inch Sensor and Bright High Quality Lens', u'http://ecx. images-amazon.com/images/I/41JNvHrzCAL._AA160_.jpg', 'NA', 319.0, 'NA', 'NA', 'N A', 'NA', 0.0, 4], [u'B00HNT5NG2', u'Sony ILCE5000L Compact System Camera with S EL-1650 Zoom Lens (20.1 MP, 180 Degrees Tiltable LCD, Wi-Fi and NFC...', u'http: //ecx.images-amazon.com/images/I/41AyLhZFIVL._AA160_.jpg', '5462', 249.0, 271.74 , 224.18, 287.04, 254.34, 11.07, 6], [u'B00WSIAE4Y', u'Sony DSCWX500 Digital Com pact High Zoom Travel Camera with 180 Degrees Tiltable LCD Screen (18.2 MP, 30 x Optical...', u'http://ecx.images-amazon.com/images/I/41hl7QCZq8L._AA160_.jpg', '3690', 202.27, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00HH8A60C', u'Sony ILCE5000 L Compact System Camera with SEL-1650 Zoom Lens (20.1 MP, 180 Degrees Tiltable L CD, Wi-Fi and NFC...', u'http://ecx.images-amazon.com/images/I/51Qm1udYpNL._AA16 0_.jpg', '1164', 239.0, 270.57, 228.42, 252.8, 254.34, 4.63, 6], [u'B00IGL9PQA', u'Sony DSCH400 Digital Compact Bridge Camera (20.1 MP, 63x Optical High Zoom, E lectronic View Finder) - Black', u'http://ecx.images-amazon.com/images/I/51h80Gv w12L._AA160_.jpg', '1863', 158.99, 191.72, 266.71, 199.08, 229.61, 0.0, 4], [u'B 00G37XCVI', u'Sony DSCH300 Digital Compact Bridge Camera (20.1 MP, 35x Optical H igh Zoom) - Black', u'http://ecx.images-amazon.com/images/I/51ofKTbBPnL._AA160_. jpg', '606', 111.49, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00IGL9PSS', u'Sony DSC HX60 Digital Compact High Zoom Travel Camera with Wi-Fi and NFC ( 20.4 MP, 30x O ptical Zoom) - Black', u'http://ecx.images-amazon.com/images/I/41W9E7oct4L._AA16 0_.jpg', '487', 167.49, 198.65, 198.65, 198.65, 198.65, 0.0, 4], [u'B00FYPUXPI', u'Sony DSCRX10 Advanced Digital Compact Bridge Camera with Large 1-inch Sensor and High Quality Lens (Tiltable LCD...', u'http://ecx.images-amazon.com/images/I /41xfTU+o5WL._AA160_.jpg', '32115', 538.99, 705.99, 741.43, 706.83, 'NA', 0.0, 4 ], [u'B003OUX6TA', u'Sony NEX5KB Alpha Compact System Camera - 18-55mm F3.5-5.6 OSS Lens - Black', u'http://ecx.images-amazon.com/images/I/51S+IxiJhzL._AA160_.j pg', u'128', 150.0, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00WJLUKKI', u'Sony DSCH X90 Digital Compact High Zoom Travel Camera with 180 Degrees Tiltable LCD Screen and View Finder (18.2...', u'http://ecx.images-amazon.com/images/I/41eDm7aZaSL. _AA160_.jpg', '11112', 294.99, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00FWUDEEC', u'Sony ILCE7B Full Frame Compact System Camera with 28-70 mm Zoom Lens ( 24.3 MP , 117 Points Hybrid AutoFocus, 3.0...', u'http://ecx.images-amazon.com/images/I/ 510OOSmhdnL._AA160_.jpg', '27498', 875.0, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B0 0IK01PJC', u'Sony DSCW800 Digital Compact Camera (20.1 MP, 5x Optical Zoom) - Bl ack', u'http://ecx.images-amazon.com/images/I/41JRFY5W6tL._AA160_.jpg', '69', 59.99, 72.51, 'NA', 80.95, 72.51, 0.0, 4], [u'B00MTZI376', u'Sony ILCE5100L Compac t System Camera - Black', u'http://ecx.images-amazon.com/images/I/51hKen+vrXL._A A160_.jpg', '2625', 344.99, 354.52, 374.91, 374.91, 360.98, 0.0, 4], [u'B00IGL9P Q0', u'Sony DSCWX350 Digital Compact Camera with Wi-Fi and NFC (18.2 MP, 20x Opt ical Zoom) - Black', u'http://ecx.images-amazon.com/images/I/41IwBcbgU4L._AA160_ .jpg', '4004', 138.99, 'NA', 186.18, 131.42, 'NA', 5.76, 7]]
table = [t  for t in table if t.count('NA')<6]

def returnPrice(i):
    if i != 'NA':
        return '&pound;'+str(i)
    else:
        return str(i)
    
def returnTableHTMl(table):
    tableString= '''<table class = "table table-bordered table-striped table-curved" id = "myTable">
                    <thead>
                                            <tr>
                                                <th>ASIN</th>
                                                <th>Title</th>
                                                <th>Image</th>
                                                <th>Sales Rank</th>
                                                <th>UK Price</th>
                                                <th>FR Price</th>
                                                <th>IT Price</th>
                                                <th>ES Price</th>
                                                <th>DE Price</th>
                                                <th>ROI (%)</th>
                                            </tr>
                                        </thead>
                    <tbody> '''
    
    for t in table:
        #print t
        #break
        tableString +=""" <tr>"""
        count = -1
        for i in t:
            print i
            if t.index(i) !=10:
                if t.index(i) ==2:
                    tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50"><img src=''' +i+''' alt="" border="3"
                                        height="100" width="100" /></td>''')
                elif t.index(i) ==4:
                    if t.index(i) == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.co.uk/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.co.uk/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                
                elif t.index(i) ==5:
                    print 'a'
                    if t.index(i) == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.fr/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.fr/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                elif t.index(i) ==6:
                    if t.index(i) == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.it/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.it/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                elif t.index(i) ==7:
                    if t.index(i) == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.es/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.es/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                elif t.index(i) ==8:
                    if t.index(i) == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.de/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.de/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                        
                else:
                    if t.index(i) == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50"
                             bgcolor="#66CDAA" >''' + str(i) +'''</td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50"
                                >''' + str(i) +'''</td>''')
        
        tableString += """</tr>"""
        break

    tableString += """</tbody></table>"""
    f = open('tableString.txt', 'wb')
    f.write(tableString)
    f.close()
    
     
    return tableString
returnTableHTMl(table)
#print returnTableHTMl(table)
