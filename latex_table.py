class latex:
    def __init__(self):
        self.rows = []
        self.num_rows = 0
    def collect_row(self, row):
        first_cell = row[0]
        str_row = ' & '.join([str(cell) for cell in row])
        self.num_rows = len(row) - 1
        if not isinstance(first_cell,str):
            self.rows.append(str_row + '\\\\ \n')
            return
        if '*' in first_cell:
            row.replace('*','$\\times$',1)
        if '_' in first_cell:
            row.replace('_','\\&',1)
        self.rows.append(str_row + '\\\\ \n')

    def hline(self):
        self.rows.append('\\hline \\\\ \n')

    def empty_row(self):
        self.rows.append('& '*self.num_rows + '\\\\ \n')
    
    def write_table(self,fname):
        with open(fname,'w') as f:
            for row in self.rows:
                f.write(row)
