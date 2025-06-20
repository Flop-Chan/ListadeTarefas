import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
from datetime import datetime

class GerenciadorTarefas:
    def __init__(self):
        self.arquivo = 'tarefas.json'
        self.tarefas = self.carregar_tarefas()
        
        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("🔥 Gerenciador de Tarefas")
        self.root.geometry("800x600")
        self.root.configure(bg='#2C3E50')
        self.root.resizable(True, True)
        
        # Configurar fonte personalizada
        self.fonte_titulo = font.Font(family="Arial", size=24, weight="bold")
        self.fonte_subtitulo = font.Font(family="Arial", size=12)
        self.fonte_tarefa = font.Font(family="Arial", size=11)
        
        self.configurar_estilo()
        self.criar_interface()
        self.atualizar_lista()
        
    def configurar_estilo(self):
        """Configura o estilo personalizado dos widgets"""
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Estilo para botões
        style.configure('Moderno.TButton',
                       background='#3498DB',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Moderno.TButton',
                 background=[('active', '#2980B9'),
                            ('pressed', '#21618C')])
        
        # Estilo para botão de remover
        style.configure('Perigo.TButton',
                       background='#E74C3C',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 5))
        
        style.map('Perigo.TButton',
                 background=[('active', '#C0392B'),
                            ('pressed', '#A93226')])
        
        # Estilo para entry
        style.configure('Moderno.TEntry',
                       borderwidth=2,
                       relief='solid',
                       padding=10)
        
    def carregar_tarefas(self):
        """Carrega tarefas do arquivo JSON"""
        if not os.path.exists(self.arquivo):
            return []
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def salvar_tarefas(self):
        """Salva tarefas no arquivo JSON"""
        try:
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.tarefas, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def criar_interface(self):
        """Cria toda a interface gráfica"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#2C3E50')
        header_frame.pack(fill='x', pady=(0, 20))
        
        titulo = tk.Label(header_frame, 
                         text="🚀 Gerenciador de Tarefas", 
                         font=self.fonte_titulo,
                         bg='#2C3E50', 
                         fg='#ECF0F1')
        titulo.pack()
        
        subtitulo = tk.Label(header_frame, 
                           text="Organize suas tarefas de forma elegante e eficiente", 
                           font=self.fonte_subtitulo,
                           bg='#2C3E50', 
                           fg='#BDC3C7')
        subtitulo.pack(pady=(5, 0))
        
        # Frame de estatísticas
        stats_frame = tk.Frame(main_frame, bg='#2C3E50')
        stats_frame.pack(fill='x', pady=(0, 20))
        
        # Cards de estatísticas
        self.card_total = self.criar_card_estatistica(stats_frame, "Total", "0", "#3498DB")
        self.card_total.pack(side='left', padx=(0, 10))
        
        self.card_concluidas = self.criar_card_estatistica(stats_frame, "Concluídas", "0", "#27AE60")
        self.card_concluidas.pack(side='left', padx=10)
        
        self.card_pendentes = self.criar_card_estatistica(stats_frame, "Pendentes", "0", "#E67E22")
        self.card_pendentes.pack(side='left', padx=(10, 0))
        
        # Frame de entrada
        entrada_frame = tk.Frame(main_frame, bg='#2C3E50')
        entrada_frame.pack(fill='x', pady=(0, 20))
        
        self.entrada_tarefa = ttk.Entry(entrada_frame, 
                                      style='Moderno.TEntry',
                                      font=self.fonte_tarefa,
                                      width=50)
        self.entrada_tarefa.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.entrada_tarefa.bind('<Return>', lambda e: self.adicionar_tarefa())
        
        btn_adicionar = ttk.Button(entrada_frame, 
                                 text="➕ Adicionar",
                                 style='Moderno.TButton',
                                 command=self.adicionar_tarefa)
        btn_adicionar.pack(side='right')
        
        # Frame da lista de tarefas
        lista_frame = tk.Frame(main_frame, bg='#2C3E50')
        lista_frame.pack(fill='both', expand=True)
        
        # Canvas e scrollbar para a lista
        self.canvas = tk.Canvas(lista_frame, bg='#34495E', highlightthickness=0)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#34495E')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind para scroll com mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def criar_card_estatistica(self, parent, titulo, valor, cor):
        """Cria um card de estatística"""
        card = tk.Frame(parent, bg=cor, relief='raised', bd=2)
        card.configure(width=150, height=80)
        card.pack_propagate(False)
        
        titulo_label = tk.Label(card, text=titulo, 
                              font=('Arial', 10, 'bold'),
                              bg=cor, fg='white')
        titulo_label.pack(pady=(10, 0))
        
        # Guardar referência do label do valor para poder atualizar depois
        valor_label = tk.Label(card, text=valor, 
                             font=('Arial', 18, 'bold'),
                             bg=cor, fg='white')
        valor_label.pack()
        
        # Armazenar a referência do label do valor no próprio card
        card.valor_label = valor_label
        
        return card
    
    def _on_mousewheel(self, event):
        """Função para scroll com mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def adicionar_tarefa(self):
        """Adiciona uma nova tarefa"""
        texto = self.entrada_tarefa.get().strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite uma tarefa!")
            return
        
        nova_tarefa = {
            "nome": texto,
            "concluida": False,
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        self.tarefas.append(nova_tarefa)
        self.salvar_tarefas()
        self.entrada_tarefa.delete(0, tk.END)
        self.atualizar_lista()
        
        # Feedback visual
        self.entrada_tarefa.configure(style='Sucesso.TEntry')
        self.root.after(1000, lambda: self.entrada_tarefa.configure(style='Moderno.TEntry'))
    
    def alternar_tarefa(self, index):
        """Alterna o status de conclusão da tarefa"""
        self.tarefas[index]["concluida"] = not self.tarefas[index]["concluida"]
        self.salvar_tarefas()
        self.atualizar_lista()
    
    def remover_tarefa(self, index):
        """Remove uma tarefa"""
        if messagebox.askyesno("Confirmar", "Deseja realmente remover esta tarefa?"):
            del self.tarefas[index]
            self.salvar_tarefas()
            self.atualizar_lista()
    
    def atualizar_lista(self):
        """Atualiza a lista de tarefas na interface"""
        # Limpar frame atual
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Atualizar estatísticas
        total = len(self.tarefas)
        concluidas = sum(1 for t in self.tarefas if t["concluida"])
        pendentes = total - concluidas
        
        # Atualizar cards
        self.atualizar_card(self.card_total, str(total))
        self.atualizar_card(self.card_concluidas, str(concluidas))
        self.atualizar_card(self.card_pendentes, str(pendentes))
        
        if not self.tarefas:
            # Mostrar mensagem quando não há tarefas
            empty_frame = tk.Frame(self.scrollable_frame, bg='#34495E')
            empty_frame.pack(fill='x', pady=50)
            
            tk.Label(empty_frame, 
                    text="📋", 
                    font=('Arial', 48),
                    bg='#34495E', 
                    fg='#7F8C8D').pack()
            
            tk.Label(empty_frame, 
                    text="Nenhuma tarefa ainda", 
                    font=('Arial', 16, 'bold'),
                    bg='#34495E', 
                    fg='#ECF0F1').pack()
            
            tk.Label(empty_frame, 
                    text="Adicione sua primeira tarefa acima!", 
                    font=('Arial', 12),
                    bg='#34495E', 
                    fg='#BDC3C7').pack()
            return
        
        # Criar widgets para cada tarefa
        for i, tarefa in enumerate(self.tarefas):
            self.criar_widget_tarefa(i, tarefa)
    
    def atualizar_card(self, card, novo_valor):
        """Atualiza o valor de um card de estatística"""
        # Usar a referência direta do label que guardamos
        if hasattr(card, 'valor_label'):
            card.valor_label.configure(text=novo_valor)
    
    def criar_widget_tarefa(self, index, tarefa):
        """Cria o widget para uma tarefa individual"""
        # Frame da tarefa
        cor_fundo = '#27AE60' if tarefa["concluida"] else '#ECF0F1'
        cor_texto = 'white' if tarefa["concluida"] else '#2C3E50'
        
        tarefa_frame = tk.Frame(self.scrollable_frame, 
                              bg=cor_fundo, 
                              relief='raised', 
                              bd=1)
        tarefa_frame.pack(fill='x', padx=5, pady=3)
        
        # Frame interno para organizar elementos
        conteudo_frame = tk.Frame(tarefa_frame, bg=cor_fundo)
        conteudo_frame.pack(fill='x', padx=15, pady=10)
        
        # Checkbox
        checkbox_var = tk.BooleanVar(value=tarefa["concluida"])
        checkbox = tk.Checkbutton(conteudo_frame,
                                variable=checkbox_var,
                                command=lambda: self.alternar_tarefa(index),
                                bg=cor_fundo,
                                activebackground=cor_fundo,
                                font=('Arial', 12))
        checkbox.pack(side='left')
        
        # Texto da tarefa
        texto_tarefa = tk.Label(conteudo_frame,
                              text=tarefa["nome"],
                              font=self.fonte_tarefa,
                              bg=cor_fundo,
                              fg=cor_texto,
                              anchor='w')
        texto_tarefa.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        if tarefa["concluida"]:
            # Adicionar efeito riscado para tarefas concluídas
            texto_tarefa.configure(font=('Arial', 11, 'overstrike'))
        
        # Data de criação
        data_label = tk.Label(conteudo_frame,
                            text=tarefa.get("data_criacao", ""),
                            font=('Arial', 8),
                            bg=cor_fundo,
                            fg=cor_texto)
        data_label.pack(side='right', padx=(10, 0))
        
        # Botão remover
        btn_remover = tk.Button(conteudo_frame,
                              text="🗑️",
                              command=lambda: self.remover_tarefa(index),
                              bg='#E74C3C',
                              fg='white',
                              font=('Arial', 10),
                              relief='flat',
                              width=3,
                              cursor='hand2')
        btn_remover.pack(side='right', padx=(5, 0))
    
    def executar(self):
        """Inicia o loop principal da aplicação"""
        self.root.mainloop()

# Executar a aplicação
if __name__ == "__main__":
    app = GerenciadorTarefas()
    app.executar()