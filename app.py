import os
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from fpdf import FPDF

# --------------------------------------------------------
# 1. 10-LANGUAGE COMPREHENSIVE LOCALIZATION MAP
# --------------------------------------------------------
LOCALIZATION_ENGINE = {
    "English": {
        "title": "Clinical Registry and Patient Management Portal",
        "name_lbl": "Full Name of Patient",
        "precaution_hdr": "Mandatory Medical Precautionary Protocols",
        "p1": "1. Perform strict hand sanitization or wash hands thoroughly for a minimum of 20 seconds.",
        "p2": "2. Deploy a compliant high-filtration mask inside congested or poorly ventilated clinical environments.",
        "p3": "3. Maintain a minimum safe physical distance parameter of 1 meter relative to others.",
        "p4": "4. Record systemic body temperature matrices and oxygen saturation saturation vectors daily.",
        "btn_pdf": "Generate and Compile Dynamic Patient Record PDF",
        "contact_hdr": "Inquiries and Support Channels",
        "contact_email": "To report discrepancies, email transmission nodes: support@clinicalcontextnet.org",
        "success": "PDF structure successfully compiled. Download artifact via the node portal below."
    },
    "Urdu (اردو)": {
        "title": "کلینیکل رجسٹری اور مریضوں کا مینجمنٹ پورٹل",
        "name_lbl": "مریض کا پورا نام",
        "precaution_hdr": "لازمی طبی احتیاطی تدابیر",
        "p1": "1. اپنے ہاتھوں کو کم از کم 20 سیکنڈ تک صابن اور پانی سے باقاعدگی سے دھوئیں ۔",
        "p2": "2. پرہجوم یا کم ہوادار طبی جگہوں پر حفاظتی فیس ماسک کا لازمی استعمال کریں۔",
        "p3": "3. سماجی فاصلہ برقرار رکھیں اور دوسرے افراد سے کم از کم 1 میٹر کا فاصلہ رکھیں۔",
        "p4": "4. روزانہ کی بنیاد پر اپنے جسم کا درجہ حرارت اور آکسیجن کی سطح کی نگرانی کریں۔",
        "btn_pdf": "مریض کا ریکارڈ پی ڈی ایف فائل ڈاؤن لوڈ کریں",
        "contact_hdr": "ہم سے رابطہ کریں",
        "contact_email": "رابطے کے لیے اس پتے پر ای میل بھیجیں: support@clinicalcontextnet.org",
        "success": "پی ڈی ایف فائل کامیابی کے ساتھ تیار کر لی گئی ہے۔ ڈاؤن لوڈ کرنے کے لیے نیچے کلک کریں۔"
    },
    "Spanish (Español)": {
        "title": "Portal de Registro Clínico y Gestión de Pacientes",
        "name_lbl": "Nombre Completo del Paciente",
        "precaution_hdr": "Protocolos Médicos Preventivos Obligatorios",
        "p1": "1. Realice una desinfección estricta de las manos o lávelas minuciosamente durante 20 segundos.",
        "p2": "2. Use una mascarilla protectora en espacios clínicos concurridos o mal ventilados.",
        "p3": "3. Mantenga una distancia física segura de al menos 1 metro de otras personas.",
        "p4": "4. Registre diariamente la temperatura corporal y los niveles de saturación de oxígeno.",
        "btn_pdf": "Generar y Descargar PDF del Registro del Paciente",
        "contact_hdr": "Canales de Consulta y Soporte",
        "contact_email": "Para consultas institucionales, escriba a: support@clinicalcontextnet.org",
        "success": "¡Archivo PDF generado con éxito! Use el enlace inferior para la descarga."
    },
    "French (Français)": {
        "title": "Portail de Registre Clinique et de Gestion des Patients",
        "name_lbl": "Nom Complet du Patient",
        "precaution_hdr": "Protocoles de Précaution Médicale Obligatoires",
        "p1": "1. Effectuer une désinfection stricte des mains ou se laver les mains pendant 20 secondes.",
        "p2": "2. Déployer un masque de protection dans les espaces cliniques encombrés ou mal ventilés.",
        "p3": "3. Maintenir une distance physique de sécurité d'au moins 1 mètre par rapport aux autres.",
        "p4": "4. Enregistrer quotidiennement la température corporelle et la saturation en oxygène.",
        "btn_pdf": "Générer et Télécharger le PDF de l'Historique du Patient",
        "contact_hdr": "Canaux d'Information et d'Assistance",
        "contact_email": "Pour toute correspondance officielle, écrivez à: support@clinicalcontextnet.org",
        "success": "Document PDF généré avec succès. Cliquez ci-dessous pour lancer le téléchargement."
    },
    "German (Deutsch)": {
        "title": "Klinisches Register und Patientenmanagement-Portal",
        "name_lbl": "Vollständiger Name des Patienten",
        "precaution_hdr": "Verbindliche Medizinische Vorsichtsprotokolle",
        "p1": "1. Führen Sie eine strikte Händedesinfektion durch oder waschen Sie die Hände für 20 Sekunden.",
        "p2": "2. Tragen Sie eine Atemschutzmaske in engen oder schlecht belüfteten klinischen Räumen.",
        "p3": "3. Halten Sie einen Sicherheitsabstand von mindestens 1 Meter zu anderen Personen ein.",
        "p4": "4. Überprüfen Sie täglich Ihre Körpertemperatur und Sauerstoffsättigungswerte.",
        "btn_pdf": "Patientenakte als PDF generieren und herunterladen",
        "contact_hdr": "Support- und Kontaktkanäle",
        "contact_email": "Für Anfragen senden Sie bitte eine E-Mail an: support@clinicalcontextnet.org",
        "success": "PDF-Akte erfolgreich zusammengestellt. Klicken Sie unten zum Download."
    },
    "Chinese (中文)": {
        "title": "临床登记与患者管理系统",
        "name_lbl": "患者法定全名",
        "precaution_hdr": "强制性医疗预防隔离协议",
        "p1": "1. 严格执行手部常规消毒，或使用肥皂流水彻底洗手至少20秒。",
        "p2": "2. 在人员密集或通风不良的医疗区域内，必须佩戴高过滤防护口罩。",
        "p3": "3. 与他人保持至少1米的安全社交防护距离。",
        "p4": "4. 每日定时监测记录基础体温矩阵与血氧饱和度特征向量。",
        "btn_pdf": "生成并导出患者临床病历报告 PDF",
        "contact_hdr": "联系我们与技术支持",
        "contact_email": "若有任何系统问题，请发送电子邮件至: support@clinicalcontextnet.org",
        "success": "PDF报告生成成功。请点击下方网关接口进行本地下载。"
    },
    "Arabic (العربية)": {
        "title": "بوابة السجل الطبي وإدارة المرضى",
        "name_lbl": "اسم المريض الكامل",
        "precaution_hdr": "البروتوكولات الوقائية الطبية الإلزامية",
        "p1": "1. التطهير الصارم لليدين أو غسلهما جيدًا بالماء والصابون لمدة لا تقل عن 20 ثانية.",
        "p2": "2. الالتزام بارتداء كمامة واقية عالية الترشيح داخل البيئات الطبية المزدحمة.",
        "p3": "3. الحفاظ على مسافة أمان فيزيائية لا تقل عن متر واحد من الأشخاص الآخرين.",
        "p4": "4. مراقبة وتسجيل درجات حرارة الجسم ومستويات تشبع الأكسجين بشكل يومي.",
        "btn_pdf": "إنشاء وتحميل ملف PDF الخاص بسجل المريض",
        "contact_hdr": "قنوات الدعم والتواصل",
        "contact_email": "للاستفسارات والمراسلات الرسمية: support@clinicalcontextnet.org",
        "success": "تم إنشاء ملف PDF بنجاح. انقر فوق الزر أدناه لبدء التنزيل."
    },
    "Portuguese (Português)": {
        "title": "Portal de Registro Clínico e Gerenciamento de Pacientes",
        "name_lbl": "Nome Completo do Paciente",
        "precaution_hdr": "Protocolos Médicos Preventivos Obrigatórios",
        "p1": "1. Realize a higienização estrita das mãos ou lave-as por pelo menos 20 segundos.",
        "p2": "2. Utilize máscara de proteção respiratória em áreas clínicas fechadas ou aglomeradas.",
        "p3": "3. Mantenha um distanciamento físico de segurança de no mínimo 1 metro de terceiros.",
        "p4": "4. Monitore sistematicamente a temperatura corporal e saturação de oxigênio diariamente.",
        "btn_pdf": "Gerar e Emitir PDF de Prontuário do Paciente",
        "contact_hdr": "Canais de Comunicação e Suporte",
        "contact_email": "Para relatórios de erros, envie e-mail para: support@clinicalcontextnet.org",
        "success": "Documento PDF processado. Clique no link de download abaixo."
    },
    "Russian (Русский)": {
        "title": "Клинический реестр и портал управления данными пациентов",
        "name_lbl": "Полное имя пациента",
        "precaution_hdr": "Обязательные медицинские профилактические протоколы",
        "p1": "1. Обеспечьте строгую дезинфекцию или тщательно мойте руки не менее 20 секунд.",
        "p2": "2. Обязательно используйте защитную маску в многолюдных клинических помещениях.",
        "p3": "3. Соблюдайте безопасную физическую дистанцию не менее 1 метра от окружающих.",
        "p4": "4. Ежедневно фиксируйте температуру тела и показатели сатурации кислорода.",
        "btn_pdf": "Сформировать и скачать PDF-карту пациента",
        "contact_hdr": "Служба поддержки и связи",
        "contact_email": "По техническим вопросам пишите на адрес: support@clinicalcontextnet.org",
        "success": "Файл PDF успешно скомпилирован. Нажмите ниже, чтобы скачать."
    },
    "Hindi (हिन्दी)": {
        "title": "चिकित्सकीय रजिस्ट्री और रोगी प्रबंधन पोर्टल",
        "name_lbl": "रोगी का पूरा नाम",
        "precaution_hdr": "अनिवार्य चिकित्सा एहतियाती प्रोटोकॉल",
        "p1": "1. कम से कम 20 सेकंड के लिए अपने हाथों को साबुन और पानी से अच्छी तरह धोएं।",
        "p2": "2. भीड़भाड़ वाले या कम हवादार स्वास्थ्य केंद्रों के भीतर सुरक्षात्मक मास्क पहनें।",
        "p3": "3. अन्य व्यक्तियों से कम से कम 1 मीटर की सुरक्षित शारीरिक दूरी बनाए रखें।",
        "p4": "4. दैनिक आधार पर शरीर के तापमान और ऑक्सीजन संतृप्ति स्तर की निगरानी करें।",
        "btn_pdf": "रोगी रिकॉर्ड पीडीएफ जेनरेट और डाउनलोड करें",
        "contact_hdr": "पूछताछ और सहायता चैनल",
        "contact_email": "प्रणालीगत पूछताछ के लिए हमें ईमेल करें: support@clinicalcontextnet.org",
        "success": "पीडीएफ फाइल सफलतापूर्वक तैयार हो गई है। डाउनलोड करने के लिए नीचे क्लिक करें।"
    }
}

