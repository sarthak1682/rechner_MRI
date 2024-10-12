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
import requests
import pdfplumber
import re

url = 'https://www.dfg.de/formulare/60_12/v/60_12_-2023-_de.pdf'
url_2 = 'https://www.dfg.de/resource/blob/323036/2f7e7eb3e4110dd63ae9bad50a3602e4/60-12-2024-de-data.pdf'


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
    

    # Normalize user input
    normalized_user_stellenart = normalize_stellenart(info['stellenart'])
    """
    # Display user input
    put_html("<h3>Debug Information</h3>")
    put_text(f"User selected Stellenart: {normalized_user_stellenart}")
    put_text(f"User selected Stufe: {info['stufe']}")
    """
    # TODO implement better error handling
    #try:
    data = create_data(info['stellenart'], info['stufe'], info['percent'], info['jahr'], table_month, table_year)
    # except:
    #     put_text('Failed, please try again!(Try to change input)') 
    
    # New stuff
    #put_html('<div id="cost_table_container">')  # Add a container div with ID
    #/New stuff

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
    # New stuff
    #put_html('</div>')  # Close the container div
    #/New stuff


    project_sum = round(data[0][5], 2)
    zusatz = ''
    vetrags_sum = ''
    stufen_data = make_table(url_2)
    matching_row = None
    comparison_results = []
    if info['employer'] == 'DFG Normalverfahren':  # Check DRM-geber
        for row in stufen_data:
            comparison_result = (row[0] == normalized_user_stellenart and 
                                row[1] ==  str(get_index_exp(info['stufe'])))
            if comparison_result:
                matching_row = row
                break


    

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

    if matching_row:
        # Extract Monatskosten and Jahreskosten from stufen_data
        monatskosten_dfg = matching_row[3]
        jahreskosten_dfg = matching_row[2]
        # Display the information
        put_text(f"According to DFG the Monats-kosten are {monatskosten_dfg} and Jahreskosten are {jahreskosten_dfg}. See more details at: ({url_2}).")
    op = {}
    op['New Request To Calculate'] = 'window.location.reload()'
    put_buttons(op.keys(), onclick=tab_operation)
    #put_buttons(['Print Table'], onclick=lambda _: run_js('print_table()'))
    #put_html("<script>function print_table() { document.getElementById('cost_table').style.display = 'block'; window.print(); }</script>")


    #New stuff
    #put_buttons(['Print Table'], onclick=lambda _: run_js('print_table("cost_table_container")'))  # Pass container ID to the function
    #put_buttons(['Print Table'], onclick=lambda _: print_full_table(table_month, table_year))  # Call print_full_table

    #/New stuff

    hold()



op = {}
op['New Request To Calculate'] = 'window.location.reload()'


def normalize_stellenart(stellenart):
    """Remove underscores from Stellenart strings."""
    return stellenart.replace('_', '')

#New stuff
def print_table(table_id):
     run_js(f"""
        let printWindow = window.open('', 'Print Table');
        printWindow.document.write('<html><head><title>Print Table</title></head><body>');
        printWindow.document.write(document.getElementById('{table_id}').outerHTML);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
        printWindow.close();
    """) # Show the table and print it

def print_full_table(table_month, table_year):
    # Generate HTML for the full table
    html = '<html><head><title>Full Data Table</title></head><body>'
    html += '<h1>Full Data Table</h1>'

    for stellenart in table_month:
        html += f'<h2>{stellenart}</h2>'
        html += '<table><thead><tr><th>Erfahrungsstufe</th><th>Monatsgehalt</th><th>Jahresgehalt</th></tr></thead><tbody>'
        for exp in range(1, len(table_month[stellenart]) + 1):
            monthly_salary = table_month[stellenart][exp]
            yearly_salary = table_year[stellenart][exp]
            html += f'<tr><td>Stufe {exp}</td><td>{monthly_salary}</td><td>{yearly_salary}</td></tr>'
        html += '</tbody></table>'

    html += '</body></html>'

    # Open a new window and write the HTML content
    run_js(f"""
        let printWindow = window.open('', 'Print Full Table');
        printWindow.document.write(`{html}`);
        printWindow.document.close();
        printWindow.print();
        printWindow.close();
    """)

#/New stuff


def clean_string(text):
    """
    Replaces newline characters with spaces, and removes forward slashes.

    Args:
      text: The string to clean.

    Returns:
      The cleaned string.
    """
    text = text.replace('\n', ' ')  # Replace newline characters with spaces
    text = text.replace('/', '')   # Remove forward slashes
    return text


