CMPUT404-assignment-web-client
==============================

CMPUT404-assignment-web-client

See requirements.org (plain-text) for a description of the project.

Make a simple web-client like curl or wget

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle, 
https://github.com/tywtyw2002, and https://github.com/treedust

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

Citation:
========================
stolen from Adam Smith https://stackoverflow.com/users/3058609/adam-smith
From Stackoverflow
https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3
"result = urlencode(payload, quote_via=quote_plus)" I learnt how to use urlencode
and used in line 44, 148, 156 in httpclient.py

stolen from stwhite https://stackoverflow.com/users/415763/stwhite
From Stackoverflow
https://stackoverflow.com/questions/10115126/python-requests-close-http-connection
"r = requests.post(url=url, data=body, headers={'Connection':'close'})" I learnt how to use "connection:close"
and used in line 126, 164 in httpclient.py

refer to https://docs.python.org/3/library/urllib.parse.html
"urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)"
 used in line 44, 60, 71 in httpclient.py
 Example of http GET and POST Request Message is from 
 https://www.tutorialspoint.com/http/http_requests.htm#:~:text=The%20GET%20method%20is%20used,other%20effect%20on%20the%20data. 

 Collaboration:
 ========================
 I consult with Shuwei Wang(ccid:shuwei4) about using "connection: close" in payload to reduce running time, fields in payload and if we need to handle args in GET request method.

