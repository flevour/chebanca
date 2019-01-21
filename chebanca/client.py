import requests
import os
import json
import urllib3

urllib3.disable_warnings()

class HttpAdapter(object):
  def __init__(self, **kwargs):
    self.username = os.environ['CHEBANCA_USER']
    self.password = os.environ['CHEBANCA_PASS']
    self.date = os.environ['CHEBANCA_DATE']
    self.user_id = os.environ['CHEBANCA_USER_ID']
    self.s = requests.Session()
    self.s.verify = False
    self.s.headers = {
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    # self.s.cookies = cookielib.LWPCookieJar(filename="test.cookies")
    # self.s.cookies.load(ignore_discard=True, ignore_expires=True)

  def login(self):
    data = {
      'USER': self.username,
      'PIN': self.password,
      'DATE': self.date,
      'target': "https://www.chebanca.it/portalserver/services/login?TARGET2=https://www.chebanca.it/portalserver/homebanking/home",
    }
    response = self.s.post('https://clienti.chebanca.it/sm/login.fcc', data)
    response.raise_for_status()
    # self.s.cookies.save(ignore_discard=True, ignore_expires=True)

  def get(self, url):
    url = 'https://api.chebanca.it/private/{}'.format(url)
    response = self.s.get(url)
    response.raise_for_status()
    return response.json()

  def list_products(self):
    return self.get('customers/{}/products'.format(self.user_id))

  def product_transactions(self, product_id):
    url = 'customers/{user_id}/products/{product_id}/transactions/retrieve?accountingElementsNumber=15'
    url = url.format(user_id=self.user_id, product_id=product_id)
    return self.get(url)

  def product_balance(self, product_id):
    url = 'customers/{user_id}/products/{product_id}/balance/retrieve'
    url = url.format(user_id=self.user_id, product_id=product_id)
    return self.get(url)


class FileAdapter(object):
  def __init__(self, **kwargs):
    pass

  def login(self):
    pass

  def list_products(self):
    with open("../responses/list-products.json") as f:
      return json.load(f)

  def product_transactions(self, product_id):
    with open("../responses/product-{product_id}-transactions.json".format(product_id=product_id)) as f:
      return json.load(f)

  def product_balance(self, product_id):
    with open("../responses/product-{product_id}-balance.json".format(product_id=product_id)) as f:
      return json.load(f)


class CheBanca(object):
  def __init__(self, adapter):
    self.adapter = adapter

  def login(self):
    return self.adapter.login()

  def list_products(self):
    return self.adapter.list_products()

  def product_transactions(self, product_id):
    return self.adapter.product_transactions(product_id)

  def product_balance(self, product_id):
    return self.adapter.product_balance(product_id)

def file_client():
  adapter = FileAdapter()
  client = CheBanca(adapter)
  client.login()
  return client

def http_client():
  adapter = HttpAdapter()
  client = CheBanca(adapter)
  client.login()
  return client

if __name__ == '__main__':
  file_adapter = FileAdapter()
  client = CheBanca(file_adapter)
  client.login()
  products = client.list_products()
  for product in [p for p in products['data']['products'] if p['status']['code'] == 'A']:
    print("{}: {}".format(product['type']['nickname'], product['productId']))
    balance = client.product_balance(product['productId'])['data']
    print("DATE: {}".format(balance['date']))
    print("Account Balance: {}".format(monetaryamount(balance['accountBalance'])))
    print("Available Balance: {}".format(monetaryamount(balance['availableBalance'])))
    print("=" * 30)
