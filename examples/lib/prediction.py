class Prediction:
  def __init__(self, question, solver, debug=False):
    self.matrix = Matrix(question)
    self.solver = solver(self.matrix, debug)

    for cell in self.matrix.flatten():
      if cell.is_fixed: continue
      box = self.matrix.get_box_by_global_point(cell.row, cell.col)
      candidate_values = [[], []]

      for i,target in enumerate([self.matrix.get_row(cell.row), self.matrix.get_col(cell.col)]):
        used_values = [c.value for c in target.cells if c.is_fixed]
        candidate_values[i] = [j+1 for j in range(len(self.matrix.data)) if not j+1 in used_values]

      cell.candidates.add([x for x in candidate_values[0] if x in candidate_values[1] and not box.has_value(x)])
    self.solver.solve()


from math import sqrt
class Matrix:
  def __init__(self, question):
    self.data = []
    self.order = int(len(question))
    for i, row in enumerate(question):
      self.data.append([])
      for j, value in enumerate(row):
        self.data[i].append(Cell(i, j, value))

  def raw(self):
    rows = []
    for i in range(self.order):
      rows.append([cell.value for cell in self.get_row(i).cells])
    return rows

  def get_cell(self, row, col):
    return self.data[row][col]

  def get_row(self, num):
    start_position = self.order * num
    end_position = start_position + self.order
    row = Row(self.order)
    for cell in self.flatten()[start_position:end_position]: row.set(cell)
    return row

  def get_col(self, num):
    cells = self.flatten()
    column = Column(self.order)
    for i in range(self.order):
      start_position = self.order * i
      end_position = start_position + self.order
      column.set(cells[start_position:end_position][num])
    return column
  
  def get_box_by_global_point(self, row, col):
    sqrt_order = int(sqrt(self.order))
    box_row = int(row / sqrt_order)
    box_col = int(col / sqrt_order)
    box = Box(box_row, box_col, sqrt_order)
    start_row = box_row * sqrt_order
    end_row = start_row + sqrt_order
    start_col = box_col * sqrt_order
    end_col = start_col + sqrt_order
    for cell in self.flatten():
      if start_row <= cell.row < end_row and start_col <= cell.col < end_col:
        box.set(cell)
    return box

  def flatten(self):
    def _flatten(data):
      return [element
        for item in data
        for element in (_flatten(item) if hasattr(item, '__iter__') else [item])]
    return _flatten(self.data)


class Unit:
  def __init__(self, size):
    self.data = []
    self.size = size

  @property
  def values(self):
    values = []
    for target in self.data:
      if type(target) is list:
        values += [cell.value for cell in target]
      else:
        values.append(target.value)
    return values

  @property
  def cells(self):
    cells = []
    for target in self.data:
      if type(target) is list:
        cells += [cell for cell in target]
      else:
        cells.append(target)
    return cells

  def has_value(self, value):
    return value in self.values


class Box(Unit):
  def __init__(self, row, col, size):
    super().__init__(size)
    self.row = row
    self.col = col
    for i in range(size):
      self.data.append([])
      for j in range(size):
        self.data[i].append(None)
    
  def set(self, cell):
    index_row = cell.row - self.row*self.size
    index_col = cell.col - self.col*self.size
    self.data[index_row][index_col] = cell


class Row(Unit):
  def __init__(self, size):
    super().__init__(size)
    for _ in range(size): self.data.append(None)

  def set(self, cell):
    self.data[cell.col] = cell


class Column(Unit):
  def __init__(self, size):
    super().__init__(size)
    for _ in range(size): self.data.append(None)

  def set(self, cell):
    self.data[cell.row] = cell


class Cell:
  def __init__(self, row, col, value):
    self.row = row
    self.col = col
    self.value = value
    self.candidates = Candidates()
    self.is_fixed = self.value is not 0


class Candidates:
  def __init__(self):
    self.data = []

  def add(self, values):
    if type(values) is not list:
      values = [values]
    for value in values:
      self.data.append(value)
