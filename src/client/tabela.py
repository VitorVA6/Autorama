from tkinter import *
  
  
class Table:
      
    def __init__(self,root, p1, p2, p3, p4):        
        lst = [
            (p1['pos'], p1['nome'], p1['equipe'], str(p1['time'])[0:6], str(p1['bestTime'])[0:6], p1['voltas']),
            (p2['pos'], p2['nome'], p2['equipe'], str(p2['time'])[0:6], str(p2['bestTime'])[0:6], p2['voltas']),
            (p3['pos'], p3['nome'], p1['equipe'], str(p3['time'])[0:6], str(p3['bestTime'])[0:6], p3['voltas']),
            (p4['pos'], p4['nome'], p4['equipe'], str(p4['time'])[0:6], str(p4['bestTime'])[0:6], p4['voltas']),
        ]
        lst.sort(key = lambda c: float(c[4]))  

        total_rows = len(lst)
        total_columns = len(lst[0])
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                  
                self.e = Entry(root, width=8, fg='blue',
                               font=('Arial',16,'bold'))
                  
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])