import pygame 
import sys
import importlib
import os
import glob
import re
import subprocess
import numpy as np

# Inicializar o pygame
pygame.init()

# Criar a janela
largura, altura = 1400, 750
screen = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
pygame.display.set_caption("Menu")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (200, 200, 200)
AZUL_CLARO = (100, 150, 200)

# Fonte
fonte = pygame.font.SysFont(None, 36)

input_size = 7
hidden_size = 20
output_size = 2 

# Função para desenhar um botão
def draw_button(texto, x, y, largura, altura, ativo):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    cor = CINZENTO if ativo else BRANCO
    pygame.draw.rect(screen, cor, (x, y, largura, altura))
    mensagem = fonte.render(texto, True, PRETO)
    screen.blit(mensagem, (x + 10, y + 15))
    
    if x + largura > mouse[0] > x and y + altura > mouse[1] > y:
        if click[0] == 1:
            return True
    return False

# Classe para o checkbox
class Checkbox:
    def __init__(self, x, y, texto, grupo_exclusivo=None, enabled=True):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.checked = False
        self.texto = texto
        self.grupo_exclusivo = grupo_exclusivo
        self.enabled = enabled

    def draw(self):
        cor_fundo = BRANCO if self.enabled else CINZENTO
        pygame.draw.rect(screen, cor_fundo, self.rect)
        pygame.draw.rect(screen, PRETO, self.rect, 2)
        if self.checked:
            pygame.draw.line(screen, PRETO, (self.rect.left+3, self.rect.centery), (self.rect.centerx, self.rect.bottom-3), 2)
            pygame.draw.line(screen, PRETO, (self.rect.centerx, self.rect.bottom-3), (self.rect.right-3, self.rect.top+3), 2)
        texto_render = fonte.render(self.texto, True, PRETO)
        screen.blit(texto_render, (self.rect.right + 10, self.rect.top))

    def handle_event(self, event, todos_checkboxes):
        if not self.enabled:
            return  # Se não está ativado, ignora clique!
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.grupo_exclusivo:
                    if self.checked:
                        self.checked = False
                    else:
                        for cb in todos_checkboxes:
                            if cb.grupo_exclusivo == self.grupo_exclusivo:
                                cb.checked = False
                        self.checked = True
                else:
                    self.checked = not self.checked
    def get_track(self):
        if self.texto=="Pista 1 (fácil)":
            return 0
        elif self.texto=="Pista 2 (médio)":
            return 1
        elif self.texto=="Pista 3 (difícil)":
            return 2
        return None

# Criar checkboxes
checkboxes = [
    Checkbox(250, 10, "Q-learning", grupo_exclusivo="grupo12"),
    Checkbox(250, 40, "Neural Network", grupo_exclusivo="grupo12"),
    Checkbox(250, 70, "Neural Network2", grupo_exclusivo="grupo12"),
    Checkbox(480, 10, "Pista 1 (fácil)", grupo_exclusivo="grupo35"),
    Checkbox(480, 40, "Pista 2 (médio)", grupo_exclusivo="grupo35"),
    Checkbox(480, 70, "Pista 3 (difícil)", grupo_exclusivo="grupo35"),
    Checkbox(480, 100, "Pista 4 (difícil)", grupo_exclusivo="grupo35"),
    Checkbox(480, 130, "Pista 5 (difícil)", grupo_exclusivo="grupo35")
]

# NOVOS checkboxes (por exemplo para Opção 2) todos desativados no início
checkboxes_opcao2 = [
    Checkbox(250, 10, "Q-learning", grupo_exclusivo="grupo12", enabled=False),
    Checkbox(250, 40, "Neural Network", grupo_exclusivo="grupo12", enabled=False),
    Checkbox(250, 70, "Neural Network2", grupo_exclusivo="grupo12", enabled=False),
    Checkbox(480, 10, "Pista 1 (fácil)", grupo_exclusivo="grupo35a", enabled=False),
    Checkbox(480, 40, "Pista 2 (médio)", grupo_exclusivo="grupo35a", enabled=False),
    Checkbox(480, 70, "Pista 3 (difícil)", grupo_exclusivo="grupo35a", enabled=False),
    Checkbox(480, 100, "Pista 4 (difícil)", grupo_exclusivo="grupo35a", enabled=False),
    Checkbox(480, 130, "Pista 5 (difícil)", grupo_exclusivo="grupo35a", enabled=False),
    Checkbox(480, 10, "Pista 1 (fácil)", grupo_exclusivo="grupo35b", enabled=False),
    Checkbox(480, 40, "Pista 2 (médio)", grupo_exclusivo="grupo35b", enabled=False),
    Checkbox(480, 70, "Pista 3 (difícil)", grupo_exclusivo="grupo35b", enabled=False),
    Checkbox(480, 100, "Pista 4 (difícil)", grupo_exclusivo="grupo35b", enabled=False),
    Checkbox(480, 130, "Pista 5 (difícil)", grupo_exclusivo="grupo35b", enabled=False),
    Checkbox(480, 10, "Pista 1 (fácil)", grupo_exclusivo="grupo35c", enabled=False),
    Checkbox(480, 40, "Pista 2 (médio)", grupo_exclusivo="grupo35c", enabled=False),
    Checkbox(480, 70, "Pista 3 (difícil)", grupo_exclusivo="grupo35c", enabled=False),
    Checkbox(480, 100, "Pista 4 (difícil)", grupo_exclusivo="grupo35c", enabled=False),
    Checkbox(480, 130, "Pista 5 (difícil)", grupo_exclusivo="grupo35c", enabled=False)
]

