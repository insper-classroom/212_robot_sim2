import cv2
import math

def calcula_pf(linha1, linha2):
    x0, y0, x1, y1 = linha1
    m1 = (y1-y0)/(x1-x0)
    h1 = y1 - m1*x1

    x0, y0, x1, y1 = linha2
    m2 = (y1-y0)/(x1-x0)
    h2 = y1 - m2*x1

    x_i = (h2 - h1)/(m1 - m2)
    y_i = m1*x_i + h1

    return int(x_i), int(y_i)


def pontos_fuga(img_bgr):
    """
    Cria e retorna uma nova imagem BGR com os
    pontos de fuga desenhados.

    Entrada:
    - img_bgr: imagem original no formato BGR

    Saída:
    - resultado: imagem BGR com os pontos de fuga desenhados 
    """

    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    min_hsv = (220/2, 50, 50)
    max_hsv = (260/2, 255, 255)

    mask = cv2.inRange(hsv, min_hsv, max_hsv)

    cv2.imshow('Mascara', mask)

    # Pegar as linhas
    linhas = cv2.HoughLinesP(mask, 1, math.radians(1), 300)
    print(linhas.shape)
    print(linhas)

    m_positivo = []
    m_negativo = []

    for linha in linhas:
        x0 = linha[0][0]
        y0 = linha[0][1]
        x1 = linha[0][2]
        y1 = linha[0][3]

        # Calcular m
        m = (y1 - y0)/(x1 - x0)

        if ((y1-y0)**2+(x1-x0)**2)**0.5 > 100:
            if m > 0:
                m_positivo.append((m, linha))
            else :
                m_negativo.append((m, linha))

    # Encontrar a L1 e L3
    menor_valor = 999999
    menor_linha = None
    maior_valor = -99999
    maior_linha = None
    for m, linha in m_negativo:
        if menor_valor > m:
            menor_valor = m
            menor_linha = linha
        if maior_valor < m:
            maior_valor = m
            maior_linha = linha

    resultado = img_bgr.copy()

    L3_x0, L3_y0, L3_x1, L3_y1 = maior_linha[0]
    cv2.line(resultado, (L3_x0,L3_y0), (L3_x1, L3_y1), (0,0,255), 5)

    L1_x0, L1_y0, L1_x1, L1_y1 = menor_linha[0]
    cv2.line(resultado, (L1_x0,L1_y0), (L1_x1, L1_y1), (0,225,0), 5)

    # Encontrar a L2:
    L2_x0, L2_y0, L2_x1, L2_y1 = m_positivo[0][1][0]
    cv2.line(resultado, (L2_x0,L2_y0), (L2_x1, L2_y1), (0,225,255), 5)

    # Encontrar os pontos de fuga
    linha1 = L1_x0, L1_y0, L1_x1, L1_y1
    linha2 = L2_x0, L2_y0, L2_x1, L2_y1
    linha3 = L3_x0, L3_y0, L3_x1, L3_y1

    ponto1 = calcula_pf(linha1, linha2)
    ponto2 = calcula_pf(linha2, linha3)

    print(ponto1)
    print(ponto2)

    cv2.circle(resultado, ponto1, 10, (0,255,0), -1)
    cv2.circle(resultado, ponto2, 10, (0,0,255), -1)

    return resultado


if __name__ == "__main__":
    bgr = cv2.imread('figura_q1.png')
    resultado = pontos_fuga(bgr)

    cv2.imwrite("figura_q1_resultado.png", resultado)

    cv2.imshow('Original', bgr)
    cv2.imshow('Pontos de fuga', resultado)
    cv2.waitKey()
    cv2.destroyAllWindows()