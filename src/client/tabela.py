from tkinter import *
  
  
class Table:
      
    def __init__(self,root, p1, p2):
        if p1['pos'] == '1':
            lst = [
                (p1['pos'], p1['nome'], p1['equipe'], str(p1['time'])[1:7], str(p1['bestTime'])[1:7], p1['voltas']-1),
                (p2['pos'], p2['nome'], p2['equipe'], str(p2['time'])[1:7], str(p2['bestTime'])[1:7], p2['voltas']-1),
                ]
        else:
            lst = [                
                (p2['pos'], p2['nome'], p2['equipe'], str(p2['time'])[1:7], str(p2['bestTime'])[1:7], p2['voltas']-1),
                (p1['pos'], p1['nome'], p1['equipe'], str(p1['time'])[1:7], str(p1['bestTime'])[1:7], p1['voltas']-1),
                ]

        total_rows = len(lst)
        total_columns = len(lst[0])
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                  
                self.e = Entry(root, width=8, fg='blue',
                               font=('Arial',16,'bold'))
                  
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])