from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'high_convert_edu_dynamic_2024'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Extensões permitidas para upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}

# Criar diretórios se não existirem
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def slugify(text):
    """Converter texto para slug URL-friendly"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def hex_to_rgb(hex_color):
    """Converter hex para RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_color_css(primary_color, accent_color, secondary_color):
    """Gerar CSS customizado com as cores escolhidas"""
    primary_rgb = hex_to_rgb(primary_color)
    accent_rgb = hex_to_rgb(accent_color)
    secondary_rgb = hex_to_rgb(secondary_color)
    
    css_template = f"""
    :root {{
        --color-primary: {primary_rgb[0]} {primary_rgb[1]} {primary_rgb[2]};
        --color-accent: {accent_rgb[0]} {accent_rgb[1]} {accent_rgb[2]};
        --color-secondary: {secondary_rgb[0]} {secondary_rgb[1]} {secondary_rgb[2]};
        
        --color-primary-hex: {primary_color};
        --color-accent-hex: {accent_color};
        --color-secondary-hex: {secondary_color};
    }}
    
    .bg-brand-primary {{ background-color: rgb(var(--color-primary)); }}
    .bg-brand-accent {{ background-color: rgb(var(--color-accent)); }}
    .bg-brand-secondary {{ background-color: rgb(var(--color-secondary)); }}
    
    .text-brand-primary {{ color: rgb(var(--color-primary)); }}
    .text-brand-accent {{ color: rgb(var(--color-accent)); }}
    .text-brand-secondary {{ color: rgb(var(--color-secondary)); }}
    
    .border-brand-primary {{ border-color: rgb(var(--color-primary)); }}
    .border-brand-accent {{ border-color: rgb(var(--color-accent)); }}
    .border-brand-secondary {{ border-color: rgb(var(--color-secondary)); }}
    
    .hover\\:bg-brand-accent:hover {{ background-color: rgb(var(--color-accent)); }}
    .hover\\:text-brand-accent:hover {{ color: rgb(var(--color-accent)); }}
    
    .cta-glow {{ 
        box-shadow: 0 0 25px rgba(var(--color-accent), 0.4);
        transition: all 0.3s ease;
    }}
    
    .cta-glow:hover {{ 
        box-shadow: 0 0 35px rgba(var(--color-accent), 0.6);
        transform: translateY(-2px) scale(1.05);
    }}
    
    .gradient-hero {{ 
        background: linear-gradient(135deg, 
            rgb(var(--color-primary)) 0%, 
            rgb(var(--color-secondary)) 100%);
    }}
    
    .gradient-animated {{
        background: linear-gradient(-45deg, 
            rgb(var(--color-primary)), 
            rgb(var(--color-accent)), 
            rgb(var(--color-secondary)), 
            rgb(var(--color-primary)));
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    """
    
    return css_template

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Processar dados do formulário
        dados = {
            # Cores customizáveis
            'primary_color': request.form.get('primary_color', '#3B82F6'),
            'accent_color': request.form.get('accent_color', '#06FFA5'),
            'secondary_color': request.form.get('secondary_color', '#8B5CF6'),
            
            # SEO e Analytics
            'meta_title': request.form.get('meta_title', ''),
            'meta_description': request.form.get('meta_description', ''),
            'google_analytics_id': request.form.get('google_analytics_id', ''),
            
            # Informações básicas
            'nome_escola': request.form.get('nome_escola', ''),
            'endereco': request.form.get('endereco', ''),
            'telefone': request.form.get('telefone', ''),
            'email': request.form.get('email', ''),
            'whatsapp': request.form.get('whatsapp', ''),
            
            # Hero Section
            'slogan_principal': request.form.get('slogan_principal', ''),
            'sub_slogan': request.form.get('sub_slogan', ''),
            'cta_principal': request.form.get('cta_principal', 'Matricule-se Agora'),
            
            # Listas dinâmicas
            'botoes_menu': [],
            'redes_sociais': [],
            'segmentos': [],
            'beneficios': [],
            'metricas_sucesso': [],
            
            # URLs de arquivos
            'logo_url': '',
            'banner_url': '',
            'video_institucional_url': request.form.get('video_institucional_url', ''),
            
            # CSS customizado
            'custom_css': '',
            
            # Timestamp
            'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S')
        }
        
        # Gerar CSS customizado com as cores
        dados['custom_css'] = generate_color_css(
            dados['primary_color'], 
            dados['accent_color'], 
            dados['secondary_color']
        )
        
        # Processar botões do menu
        for i in range(1, 6):  # Máximo 5 botões
            botao = request.form.get(f'botao_menu_{i}')
            if botao:
                dados['botoes_menu'].append({
                    'nome': botao,
                    'slug': slugify(botao)
                })
        
        # Processar segmentos da escola (NOVO FOCO)
        for i in range(1, 6):  # Máximo 5 segmentos
            nome = request.form.get(f'segmento_nome_{i}')
            descricao = request.form.get(f'segmento_descricao_{i}')
            cta_texto = request.form.get(f'segmento_cta_{i}')
            if nome and descricao:
                dados['segmentos'].append({
                    'nome': nome,
                    'descricao': descricao,
                    'cta_texto': cta_texto or f'Inscreva-se no {nome}',
                    'icone': get_segment_icon(i),
                    'slug': slugify(nome)
                })
        
        # Processar redes sociais
        redes = ['facebook', 'instagram', 'youtube', 'linkedin', 'tiktok']
        for rede in redes:
            link = request.form.get(f'rede_{rede}')
            if link:
                dados['redes_sociais'].append({
                    'nome': rede,
                    'link': link,
                    'icone': get_social_icon(rede)
                })
        
        # Processar benefícios/cards
        for i in range(1, 5):  # Máximo 4 benefícios
            titulo = request.form.get(f'beneficio_titulo_{i}')
            descricao = request.form.get(f'beneficio_descricao_{i}')
            if titulo and descricao:
                dados['beneficios'].append({
                    'titulo': titulo,
                    'descricao': descricao,
                    'icone': get_benefit_icon(i)
                })
        
        # Processar métricas de sucesso
        metricas = ['anos_mercado', 'alunos_formados', 'taxa_aprovacao', 'professores']
        for metrica in metricas:
            valor = request.form.get(f'metrica_{metrica}')
            if valor:
                dados['metricas_sucesso'].append({
                    'nome': metrica,
                    'valor': valor,
                    'label': get_metric_label(metrica),
                    'icone': get_metric_icon(metrica)
                })
        
        # Processar uploads de arquivos
        arquivos_processados = processar_uploads(request.files)
        dados.update(arquivos_processados)
        
        # Gerar página HTML
        return gerar_pagina_html(dados)
    
    return render_template('form.html')

