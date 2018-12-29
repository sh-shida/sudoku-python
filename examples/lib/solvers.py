class Solver:
  def __init__(self, matrix, debug):
    self.matrix = matrix
    self.debug = debug

  def solve(self):
    pass
  
  def debug_print(self, message):
    if self.debug: print(message)


class SimpleSolver(Solver):
  def __init__(self, matrix, debug=False):
    super().__init__(matrix, debug)

  def solve(self, epochs=10):
    def fix(cell, num):
      self.debug_print('update %s:%s "%s" => "%s"' % (cell.row+1, cell.col+1, cell.value, num))
      cell.value = num
      cell.is_fixed = True
      cell.candidates.data = []

      for cells in [self.matrix.get_row(cell.row).cells, self.matrix.get_col(cell.col).cells]:
        for cell in cells:
          if num in cell.candidates.data:
            self.debug_print('remove %s from %s:%s' % (num, cell.row+1, cell.col+1))
            cell.candidates.data.remove(num)

    for _ in range(epochs):
      for num in range(self.matrix.order):
        num += 1

        for target in [self.matrix.get_row, self.matrix.get_col]:
          for i in range(self.matrix.order):      
            unit = target(i)
            if num in unit.values: continue

            cells = [cell for cell in unit.cells if num in cell.candidates.data]
            if len(cells) is 1:
              fix(cells[0], num)
              break
