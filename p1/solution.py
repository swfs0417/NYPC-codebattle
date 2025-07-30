import numpy as np

board = np.zeros(10, 17)
selected = np.zeros(10, 17)
# 선택된 칸은 0으로 나타낼 예정
# 내 다음 사람이 내거를 덮어쓰지 않게만 배치
# 불가능할 경우 패스

def deepcopy(a):
    return np.array([arr[:] for arr in a])

while True:
  line = input().split()
  if line[0] == 'READY':
      print('OK')
  elif line[0] == 'INIT':
      # 시작
      board = np.array(map(list, line[1:]))
  elif line[0] == 'TIME':
      # 본인 선택
      pass 
  elif line[0] == 'OPP':
      # 상대 선택
      x1, y1, x2, y2 = map(int, line[1:-1])
      board[x1:x2, y1:y2] = 0
      selected[x1:x2, y1:y2] = -1
  elif line[0] == 'FINISH':
      break

def check(r1, c1, r2, c2, board = board):
    if board[r1] and board[r2] and board[c1] and board[c2]:
        # 선택 가능한 범위의 합
        return board[r1:r2, c1:c2].sum()
    else:
        # 선택할 수 없는 범위
        return False

def findcan(x1 = 0, y1 = 0, x2 = 10, r2 = 17, board = board):
    cando = []
    for r1 in range(x1, x2):
        for c1 in range(y1, r2):
            for r2 in range(r1, x2):
                for c2 in range(c1, r2):
                    nowsize = check(r1, c1, r2, c2)
                    if nowsize == 10:
                        temp = deepcopy(board)
                        temp[r1:c1, r2:c2] = 0
                    elif nowsize > 10:
                        break
    