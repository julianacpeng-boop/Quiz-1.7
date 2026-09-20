from pathlib import Path
import asyncio
import math
import re
import shutil
import subprocess
import sys
import unicodedata

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import edge_tts

from dados_quiz import QUIZZES


# ============================================================
# CONFIGURAÇÕES
# ============================================================

W, H = 1080, 1920
FPS = 30
ANIM_FPS = 20

FUNDO = Path("assets/template_educativo_juh_quiz.png")
SAIDA = Path("output_juh_caderno")

VOICE = "pt-BR-AntonioNeural"
VOICE_RATE = "+10%"

# Cores da identidade visual
AZUL = (17, 47, 121)
AZUL_ESCURO = (7, 23, 78)
ROSA = (255, 58, 150)
ROSA_CLARO = (255, 190, 221, 120)
AMARELO = (255, 215, 25)
PRETO = (18, 18, 22)
BRANCO = (255, 255, 255)

# Área útil da folha do caderno, já no vídeo 1080x1920
PAGE_LEFT = 95
PAGE_RIGHT = 990
PAGE_TOP = 485
PAGE_BOTTOM = 1515

THEME_Y = 525
QUESTION_Y = 665
OPTIONS_Y = 1015

PAUSA_APOS_PERGUNTA = 0.75
PAUSA_APOS_RESPOSTA = 0.70

LETRAS = ("A", "B", "C")


# ============================================================
# UTILIDADES
# ============================================================

def executar(cmd):
    print(" ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, check=True)


def slug(texto):
    s = unicodedata.normalize("NFKD", texto)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "quiz"


def fonte(size, bold=False):
    candidatos = []
    if bold:
        candidatos = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        ]
    else:
        candidatos = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        ]

    for p in candidatos:
        if Path(p).exists():
            return ImageFont.truetype(p, size)

    return ImageFont.load_default()


def fundo_base():
    if not FUNDO.exists():
        raise FileNotFoundError(
            f"Fundo não encontrado: {FUNDO}\n"
            "Coloque a imagem em assets/template_educativo_juh_quiz.png"
        )

    img = Image.open(FUNDO).convert("RGB")
    return img.resize((W, H), Image.Resampling.LANCZOS)


def wrap_pixels(draw, texto, font, max_width):
    palavras = texto.split()
    linhas = []
    atual = ""

    for palavra in palavras:
        teste = palavra if not atual else atual + " " + palavra
        bb = draw.textbbox((0, 0), teste, font=font)
        if bb[2] - bb[0] <= max_width:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra

    if atual:
        linhas.append(atual)

    return linhas


def fit_text(draw, texto, max_width, max_lines, max_size, min_size, bold=True):
    for size in range(max_size, min_size - 1, -2):
        f = fonte(size, bold=bold)
        lines = wrap_pixels(draw, texto, f, max_width)
        if len(lines) <= max_lines:
            return f, lines

    f = fonte(min_size, bold=bold)
    return f, wrap_pixels(draw, texto, f, max_width)[:max_lines]


def text_line_height(draw, font):
    bb = draw.textbbox((0, 0), "Ag", font=font)
    return bb[3] - bb[1]


def duracao_audio(path):
    r = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(r.stdout.strip())


async def _tts(texto, saida):
    communicate = edge_tts.Communicate(
        texto,
        VOICE,
        rate=VOICE_RATE,
    )
    await communicate.save(str(saida))


def tts_salvar(texto, saida):
    saida.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(_tts(texto, saida))


def criar_beep(path, dur=0.20, freq=880):
    executar([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency={freq}:sample_rate=48000:duration={dur}",
        "-ar", "48000",
        "-ac", "2",
        "-c:a", "libmp3lame",
        "-q:a", "4",
        str(path),
    ])

def criar_clipe_imagem(img_path, duracao, out_path, audio_path=None):
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(img_path),
    ]

    if audio_path:
        cmd += ["-i", str(audio_path)]
    else:
        cmd += [
            "-f", "lavfi",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        ]

    cmd += [
        "-t", f"{duracao:.3f}",
        "-vf", f"scale={W}:{H},fps={FPS}",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
    ]

    if audio_path:
        cmd += [
            "-af", "apad,aresample=48000",
            "-ar", "48000",
            "-ac", "2",
            "-c:a", "aac",
            "-b:a", "192k",
        ]
    else:
        cmd += [
            "-ar", "48000",
            "-ac", "2",
            "-c:a", "aac",
            "-b:a", "128k",
        ]

    cmd += [str(out_path)]
    executar(cmd)

