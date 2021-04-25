from tkinter import *
  
  
class RaceTable:
      
    def __init__(self,root, p1, p2):
        if p1['pos'] == '1':
            lst = [
                (p1['pos'], p1['nome'], p1['equipe'], str(p1['time'])[0:6], p1['voltas']),
                (p2['pos'], p2['nome'], p2['equipe'], str(p2['time'])[0:6], p2['voltas']),
                ]
        else:
            lst = [                
                (p2['pos'], p2['nome'], p2['equipe'], str(p2['time'])[0:6], p2['voltas']),
                (p1['pos'], p1['nome'], p1['equipe'], str(p1['time'])[0:6], p1['voltas']),
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