checkboxes_opcao2_1 = [
    Checkbox(250, 160, "Select all graphs", grupo_exclusivo="grupo12"),
    Checkbox(250, 190, "Select all graphs and GIFs", grupo_exclusivo="grupo12"), 
    Checkbox(250, 220, "Fitness evolution", grupo_exclusivo="grupo_fit"),
    Checkbox(250, 250, "Crashes position", grupo_exclusivo="grupo_crash"),
    Checkbox(250, 280, "Speed, acceleration and steer over time", grupo_exclusivo="grupo_time"),
    Checkbox(250, 310, "Speed and acceleration on track", grupo_exclusivo="grupo_track"),
    Checkbox(250, 340, "GIFs of speed and acceleration over time on track", grupo_exclusivo="grupo_gif"),
    Checkbox(250, 370, "Graphs for saved results?", grupo_exclusivo="grupo_saved")
]

def result_checkboxes():
    # Mapeia índice das checkboxes de pistas por método
    pistas_por_metodo = {
        "Q-learning": ["results1", "results2", "results3", "results4","results5"],
        "Neural Network": ["results1", "results2", "results3", "results4","results5"],
        "Neural Network2": ["results1", "results2", "results3", "results4","results5"]
    }

    for checkbox in checkboxes_opcao2:
        texto = checkbox.texto

        if texto in ["Q-learning", "Neural Network","Neural Network2"]:
            metodo = texto
            base_path = metodo.replace(" ", "_")  # folder name
            existe_alguma_pista = any(os.path.exists(os.path.join(base_path, pista)) for pista in pistas_por_metodo[metodo])
            checkbox.enabled = existe_alguma_pista

        elif "Pista" in texto:
            if "grupo35a" in checkbox.grupo_exclusivo:
                metodo = "Q-learning"
            elif "grupo35b" in checkbox.grupo_exclusivo:
                metodo = "Neural Network"
            elif "grupo35c" in checkbox.grupo_exclusivo:
                metodo = "Neural Network2"
            else:
                continue
            
            base_path = metodo.replace(" ", "_")
            if "Pista 1" in texto:
                pista_n = "results1"
            elif "Pista 2" in texto:
                pista_n = "results2"
            elif "Pista 3" in texto:
                pista_n = "results3"
            elif "Pista 4" in texto:
                pista_n = "results4"
            elif "Pista 5" in texto:
                pista_n = "results5"
            else:
                continue

            checkbox.enabled = os.path.exists(os.path.join(base_path, pista_n))

def draw_group(checkboxes, group=None):
    if group=='all':
        for checkbox in checkboxes:
            checkbox.draw()
    else:
        for checkbox in checkboxes:
            if checkbox.grupo_exclusivo==group:
                checkbox.draw()

# Função para verificar se temos um selecionado em cada grupo
def grupos_selecionados(checkboxes):
    grupo12_checked = any(cb.checked for cb in checkboxes if cb.grupo_exclusivo == "grupo12")
    grupo35_checked = any(cb.checked for cb in checkboxes if cb.grupo_exclusivo == "grupo35")
    return grupo12_checked and grupo35_checked

# Função para obter o texto selecionado de cada grupo
def get_checkbox(checkboxes):
    selecionados = {}
    for cb in checkboxes:
        if cb.checked:
            selecionados[cb.grupo_exclusivo] = cb.texto
    return selecionados