def criar_clipe_animado(frames_dir, fps_anim, duracao, out_path, audio_path=None):
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps_anim),
        "-i", str(frames_dir / "frame_%04d.jpg"),
    ]

    if audio_path:
        cmd += ["-i", str(audio_path)]
    else:
        cmd += [
            "-f", "lavfi",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        ]

    cmd += [
        "-t", f"{duracao:.3f}",
        "-vf", f"scale={W}:{H},fps={FPS}",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
    ]

    if audio_path:
        cmd += [
            "-af", "apad,aresample=48000",
            "-ar", "48000",
            "-ac", "2",
            "-c:a", "aac",
            "-b:a", "192k",
        ]
    else:
        cmd += [
            "-ar", "48000",
            "-ac", "2",
            "-c:a", "aac",
            "-b:a", "128k",
        ]

    cmd += [str(out_path)]
    executar(cmd)

def concatenar(clipes, saida):
    lista = saida.parent / "concat.txt"
    with lista.open("w", encoding="utf-8") as f:
        for c in clipes:
            f.write("file '" + str(c.resolve()) + "'\n")

    executar([
        "ffmpeg", "-y",
        "-fflags", "+genpts",
        "-f", "concat",
        "-safe", "0",
        "-i", str(lista),
        "-c:v", "copy",
        "-c:a", "aac",
        "-ar", "48000",
        "-ac", "2",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(saida),
    ])

# ============================================================
# DESENHO DO QUIZ
# ============================================================

