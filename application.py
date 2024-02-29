from flask import Flask, request, render_template
import requests

application = Flask(__name__)

def convertDict(data):
 if isinstance(data, list): # Check if data is a list
     if data:
         return data[0]
     else:
         return None
 else:
     return data

@application.route('/', methods=['GET', 'POST'])
def index():
   return render_template('default.html')

@application.route('/search', methods=['GET'])
def search():
   message = "ticker invalid, please enter another ticker!"
   ticker = request.args.get('ticker')
   API_KEY = '74982aa3f791602204f157617228ecc88253d8bb'

   response1 = requests.get(f'https://api.tiingo.com/tiingo/daily/{ticker}?token={API_KEY}')
   data1 = response1.json()
   if data1.get('detail') == 'Not found.':
     return render_template('error.html')
   data1 = convertDict(data1)

   response2 = requests.get(f'https://api.tiingo.com/iex/{ticker}?token={API_KEY}')
   data2 = response2.json()
   if not data2:
     return render_template('error.html')
   data2 = convertDict(data2)

   data = {**data1, **data2}

   data = {k: v for k, v in data.items() if v is not None}

   if 'last' in data and 'prevClose' in data:

      change = data['last'] - data['prevClose']
      change_percent = (change / data['prevClose']) * 100
      change_percent_str = f"{change_percent:.2%}"

      data['change'] = change
      data['change_percent'] = change_percent_str

   return render_template('result.html', data=data)

if __name__ == '__main__':
   application.run(debug=True)
