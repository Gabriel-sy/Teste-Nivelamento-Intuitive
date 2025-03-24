# Download de Anexos da ANS

Este script Python baixa os anexos (Anexo I e Anexo II) do site da Agência Nacional de Saúde Suplementar (ANS) e os compacta em um arquivo ZIP.

## O que ele faz

O script realiza as seguintes etapas:

1.  Acessa a página da ANS onde os anexos estão disponíveis.
2.  Localiza os links para os arquivos PDF dos "Anexo I." e "Anexo II.".
3.  Baixa os arquivos PDF.
4.  Cria um arquivo ZIP chamado `Anexos.zip` contendo os PDFs baixados.
5.  Em caso de erro, imprime mensagens informativas.

## Como usar

1.  Certifique-se de ter o Python 3 instalado.
2.  Clone o repositório:
    ```bash
    git clone https://github.com/Gabriel-sy/Teste-Nivelamento-Intuitive.git
    ```
2.  Instale as bibliotecas necessárias:

    ```bash
    pip install requests beautifulsoup4
    ```
4.  Execute o script:

    ```bash
    cd Teste-Web-Scraping
    python main.py
    ```

5.  Após a execução, os arquivos PDF baixados e o arquivo `Anexos.zip` estarão no mesmo diretório em que o script foi executado.

## Testes

O script também inclui testes unitários para verificar a funcionalidade principal. Para executar os testes, certifique-se de ter o `pytest` instalado:

```bash
pip install pytest requests_mock