def desenhar_lapis(img, x, y, angle=-8):
    """Desenha um lápis animado, sem braço/mão, para evitar corte visual."""
    pencil = Image.new("RGBA", (240, 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(pencil)

    # corpo amarelo
    d.rounded_rectangle([35, 19, 195, 50], radius=8, fill=(255, 205, 35, 255))
    # faixa
    d.rectangle([165, 19, 185, 50], fill=(230, 65, 120, 255))
    # borracha
    d.rounded_rectangle([185, 19, 218, 50], radius=7, fill=(245, 115, 150, 255))
    # madeira
    d.polygon([(35, 19), (35, 50), (6, 35)], fill=(232, 190, 130, 255))
    # grafite
    d.polygon([(6, 35), (17, 29), (17, 41)], fill=(25, 25, 30, 255))
    # detalhe
    d.line([(50, 26), (155, 26)], fill=(255, 235, 120, 220), width=3)

    pencil = pencil.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    base = img.convert("RGBA")
    base.alpha_composite(pencil, (int(x), int(y)))
    return base.convert("RGB")


def desenhar_tema(img, tema):
    draw = ImageDraw.Draw(img)
    f, lines = fit_text(
        draw, tema.upper(),
        max_width=700,
        max_lines=1,
        max_size=55,
        min_size=35,
        bold=True,
    )
    txt = lines[0]
    bb = draw.textbbox((0, 0), txt, font=f)
    tw = bb[2] - bb[0]
    x = (W - tw) // 2

    # faixa suave rosa atrás do tema
    pad_x = 24
    pad_y = 10
    draw.rounded_rectangle(
        [x - pad_x, THEME_Y - pad_y, x + tw + pad_x, THEME_Y + (bb[3]-bb[1]) + pad_y],
        radius=18,
        fill=(255, 208, 226),
    )
    draw.text((x, THEME_Y), txt, font=f, fill=AZUL_ESCURO)


def desenhar_pergunta_e_opcoes(tema, numero, pergunta):
    img = fundo_base()
    desenhar_tema(img, tema)
    draw = ImageDraw.Draw(img)

    # número da questão
    badge_x, badge_y = 120, QUESTION_Y - 8
    draw.ellipse(
        [badge_x, badge_y, badge_x + 66, badge_y + 66],
        fill=ROSA,
    )
    nfont = fonte(34, bold=True)
    ntext = str(numero)
    bb = draw.textbbox((0, 0), ntext, font=nfont)
    draw.text(
        (
            badge_x + 33 - (bb[2]-bb[0])/2,
            badge_y + 33 - (bb[3]-bb[1])/2 - 4,
        ),
        ntext,
        font=nfont,
        fill=BRANCO,
    )

    qx = 210
    qmaxw = PAGE_RIGHT - qx - 35
    qfont, qlines = fit_text(
        draw,
        pergunta["pergunta"],
        max_width=qmaxw,
        max_lines=3,
        max_size=49,
        min_size=35,
        bold=True,
    )
    qlh = text_line_height(draw, qfont) + 12

    q_strokes = []
    y = QUESTION_Y
    for line in qlines:
        draw.text((qx, y), line, font=qfont, fill=PRETO)
        bb = draw.textbbox((qx, y), line, font=qfont)

        # linha por onde o lápis vai passar
        underline_y = bb[3] + 7
        q_strokes.append((bb[0], underline_y, bb[2], underline_y))

        y += qlh

    # alternativas
    options = []
    afont = fonte(42, bold=False)
    a_lh = text_line_height(draw, afont)
    option_y = max(OPTIONS_Y, y + 110)

    for i, alt in enumerate(pergunta["alternativas"]):
        oy = option_y + i * 135
        cx, cy, r = 175, oy + 30, 30

        draw.ellipse(
            [cx-r, cy-r, cx+r, cy+r],
            outline=AZUL_ESCURO,
            width=5,
            fill=BRANCO,
        )
        txt = f"{LETRAS[i]}) {alt}"
        draw.text((240, oy), txt, font=afont, fill=AZUL_ESCURO)
        options.append({
            "circle": (cx, cy, r),
            "text": txt,
        })

    return img, q_strokes, options


def aplicar_traco_rosa(img, strokes, progresso):
    """O lápis passa por todas as linhas da pergunta, uma após a outra."""
    if not strokes:
        return img, (0, 0)

    progresso = max(0.0, min(1.0, progresso))
    n = len(strokes)
    bloco = 1.0 / n

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    tip_x = strokes[0][0]
    tip_y = strokes[0][1]

    for i, (x1, y1, x2, y2) in enumerate(strokes):
        inicio = i * bloco
        fim = (i + 1) * bloco

        if progresso <= inicio:
            break

        if progresso >= fim:
            local = 1.0
        else:
            local = (progresso - inicio) / bloco

        x_atual = x1 + int((x2 - x1) * local)

        d.line(
            [(x1, y1), (x_atual, y1)],
            fill=(255, 75, 160, 165),
            width=16,
        )
        rr = 8
        d.ellipse(
            [x1-rr, y1-rr, x1+rr, y1+rr],
            fill=(255, 75, 160, 165),
        )
        d.ellipse(
            [x_atual-rr, y1-rr, x_atual+rr, y1+rr],
            fill=(255, 75, 160, 165),
        )

        tip_x, tip_y = x_atual, y1

        if local < 1.0:
            break

    out = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return out, (tip_x, tip_y)


def pintar_resposta(img, circle, progresso):
    progresso = max(0.0, min(1.0, progresso))
    cx, cy, r = circle

    out = img.convert("RGBA")
    overlay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # preenchimento amarelo crescendo do centro
    rr = max(1, int(r * progresso))
    d.ellipse(
        [cx-rr, cy-rr, cx+rr, cy+rr],
        fill=(255, 215, 25, 235),
    )

    # contorno permanece visível
    d.ellipse(
        [cx-r, cy-r, cx+r, cy+r],
        outline=AZUL_ESCURO + (255,),
        width=5,
    )

    out = Image.alpha_composite(out, overlay)
    return out.convert("RGB")


def desenhar_contagem(img, numero):
    out = img.copy()
    d = ImageDraw.Draw(out)

    cx, cy = W//2, 1465
    r = 74

    d.ellipse(
        [cx-r, cy-r, cx+r, cy+r],
        fill=(255, 255, 255),
        outline=ROSA,
        width=8,
    )

    f = fonte(72, bold=True)
    txt = str(numero)
    bb = d.textbbox((0, 0), txt, font=f)
    d.text(
        (
            cx - (bb[2]-bb[0])/2,
            cy - (bb[3]-bb[1])/2 - 8,
        ),
        txt,
        font=f,
        fill=AZUL_ESCURO,
    )

    return out


# ============================================================
# GERAÇÃO
# ============================================================

def gerar_video_tema(indice_tema, tema, perguntas):
    pasta = SAIDA / f"{indice_tema:02d}_{slug(tema)}"
    if pasta.exists():
        shutil.rmtree(pasta)
    pasta.mkdir(parents=True, exist_ok=True)

    clipes = []
    beep = pasta / "beep.mp3"
    criar_beep(beep)

    for q_idx, pergunta in enumerate(perguntas, start=1):
        print(f"\n[{tema}] Pergunta {q_idx}", flush=True)

        base, strokes, options = desenhar_pergunta_e_opcoes(
            tema,
            q_idx,
            pergunta,
        )

        # 1) Áudio da pergunta
        audio_q = pasta / f"q{q_idx:02d}_pergunta.mp3"
        tts_salvar(pergunta["pergunta"], audio_q)
        qdur = duracao_audio(audio_q) + PAUSA_APOS_PERGUNTA

        # 2) Lápis passando por todas as linhas da pergunta
        frames_q = pasta / f"frames_q{q_idx:02d}"
        frames_q.mkdir(parents=True, exist_ok=True)

        total_frames = max(18, int(math.ceil(qdur * ANIM_FPS)))

        for fidx in range(total_frames):
            p = fidx / max(1, total_frames - 1)
            frame, (tip_x, tip_y) = aplicar_traco_rosa(
                base.copy(),
                strokes,
                p,
            )

            # posiciona o lápis logo após a ponta do traço
            frame = desenhar_lapis(
                frame,
                tip_x - 18,
                tip_y - 40,
                angle=-8,
            )

            frame.save(
                frames_q / f"frame_{fidx:04d}.jpg",
                quality=92,
            )

        clip_q = pasta / f"{q_idx:02d}_pergunta.mp4"
        criar_clipe_animado(
            frames_q,
            ANIM_FPS,
            qdur,
            clip_q,
            audio_q,
        )
        clipes.append(clip_q)

        # base já marcada por completo para contagem
        marcada, _ = aplicar_traco_rosa(
            base.copy(),
            strokes,
            1.0,
        )

        # 3) Contagem 3, 2, 1
        for numero in (3, 2, 1):
            img_count = desenhar_contagem(marcada, numero)
            png = pasta / f"q{q_idx:02d}_count_{numero}.png"
            img_count.save(png)

            clip = pasta / f"{q_idx:02d}_count_{numero}.mp4"
            criar_clipe_imagem(
                png,
                0.78,
                clip,
                beep,
            )
            clipes.append(clip)

        # 4) Resposta correta: bola fica amarela
        correta = int(pergunta["correta"])
        resposta = pergunta["alternativas"][correta]

        audio_a = pasta / f"q{q_idx:02d}_resposta.mp3"
        tts_salvar(
            f"A resposta correta é: {resposta}.",
            audio_a,
        )
        adur = duracao_audio(audio_a) + PAUSA_APOS_RESPOSTA

        frames_a = pasta / f"frames_a{q_idx:02d}"
        frames_a.mkdir(parents=True, exist_ok=True)

        total_answer_frames = max(14, int(math.ceil(adur * ANIM_FPS)))

        for fidx in range(total_answer_frames):
            p = fidx / max(1, total_answer_frames - 1)
            answer_frame = pintar_resposta(
                marcada.copy(),
                options[correta]["circle"],
                min(1.0, p * 2.4),
            )
            answer_frame.save(
                frames_a / f"frame_{fidx:04d}.jpg",
                quality=92,
            )

        clip_a = pasta / f"{q_idx:02d}_resposta.mp4"
        criar_clipe_animado(
            frames_a,
            ANIM_FPS,
            adur,
            clip_a,
            audio_a,
        )
        clipes.append(clip_a)

    # Tela final
    final_img = fundo_base()
    desenhar_tema(final_img, tema)
    d = ImageDraw.Draw(final_img)
    f1 = fonte(70, bold=True)
    f2 = fonte(44, bold=True)

    txt1 = "QUANTAS VOCÊ ACERTOU?"
    bb = d.textbbox((0, 0), txt1, font=f1)
    d.text(
        ((W - (bb[2]-bb[0]))/2, 820),
        txt1,
        font=f1,
        fill=AZUL_ESCURO,
    )

    txt2 = "Comenta o resultado!"
    bb2 = d.textbbox((0, 0), txt2, font=f2)
    d.text(
        ((W - (bb2[2]-bb2[0]))/2, 960),
        txt2,
        font=f2,
        fill=ROSA,
    )

    final_png = pasta / "final.png"
    final_img.save(final_png)

    final_clip = pasta / "99_final.mp4"
    criar_clipe_imagem(final_png, 2.2, final_clip)
    clipes.append(final_clip)

    saida = SAIDA / f"{indice_tema:02d}_{slug(tema)}.mp4"
    concatenar(clipes, saida)

    print(f"\n✅ Gerado: {saida}", flush=True)


def main():
    if not QUIZZES:
        raise RuntimeError("O dicionário QUIZZES está vazio.")

    SAIDA.mkdir(parents=True, exist_ok=True)

    for indice, (tema, perguntas) in enumerate(QUIZZES.items(), start=1):
        if len(perguntas) == 0:
            continue

        for p in perguntas:
            if len(p["alternativas"]) != 3:
                raise ValueError(
                    f'O tema "{tema}" possui pergunta sem exatamente 3 alternativas.'
                )
            if int(p["correta"]) not in (0, 1, 2):
                raise ValueError(
                    f'O tema "{tema}" possui índice "correta" inválido.'
                )

        gerar_video_tema(indice, tema, perguntas)

    print("\n🎉 Todos os vídeos foram gerados.", flush=True)


if __name__ == "__main__":
    main()