# Loop principal
def menu():
    global screen
    opcao_ativa = None
    selecionados={}
    result_checkboxes()
    while True:
        pista_n = None
        miniatura_imagem = None
        screen.fill(AZUL_CLARO)  # Fundo azul claro

        if draw_button("Começar Novo", 20, 10, 200, 60, opcao_ativa == 1):
            opcao_ativa = 1

        if draw_button("Ver Resultados", 20, 110, 200, 60, opcao_ativa == 2):
            opcao_ativa = 2
        
        if draw_button("Sair", 20, 210, 200, 60, opcao_ativa == 3):
            pygame.quit()
            sys.exit()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if opcao_ativa == 1:
                for checkbox in checkboxes:
                    checkbox.handle_event(evento, checkboxes)
            if opcao_ativa == 2:
                for checkbox in checkboxes_opcao2:
                    checkbox.handle_event(evento, checkboxes_opcao2)
                for checkbox in checkboxes_opcao2_1:
                    checkbox.handle_event(evento, checkboxes_opcao2_1)
        if opcao_ativa == 1:
            for checkbox in checkboxes:
                checkbox.draw()
            selecionados = get_checkbox(checkboxes)
            if "grupo12" in selecionados and ("grupo35" in selecionados):
                metodo = selecionados.get("grupo12")
                pista = selecionados.get("grupo35")
                if pista == "Pista 1 (fácil)":
                        pista_n = 0
                        miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track1.png"), (300, 200))
                elif pista == "Pista 2 (médio)":
                    pista_n = 1
                    miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track2.png"), (300, 200))
                elif pista == "Pista 3 (difícil)":
                    pista_n = 2
                    miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track3.png"), (400, 300)) 
                elif pista == "Pista 4 (difícil)":       
                    pista_n = 3
                    miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track4.png"), (500, 400)) 
                elif pista == "Pista 5 (difícil)":       
                        pista_n = 4
                        miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track5.png"), (300, 200))

                if draw_button("Start", largura-250, 20, 200, 60, False):
                    if metodo == "Q-learning":
                        checkboxes_opcao2[0].enabled = True  # Ativar Q-learning
                        checkboxes_opcao2[pista_n+2].enabled = True
                        if opcao_ativa==1:
                            modulo = importlib.import_module('Q-learning.Q-learn')
                            modulo.main(pista_n, screen)
                        
                    elif metodo == "Neural Network":
                        checkboxes_opcao2[1].enabled = True
                        checkboxes_opcao2[pista_n+5].enabled = True
                        if opcao_ativa==1:
                            screen.fill(AZUL_CLARO)
                            pygame.display.update() # para limpar o fundo
                            modulo = importlib.import_module('Neural_Network.car_nn')
                            importlib.reload(modulo)
                            modulo.main(pista_n, screen)
                    elif metodo == "Neural Network2":
                        checkboxes_opcao2[1].enabled = True
                        checkboxes_opcao2[pista_n+5].enabled = True
                        if opcao_ativa==1:
                            screen.fill(AZUL_CLARO)
                            pygame.display.update() # para limpar o fundo
                            deb_path_module = importlib.import_module('Neural_Network2.debug_path')
                            modulo = importlib.import_module('Neural_Network2.car_nn')
                            importlib.reload(modulo)
                            deb_path_module.main(pista_n)
                            modulo.main(pista_n, screen)
                    pygame.event.clear()
                    screen = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
                    pygame.display.set_caption("Menu")
                    for cb in checkboxes:
                        cb.checked = False
        if opcao_ativa == 2:
            for checkbox in checkboxes_opcao2:
                if checkbox.grupo_exclusivo == "grupo12":
                    draw_group(checkboxes_opcao2, "grupo12")

            selecionados = get_checkbox(checkboxes_opcao2)

            if "grupo12" in selecionados:
                metodo = selecionados["grupo12"]

                # Desenhar grupo35a ou grupo35b dependendo do método
                for checkbox in checkboxes_opcao2:
                    if metodo == "Q-learning" and checkbox.grupo_exclusivo == "grupo35a":
                        checkbox.draw()
                    elif metodo == "Neural Network" and checkbox.grupo_exclusivo == "grupo35b":
                        checkbox.draw()
                    elif metodo == "Neural Network2" and checkbox.grupo_exclusivo == "grupo35c":
                        checkbox.draw()

                selecionados = get_checkbox(checkboxes_opcao2)
                if "grupo35a" in selecionados or "grupo35b" in selecionados or "grupo35c" in selecionados:
                    pista = selecionados.get("grupo35a") or selecionados.get("grupo35b") or selecionados.get("grupo35c")
                    
                    # Determinar o índice da pista e miniatura
                    if pista == "Pista 1 (fácil)":
                        pista_n = 0
                        miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track1.png"), (300, 200))
                    elif pista == "Pista 2 (médio)":
                        pista_n = 1
                        miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track2.png"), (300, 200))
                    elif pista == "Pista 3 (difícil)":
                        pista_n = 2
                        miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track3.png"), (400, 300)) 
                    elif pista == "Pista 4 (difícil)":       
                        pista_n = 3
                        miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track4.png"), (300, 200)) 
                    elif pista == "Pista 5 (difícil)":       
                        pista_n = 4
                        miniatura_imagem = pygame.transform.scale(pygame.image.load("images/Track5.png"), (500, 400))

                    # Desenha botão Start

                    for checkbox in checkboxes_opcao2_1:
                        checkbox.draw()
                    if draw_button("Get Results", largura-250, 20, 200, 60, False):
                        if metodo == "Q-learning":
                            modulo = importlib.import_module("Q-learning.results")
                            modulo.main()
                        elif metodo == "Neural Network":
                            options, gifs, saved = get_results()
                            modulo = importlib.import_module("Neural_Network.results")
                            importlib.reload(modulo)
                            modulo.main(pista_n, options, gifs=gifs, saved_option=saved)
                        elif metodo == "Neural Network2":
                            options, gifs, saved = get_results()
                            modulo = importlib.import_module("Neural_Network2.results")
                            importlib.reload(modulo)
                            modulo.main(pista_n, options, gifs=gifs, saved_option=saved)
                        see_results(metodo, pista_n, options, gifs)
                        # resetar
                        pygame.event.clear()
                        screen = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
                        pygame.display.set_caption("Menu")
                        for cb in checkboxes:
                            cb.checked = False
        if miniatura_imagem:
            comp,alt= miniatura_imagem.get_size()
            screen.blit(miniatura_imagem, (largura - comp - 20, altura - alt - 20))  # 20px margem    
        pygame.display.update()

