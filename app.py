import streamlit as st
from PIL import Image, ImageOps
import io
from streamlit_cropper import st_cropper

# Função para redimensionar a marca d'água e aplicar sobre a imagem
def add_watermark(base_image, watermark, position='bottom', scale=0.1):
    # Redimensiona a marca d'água proporcionalmente ao tamanho da imagem base
    watermark_size = (int(base_image.width * scale), int(watermark.height * (base_image.width * scale) / watermark.width))
    watermark = watermark.resize(watermark_size, Image.LANCZOS)

    # Determina a posição onde a marca d'água será colada
    if position == 'bottom':
        x = (base_image.width - watermark.width) // 2
        y = base_image.height - watermark.height - 10
    else:
        x, y = 0, 0

    # Aplica a marca d'água sobre a imagem base
    transparent = Image.new('RGBA', base_image.size)
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (x, y), watermark)
    return transparent.convert("RGB")

# Interface do Streamlit
st.title("Fique com a cara do bem!")

# Upload da imagem base
uploaded_image = st.file_uploader("Envie sua foto!", type=["png", "jpg", "jpeg"])

# Caminho da marca d'água (pode ser alterado para upload)
uploaded_watermark = "watermark.png"

# Parâmetro de escala da marca d'água
scale = 1

if uploaded_image is not None:
    # Carrega a imagem e corrige a orientação, se necessário
    image = Image.open(uploaded_image)
    image = ImageOps.exif_transpose(image)  # Corrige a orientação da imagem

    # Define a proporção do corte como uma tupla
    aspect_ratio = image.width / image.height
    if aspect_ratio > 1:
        aspect_ratio = (aspect_ratio, 1)  # Se a imagem for mais larga
    else:
        aspect_ratio = (1, aspect_ratio)  # Se a imagem for mais alta

    # Cria duas colunas: uma para o cropper e outra para a imagem resultante
    col1, col2 = st.columns([1, 1])

    # Corte da imagem
    with col1:
        st.write("Selecione a área")
        cropped_image = st_cropper(image, realtime_update=True, box_color="blue", aspect_ratio=aspect_ratio)

    # Carrega a marca d'água
    watermark = Image.open(uploaded_watermark)

    # Adiciona a marca d'água
    result_image = add_watermark(cropped_image, watermark, scale=scale)
    
    # Botão para download
    buf = io.BytesIO()
    result_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="Baixar Imagem",
        data=byte_im,
        file_name="imagem_com_marca_dagua.png",
        mime="image/png"
    )

# Estilização CSS para ajustar a altura da imagem sem ocupar toda a largura da tela
st.markdown(
    """
    <style>
    .css-1v0mbdj, .css-12w0qpk {
        height: 100vh !important;
        max-height: 90vh !important;
        overflow-y: hidden !important;
    }
    .css-1v0mbdj img, .css-12w0qpk img {
        max-height: 90vh;
        object-fit: contain;
    }
    </style>
    """,
    unsafe_allow_html=True
)
