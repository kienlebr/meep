from Cookie import SimpleCookie
import cgi
import meep_example_app
import time

def __main__():
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
                
    filename = '1-request.txt'
    fp = open(filename, 'rb')
    text = fp.read()
    list = text.split('\r\n')
    value = '';
    thing =[]
    
    

    app = meep_example_app.MeepExampleApp()

    environ = {}
    hold = str(list[0]).split(' ')
    value += (hold[0] + ' ')
    environ['REQUEST_METHOD'] = hold[0]
    environ['PATH_INFO'] = hold[1]
    environ['SERVER_PROTOCOL'] = hold[2]
    for x in list:
        pair = str(x).split(": ")
        if pair[0] == 'referer':
            environ['SCRIPT_NAME'] = pair[1]
        #if pair[0] == 'cookie':
        #    environ['HTTP_COOKIE'] == pair[1]

    def fake_start_response(status, headers):
        #hold = value
        #hold += (status + '\r\n')
        thing.append(status)
        thing.append(headers[0])
        #thing.append(headers[1])
        assert status ==  '200 OK'
        assert ('Content-type', 'text/html') in headers 
        #print thing
        #print headers

    html = app(environ, fake_start_response)
    #print html

    value += thing[0] + '\r\n'

    date = time.localtime()
    #print date
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
    value += str(thing[1][0]) + ': ' + str(thing[1][1]) + '\r\n'
    #print html
    html[0] = str(html[0]).strip('\n\r')
    html[0] = str(html[0]).strip('\t')
    value += '\r\n' + html[0] +'\r\n'
    #print value
    #print thing

    filename = '1-response.txt'
    fp = open(filename, 'wb')
    fp.write(value)


    
__main__()