def create_stufen_data(extracted_data):
    """
    Creates a list of Stellenart-Stufe combinations with corresponding salary data.

    Args:
        extracted_data: A list of lists containing salary data extracted from the PDF.

    Returns:
        A list of lists, where each inner list represents a Stellenart-Stufe combination with salary data.
    """
    stufen_data = []

    # Hardcoded Stufe ranges for each Stellenart
    stufen_ranges = {
        'E14': ['E14 Stufe 5', 'E14 Stufe 6', 'E15 Stufe 1', 'E15 Stufe 2', 'E15 Stufe 3', 'E15 Stufe 4'],
        'E13': ['E13 Stufe 3', 'E13 Stufe 4', 'E13 Stufe 5', 'E13 Stufe 6', 'E14 Stufe 1', 'E14 Stufe 2'],
        'Ä1': ['Ä1 Stufe 2', 'Ä1 Stufe 3', 'Ä1 Stufe 4', 'Ä1 Stufe 5', 'Ä1 Stufe 6', 'Ä2 Stufe 1'],
        'E12': ['E12 Stufe 2', 'E12 Stufe 3', 'E12 Stufe 4', 'E12 Stufe 5', 'E12 Stufe 6', 'E13 Stufe 1'],
        'E9': ['E9 Stufe 1', 'E9 Stufe 2', 'E9 Stufe 3', 'E9 Stufe 4', 'E9 Stufe 5', 'E9 Stufe 6',
               'E10 Stufe 1', 'E10 Stufe 2', 'E10 Stufe 3', 'E10 Stufe 4', 'E10 Stufe 5', 'E10 Stufe 6',
               'E11 Stufe 1', 'E11 Stufe 2', 'E11 Stufe 3', 'E11 Stufe 4', 'E11 Stufe 5', 'E11 Stufe 6',
               'E12 Stufe 1', 'E12 Stufe 2', 'E12 Stufe 3', 'E12 Stufe 4', 'E12 Stufe 5', 'E12 Stufe 6'],
        'E2': ['E2 Stufe 1', 'E2 Stufe 2', 'E2 Stufe 3', 'E2 Stufe 4', 'E2 Stufe 5', 'E2 Stufe 6',
               'E3 Stufe 1', 'E3 Stufe 2', 'E3 Stufe 3', 'E3 Stufe 4', 'E3 Stufe 5', 'E3 Stufe 6',
               'E4 Stufe 1', 'E4 Stufe 2', 'E4 Stufe 3', 'E4 Stufe 4', 'E4 Stufe 5', 'E4 Stufe 6',
               'E5 Stufe 1', 'E5 Stufe 2', 'E5 Stufe 3', 'E5 Stufe 4', 'E5 Stufe 5', 'E5 Stufe 6',
               'E6 Stufe 1', 'E6 Stufe 2', 'E6 Stufe 3', 'E6 Stufe 4', 'E6 Stufe 5', 'E6 Stufe 6',
               'E7 Stufe 1', 'E7 Stufe 2', 'E7 Stufe 3', 'E7 Stufe 4', 'E7 Stufe 5', 'E7 Stufe 6',
               'E8 Stufe 1', 'E8 Stufe 2', 'E8 Stufe 3', 'E8 Stufe 4', 'E8 Stufe 5', 'E8 Stufe 6',
               'E9 Stufe 1', 'E9 Stufe 2']
    }

    for i, row in enumerate(extracted_data):
        stellenart_key = row[2].split()[0] + row[2].split()[1]  # Extract the Stellenart key (e.g., 'E14')
        #print(stellenart_key)
        if stellenart_key in stufen_ranges:
            #print("Hey")
            for stufe in stufen_ranges[stellenart_key]:
                stellenart, stufe_num = stufe.split(' Stufe ')
                stufen_data.append([stellenart, stufe_num, row[0], row[1]])
                #print(f"Stellenart: {stellenart}, Stufe: {stufe_num}, Jahreskosten: {row[0]}, Monatskosten: {row[1]}")

    return stufen_data



def make_table(url):
    
    response = requests.get(url)
    with open("test_file.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)

    with pdfplumber.open('test_file.pdf') as f:
        for i in f.pages:
            extracted_table = i.extract_tables()
    del extracted_table[0][1]
    table = []
    for i in range(2,8):
        data = extracted_table[0][i]
        table.append(data[1:4])

    #print(table)
    stufen_data = create_stufen_data(table)
    
    #print(extracted_table)
    return stufen_data


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
    #salary = salary + 50
    #salary = float(table_month[stellenart][exp] * percent / 100)
    #sozial = table_year[stellenart][exp]
    sozial = float(table_year[stellenart][exp]) * percent / 100 - salary*12
    ag_brutto = salary + sozial/12
    jahreskosten = table_year[stellenart][exp]
    jahreskosten = jahreskosten + 50
    data.append(
        [year, stufe, round(salary, 2), round(sozial, 2),
         round(ag_brutto, 2),
         round(jahreskosten, 2)])
    
    #data[0][4] += 50  # Add 50 to AG-Monats-Brutto
    return data

app.add_url_rule('/', 'webio_view', webio_view(main), methods = ['GET', 'POST']) #newLine

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
