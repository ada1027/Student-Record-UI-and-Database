import tkinter
import tkinter.font as tkFont

# reference: https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
class Sortable_list_box(object):
    def __init__(self, ttk, container, headings, height):
        self.tree = None
        self.ttk = ttk
        self.container = container
        self.headings = headings
        self.height = height
        self._setup_widgets()

    def show_items(self, items):
        self.items = items
        if (self.tree != None):
            for i in self.tree.get_children():
                self.tree.delete(i)
        for item in self.items:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                if val:
                    col_w = tkFont.Font().measure(val)
                    if self.tree.column(self.headings[ix],width=None)<col_w:
                        self.tree.column(self.headings[ix], width=col_w)

    def _setup_widgets(self):
        container = tkinter.Frame(self.container)
        container.pack(fill='both', expand=True)

        # create a treeview with dual scrollbars
        self.tree = self.ttk.Treeview(self.container, columns=self.headings, show="headings", height = self.height)
        vsb = self.ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = self.ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        for col in self.headings:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: self.sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()),)

    def sortby(self, tree, col, descending):
        # grab values to sort
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda c=col: self.sortby(tree, c, \
            int(not descending)))
        
''' end of sortable_list_box '''
