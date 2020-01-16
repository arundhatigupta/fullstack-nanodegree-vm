import cgi
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # if self.path.endswith("/hello"):
            #     self.send_response(200)
            #     self.send_header('Content-Type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>Hello!</h1>"
            #     output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'
            #     output += "</body></html>"
            #     self.wfile.write(bytes(output, 'utf-8'))
            #     # print(output)
            #     return

            # if self.path.endswith("/hola"):
            #     self.send_response(200)
            #     self.send_header('Content-Type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>&#161 Hola !</h1>"
            #     output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'
            #     output += "</body></html>"
            #     self.wfile.write(bytes(output, 'utf-8'))
            #     # print(output)
            #     return
            
            if self.path.endswith('/edit'):
                restaurantIDPath = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if restaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += restaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type = 'text' placeholder = '%s' >" % restaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form></body></html>"
                    self.wfile.write(bytes(output, 'utf-8'))
                    return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(bytes(output, 'utf-8'))
                return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                # Create a Link to create a new menu item
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    # Add Edit and Delete Links
                    output += "<a href ='/restaurants/%s/edit' >Edit </a> " % restaurant.id
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(bytes(output, 'utf-8'))
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # self.send_response(301)
            # self.send_header('Content-Type', 'text/html')
            # self.end_headers()
            # ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            # pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
            # content_len, x = cgi.parse_header(self.headers['Content-length'])
            # pdict['CONTENT-LENGTH'] = int(content_len)
            # print(f"pdict = {pdict}")
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     messagecontent = fields['message']
            # output = ""
            # output += "<html><body>"
            # output += " <h2> Okay, how about this: </h2>"
            # output += "<h1> %s </h1>" % messagecontent[0]
            # output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'
            # output += "</body></html>"
            # self.wfile.write(bytes(output, 'utf-8'))

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                content_len, x = cgi.parse_header(self.headers['Content-length'])
                pdict['CONTENT-LENGTH'] = int(content_len)
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                restaurantIDPath = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if restaurantQuery != []:
                    restaurantQuery.name = messagecontent[0]
                    session.add(restaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    elf.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                content_len, x = cgi.parse_header(self.headers['Content-length'])
                pdict['CONTENT-LENGTH'] = int(content_len)
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            # print(output)
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