def gerar_pagina_html(dados):
    """Gerar HTML da página com cores customizadas e retornar arquivo para download"""
    try:
        # Renderizar template com os dados
        html_gerado = render_template('page_template.html', **dados)
        
        # Nome do arquivo baseado no nome da escola
        nome_arquivo = f"{slugify(dados['nome_escola']) or 'escola'}_{dados['timestamp']}.html"
        caminho_arquivo = os.path.join(app.config['OUTPUT_FOLDER'], nome_arquivo)
        
        # Salvar arquivo HTML
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(html_gerado)
        
        # Retornar arquivo para download
        return send_file(
            caminho_arquivo, 
            as_attachment=True, 
            download_name=nome_arquivo,
            mimetype='text/html'
        )
        
    except Exception as e:
        print(f"Erro ao gerar página: {e}")
        flash('Erro ao gerar página. Tente novamente.', 'error')
        return redirect(url_for('formulario'))

def processar_uploads(files):
    """Processar arquivos enviados"""
    dados_arquivos = {
        'logo_url': 'https://via.placeholder.com/200x80/3B82F6/ffffff?text=LOGO',
        'banner_url': 'https://via.placeholder.com/1200x600/3B82F6/ffffff?text=BANNER+HERO'
    }
    
    campos_arquivo = {
        'logo': 'logo_url',
        'banner_principal': 'banner_url'
    }
    
    for campo, url_key in campos_arquivo.items():
        if campo in files:
            file = files[campo]
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                dados_arquivos[url_key] = f"/static/uploads/{filename}"
    
    return dados_arquivos

def get_segment_icon(index):
    """Retornar ícone para segmentos escolares"""
    icones = [
        'fas fa-baby',           # Educação Infantil
        'fas fa-child',          # Fundamental I
        'fas fa-user-graduate',  # Fundamental II
        'fas fa-graduation-cap', # Ensino Médio
        'fas fa-university'      # Pré-vestibular
    ]
    return icones[index - 1] if index <= len(icones) else 'fas fa-school'

def get_social_icon(rede):
    """Retornar ícone FontAwesome para rede social"""
    icones = {
        'facebook': 'fab fa-facebook-f',
        'instagram': 'fab fa-instagram',
        'youtube': 'fab fa-youtube',
        'linkedin': 'fab fa-linkedin-in',
        'tiktok': 'fab fa-tiktok',
        'twitter': 'fab fa-x-twitter'
    }
    return icones.get(rede, 'fas fa-link')

def get_benefit_icon(index):
    """Retornar ícone para benefícios"""
    icones = [
        'fas fa-star',
        'fas fa-trophy',
        'fas fa-heart',
        'fas fa-rocket'
    ]
    return icones[index - 1] if index <= len(icones) else 'fas fa-check'

def get_metric_label(metrica):
    """Retornar label para métricas"""
    labels = {
        'anos_mercado': 'Anos de Experiência',
        'alunos_formados': 'Alunos Formados',
        'taxa_aprovacao': 'Taxa de Aprovação',
        'professores': 'Professores Qualificados'
    }
    return labels.get(metrica, metrica.title())

def get_metric_icon(metrica):
    """Retornar ícone para métricas"""
    icones = {
        'anos_mercado': 'fas fa-calendar-alt',
        'alunos_formados': 'fas fa-user-graduate',
        'taxa_aprovacao': 'fas fa-chart-line',
        'professores': 'fas fa-chalkboard-teacher'
    }
    return icones.get(metrica, 'fas fa-star')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
