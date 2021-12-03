from playwright.sync_api import *
import time as tm
from urllib.parse import quote as q
import webbrowser
import datetime
import pyautogui as pg

def get_avec_schedule(which_day=0):
    #pegando os dados da agenda p montar os lembretes
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto("https://admin.salaovip.com.br/beautypalace/admin")
        page.fill('//*[@id="formEmail"]', 'mannaramos54@gmail.com')
        page.fill('//*[@id="formSenha"]', '06052001')
        page.click('text="Entrar"')
        print('successfully logged in')
        tm.sleep(3)
        day = '"' + str(int(datetime.date.today().day) + which_day) + '"'
        page.click(':is(td:has-text(' + day + '))')
        # page.click('div.datepicker:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(4)')
        try:
            with page.expect_response("https://admin.salaovip.com.br/admin/agenda/carregarAgenda") as response_info:
                page.click(':is(td:has-text(' + day + '))')
                print('trying keep appointments of day ' + day)
                # vamos trabalhar tod o projeto com a variavel response dados
                response_dados = response_info.value.json()['dados']
                print('appointments were collected successfully')
        except:
            print('appointments not found')
            exit('appointments not found')
        # organizando as clientes e serviços em dicionário para poder trabalhar com as informações
        clientes = {}
        nomes = []
        for index in range(len(response_dados)):
            reserva = response_dados[index]['reservas']
            for t in range(len(reserva)):
                if reserva[t]['cliente_nome'] in clientes.keys():
                    clientes[reserva[t]['cliente_nome']]['servico'].append(reserva[t]['servico'])
                    if int(reserva[t]['hora_inicio']) < int(clientes[reserva[t]['cliente_nome']]['horario']):
                        clientes[reserva[t]['cliente_nome']]['horario'] = reserva[t]['hora_inicio']
                else:
                    nomes.append(reserva[t]['cliente_nome'])
                    clientes[reserva[t]['cliente_nome']] = {
                        'tel': reserva[t]['cliente_tel'],
                        'servico': [reserva[t]['servico']],
                        'horario': int(reserva[t]['hora_inicio'])}
                print(clientes[reserva[t]['cliente_nome']])
        for o in range(len(nomes)):
            servico = ''
            for x in range(len(clientes[nomes[o]]['servico'])):
                servico = servico + ' ' + clientes[nomes[o]]['servico'][x] +','
            amanha = datetime.date.today() + datetime.timedelta(days=1)
            amanha = amanha.strftime(f'%d/%m/%Y')
            servico = f'👑Olá princesa, lembrete de agendamento no Beauty Palace para o dia {amanha} ás {str(datetime.timedelta(minutes=int(clientes[nomes[o]]["horario"])))}👑'
            servico2 = '❓Posso confirmar o seu horário❓'
            servico3 = 'Caso não consiga comparecer no atendimento, peço que desmarque com no mínimo 2 horas de antecedência para que possamos encaixar outra cliente no horário. Caso haja falta sem um aviso prévio, será aplicada uma multa com o valor de 50% referente ao(s) serviço(s) que seria prestado.'
            clientes[nomes[o]]['servico'] = servico
    d = [clientes, nomes]
    tel = '+5511982153054'
    return d

d = get_avec_schedule(1)


luh_chat = f'https://web.whatsapp.com/send?phone=+5511982153054&text={q("O Beauty Palace Sistem começou a enviar os lembretes para as clientes")}'
webbrowser.open(luh_chat, new=0, autoraise=True)
tm.sleep(20)
pg.press('enter')
tm.sleep(2)
for c in range(len(d[1])):
    m = d[0][d[1][c]]['servico']
    tel = d[0][d[1][c]]['tel']
    if len(tel) == 11 and tel != "":
        url = f'https://web.whatsapp.com/send?phone=+55{tel}&text={q(m)}%0A%0A{q("❓Posso confirmar o seu horário❓")}%0A%0a{q("Caso não consiga comparecer no atendimento, peço que desmarque com no mínimo 2 horas de antecedência para que possamos encaixar outra cliente no horário. Caso haja falta sem um aviso prévio, será aplicada uma multa com o valor de 50% referente ao(s) serviço(s) que seria prestado. ** mensagem automatica")}'
        pg.hotkey('ctrl', 'l')
        tm.sleep(4)
        pg.write(url)
        pg.press('enter')
        tm.sleep(15)
        pg.press('enter')
        tm.sleep(10)
        pg.press('enter')
        tm.sleep(3)
pg.hotkey('ctrl', 'w')


