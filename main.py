import tkinter as tk
from tkinter import ttk

n = 20
m = 20
def inicjalizacjaokna():
    root = tk.Tk()
    root.geometry('800x800')
    root.title('saper')
    
    return root


def panelgorny(root):
    licznik_min = tk.Label(root,bg='black',fg='red',font='Digital-7, 40')
    licznik_min.grid(row=0,column=0)
    licznik_min['text'] = '0110'
    
    buzka = tk.Button(root,text='start')
    buzka.grid(row=0,column=m//2 - 1)  
    
    zegar = tk.Label(root,bg='black',fg='red',font='Digital-7, 40')
    zegar.grid(row=0,column=m//2 - 6)  
    zegar['text'] = '0001'
    
    gorny_panel = [licznik_min,buzka,zegar]
    
    return gorny_panel

def plansza(root):
    przyciski = [tk.Button(root)for i in range(n*m)]
    
    for i in range(n):
        for j in range(m):
            przyciski[i*m+j].grid(row=i+1,column=j)
            
    return przyciski
            
    

if __name__ == '__main__':
    root = inicjalizacjaokna()
    
    gorny_panel = panelgorny(root)
    
    przyciski = plansza(root)
    
    
    root.mainloop()
