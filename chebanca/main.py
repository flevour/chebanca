import click
from .client import file_client, http_client
from terminaltables import AsciiTable

client = file_client()
# client = http_client()

def monetaryamount(data):
  return "{} {}".format(data['amount'], data['currency'])


@click.group()
def cli():
    pass


@cli.command()
def balances():
  products = client.list_products()
  for product in [p for p in products['data']['products'] if p['status']['code'] == 'A']:
    print("{}: {}".format(product['type']['nickname'], product['productId']))
    balance = client.product_balance(product['productId'])['data']
    print("DATE: {}".format(balance['date']))
    print("Account Balance: {}".format(monetaryamount(balance['accountBalance'])))
    print("Available Balance: {}".format(monetaryamount(balance['availableBalance'])))
    print("=" * 30)


@cli.command()
@click.argument('product_id')
def transactions(product_id):
    transactions = client.product_transactions(product_id)['data']
    table_data = [
        ["Data Contabile", "Data Valuta", "Importo", "Descrizione"]
    ]
    for transaction in transactions['transactionsAccounting']:
        table_data.append([
            transaction['dateAccountingCurrency'],
            transaction['dateLiquidationValue'],
            monetaryamount(transaction['amountTransaction']),
            transaction['extendedDescription'],
        ])
    table = AsciiTable(table_data)
    print(table.table)





if __name__ == '__main__':
    cli()
