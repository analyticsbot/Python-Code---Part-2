
table = [[u'B00NVDO2AW', u'Star Wars LEGO Snowspeeder 75074', u'http://ecx.images-amazon .com/images/I/61FcEMHoF1L._AA160_.jpg', '146', 13.79, 14.04, 14.04, 14.04, 0.0, 4], [u'B012NODIJA', u'LEGO Star Wars TM 75137: Carbon-Freezing Chamber Mixed', u'http://ecx.images-amazon.com/images/I/61Hj1Xlus3L._AA160_.jpg', '72', 19.98, 23.15, 22.29, 23.22, 0.0, 4], [u'B00NVDLI7M', u'LEGO Creator 31029: Cargo Heli', u'http://ecx.images-amazon.com/images/I/61fmz3bV22L._AA160_.jpg', '177', 7.98, 7.67, 7.74, 8.51, 4.04, 5], [u'B00O1G4N48', u'LEGO Marvel Super Heroes', u'http:/ /ecx.images-amazon.com/images/I/61v220zGzwL._PI_PJStripe-Prime-Only-500px,TopLef t,0,0_AA160_.jpg', 'NA', 0.0, 'NA', 'NA', 'NA', 'NA', 4], ['NA', 'NA', 'NA', 'NA ', 'NA', 'NA', 'NA', 'NA', 'NA'], [u'B00SDTT1QY', u'LEGO Minecraft The Dungeon', u'http://ecx.images-amazon.com/images/I/61POi67xsfL._AA160_.jpg', u'256', 16.74 , 13.86, 14.71, 15.48, 20.78, 5], [u'B00NGJO9AO', u"LEGO Disney Princess 41062: Elsa's Sparkling Ice Castle", u'http://ecx.images-amazon.com/images/I/61rtxjWED% 2BL._AA160_.jpg', '25', 24.99, 29.26, 27.1, 29.26, 0.0, 4], [u'B00F3B2Y6O', u'LE GO Juniors 10667: Construction', u'http://ecx.images-amazon.com/images/I/61hFydu RzdL._AA160_.jpg', '308', 18.95, 13.93, 12.23, 13.93, 54.95, 6], [u'B00NVDMREA', u'LEGO Creator 31028 Sea Plane', u'http://ecx.images-amazon.com/images/I/61GarQ yjVCL._AA160_.jpg', '152', 4.97, 7.74, 'NA', 'NA', 0.0, 4], [u'B00NVDNDUW', u'LE GO Creator 31032: Red Creatures', u'http://ecx.images-amazon.com/images/I/61rfvk kvHIL._AA160_.jpg', '245', 12.99, 11.44, 11.61, 12.38, 13.55, 5], [u'B00NVDLB56' , u'LEGO Speed Champions 75899: LaFerrari', u'http://ecx.images-amazon.com/image s/I/61ASrE-yS1L._AA160_.jpg', '243', 12.99, 11.61, 12.99, 12.37, 11.89, 5], [u'B 00SDTZ0QO', u'LEGO 60091 City Explorers Deep Sea Starter Set', u'http://ecx.imag es-amazon.com/images/I/61XRd9128fL._AA160_.jpg', '53', 6.54, 6.54, 6.96, 7.74, 0.0, 4], [u'B00NVDOWUW', u'LEGO Classic 10692 LEGO Creative Bricks', u'http://ecx .images-amazon.com/images/I/51SvVEAaIuL._AA160_.jpg', '164', 12.97, 10.86, 10.06 , 11.61, 28.93, 6], [u'B00PY3EYSW', u'LEGO Classic 10695: LEGO Creative Building Box', u'http://ecx.images-amazon.com/images/I/61Lb7-oMXZL._AA160_.jpg', '103', 19.98, 20.9, 20.62, 20.9, 0.0, 4], [u'B00NVDJ7VG', u'LEGO Speed Champions 75910: Porsche 918 Spyder', u'http://ecx.images-amazon.com/images/I/61Oh8fUJx0L._AA160 _.jpg', '176', 11.45, 10.99, 10.06, 12.38, 13.82, 6], [u'B00NGJCKS2', u'LEGO Tec hnic 42031: Cherry Picker', u'http://ecx.images-amazon.com/images/I/51VYmmAFaGL. _AA160_.jpg', '136', 7.99, 7.67, 6.88, 13.15, 16.13, 6]]
table = [t  for t in table if t.count('NA')<6]
tableString = ''

def returnPrice(i):
    if i != 'NA':
        return '&pound;'+str(i)
    else:
        return str(i)
    
for t in table:
    tableString +=""" <tr>"""
    for i in t:
        if t.index(i) !=9:
            print t.index(i)
            if t.index(i) ==3:
                tableString += '''<td style='text-align:center;vertical-align:middle' height="50"><img src=''' +str(i)+''' alt="" border="3"
                                    height="100" width="100" /></td>'''
            elif t.index(i) ==5:
                if t.index(i) == t[9]:
                    tableString += '''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                > <a href="http://www.amazon.co.uk/dp/'''+t[0]+'''"><i>''' +returnPrice(i)+'''</i></a></td>'''
                else:
                    tableString += '''<td style='text-align:center;vertical-align:middle' height="50" >
                                    <a href="http://www.amazon.co.uk/dp/'''+t[0]+'''"><i>''' +returnPrice(i)+'''</i></a></td>'''
            
            elif t.index(i) ==6:
                if t.index(i) == t[9]:
                    tableString += '''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                > <a href="http://www.amazon.fr/dp/'''+t[0]+'''"><i>''' +returnPrice(i)+'''</i></a></td>'''
                else:
                    tableString += '''<td style='text-align:center;vertical-align:middle' height="50" >
                                    <a href="http://www.amazon.co.uk/dp/'''+t[0]+'''"><i>''' +returnPrice(i)+'''</i></a></td>'''
            elif t.index(i) ==7:
                if t.index(i) == t[9]:
                    tableString += '''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                > <a href="http://www.amazon.it/dp/'''+t[0]+'''"><i>''' +returnPrice(i)+'''</i></a></td>'''
                else:
                    tableString += '''<td style='text-align:center;vertical-align:middle' height="50" >
                                    <a href="http://www.amazon.it/dp/'''+t[0]+'''"><i>''' +returnPrice(i)+'''</i></a></td>'''
            elif t.index(i) ==8:
                if t.index(i) == t[9]:
                    tableString += '''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                > <a href="http://www.amazon.es/dp/'''+t[0]+'''"><i>''' +returnPrice(i)+'''</i></a></td>'''
                else:
                    tableString += '''<td style='text-align:center;vertical-align:middle' height="50" >
                                    <a href="http://www.amazon.es/dp/'''+t[0]+'''"><i>''' +returnPrice(i)+'''</i></a></td>'''
            else:
                try:
                    if t.index(i) == t[9]:
                        tableString += '''<td style='text-align:center;vertical-align:middle' height="50"
                         bgcolor="#66CDAA" >''' + str(i) +'''</td>'''
                    else:
                        tableString += '''<td style='text-align:center;vertical-align:middle' height="50"
                            >''' + str(i) +'''</td>'''
                except:
                    print t
    
    tableString += """</tr>"""   

tableString += """</tbody></table>"""
