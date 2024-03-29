def star(tval):
    v = abs(tval)
    stars = ""
    if v > 1.644:
        stars = "*"
    if v >= 1.96:
        stars = "**"
    if v > 2.575:
        stars = "***"
    return stars


def normal(x, rounding):
    if isinstance(x, float):
        if rounding == 0:
            return str(int(x))
        return format(round(x, rounding), f".{rounding}f")
    return str(x)


class latex:
    def __init__(self, bdec=3, tdec=2, sdec=3):
        self.rows = []
        self.num_rows = 0
        self.bdec = bdec
        self.tdec = tdec
        self.sdec = sdec

    def collect_list(self, text, rounding=0):
        text = [normal(x, rounding) for x in text]
        self.rows.append(" & ".join(text) + "\\\\ \n")

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

    def collect_beta_t(self, zipped, se=False, stars=True):
        betas, ts = [], []
        for beta, t in zipped:
            if isinstance(beta, float):
                if star:
                    betas.append(f"{beta:.{self.bdec}f}" + star(t))
                else:
                    betas.append(f"{beta:.{self.bdec}f}")
                if se:
                    ts.append(f"({t:.{self.sdec}f})")
                else:
                    ts.append(f"({t:.{self.tdec}f})")
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
        self.rows.append("\\hline \n")

    def write_empty_row(self):
        self.rows.append("\\\\ \n")

    def write_plain_row(self, text):
        self.rows.append(text + "\\\\ \n")

    def write_table(self, fname, mode="w", debug=False):
        self.rows[-1] = self.rows[-1].strip().rstrip("\\\\")
        if self.rows[-1].strip() == "\\":
            self.rows.pop()
        if debug:
            print(self.rows)
        with open(fname, mode) as f:
            for row in self.rows:
                f.write(row)