def get_results():
    selecionados = get_checkbox(checkboxes_opcao2_1)

    gifs = False
    saved = False
    options = []

    textos = list(selecionados.values())

    if "Select all graphs" in textos:
        options.append(0)  # 4: graphs over time, 5: graphs on track
    elif "Select all graphs and GIFs" in textos:
        options.append(1)
        gifs = True
    else:
        if "Fitness evolution" in textos:
            options.append(2)
        if "Crashes position" in textos:
            options.append(3)
        if "Speed, acceleration and steer over time" in textos:
            options.append(4)
        if "Speed and acceleration on track" in textos:
            options.append(5)
        if "GIFs of speed and acceleration over time on track" in textos:
            gifs = True

    if "Graphs for saved results?" in textos:
        saved = True
    print(f'Options: {options}, gifs: {gifs}, saved: {saved}')
    return options, gifs, saved

def see_results(metodo, pista_n, options, gifs):
    results_name_nn = {
        'acc_gen{}.jpeg':[0,1,4],
        'crash_positions.jpeg':[0,1,3],
        'fitness.jpeg':[0,1,2],
        'speed_gen{}.jpeg':[0,1,4],
        'streering_gen{}.jpeg':[0,1,4],
        'track_acc_gen{}.jpeg':[0,1,5],
        'track_speed_gen{}.jpeg':[0,1,5]
        }
    
    imagens = []
    
    if metodo == "Q-learning":
        pasta = 'Q-learning'
    if metodo == 'Neural Network':
        pasta = 'Neural_Network'
    if metodo == 'Neural_Network2':
        pasta = 'Neural_Network2'
    else:
        return
    subpasta = os.path.join(pasta, f"results{pista_n+1}")
    if not os.path.exists(subpasta):
        print("Nenhuma pasta de resultados encontrada.")
        return
        
    padrao_num = re.compile(r'.*\d+\.(jpeg|gif)$')

    for nome, opt in results_name_nn.items():
        to_add = any(op in options for op in opt)
        if not to_add:
            continue

        if '{}' in nome:
            padrao_glob = os.path.join(subpasta, nome.format('*'))
            for caminho in glob.glob(padrao_glob):
                if padrao_num.match(os.path.basename(caminho)):
                    imagens.append(caminho)
        else:
            path = os.path.join(subpasta, nome)
            if os.path.exists(path):
                imagens.append(path)

    if imagens:
        show_results(imagens)
    else:
        print("Nenhuma imagem encontrada.")

def show_results(imagens):
    idx = 0
    clock = pygame.time.Clock()
    mostrar = True
    print(imagens)
    while mostrar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mostrar = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_RIGHT:
                    idx = (idx + 1) % len(imagens)
                elif event.key == pygame.K_d or event.key == pygame.K_LEFT:
                    idx = (idx - 1) % len(imagens)
                elif event.key == pygame.K_ESCAPE:
                    mostrar = False

        # Limpa a tela
        screen.fill(AZUL_CLARO)

        # Carrega a imagem atual
        try:
            largura, altura = screen.get_size()
            caminho = imagens[idx]
            img = pygame.image.load(caminho)
            img_w, img_h = img.get_size()
            max_w, max_h = largura - 20, altura - 20
            scale = min(max_w / img_w, max_h / img_h)
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            img = pygame.transform.scale(img, (new_w, new_h))

            # Centralizar na tela
            x = (largura - new_w) // 2
            y = (altura - new_h) // 2

            screen.blit(img, (x, y))
        except Exception as e:
            print(f"Erro ao carregar imagem {imagens[idx]}: {e}")

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(30)
if __name__ == "__main__":
    menu()
