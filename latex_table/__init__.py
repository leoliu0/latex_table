class latex:
    def __init__(self, bdec=3, tdec=2):
        self.rows = []
        self.num_rows = 0
        self.bdec = bdec
        self.tdec = tdec

    def star(self, tval):
        v = abs(tval)
        stars = ""
        if v > 1.644:
            stars = "*"
        if v >= 1.96:
            stars = "**"
        if v > 2.575:
            stars = "***"
        return stars

    def collect_row(self, row, rounding=0):
        first_cell = row[0]
        self.num_rows = len(row) - 1
        try:
            if rounding == 0:
                str_row = " & ".join([f"{int(cell):,}" for cell in row[1:]])
            else:
                str_row = " & ".join([f"{round(cell,rounding):,}" for cell in row[1:]])
        except:
            str_row = " & ".join(row[1:])

        if not isinstance(first_cell, str):
            self.rows.append(str_row + "\\\\ \n")
            return
        if "*" in first_cell:
            row.replace("*", "$\\times$", 1)
        if "_" in first_cell:
            row.replace("_", "\\&", 1)
        self.rows.append(first_cell + "&" + str_row + "\\\\ \n")

    def collect_t(self, row):
        first_cell = row[0]
        str_row = " & ".join(["(" + str(round(cell, self.tdec)) + ")" for cell in row])
        self.num_rows = len(row) - 1
        if not isinstance(first_cell, str):
            self.rows.append(str_row + "\\\\ \n")
            return
        if "*" in first_cell:
            row.replace("*", "$\\times$", 1)
        if "_" in first_cell:
            row.replace("_", "\\&", 1)
        self.rows.append(str_row + "\\\\ \n")

    def collect_beta_t(self, zipped):
        betas, ts = [], []
        for beta, t in zipped:
            if isinstance(beta, float):
                betas.append(str(round(beta, self.bdec)) + self.star(t))
                ts.append("(" + str(round(t, self.tdec)) + ")")
            else:
                betas.append(beta)
                ts.append(t)
        row = betas
        first_cell = row[0]
        str_row = " & ".join([cell for cell in row])
        str_t = " & ".join([cell for cell in ts])
        self.num_rows = len(row) - 1
        if not isinstance(first_cell, str):
            self.rows.append(str_row + "\\\\ \n")
            return
        if "*" in first_cell:
            str_row.replace("*", "$\\times$", 1)
        if "_" in first_cell:
            str_row.replace("_", "\\&", 1)
        self.rows.append(str_row + "\\\\ \n")
        self.rows.append(str_t + "\\\\ \n")

    def hline(self):
        #  self.rows.append('\\hline \\\\ \n')
        self.rows.append("\\hline \n")

    def write_empty_row(self):
        self.rows.append("\\\\ \n")

    def write_plain_row(self, text):
        self.rows.append(text + "\\\\ \n")

    def write_table(self, fname, mode, debug=False):
        for i in range(1, 10):
            self.rows[-i] = self.rows[-i].replace("hline", "").strip().strip("\\")
            if self.rows[-i]:
                break
        if debug:
            print(self.rows)
        with open(fname, mode) as f:
            for row in self.rows:
                f.write(row)
