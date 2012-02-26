from Cookie import SimpleCookie
import cgi
import meep_example_app
import time

def format_return(data):
    weekdays = {0: 'Sun',
                1: 'Mon',
                2: 'Tue',
                3: 'Wed',
                4: 'Thu',
                5: 'Fri',
                6: 'Sat'
                }
    months = {1: 'Jan',
                2: 'Feb',
                3: 'Mar',
                4: 'Apr',
                5: 'May',
                6: 'Jun',
                7: 'Jul',
                8: 'Aug',
                9: 'Sep',
                10: 'Oct',
                11: 'Nov',
                12: 'Dec'
                }
                
    #filename = '1-request.txt'
    #fp = open(filename, 'rb')
    #text = fp.read()
    #text = data;
    list = data.split('\r\n')
    value = '';
    thing =[]
    
    

    app = meep_example_app.MeepExampleApp()

    environ = {}
    hold = str(list[0]).split(' ')
    value += ('HTTP/1.0' + ' ')
    environ['REQUEST_METHOD'] = hold[0]
    environ['PATH_INFO'] = hold[1]
    environ['SERVER_PROTOCOL'] = hold[2]
    for x in list:
        pair = str(x).split(": ")
        if pair[0] == 'Host':
            #print pair[1]
            environ['SCRIPT_NAME'] = pair[1]

    def fake_start_response(status, headers):
        thing.append(status)
        thing.append(headers[0])
        #assert status ==  '200 OK'
        #assert ('Content-type', 'text/html') in headers 

    html = app(environ, fake_start_response)

    value += thing[0] + '\r\n'

    date = time.localtime()
    value+= ("Date: ")
    value+= (weekdays[date[6]])
    value+= (', ')
    value+= (str(date[2]))
    value+= (' ')
    value+= (months[date[1]])
    value+= (' ')
    value+= (str(date[0]))
    value+= (' ')
    value+= (str(date[3]))
    value+= (':')
    value+= (str(date[4]))
    value+= (':')
    value+= (str(date[5]))
    value+= (" GMT\r\n")
    value += 'Server: WSGIServer/0.1 Python/2.5\r\n'
    #value += 'Content-type: text/plain\r\n'
    value += str(thing[1][0]) + ': ' + str(thing[1][1]) + '\r\n'
    value += 'Content Length: '
    value += str(html[0].__len__()) + '\r\n'
    html[0] = str(html[0]).strip('\n\r')
    html[0] = str(html[0]).strip('\n')
    #html[0] = str(html[0]).strip('<html>')
    #html[0] = str(html[0]).strip('</html>')
            
    value += '\r\n' + html[0] + '\r\n'

    #print value
    return value

    #filename = '1-response.txt'
    #fp = open(filename, 'wb')
    #fp.write(value)