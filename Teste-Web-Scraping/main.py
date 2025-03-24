import requests
from bs4 import BeautifulSoup

def main():
  try:
    response = requests.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
    
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    download_annex(soup, "Anexo I.")
    download_annex(soup, "Anexo II.")
    
  except:
    print("Ocorreu um erro ao realizar os downloads dos anexos")

def download_annex(soup, annex_name):
  first_annex_element = soup.find('a', string=annex_name)
  if first_annex_element:
      href = first_annex_element.get('href')
      if href:
        print(f"Baixando {annex_name}...")
        file_response = requests.get(href)
        file_response.raise_for_status()
        
        with open(annex_name + '.pdf', 'wb') as file:
          file.write(file_response.content)
        print(f"Download feito com sucesso: {annex_name}")
      else:
        print("Anexo I não encontrado")
  else:
      print("Anexo I não encontrado")

main()
  