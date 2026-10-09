QUIZZES = {

    "A novela que marcou época": [
        {"pergunta": "Quem interpretou Carminha em Avenida Brasil?", "alternativas": ["Adriana Esteves", "Glória Pires", "Débora Falabella"], "correta": 0},
        {"pergunta": "Juma Marruá é personagem de qual novela?", "alternativas": ["Pantanal", "O Rei do Gado", "Renascer"], "correta": 0},
        {"pergunta": "Nazaré Tedesco é personagem de qual novela?", "alternativas": ["Senhora do Destino", "Avenida Brasil", "Mulheres de Areia"], "correta": 0},
    ],

    "Desafio de lógica: pense antes de responder": [
        {"pergunta": "Se você ultrapassa a pessoa que está em segundo lugar numa corrida, em que posição fica?", "alternativas": ["Em primeiro", "Em segundo", "Em terceiro"], "correta": 1},
        {"pergunta": "Cinco máquinas fazem cinco peças em cinco minutos. Quanto tempo 100 máquinas levam para fazer 100 peças?", "alternativas": ["5 minutos", "20 minutos", "100 minutos"], "correta": 0},
        {"pergunta": "Dois pais e dois filhos sentam à mesa, mas são apenas três pessoas. Como isso é possível?", "alternativas": ["São avô, pai e filho", "Um deles não come", "Há um filho imaginário"], "correta": 0},
    ],

    "Português sem tropeço": [
        {"pergunta": "Qual palavra está escrita corretamente?", "alternativas": ["Excessão", "Exceção", "Eceção"], "correta": 1},
        {"pergunta": "Qual é o plural de cidadão?", "alternativas": ["Cidadões", "Cidadães", "Cidadãos"], "correta": 2},
        {"pergunta": "Na frase ‘Quero mais café, mas já está tarde’, qual palavra indica oposição?", "alternativas": ["Quero", "Mais", "Mas"], "correta": 2},
    ],

    "Curiosidades do Brasil": [
        {"pergunta": "Qual cidade é conhecida como Cidade Maravilhosa?", "alternativas": ["Rio de Janeiro", "Salvador", "Recife"], "correta": 0},
        {"pergunta": "Em qual estado fica a cidade histórica de Ouro Preto?", "alternativas": ["Bahia", "Minas Gerais", "Goiás"], "correta": 1},
        {"pergunta": "O frevo é uma manifestação cultural tradicional de qual estado?", "alternativas": ["Amazonas", "Paraná", "Pernambuco"], "correta": 2},
    ],

    "Animais que parecem inventados": [
        {"pergunta": "Qual animal possui três corações?", "alternativas": ["Polvo", "Tartaruga", "Crocodilo"], "correta": 0},
        {"pergunta": "Qual mamífero põe ovos?", "alternativas": ["Canguru", "Ornitorrinco", "Lontra"], "correta": 1},
        {"pergunta": "Qual ave consegue voar para trás?", "alternativas": ["Pinguim", "Avestruz", "Beija-flor"], "correta": 2},
    ],

    "Comidas famosas pelo mundo": [
        {"pergunta": "Qual é o principal ingrediente do guacamole?", "alternativas": ["Abacate", "Maçã", "Melancia"], "correta": 0},
        {"pergunta": "O sushi é tradicionalmente associado à culinária de qual país?", "alternativas": ["Itália", "Japão", "México"], "correta": 1},
        {"pergunta": "A pizza Margherita surgiu em qual cidade italiana?", "alternativas": ["Roma", "Milão", "Nápoles"], "correta": 2},
    ],

    "Você viveu os anos 2000?": [
        {"pergunta": "Qual rede social ficou muito popular no Brasil nos anos 2000?", "alternativas": ["Orkut", "TikTok", "Threads"], "correta": 0},
        {"pergunta": "Qual aparelho portátil era usado para ouvir músicas em arquivos MP3?", "alternativas": ["Pager", "MP3 player", "Fax"], "correta": 1},
        {"pergunta": "GTA San Andreas ficou muito conhecido no Brasil em qual videogame?", "alternativas": ["Nintendo DS", "Game Boy", "PlayStation 2"], "correta": 2},
    ],

    "Ciência do dia a dia": [
        {"pergunta": "Qual é o maior planeta do Sistema Solar?", "alternativas": ["Júpiter", "Marte", "Mercúrio"], "correta": 0},
        {"pergunta": "Qual é o maior órgão do corpo humano?", "alternativas": ["Fígado", "Pele", "Coração"], "correta": 1},
        {"pergunta": "Ao nível do mar, a água ferve aproximadamente a quantos graus Celsius?", "alternativas": ["50 °C", "80 °C", "100 °C"], "correta": 2},
    ],

    "Mistérios e fatos da história": [
        {"pergunta": "As pirâmides de Gizé ficam em qual país?", "alternativas": ["Egito", "Peru", "Grécia"], "correta": 0},
        {"pergunta": "Qual monumento pré-histórico fica na Inglaterra?", "alternativas": ["Machu Picchu", "Stonehenge", "Taj Mahal"], "correta": 1},
        {"pergunta": "Quem foi o primeiro ser humano a pisar na Lua?", "alternativas": ["Yuri Gagarin", "Buzz Aldrin", "Neil Armstrong"], "correta": 2},
    ],

    "Cinema e animação: você reconhece?": [
        {"pergunta": "Em qual escola de magia Harry Potter estuda?", "alternativas": ["Hogwarts", "Nárnia", "Nevermore"], "correta": 0},
        {"pergunta": "Qual personagem canta ‘Livre Estou’ em Frozen?", "alternativas": ["Anna", "Elsa", "Olaf"], "correta": 1},
        {"pergunta": "Shrek é de que tipo de criatura?", "alternativas": ["Dragão", "Gigante", "Ogro"], "correta": 2},
    ],

    "Coisas do cotidiano que todo mundo conhece": [
        {"pergunta": "Qual objeto usamos para apagar o que foi escrito a lápis?", "alternativas": ["Borracha", "Colher", "Pente"], "correta": 0},
        {"pergunta": "Qual destes objetos costuma ter ponteiros?", "alternativas": ["Copo", "Relógio", "Prato"], "correta": 1},
        {"pergunta": "Qual objeto normalmente usamos para abrir uma porta trancada?", "alternativas": ["Garfo", "Tesoura", "Chave"], "correta": 2},
    ],

}


