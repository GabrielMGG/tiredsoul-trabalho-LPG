import pygame
import sys

# Inicializar
pygame.init()

tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Tired soul")

# cor
preto = (0,0,0)
branco = (255,255,255)



#funçoes do jogo
def mostrar_tela_texto(titulo, mensagem, duracao=50000):
    
    tempo_inicio = pygame.time.get_ticks()
    fonte_titulo = pygame.font.SysFont('arial', 48, bold=True)
    fonte_mensagem = pygame.font.SysFont('arial', 20)

    quebra_linhas = mensagem.split('\n')
    
    while True:
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_inicio >= duracao:
            break
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                return tela.fill(preto)
        
        tela.fill(preto)
        

        texto_titulo = fonte_titulo.render(titulo, True, branco)
        titulo_rect = texto_titulo.get_rect(center=(400, 100))
        tela.blit(texto_titulo, titulo_rect)

        y_pos = 150
        for linha in quebra_linhas:
            if linha.strip():  
                texto_linha = fonte_mensagem.render(linha.strip(), True, branco)
                linha_rect = texto_linha.get_rect(center=(400, y_pos))
                tela.blit(texto_linha, linha_rect)
                y_pos += 30 
        
        
        texto_pular = fonte_mensagem.render("pressione qualquer tecla para pular", True, branco)
        pular_rect = texto_pular.get_rect(center=(400, 50))
        tela.blit(texto_pular, pular_rect)
        
        pygame.display.flip()

def tela_input_nome():
    nome = ""
    input_ativo = True
    fonte = pygame.font.SysFont('arial', 36)
    
    while input_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nome.strip():  
                        input_ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    
                    if len(nome) < 15: 
                        nome += evento.unicode
        
        tela.fill(preto)
        
        texto_instrucao = fonte.render("Digite o nome do seu personagem:", True, branco)
        tela.blit(texto_instrucao, (200, 300))
        
        # O input
        pygame.draw.rect(tela, branco, (250, 350, 300, 50), 2)
        
        texto_nome = fonte.render(nome, True, branco)
        tela.blit(texto_nome, (260, 360))
        
        # ajudar o amiguinho a prosseguir
        texto_ajuda = pygame.font.SysFont('arial', 20).render("Pressione ENTER para confirmar", True, branco)
        tela.blit(texto_ajuda, (280, 420))
        
        pygame.display.flip()
    
    return nome.strip()

class Animation:
    def __init__(self, pasta_animacao, scale=1, frame_delay=10):
        self.frames = []
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = frame_delay
        self.scale = scale
        
        #se nao funcionar olhar aqui
        self.carregar_frames_separados(pasta_animacao)
    
    def carregar_frames_separados(self, pasta):
        import os
        arquivos = os.listdir(pasta)
        arquivos_png = [f for f in arquivos if f.endswith('.png')]
        arquivos_png.sort() # faz o ordenamento dos frames em ordem alfabetica
        
        
        for arquivo in arquivos_png:
            caminho_completo = os.path.join(pasta, arquivo)
            frame = carregar_imagem_otimizada(caminho_completo)
            
            if self.scale != 1:
                nova_largura = int(frame.get_width() * self.scale)
                nova_altura = int(frame.get_height() * self.scale)
                frame = pygame.transform.scale(frame, (nova_largura, nova_altura))
            
            self.frames.append(frame)
        
        print(f" {len(self.frames)} frames carregados!")
    
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_current_frame(self):
        if self.frames:
            return self.frames[self.current_frame]
        else:
            surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            surf.fill((255, 0, 255))
            return surf

        

def criar_texto(surface, texto, x, y, cor=branco, tamanho=24):
    fonte =pygame.font.SysFont('arial', tamanho)
    texto_surface = fonte.render(texto, True, cor)
    surface.blit(texto_surface, (x, y))

