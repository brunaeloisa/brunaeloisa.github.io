---
title: Processamento Digital de Imagens (DCA0445)
layout: page
---

Bruna Soares <brunaeloisa7@gmail.com\>  
André Varela <andre.varela.104@ufrn.edu.br\>
<hr>

# Sumário
* [1ª Unidade](#1a-unidade)
    - [2.2. Exercícios](#exercicios2)
    - [3.2. Exercícios](#exercicios3)
    - [4.2. Exercícios](#exercicios4)
    - [5.2. Exercícios](#exercicios5)
    - [6.1. Exercícios](#exercicios6)

## 1ª Unidade <a name="1a-unidade"></a>

### 2.2. Exercícios <a name="exercicios2"></a>

* Utilizando o programa exemplos/pixels.cpp como referência, implemente um programa regions.cpp. Esse programa deverá solicitar ao usuário as coordenadas de dois pontos P1 e P2 localizados dentro dos limites do tamanho da imagem e exibir que lhe for fornecida. Entretanto, a região definida pelo retângulo de vértices opostos definidos pelos pontos P1 e P2 será exibida com o negativo da imagem na região correspondente. O efeito é ilustrado na Figura 4.

| ![Imagem de entrada2](imagens/biel.png) |
|:--:|
|*Legenda*|

* Utilizando o programa exemplos/pixels.cpp como referência, implemente um programa trocaregioes.cpp. Seu programa deverá trocar os quadrantes em diagonal na imagem. Explore o uso da classe Mat e seus construtores para criar as regiões que serão trocadas. O efeito é ilustrado na Figura 5.

~~~ python
for i in range(min(p1x, p2x), max(p1x, p2x)+1):
    for j in range(min(p1y, p2y), max(p1y, p2y)+1):
        for k in range(canais):
          img_neg[i,j,k] = 255 - img_neg[i,j,k]
cv2_imshow(img_neg)
~~~

### 3.2. Exercícios <a name="exercicios3"></a>

* Observando-se o programa labeling.cpp como exemplo, é possível verificar que caso existam mais de 255 objetos na cena, o processo de rotulação poderá ficar comprometido. Identifique a situação em que isso ocorre e proponha uma solução para este problema.

* Aprimore o algoritmo de contagem apresentado para identificar regiões com ou sem buracos internos que existam na cena. Assuma que objetos com mais de um buraco podem existir. Inclua suporte no seu algoritmo para não contar bolhas que tocam as bordas da imagem. Não se pode presumir, a priori, que elas tenham buracos ou não.

### 4.2. Exercícios <a name="exercicios4"></a>

* Utilizando o programa exemplos/histogram.cpp como referência, implemente um programa equalize.cpp. Este deverá, para cada imagem capturada, realizar a equalização do histogram antes de exibir a imagem. Teste sua implementação apontando a câmera para ambientes com iluminações variadas e observando o efeito gerado. Assuma que as imagens processadas serão em tons de cinza.

* Utilizando o programa exemplos/histogram.cpp como referência, implemente um programa motiondetector.cpp. Este deverá continuamente calcular o histograma da imagem (apenas uma componente de cor é suficiente) e compará-lo com o último histograma calculado. Quando a diferença entre estes ultrapassar um limiar pré-estabelecido, ative um alarme. Utilize uma função de comparação que julgar conveniente.

### 5.2. Exercícios <a name="exercicios5"></a>

* Utilizando o programa exemplos/filtroespacial.cpp como referência, implemente um programa laplgauss.cpp. O programa deverá acrescentar mais uma funcionalidade ao exemplo fornecido, permitindo que seja calculado o laplaciano do gaussiano das imagens capturadas. Compare o resultado desse filtro com a simples aplicação do filtro laplaciano.

### 6.1. Exercícios <a name="exercicios6"></a>

* Utilizando o programa exemplos/addweighted.cpp como referência, implemente um programa tiltshift.cpp. Três ajustes deverão ser providos na tela da interface:
    - um ajuste para regular a altura da região central que entrará em foco;
    - um ajuste para regular a força de decaimento da região borrada;
    - um ajuste para regular a posição vertical do centro da região que entrará em foco. Finalizado o programa, a imagem produzida deverá ser salva em arquivo.


* Utilizando o programa exemplos/addweighted.cpp como referência, implemente um programa tiltshiftvideo.cpp. Tal programa deverá ser capaz de processar um arquivo de vídeo, produzir o efeito de tilt-shift nos quadros presentes e escrever o resultado em outro arquivo de vídeo. A ideia é criar um efeito de miniaturização de cenas. Descarte quadros em uma taxa que julgar conveniente para evidenciar o efeito de stop motion, comum em vídeos desse tipo.