import pandas as pd

# 레벤슈타인 거리 구하기
def calc_distance(a, b):
    ''' 레벤슈타인 거리 계산하기 
        refference : 12주차 실습자료 '''
    if a == b: return 0 # 같으면 0을 반환
    a_len = len(a) # a 길이
    b_len = len(b) # b 길이
    if a == "": return b_len
    if b == "": return a_len
    
    # 2차원 표 (a_len+1, b_len+1) 준비하기 --- (※1)
    # matrix 초기화의 예 : [[0, 1, 2, 3], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [3, 0, 0, 0, 0], [4, 0, 0, 0, 0]]
    #    [0, 1, 2, 3]
    #    [1, 0, 0, 0]
    #    [2, 0, 0, 0]
    #    [3, 0, 0, 0] 
    #       서  울 시
    #    [0, 1, 2, 3]
    # 서 [1, 0, 1, 2]
    # 울 [2, 1, 0, 1]
    # 시 [3, 2, 1, 0] 
    matrix = [[] for i in range(a_len+1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
    for i in range(a_len+1): # 0으로 초기화
        matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
    # 0일 때 초깃값을 설정
    for i in range(a_len+1): 
        matrix[i][0] = i
    for j in range(b_len+1):
        matrix[0][j] = j
    # 표 채우기 --- (※2)
    # print(matrix,'----------')
    for i in range(1, a_len+1):
        ac = a[i-1]
        # print(ac,'=============')
        for j in range(1, b_len+1):
            bc = b[j-1] 
            # print(bc)
            cost = 0 if (ac == bc) else 1  #  파이썬 조건 표현식 예:) result = value1 if condition else value2
            matrix[i][j] = min([
                matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
            ])
            # print(matrix)
        # print(matrix,'----------끝')
    return matrix[a_len][b_len]


def find_best_answer(input_sentence):
    # 파일 경로 지정
    filepath = 'ChatbotData.csv'

    data = pd.read_csv(filepath)            # csv파일 읽어 오기
    questions = data['Q'].tolist()          # 질문열만 뽑아 파이썬 리스트로 저장
    distance = 0                            # 거리값 결과 저장 변수 초기화
    
    for i in range(len(questions)) : # 입력된 질문과 전체 질문(보유한)과의 레빈스타인 거리값을 구하기 위한 반복문
        
        # 데이터프레임의 question행과 비교해서 레빈스타인 거리 구하는 함수 호출    
        distance = calc_distance(input_sentence, questions[i])  
        data.loc[i, 'label'] = distance     # 구한 거리값을 데이터 프레임 label 컬럼에 저장
        # print(data.loc[i])
  
    result = data.sort_values(by='label').iat[0,1]  # label 컬럼(레빈스타인 거리값)을 오름차순으로 정렬 후 값만 추출
    return result


# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')         # 입력 질문 받기
    if input_sentence.lower() == '종료':    # [종료]입력시 프로그램 종료
        break
    response = find_best_answer(input_sentence) # 대답 구하는 함수 호출
    print('Chatbot:', response)
    
