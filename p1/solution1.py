import numpy as np
import time

# 선택된 칸은 0으로 나타낼 예정
# 가능한 상대칸을 많이 포함하는 경우로 결정

log = ""

board = 0
selected = np.zeros((10, 17))
selected.fill(1)  # 내 선택 0, 남 선택 2, 기본 1


def deepcopy(a):
  """2차원 배열 copy용"""
  return np.array([arr[:] for arr in a])


def check(r1, c1, r2, c2, board=board):
  """선택 가능한 범위라면 그 합을, 선택 불가능하다면 -1을 리턴"""
  r1, r2 = min(r1, r2), max(r1, r2)
  c1, c2 = min(c1, c2), max(c1, c2)

  if (board[r1, c1] and board[r2, c2]) or (board[r1, c2] and board[r2, c1]):
    # 선택 가능한 범위의 합
    return board[r1 : r2 + 1, c1 : c2 + 1].sum()
  else:
    # 선택할 수 없는 범위
    return -1


def findcan(x1=0, y1=0, x2=10, y2=17, board=board):
  """가능한 선택을 제시(힌트)"""
  cando = []
  for r1 in range(x1, x2):
    for c1 in range(y1, y2):
      for r2 in range(r1, x2):
        for c2 in range(c1, y2):
          nowsize = check(r1, c1, r2, c2, board)
          if nowsize == 10:
            cando.append((r1, c1, r2, c2))
          elif nowsize > 10:
            break
  return cando


def overlapping_area(rect1, rect2):
  """
  두 직사각형의 겹치는 영역의 넓이를 반환.
  겹치지 않으면 0을 반환.
  """
  x1_min, y1_min, x1_max, y1_max = rect1
  x2_min, y2_min, x2_max, y2_max = rect2

  # 겹치는 영역의 좌표 계산
  x_overlap = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))
  y_overlap = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))

  return x_overlap * y_overlap


def count_selected_in_rectangle(pos, board=selected, n=0):
  """
  상대가 뺏을 점수계산용

  matrix: 2D numpy array
  rect: (x_min, y_min, x_max, y_max) 형태의 튜플
        - x는 열 (column), y는 행 (row)을 의미

  반환값: 직사각형 내에 있는 n의 개수
  """
  x_min, y_min, x_max, y_max = pos
  submatrix = board[y_min : y_max + 1, x_min : x_max + 1]

  return np.sum(submatrix == n)


def apply(x1, y1, x2, y2, board=board, score=0):
  board[x1 : x2 + 1, y1 : y2 + 1] = 0
  selected[x1 : x2 + 1, y1 : y2 + 1] = score


while True:
  line = input().split()
  if line[0] == "READY":
    print("OK")
  elif line[0] == "INIT":
    # 시작
    board = np.array([list(map(int, list(x))) for x in line[1:]])
  elif line[0] == "TIME":
    # 본인 선택
    cando = findcan(board=board)
    goodtodo = []

    for x1, y1, x2, y2 in cando:
      temp_b = deepcopy(board)
      temp_s = deepcopy(selected)
      temp_b[x1 : x2 + 1, y1 : y2 + 1] = 0
      temp_s[x1 : x2 + 1, y1 : y2 + 1] = 0
      fc = findcan(board=temp_b)  # 다음턴 힌트
      toppos = (-1, -1, -1, -1)
      topscore = 0
      for pos in fc:
        scr = count_selected_in_rectangle(
          pos, temp_s
        ) * 2 + count_selected_in_rectangle(pos, temp_s, 1)
        if scr > topscore:
          topscore = scr
          toppos = pos
      # with open("D:/chanwoo/code/nypc/NYPC-codebattle/p1/log2.txt", "a") as f:
      #   f.writelines(str(topscore) + str(toppos) + "\n\n")
      goodtodo.append(
        (
          x1,
          y1,
          x2,
          y2,
          count_selected_in_rectangle((x1, y1, x2, y2), board=selected, n=2) * 2
          + count_selected_in_rectangle((x1, y1, x2, y2), board=selected, n=1)
          - (topscore),
        )  # 내가 얻을 점수 - 해당 선택에 대해 상대가 얻을 점수
      )
    top = (-1, -1, -1, -1)
    ts = -1
    for x1, y1, x2, y2, score in goodtodo:
      # with open("D:/chanwoo/code/nypc/NYPC-codebattle/p1/log2.txt", "a") as f:
      #   f.writelines(str(selected[x1 : x2 + 1, y1 : y2 + 1].sum()) + "\n")
      if score > ts:
        top = (x1, y1, x2, y2)
        ts = score
    print(*top)
    apply(*top, board)

  elif line[0] == "OPP":
    # 상대 선택
    apply(*map(int, line[1:5]), board, 2)
  elif line[0] == "FINISH":
    break