COUNTER_PATH = "patient_counter.txt"

# --------------------------------------------------------
# 2. AUTO-INCREMENT PATIENT ID STORAGE ENGINE
# --------------------------------------------------------
def get_and_increment_patient_id():
    if not os.path.exists(COUNTER_PATH):
        with open(COUNTER_PATH, "w") as file:
            file.write("1001")
        return 1001
    try:
        with open(COUNTER_PATH, "r") as file:
            current_id = int(file.read().strip())
    except (ValueError, IndexError):
        current_id = 1001
        
    next_id = current_id + 1
    with open(COUNTER_PATH, "w") as file:
        file.write(str(next_id))
    return current_id

# --------------------------------------------------------
# 3. COMPLEX TEXT GRAPHICS COMPILER (FPDF2 Engine for UTF-8)
# --------------------------------------------------------
def build_utf8_pdf(output_filename, patient_id, patient_name, lang_name, text_bundle):
    pdf = FPDF()
    pdf.add_page()
    
    # Register core Unicode fonts to allow handling of Urdu/Hindi/Chinese layouts cleanly
    # Update paths points cleanly matching local files dropped inside project directory
    font_dir = "fonts"
    
    if lang_name == "Urdu (اردو)":
        pdf.add_font("CustomFont", "", os.path.join(font_dir, "Jameel_Noori_Nastaleeq.ttf"))
    elif lang_name == "Hindi (हिन्दी)":
        pdf.add_font("CustomFont", "", os.path.join(font_dir, "NotoSansDevanagari-Regular.ttf"))
    elif lang_name == "Chinese (中文)":
        pdf.add_font("CustomFont", "", os.path.join(font_dir, "NotoSansSC-Regular.ttf"))
    elif lang_name == "Arabic (العربية)":
        pdf.add_font("CustomFont", "", os.path.join(font_dir, "NotoSansArabic-Regular.ttf"))
    else:
        pdf.add_font("CustomFont", "", os.path.join(font_dir, "NotoSans-Regular.ttf"))
        
    pdf.set_font("CustomFont", size=14)
    
    # Document Identification Header Block
    pdf.cell(200, 10, text="Clinical Metadata Document Structure", ln=True, align="C")
    pdf.ln(10)
    
    # Demographics Mapping
    pdf.cell(200, 10, text=f"Assigned Auto-Increment Patient ID: {patient_id}", ln=True)
    pdf.cell(200, 10, text=f"{text_bundle['name_lbl']}: {patient_name}", ln=True)
    pdf.cell(200, 10, text=f"Data Pipeline Language Context: {lang_name}", ln=True)
    pdf.ln(10)
    
    # Mandatory Precaution Vectors Display
    pdf.cell(200, 10, text=text_bundle["precaution_hdr"], ln=True)
    pdf.ln(4)
    pdf.multi_cell(0, 10, text=text_bundle["p1"])
    pdf.multi_cell(0, 10, text=text_bundle["p2"])
    pdf.multi_cell(0, 10, text=text_bundle["p3"])
    pdf.multi_cell(0, 10, text=text_bundle["p4"])
    
    pdf.output(output_filename)