class Button:
    def __init__(self, x, y, width, height, text):
        #porsiçoes e tamanhos
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        #text del botao
        self.text = text

        #cor
        self.cor_normal = (200, 200, 200) #cinza
        self.hover_color = (150, 150, 150)# cinza escuro

        self.is_hovered = False

    def draw(self, surface):
        #escolhe ama cor baseada no hover
        cor = self.hover_color if self.is_hovered else self.cor_normal

        #vai cria um retângulo
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # retângulo
        pygame.draw.rect(surface, cor, rect)

        #ADICIONAR TEXTO

        #criar fonte
        fonte = pygame.font.SysFont('arial', 24)

        #transformar ele em img
        texto_surface = fonte.render(self.text, True, preto)

        #a centralizaçao do texto no botao
        texto_rect = texto_surface.get_rect(center=rect.center)

        #fazer o texto aparecer no botao
        surface.blit(texto_surface, texto_rect)

    def check_hover(self, mouse_pos):
        #vai verificar se o mouse passa em cima do botao

        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_hovered = rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, event):
        #vai verificar se o botao foi clicado
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            return rect.collidepoint(event.pos)
        return False


def carregar_imagem_otimizada(caminho, largura_max=150, altura_max=150):
    try:
        imagem = pygame.image.load(caminho)
        imagem = imagem.convert_alpha()
        
        original_largura, original_altura = imagem.get_size()
        
        # Calcular a escala pra manter a proporção
        escala_x = largura_max / original_largura
        escala_y = altura_max / original_altura
        escala = min(escala_x, escala_y) 
        
        nova_largura = int(original_largura * escala)
        nova_altura = int(original_altura * escala)
        
        imagem_redimensionada = pygame.transform.scale(imagem, (nova_largura, nova_altura))
        
        return imagem_redimensionada
        
    except pygame.error as e:
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        surf.fill((255, 0, 255))
        return surf




#Anim do prota
animacao_atual = "idle"
prota_anim_idle = Animation('assets/jogador/soul/idle/', scale=3)
prota_anim_atack = Animation('assets/jogador/soul/ataque/', scale=3)


#Anim do inimigos  
inimigo_animacao_atual = "idle"
nightBorne_anim_idle = Animation('assets/enemys/NightBorne/idle/', scale=3)
nightBorne_anim_atack = Animation('assets/enemys/NightBorne/ataque/', scale=3)

# Background 
background_img = carregar_imagem_otimizada('assets/background/orig_big.png', 800, 800)

#botoes
botao_ataque = Button(50, 700, 150, 50, "ATACAR")
botao_item = Button(220, 700, 150, 50, "ITEM")
botao_fugir = Button(390, 700, 150, 50, "FUGIR")

#Prota Status
jogador_nome = tela_input_nome()
jogador_hp = 100
jogador_max_hp = 100
jogador_level = 1
jogador_forca = 10
jogador_exp = 0
jogador_inventario = ["Poção", "Poção"]

#INIMIGOS

#nIGHTbORNE
inimigo_hp = 50
inimigo_max_hp = 50
inimigo_forca = 8
inimigo_nome = "NightBorne"

mostrar_tela_texto("Tired Soul",
    f"""
    Você, {jogador_nome}, foi, em vida, apenas uma alma cansada.
    Sem sonhos grandiosos. Sem sede de poder.
    Seu maior desejo… sempre foi descansar.

    Mas o destino cruel e irônico, tinha outros planos.

    Em um ritual proibido, seu corpo foi profanado,
    e sua alma acorrentada a uma nova existência:
    um Necromante, condenado a caminhar entre os mortos.

    Agora, aprisionado em um reino esquecido,
    onde a própria escuridão tem olhos e fome,
    você é forçado a lutar por algo que nunca quis:

    continuar existindo.

    Para conquistar sua tão sonhada paz,
    você deverá enfrentar os Dez Guardiões,
    entidades moldadas pelo caos e pelo medo…
    Cada um deles é uma porta trancada
    entre você e o descanso eterno.

    Cansado, sarcástico e sem paciência,
    você embarca nessa jornada não por glória…
    Não por poder…
    Mas por um único e verdadeiro propósito:

    acabar com tudo isso… e finalmente fazer nada.
    """)

