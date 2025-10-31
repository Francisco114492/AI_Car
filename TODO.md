 ``Parte 1:`` 

    TODO: 
    ~Continuar a implementar os dados da imagem ficarem num txt com o nome da imagem.

    ~Dividir o código em Neural Networks e update functions, para que modificar e testar novas combinações seja mais fácil
    
    (meio feito, usa uma lib) Update functions em C++ para podermos usar threads
    
    (não aplicável) neural network talvez também beneficie

    implica modificar main.py e car_nn

    função ou ficheiro que recebe nome de imagem, vai buscar a imagem e os dados


`` Futuro:``

Menu onde pode ser selecionado pixel e a distância original da pista (possivelmente também mostrar em baixo a distância em pixels)
Em baixo mostra as coordenadas.
Ao selecionar um ponto (com botão esquerdo), dá "lock" nesse ponto.
Depois de dar "lock", deixa rodar para escolher um ângulo.
A seguir deixa criar um txt com os dados.


``Next steps:``
    1 - tracks
    2 - sliders com os vários parâmetros modificáveis


Guidelines:

| Type                    | Convention                      | Example                |
| ----------------------- | ------------------------------- | ---------------------- |
| **Package (folder)**    | `lowercase_with_underscores`    | `neural_networks`      |
| **Module (file)**       | `lowercase_with_underscores.py` | `car_brain.py`         |
| **Class**               | `CamelCase`                     | `NeuralNetwork`        |
| **Function**            | `lowercase_with_underscores()`  | `train_model()`        |
| **Variable**            | `lowercase_with_underscores`    | `learning_rate`        |
| **Constant**            | `ALL_CAPS_WITH_UNDERSCORES`     | `MAX_SPEED`            |
| **Method (class func)** | `lowercase_with_underscores()`  | `update_position()`    |
| **Private**             | `_single_leading_underscore`    | `_calculate_fitness()` |
| **Special (dunder)**    | `__double_underscores__`        | `__init__()`           |