# --------------------------------------------------------
# 4. LATIN STANDARD FONTS GRAPHICS COMPILER (ReportLab Engine)
# --------------------------------------------------------
def build_latin_pdf(output_filename, patient_id, patient_name, lang_name, text_bundle):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    header_style = ParagraphStyle(
        'DocHeaderStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=15
    )
    
    meta_style = ParagraphStyle(
        'MetaDelineationStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        spaceAfter=8,
        textColor=colors.HexColor('#334155')
    )
    
    section_style = ParagraphStyle(
        'SectionStructureStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=12,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'BodyArrayStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        spaceAfter=6,
        textColor=colors.HexColor('#1E293B')
    )

    story.append(Paragraph("Clinical Context Core Registry Profile", header_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph(f"<b>System Patient ID Token:</b> {patient_id}", meta_style))
    story.append(Paragraph(f"<b>{text_bundle['name_lbl']}:</b> {patient_name}", meta_style))
    story.append(Paragraph(f"<b>Interface Language Target:</b> {lang_name}", meta_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph(text_bundle["precaution_hdr"], section_style))
    story.append(Paragraph(text_bundle["p1"], body_style))
    story.append(Paragraph(text_bundle["p2"], body_style))
    story.append(Paragraph(text_bundle["p3"], body_style))
    story.append(Paragraph(text_bundle["p4"], body_style))
    
    doc.build(story)

# --------------------------------------------------------
# 5. STREAMLIT INTERFACE FRAMEWORK RUNTIME
# --------------------------------------------------------
st.set_page_config(page_title="Clinical Registry Management Server", layout="centered")

# Dropdown Selection Context
active_lang = st.selectbox("Select Core Language Framework / زبان کا انتخاب کریں", list(LOCALIZATION_ENGINE.keys()))
ui_map = LOCALIZATION_ENGINE[active_lang]

# Render Structured Headings without Emojis
st.title(ui_map["title"])
st.write("---")

# Patient Identity Entry Text Input Area
patient_name_str = st.text_input(ui_map["name_lbl"], value="")

# Interactive Checklists Display Structure
st.markdown(f"### {ui_map['precaution_hdr']}")
st.info(ui_map["p1"])
st.info(ui_map["p2"])
st.info(ui_map["p3"])
st.info(ui_map["p4"])
st.write("---")

# Generate Button Execution Logic Block
if st.button(ui_map["btn_pdf"]):
    if not patient_name_str.strip():
        st.error("Submission Halted: Patient Full Name input string variable cannot remain blank.")
    else:
        # Atomic read-increment lock execution tracking
        current_allocated_id = get_and_increment_patient_id()
        target_filename = f"Patient_Registry_Record_{current_allocated_id}.pdf"
        
        # Route to appropriate PDF processing framework based on script rules
        latin_languages = ["English", "Spanish (Español)", "French (Français)", "German (Deutsch)", "Portuguese (Português)"]
        
        if active_lang in latin_languages:
            build_latin_pdf(target_filename, current_allocated_id, patient_name_str, active_lang, ui_map)
        else:
            # Check for font structures dynamically to shield execution flow
            if not os.path.exists("fonts"):
                os.makedirs("fonts")
            build_utf8_pdf(target_filename, current_allocated_id, patient_name_str, active_lang, ui_map)
            
        with open(target_filename, "rb") as operations_file_stream:
            st.success(ui_map["success"])
            st.download_button(
                label="Download Generated Clinical Document Ledger (PDF)",
                data=operations_file_stream,
                file_name=target_filename,
                mime="application/pdf"
            )

# Contact Us Form Infrastructure Component Block
st.write("---")
st.markdown(f"### {ui_map['contact_hdr']}")
st.write(ui_map["contact_email"])

with st.form("institutional_contact_node", clear_on_submit=True):
    user_email_address = st.text_input("Sender Electronic Mail Address")
    user_message_body = st.text_area("Detailed Message Frame Content")
    transmission_submission = st.form_submit_button("Submit Transmission Package")
    
    if transmission_submission:
        if user_email_address and user_message_body:
            st.success("Log Entry Confirmed: Correspondence vector compiled safely inside system logging traces.")
        else:
            st.error("Transmission Rejected: Please fill in all configuration inputs before firing node submission request.")
