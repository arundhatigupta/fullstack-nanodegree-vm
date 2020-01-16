from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'
                output += "</body></html>"
                self.wfile.write(bytes(output, 'utf-8'))
                # print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'
                output += "</body></html>"
                self.wfile.write(bytes(output, 'utf-8'))
                # print(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
            content_len, x = cgi.parse_header(self.headers['Content-length'])
            pdict['CONTENT-LENGTH'] = int(content_len)
            print(f"pdict = {pdict}")
            if ctype == 'multipart/form-data':
                print("in")
                try:
                    fields = cgi.parse_multipart(self.rfile, pdict)
                except Exception as e:
                    print(e)
                print(f"{fields}")
                messagecontent = fields['message']
            print("Here")
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'
            output += "</body></html>"
            self.wfile.write(bytes(output, 'utf-8'))
            print(output)
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print(f"Web Server running on port {port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()