# Legendas prontas para publicar: uma legenda para cada vídeo gerado.
# O nome do tema deve corresponder exatamente a uma chave de QUIZZES.
LEGENDAS = {
    "A novela que marcou época": (
        "Você lembra dessas novelas que marcaram época? 📺\n"
        "Responda ao quiz e conte nos comentários quantas acertou!\n\n"
        "#Quiz #Novelas #AvenidaBrasil #Pantanal #Entretenimento #Desafio"
    ),
    "Desafio de lógica: pense antes de responder": (
        "Atenção: pense bem antes de responder! 🧠\n"
        "Faça o desafio de lógica e comente sua pontuação no final.\n\n"
        "#Quiz #DesafioDeLogica #Raciocinio #Desafio #Perguntas"
    ),
    "Português sem tropeço": (
        "Será que você acerta todas sem tropeçar? ✍️\n"
        "Teste seu português e compartilhe quantas respostas acertou!\n\n"
        "#Quiz #LinguaPortuguesa #Portugues #Conhecimento #Desafio"
    ),
    "Curiosidades do Brasil": (
        "Um passeio rápido por algumas curiosidades do Brasil! 🇧🇷\n"
        "Responda e deixe nos comentários quantas você acertou.\n\n"
        "#Quiz #Brasil #Curiosidades #CulturaBrasileira #Conhecimento"
    ),
    "Animais que parecem inventados": (
        "Esses animais parecem inventados, mas são reais! 🐙\n"
        "Tente acertar as respostas antes do tempo acabar.\n\n"
        "#Quiz #Animais #Curiosidades #Natureza #VoceSabia"
    ),
    "Comidas famosas pelo mundo": (
        "Vamos dar uma volta pelo mundo da gastronomia? 🍕\n"
        "Responda ao quiz e conte sua pontuação nos comentários!\n\n"
        "#Quiz #Comida #Gastronomia #Curiosidades #Culinaria"
    ),
    "Você viveu os anos 2000?": (
        "Bateu nostalgia dos anos 2000? 📱\n"
        "Veja quantas dessas lembranças você reconhece e comente sua pontuação!\n\n"
        "#Quiz #Anos2000 #Nostalgia #Orkut #Curiosidades"
    ),
    "Ciência do dia a dia": (
        "Quanto você sabe sobre a ciência que aparece no dia a dia? 🔬\n"
        "Responda ao quiz e veja quantas acertou!\n\n"
        "#Quiz #Ciencia #Conhecimento #Curiosidades #Aprenda"
    ),
    "Mistérios e fatos da história": (
        "Teste seus conhecimentos sobre história e mistérios! 🏛️\n"
        "Comente quantas respostas você acertou.\n\n"
        "#Quiz #Historia #Curiosidades #Conhecimento #Desafio"
    ),
    "Cinema e animação: você reconhece?": (
        "Você reconhece esses personagens do cinema e da animação? 🎬\n"
        "Responda ao quiz e conte sua pontuação nos comentários!\n\n"
        "#Quiz #Cinema #Animacao #Filmes #Entretenimento"
    ),
    "Coisas do cotidiano que todo mundo conhece": (
        "Um quiz rápido sobre objetos do nosso cotidiano! 🧩\n"
        "Será que você acerta todas? Escreva sua pontuação nos comentários.\n\n"
        "#Quiz #Cotidiano #ConhecimentosGerais #Desafio #Perguntas"
    ),
}

