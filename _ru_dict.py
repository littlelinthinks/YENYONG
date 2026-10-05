import json, os

HERE = "/tmp/yenmerge"
DICT = {}
# Merge machine translations cached from API (filled in background)
_segcache = os.path.join(HERE, "_ru_seg.json")
try:
    DICT.update(json.load(open(_segcache, encoding='utf-8')))
except Exception:
    pass

# ---- OVERRIDES: required terminology (rule 6) + boilerplate ----
OVERRIDES = {
    # Required product terminology
    "SPC Flooring": "SPC-половое покрытие",
    "SPC flooring": "SPC-половое покрытие",
    "WPC Wall Panel": "Настенная панель WPC",
    "WPC Wall Panels": "Настенные панели WPC",
    "PVC Wall Panel": "Настенная панель PVC",
    "PVC Wall Panels": "Настенные панели PVC",
    "Carbon Crystal Panel": "Панель Carbon Crystal",
    "Carbon Crystal": "Панель Carbon Crystal",
    "Carbon Crystal Panels": "Панели Carbon Crystal",
    "Acoustic Panel": "Акустическая панель",
    "Acoustic Panels": "Акустические панели",
    "Acoustic Wall Panel": "Акустическая настенная панель",
    "HPL Compact Laminate": "Компактный ламинат HPL",
    "Bamboo Crystal Panel": "Панель Bamboo Crystal",
    "Bamboo Crystal": "Панель Bamboo Crystal",
    "Aluminium Composite Panel": "Алюминиевая композитная панель",
    "Aluminium Composite Panel (ACP)": "Алюминиевая композитная панель (ACP)",
    "Aluminium Honeycomb Panel": "Алюминиевая сотовая панель",
    "Flexible Stone Veneer": "Гибкий камень",
    "Flexible Stone": "Гибкий камень",
    "Ceramic / Porcelain": "Керамика / фарфор",
    "Ceramic & Porcelain Tile": "Керамическая и фарфоровая плитка",
    "Ceramic & Porcelain Tiles": "Керамическая и фарфоровая плитка",
    "Ceramic & Porcelain Tile (per m²)": "Керамическая и фарфоровая плитка (за м²)",
    "Ceramic Tiles": "Керамическая плитка",
    "Ceramic Tile": "Керамическая плитка",
    # CTAs / buttons
    "Request Samples": "Заказать образцы",
    "Email Us": "Написать нам",
    "Get a Quote": "Запросить КП",
    "WhatsApp Us": "WhatsApp",
    "Chat on WhatsApp": "Написать в WhatsApp",
    "Ask on WhatsApp": "Спросить в WhatsApp",
    "Request samples & a quote": "Заказать образцы и запросить КП",
    "Browse Downloads →": "Смотреть загрузки →",
    "Open Colour Library →": "Открыть каталог цветов →",
    "View Certifications →": "Смотреть сертификаты →",
    "Read FAQ →": "Читать FAQ →",
    "Browse all 250+ colours in the": "Смотреть все 250+ цветов в",
    # Nav labels (rule 5)
    "Home": "Главная",
    "Products": "Продукция",
    "Downloads": "Загрузки",
    "Projects": "Проекты",
    "Insights": "Статьи",
    "Contact": "Контакты",
    "Resources": "Ресурсы",
    "Compare": "Сравнить",
    "Certifications": "Сертификаты",
    "Colour Library": "Каталог цветов",
    "FAQ": "Часто задаваемые вопросы",
    "FAQ.": "Часто задаваемые вопросы.",
    "Downloads.": "Загрузки.",
    # Footer / brand
    "Building for a Sustainable Future": "Строим будущее устойчивого развития",
    "Building for a sustainable future — responsible materials, efficient processes and transparent supply chains.": "Строим будущее устойчивого развития — ответственные материалы, эффективные процессы и прозрачные цепочки поставок.",
    "Foshan sourcing base · Singapore headquarters.": "Закупочная база в Фошане · Штаб-квартира в Сингапуре.",
    "Quality from China. Trust from Singapore.": "Качество из Китая. Доверие из Сингапура.",
    "SPC Flooring": "SPC-половое покрытие",
    "WhatsApp +86 189 2998 0066": "WhatsApp +86 189 2998 0066",
    "mellamocolin888@outlook.com": "mellamocolin888@outlook.com",
    "www.yenyong.com": "www.yenyong.com",
    # Product template headings
    "Product Overview": "Обзор изделия",
    "Key Features": "Ключевые особенности",
    "Technical Specifications": "Технические характеристики",
    "Technical Specification": "Техническая характеристика",
    "Product Gallery": "Галерея изделия",
    "Applications": "Области применения",
    "Application": "Применение",
    "Why Choose YENYONG.": "Почему выбирают YENYONG.",
    "Why Choose YENYONG": "Почему выбирают YENYONG",
    "Latest Articles": "Последние статьи",
    "Insights & Resources": "Статьи и ресурсы",
    "Insights & Blog": "Статьи и блог",
    # Stat labels
    "Indicative Price": "Ориентировочная цена",
    "Min. Order": "Мин. заказ",
    "Quote Response": "Ответ на КП",
    "Free Samples": "Бесплатные образцы",
    "Free Sample": "Бесплатный образец",
    # Common phrases
    "Technical guides, trend reports and project inspiration for specifiers and buyers.": "Технические руководства, обзоры трендов и вдохновение для проектировщиков и закупщиков.",
    "Technical guides, trend reports and project insights for architects, contractors and distributors.": "Технические руководства, обзоры трендов и аналитика для архитекторов, подрядчиков и дистрибьюторов.",
    "We ship free colour samples worldwide within 5 days.": "Мы бесплатно отправляем цветовые образцы по всему миру в течение 5 дней.",
    "Tell us your project size, finish and destination port — we respond within 24 hours.": "Сообщите нам размер проекта, отделку и порт назначения — ответим в течение 24 часов.",
    "Need samples for your project?": "Нужны образцы для вашего проекта?",
    "Catalogues, installation guides and test reports.": "Каталоги, руководства по монтажу и отчёты об испытаниях.",
    "CE, ISO 9001, SGS, REACH and fire-rating documents.": "Документы CE, ISO 9001, SGS, REACH и пожарные сертификаты.",
    "MOQ, lead times, samples, shipping and after-sales.": "Мин. объём заказа, сроки, образцы, доставка и послепродажное обслуживание.",
    "115+ wood grain and stone finishes, searchable by code.": "Более 115 декоров под дерево и камень, поиск по коду.",
    "Browse Downloads →": "Смотреть загрузки →",
    # Editorial / article meta labels
    "Acoustic · Article": "Акустика · Статья",
    "Bathroom · Article": "Ванная · Статья",
    "Construction · Article": "Строительство · Статья",
    "Healthcare · Article": "Здравоохранение · Статья",
    "Hospitality · Article": "Гостиничный бизнес · Статья",
    "Rental · Article": "Аренда · Статья",
    "Design · Article": "Дизайн · Статья",
    "Trends · Article": "Тренды · Статья",
    "Product Guide · Article": "Гид по продукту · Статья",
    "Acoustic · Design · YENYONG. Insights": "Акустика · Дизайн · Статьи YENYONG.",
    "Bathroom · Trends · YENYONG. Insights": "Ванная · Тренды · Статьи YENYONG.",
    "Construction · Efficiency · YENYONG. Insights": "Строительство · Эффективность · Статьи YENYONG.",
    "Company updates, industry insights and exhibition announcements from YENYONG.": "Новости компании, аналитика отрасли и анонсы выставок от YENYONG.",
}

DICT.update(OVERRIDES)