# criar um loop
jogoRodando = True
while jogoRodando:        
    # Vai pegar posição do mouse
    mouse_pos = pygame.mouse.get_pos()

    # Verifica o hover em todos os botoes
    botao_ataque.check_hover(mouse_pos)
    botao_item.check_hover(mouse_pos)
    botao_fugir.check_hover(mouse_pos)

    # Verificar cliques nos eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogoRodando = False
    
        # vai verificar os clique
        if botao_ataque.is_clicked(evento):
            #animation
            animacao_atual = "ataque"
            prota_anim_atack.current_frame = 0

            jogador_dano = jogador_forca

            inimigo_hp -= jogador_dano
            print(f"{jogador_nome} atacou {inimigo_nome} e tirou {jogador_dano} de vida")
            if inimigo_hp <= 0:
                inimigo_hp = 0
                print('Inimigo esta morto')
            
            elif inimigo_hp > 0:
                inimigo_animacao_atual = "ataque"
                nightBorne_anim_atack.current_frame = 0

                inimigo_dano = inimigo_forca
                jogador_hp -= inimigo_dano

            if jogador_hp <= 0:
                jogador_hp = 0
                print(f'{jogador_nome} foi brutalmente molestado pelo {inimigo_nome}')
        tela.fill(preto)   
            



        if botao_item.is_clicked(evento):
            print(f"voce tem{jogador_inventario} no inventario")

        if botao_fugir.is_clicked(evento):
            print("corre negada")

    # DESENHAR NA TELA 
    
    # 1. Fundo 
    tela.blit(background_img, (0, 0))

    
    
    # 2. Personagem 
    if animacao_atual == "idle":
        prota_anim_idle.update()
        tela.blit(prota_anim_idle.get_current_frame(),(-50, 100))
    
    elif animacao_atual == "ataque":
        prota_anim_atack.update()
        tela.blit(prota_anim_atack.get_current_frame(),(-50, 100))

        if prota_anim_atack.current_frame >= len(prota_anim_atack.frames) -1:
            animacao_atual = "idle"

    
    # 3. Inimigo
    if inimigo_animacao_atual == "idle":
        nightBorne_anim_idle.update()
        tela.blit(nightBorne_anim_idle.get_current_frame(),(400, 90))
    
    elif inimigo_animacao_atual == "ataque":
        nightBorne_anim_atack.update()
        tela.blit(nightBorne_anim_atack.get_current_frame(),(400, 90))

        if nightBorne_anim_atack.current_frame >= len(nightBorne_anim_atack.frames) -1:
            inimigo_animacao_atual = "idle"

    #vai limpar antes de criar o texto assim nao vai ficar varios texto em cima do outro
    pygame.draw.rect(tela, preto, (50, 500, 200, 100))    # Jogador
    pygame.draw.rect(tela, preto, (600, 500, 200, 100))   # Inimigo

    # Mostrar status do jogador
    criar_texto(tela, f"{jogador_nome} LV:{jogador_level}", 50, 500)
    criar_texto(tela, f"HP: {jogador_hp}/{jogador_max_hp}", 50, 530)
    criar_texto(tela, f"FOR: {jogador_forca}", 50, 560)
    criar_texto(tela, f"EXP: {jogador_exp}", 50, 590)

    # Mostrar status do inimigo
    criar_texto(tela, f"{inimigo_nome}", 600, 500)
    criar_texto(tela, f"HP: {inimigo_hp}/{inimigo_max_hp}", 600, 530)
    criar_texto(tela, f"FOR: {inimigo_forca}", 600, 560)

    #criar os botoes
    botao_ataque.draw(tela)
    botao_item.draw(tela) 
    botao_fugir.draw(tela)
    
    
    pygame.display.flip()

pygame.quit()
sys.exit()