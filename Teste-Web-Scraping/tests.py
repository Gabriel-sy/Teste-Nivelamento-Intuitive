import os
import pytest
import requests
import requests_mock
from bs4 import BeautifulSoup
from zipfile import ZipFile

from main import main, download_annex, create_zip_archive

def test_download_annex_success(tmp_path, requests_mock):
    mock_html = '''
    <html>
        <a href="https://example.com/anexo1.pdf">Anexo I.</a>
        <a href="https://example.com/anexo2.pdf">Anexo II.</a>
    </html>
    '''
    
    requests_mock.get("https://example.com/anexo1.pdf", content=b"PDF Content 1")
    soup = BeautifulSoup(mock_html, 'html.parser')
    
    os.chdir(tmp_path)
    file_path = download_annex(soup, "Anexo I.")
    
    assert file_path is not None
    assert os.path.exists(file_path)
    assert file_path == "Anexo I.pdf"
    
    with open(file_path, 'rb') as f:
        assert f.read() == b"PDF Content 1"

def test_download_annex_not_found(requests_mock):
    mock_html = '<html></html>'
    soup = BeautifulSoup(mock_html, 'html.parser')
    
    file_path = download_annex(soup, "Anexo I.")
    
    assert file_path is None

def test_download_annex_no_href(requests_mock):
    mock_html = '<html><a>Anexo I.</a></html>'
    soup = BeautifulSoup(mock_html, 'html.parser')
    
    file_path = download_annex(soup, "Anexo I.")
    
    assert file_path is None

def test_download_annex_request_error(requests_mock):
    mock_html = '''
    <html>
        <a href="https://example.com/anexo1.pdf">Anexo I.</a>
    </html>
    '''
    
    requests_mock.get("https://example.com/anexo1.pdf", status_code=404)
    soup = BeautifulSoup(mock_html, 'html.parser')
    
    file_path = download_annex(soup, "Anexo I.")
    
    assert file_path is None

def test_create_zip_archive(tmp_path):
    os.chdir(tmp_path)
    
    with open('file1.pdf', 'w') as f1, open('file2.pdf', 'w') as f2:
        f1.write("Content 1")
        f2.write("Content 2")
    
    files = ['file1.pdf', 'file2.pdf']
    create_zip_archive(files)
    
    assert os.path.exists('Anexos.zip')
    
    with ZipFile('Anexos.zip', 'r') as zip_ref:
        assert len(zip_ref.namelist()) == 2
        assert 'file1.pdf' in zip_ref.namelist()
        assert 'file2.pdf' in zip_ref.namelist()

def test_main_success(tmp_path, monkeypatch, requests_mock):
    os.chdir(tmp_path)
    
    mock_html = '''
    <html>
        <a href="https://example.com/anexo1.pdf">Anexo I.</a>
        <a href="https://example.com/anexo2.pdf">Anexo II.</a>
    </html>
    '''
    
    requests_mock.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos", text=mock_html)
    requests_mock.get("https://example.com/anexo1.pdf", content=b"PDF Content 1")
    requests_mock.get("https://example.com/anexo2.pdf", content=b"PDF Content 2")
    
    def mock_print(message):
        pass
    
    monkeypatch.setattr('builtins.print', mock_print)
    
    main()
    
    assert os.path.exists('Anexos.zip')
    
    with ZipFile('Anexos.zip', 'r') as zip_ref:
        assert len(zip_ref.namelist()) == 2

def test_main_connection_error(monkeypatch, requests_mock):
    requests_mock.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos", exc=requests.RequestException)
    
    def mock_print(message):
        assert "Erro de conexão" in message
    
    monkeypatch.setattr('builtins.print', mock_print)
    
    main()