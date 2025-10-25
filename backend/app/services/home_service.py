from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from database import get_connection

def handle_get():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM enderecos")
        rows = cursor.fetchall()

        enderecos = []
        for row in rows:
            enderecos.append({
                'id': row[0],
                'cep': row[1],
                'rua': row[2],
                'numero': row[3],
                'complemento': row[4],
                'bairro': row[5],
                'cidade': row[6],
                'estado': row[7]
            })

        conn.close()
        return {'success': True, 'enderecos': enderecos}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    
def handle_delete(request):
    endereco_id = request.get_json()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM enderecos WHERE id = ?", (endereco_id,))

        conn.commit()
        conn.close()

        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def handle_post(request):
    data = request.get_json()['endereco']
    editando = request.get_json().get('editando', False)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if editando:
            cursor.execute("""
                UPDATE enderecos
                SET cep = ?, rua = ?, numero = ?, complemento = ?, bairro = ?, cidade = ?, estado = ?
                WHERE id = ?
            """, (
                data.get("cep"),
                data.get("rua"),
                data.get("numero"),
                data.get("complemento", None),
                data.get("bairro"),
                data.get("cidade"),
                data.get("estado"),
                data.get("id")
            ))
        else:
            cursor.execute("""
                INSERT INTO enderecos (cep, rua, numero, complemento, bairro, cidade, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("cep"),
                data.get("rua"),
                data.get("numero"),
                data.get("complemento", None),
                data.get("bairro"),
                data.get("cidade"),
                data.get("estado")
            ))

        conn.commit()
        conn.close()

        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def handle_buscar_cep(request_data):
    cep = request_data.args.get('cep')
    address_data = []
    try:
        options = Options()
        options.add_argument("--headless=new")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://cepbrasil.org/")
        time.sleep(1)

        input_cep = driver.find_element(By.ID, "gsc-i-id1")
        input_cep.send_keys(cep)
        botao = driver.find_element(By.CLASS_NAME, "gsc-search-button")
        botao.click()
        time.sleep(1)  

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        div_titulo = soup.select_one(".gs-title a")
        if 'Rua' in div_titulo.next:
            rua = div_titulo.contents[0].split(' - ')[0]
        else:
            rua = div_titulo.text.split(' - ')[1]

        estado = div_titulo.attrs['href'].split('/')[3].replace('-',' ').upper()
        cidade = div_titulo.attrs['href'].split('/')[4].replace('-',' ').upper()
        bairro = div_titulo.attrs['href'].split('/')[5].replace('-',' ').upper()

        driver.quit()

        address_data = {
            'cep': cep,
            'rua': rua,
            'bairro': bairro,
            'cidade': cidade,
            'estado': estado
        }
        return {'success': True, 'dados': address_data}
    
    except Exception as e:
        return {'success': False}
    

