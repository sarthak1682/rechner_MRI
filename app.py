from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import argparse
from pywebio.platform.tornado_http import start_server as start_http_server
from pywebio import start_server as start_ws_server
import data.dataset as dt
from scrapping import scrape_data
import datetime
import re
from flask import Flask #newLine
from pywebio.platform.flask import webio_view #newLine

app = Flask(__name__) #newLine
app.secret_key = "123" #newLine

def main():
    set_env(title='Rechner für DRM-Personalkosten')
    img = open('img/med3.jpg', 'rb').read()
    put_row([
        put_image(img, width='90px', height='90px'),
        None,
        put_html('<h1>Fakultät für Medizin</h1>')
    ])
    # get current year right now
    year = datetime.datetime.now().year
    table_month, table_year = scrape_data(year)


    info = input_group("Basic Information", [
        select('DRM-Geber', dt.drm_geber, name='employer'),
        select('Stellenart', table_month.keys(), name='stellenart'),
        radio("Erfahrungsstufe", options=dt.stufe, name='stufe'),
        input("Prozentsatz: ", type=FLOAT, name='percent', value=100),
        input('Jahr', type=NUMBER, name='jahr', value=year),
    ], validate=is_valid)
    put_text(info['employer'], ', ', info['stellenart'], ', ', info['stufe'], ', ',
             info['percent'], '%')
    
    # TODO implement better error handling
    #try:
    data = create_data(info['stellenart'], info['stufe'], info['percent'], info['jahr'], table_month, table_year)
    # except:
    #     put_text('Failed, please try again!(Try to change input)') 

    put_table([
        ['Type', 'Value'],
        [put_markdown('`Jahr`'), data[0][0]],
        [put_markdown('`Erfahrungsstufe`'), data[0][1]],
        #[put_markdown('`AN-Monats-Brutto`'), format_number(data[0][2])],
        [put_markdown('`AG-Monat-Brutto`'), format_number(data[0][2])],
        [put_markdown('`Jahressonderzahlung`'), format_number(data[0][3])],
        [put_markdown('`AG-Monats-Kosten + Jahressonderzahlung`'), format_number(data[0][4])],
        [put_markdown('`AG-Jahr-Kosten`'), format_number(data[0][5])],

    ])
    project_sum = round(data[0][5], 2)
    zusatz = ''
    vetrags_sum = ''
    if info['employer'] in dt.drm_geber_spec:
        tum_overhead = round(int(project_sum) * dt.drm_geber_spec[info['employer']], 2)
        zusatz = 'Overhead: ' + format_number(tum_overhead)
        vetrags_sum = 'Vertragsumme für Personalstelle über Laufzeit: ' + format_number(project_sum + tum_overhead)
    project_sum = format_number(project_sum)
    string_to_print = 'Projektsumme für Personalstelle über Laufzeit: ' + str(
        project_sum)
    put_html("<h2>%s</h2>" % string_to_print)
    put_text(zusatz)
    put_text(vetrags_sum)
    op = {}
    op['New Request To Calculate'] = 'window.location.reload()'
    put_buttons(op.keys(), onclick=tab_operation)
    hold()


op = {}
op['New Request To Calculate'] = 'window.location.reload()'

def format_number(num):
    num = "{:,}".format(num)
    num = str(num)
    num = num.replace(',', '.')
    num = ','.join(num.rsplit('.', 1))
    return num


def is_valid(info):
    if info['stufe'] is None:
        return ('stufe', 'Please select the Erfahrungsstufe')
    if info['percent'] is None:
        return ('percent', 'Please select the percentage')


def tab_operation(choice):
    run_js(op[choice])


def get_index_exp(exp):
    #For string exp find first number and stop
    return int(re.search(r'\d+', exp).group())

def create_data(stellenart, stufe, percent, year, table_month, table_year):
    data = []
    # ballungsraumzulage = 132.5
    # salary = dt.tarif[job][get_index_exp(exp)] * percent / 100
    # if dt.tarif[job][9] == True:
    #     salary += ballungsraumzulage
    # sozial = salary * 0.26275 + 6.99
    # ag_brutto = salary + sozial
    # sonderzahlung = None
    # if dt.tarif[job][10] == False:
    #     sonderzahlung = dt.tarif[job][1] / 100
    #     jahreskosten = round(ag_brutto * 12 + ag_brutto * sonderzahlung, 2)
    #     sonderzahlung = str(int(sonderzahlung * 100)) + '%'
    # else:
    #     jahreskosten = round(ag_brutto * 12, 2)
    #scrape if year is different from today:
    if year != datetime.datetime.now().year:
        table_month, table_year = scrape_data(year)
    exp = get_index_exp(stufe)
    salary = float(table_month[stellenart][exp]) * percent / 100
    #salary = float(table_month[stellenart][exp] * percent / 100)
    #sozial = table_year[stellenart][exp]
    sozial = float(table_year[stellenart][exp]) * percent / 100 - salary*12
    ag_brutto = salary + sozial/12
    jahreskosten = table_year[stellenart][exp]
    data.append(
        [year, stufe, round(salary, 2), round(sozial, 2),
         round(ag_brutto, 2),
         round(jahreskosten, 2)])
    return data

app.add_url_rule('/', 'webio_view', webio_view(main), methods = ['GET', 'POST'] #newLine

if __name__ == '__main__':
    app.run(debug= True) 
    #oldLineparser = argparse.ArgumentParser() #oldLine
    #oldLineparser.add_argument("-p", "--port", type=int, default=5000)
    #oldLineparser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    #oldLineargs = parser.parse_args()
    #oldLineif args.http:
        #oldLinestart_http_server(main, port=args.port)
    #oldLineelse:
       #oldLine start_ws_server(main, port=args.port, websocket_ping_interval=30)
