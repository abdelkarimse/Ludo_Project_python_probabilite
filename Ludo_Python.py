import tkinter as tk
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def choix(pourcentages):
    nombres = [1, 2, 3, 4, 5, 6]
    return random.choices(nombres, weights=pourcentages, k=1)[0]

def changer_couleur(bouton, m):
    color = ["blue", "red", "green", "yellow"]
    bouton.config(bg=color[m])

def kill(playpermisition,boutons, lignescolor, m):
    for i in range(len(playpermisition)):
        if i != m:
            if lignescolor[i] == lignescolor[m] and lignescolor[i] != 18:
                lignescolor[i] = 0
                for j in range(19):
                    boutons[i][j].config(bg='white')
def win(lignescolor):
    return sum([1 if i == 18 else 0 for i in lignescolor])==len(lignescolor)-1
    
def play(names, percentages_list,root,playpermisition,player_name,bouton, boutons, lignescolor, m, pourcentages):
    if playpermisition[m]==1 :
        playpermisition[m]=0
        if m == len(playpermisition)-1:
            playpermisition[0]=1
        else :
            playpermisition[m+1]=1
        
        x = choix(pourcentages)
        bouton.config(text=player_name+" : "+str(x))
        if lignescolor[m] != 0:
            lignescolor[m] += x
            if lignescolor[m] > 18:
                lignescolor[m] -= x
            for i in range(lignescolor[m] + 1):
                bouton = boutons[m][i]
                changer_couleur(bouton, m)
            kill(playpermisition,boutons, lignescolor, m)
        elif x == 6:
            lignescolor[m] += 1
            bouton = boutons[m][0]
            changer_couleur(bouton, m)
        if win(lignescolor):
            destroy_current_interface(root)
            show_three_interfaces(names, percentages_list)

            
            

def destroy_current_interface(a):
    a.destroy()

def submit_names():
    player_names = []
    percentages_list = []

    for entry, pour_list in entry_list.items():
        player_name = entry.get()
        player_names.append(player_name)
        percentages = [int(pour_entry.get()) for j, pour_entry in pour_list.items()]
        percentages_list.append(percentages)
        print(f"Player: {player_name}, Percentages: {percentages}")

    destroy_current_interface(inter1)
    show_deux_interfaces(player_names, percentages_list)

def show_deux_interfaces(names, percentages_list):
    root = tk.Tk()
    root.title("LUDO Interface")
    color = ["blue", "red", "green", "yellow"]

    lignescolor = [0 for i in range(len(names))]
    playpermisition=[1]+[0 for i in range(len(names)-1)]
    boutons = []
    for i, (player_name, percentages) in enumerate(zip(names, percentages_list)):
        ligne_boutons = []
        bouton = tk.Button(root, text=player_name, width=8, height=2, bg=color[i])
        bouton.config(font=("Arial", 12))
        bouton.grid(row=i, column=0, padx=20, pady=20)
        bouton.config(command=lambda m=i, bouton=bouton,name=player_name, boutons=boutons: play(names, percentages_list,root,playpermisition,name,bouton, boutons, lignescolor, m, percentages))
        for j in range(1, 20):
            bouton = tk.Button(root, text="", width=7, height=2, bg='white')
            bouton.grid(row=i, column=j, pady=2)
            ligne_boutons.append(bouton)
        boutons.append(ligne_boutons)

def show_three_interfaces(names, percentages_list):
    graphe = tk.Tk()
    graphe.title("Player Percentages Graphs")

    for i, (player_name, percentages) in enumerate(zip(names, percentages_list)):
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(range(1, 7), percentages)
        ax.set_xlabel('Die Number')
        ax.set_ylabel('Percentage')
        ax.set_title(f'{player_name} Percentages')
        ax.set_ylim(0, 100)
        canvas = FigureCanvasTkAgg(fig, master=graphe)
        canvas.get_tk_widget().grid(row=0, column=i, padx=20, pady=20)

    graphe.mainloop()

inter1 = tk.Tk()
inter1.title("Player Names Input")

entry_list = {}
k=int(input("donner le nombre de player : "))
while(k>4):
    k=int(input("donner le nombre de player : "))

for i in range(k):
    player_frame = tk.Frame(inter1, padx=10, pady=20)
    player_frame.pack()

    label = tk.Label(player_frame, text=f"Player {i+1}:")
    label.grid(row=0, column=0, padx=5, pady=15)

    
    entry = tk.Entry(player_frame, width=30)
    entry.grid(row=0, column=1, padx=5, pady=15)
    entry_list[entry] = {}

    for j in range(1, 7):
        label = tk.Label(player_frame, text=f"{j}")
        label.grid(row=1, column=j, pady=10)
        pour_entry = tk.Entry(player_frame, width=5)
        pour_entry.grid(row=2, column=j, padx=5)
        entry_list[entry][j] = pour_entry

submit_button = tk.Button(inter1, text="GO player", command=submit_names)
submit_button.pack(pady=10)

inter1.geometry('600x700')
inter1.mainloop()