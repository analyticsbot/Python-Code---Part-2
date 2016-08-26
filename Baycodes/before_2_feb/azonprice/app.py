        # -*- coding: cp1252 -*-
        # import the Flask class from the flask module
        from flask import Flask, render_template, request

        # create the application object
        app = Flask(__name__)


        @app.route('/', methods=['GET'])
        def home():
            return render_template('index.html')

        @app.route('/search', methods=['POST'])
        def search():
            if request.method == "POST":
                print request.json
                searchterm = request.json['searchterm']
                maxPages = request.json['maxPages']


                table = [['Item1', 'http://ecx.images-amazon.com/images/I/51SvVEAaIuL._AA160_.jpg', 21.95, 21.99, 24.06, 9.98, 1.19]]
                errors = {}
                return render_template('index.html', table = table, title = 'hello')
                
                
        if __name__ == '__main__':
            app.run(debug=True)
