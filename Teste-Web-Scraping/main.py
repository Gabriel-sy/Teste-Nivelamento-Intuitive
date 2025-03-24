import requests
from zipfile import ZipFile
import os
from bs4 import BeautifulSoup

def main():
    try:
        response = requests.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        annexes = ["Anexo I.", "Anexo II."]
        downloaded_files = []

        for annex_name in annexes:
            file_path = download_annex(soup, annex_name)
            if file_path:
                downloaded_files.append(file_path)

        if downloaded_files:
            create_zip_archive(downloaded_files)
        else:
            print("Nenhum anexo foi baixado.")
    
    except requests.RequestException as e:
        print(f"Erro de conexão: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def download_annex(soup, annex_name):
    first_annex_element = soup.find('a', string=annex_name)
    if not first_annex_element:
        print(f"{annex_name} não encontrado")
        return None

    href = first_annex_element.get('href')
    if not href:
        print(f"{annex_name} sem link de download")
        return None

    try:
        print(f"Baixando {annex_name}...")
        file_response = requests.get(href)
        file_response.raise_for_status()
        
        file_path = annex_name.replace(".", "") + '.pdf'
        with open(file_path, 'wb') as file:
            file.write(file_response.content)
        
        print(f"Download feito com sucesso: {annex_name}")
        return file_path
    
    except requests.RequestException as e:
        print(f"Erro ao baixar {annex_name}: {e}")
        return None

def create_zip_archive(files):
    with ZipFile('Anexos.zip', 'w') as zip_file:
        for file_path in files:
            if os.path.exists(file_path):
                zip_file.write(file_path, arcname=os.path.basename(file_path))
            else:
                print(f"Arquivo não encontrado: {file_path}")

if __name__ == "__main__":
    main()