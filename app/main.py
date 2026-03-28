from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.controllers.part_controller import router as parts_router

# Создаём приложение
app = FastAPI(
    title="Auto Parts API",
    description="API для управления запчастями",
    version="2.0.0"
)

# Подключаем роутеры
app.include_router(parts_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Auto Parts API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Кастомная Swagger UI страница с автозаполнением данных
@app.get("/docs", response_class=HTMLResponse)
async def custom_docs():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html>
<head>
    <title>Auto Parts API - Swagger UI</title>
    <meta charset="utf-8"/>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png"/>
    <style>
        .auto-fill-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
            font-size: 12px;
            display: inline-block;
        }
        .auto-fill-btn:hover { background: #45a049; }
        .auto-fill-info {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 13px;
            border-left: 4px solid #2196F3;
        }
        .auto-fill-error {
            background: #ffebee;
            border-left-color: #f44336;
        }
        .part-preview {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            font-family: monospace;
            font-size: 12px;
            white-space: pre-wrap;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
    <script>
        const ui = SwaggerUIBundle({
            url: '/openapi.json',
            dom_id: '#swagger-ui',
            layout: 'BaseLayout',
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true,
            tryItOutEnabled: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
            onComplete: function() {
                console.log('Swagger UI loaded, setting up auto-fill...');
                
                // Функция загрузки данных запчасти и автозаполнения
                async function loadAndFillPartData(partId, section, method) {
                    if (!partId || partId === '') {
                        showPreview(section, '⚠️ Введите part_id', true);
                        return;
                    }
                    
                    try {
                        const response = await fetch('/api/v1/parts/' + partId);
                        
                        if (!response.ok) {
                            showPreview(section, '❌ Запчасть не найдена (ID: ' + partId + ')', true);
                            return;
                        }
                        
                        const data = await response.json();
                        
                        // Показываем превью данных
                        const previewText = '📦 Запчасть найдена:\\n' + 
                                          'ID: ' + data.id + '\\n' +
                                          'Название: ' + data.name + '\\n' +
                                          'Артикул: ' + data.part_number + '\\n' +
                                          'Цена: ' + data.price + ' руб.\\n' +
                                          'Описание: ' + (data.description || '—');
                        showPreview(section, previewText, false);
                        
                        // Автозаполняем textarea для PUT и PATCH
                        if (method !== 'DELETE') {
                            const textarea = section.querySelector('textarea[aria-label="Request body"]');
                            if (textarea) {
                                // Для PUT заполняем все поля, для PATCH только изменяемые
                                const bodyData = method === 'PUT' ? {
                                    name: data.name,
                                    part_number: data.part_number,
                                    price: data.price,
                                    description: data.description || ""
                                } : {
                                    price: data.price
                                };
                                
                                // Форматируем и вставляем
                                textarea.value = JSON.stringify(bodyData, null, 2);
                                
                                // Подсвечиваем успешное заполнение
                                textarea.style.border = '2px solid #4CAF50';
                                setTimeout(() => textarea.style.border = '', 2000);
                            }
                        } else {
                            // Для DELETE просто показываем данные
                            showPreview(section, '⚠️ Вы собираетесь удалить запчасть:\\n' + 
                                       JSON.stringify(data, null, 2), false);
                        }
                        
                    } catch (err) {
                        showPreview(section, '❌ Ошибка: ' + err.message, true);
                    }
                }
                
                // Показ превью данных
                function showPreview(section, text, isError) {
                    // Удаляем старое превью
                    const oldPreview = section.querySelector('.part-preview-container');
                    if (oldPreview) oldPreview.remove();
                    
                    const container = document.createElement('div');
                    container.className = 'part-preview-container';
                    
                    const infoDiv = document.createElement('div');
                    infoDiv.className = 'auto-fill-info ' + (isError ? 'auto-fill-error' : '');
                    infoDiv.style.whiteSpace = 'pre-wrap';
                    infoDiv.textContent = text;
                    
                    container.appendChild(infoDiv);
                    
                    // Вставляем после Parameters секции
                    const paramsSection = section.querySelector('.parameters-col_description');
                    if (paramsSection) {
                        paramsSection.appendChild(container);
                    }
                }
                
                // Добавляем обработчики на поля part_id
                function setupPartIdListeners() {
                    const methods = ['put', 'patch', 'delete'];
                    
                    methods.forEach(method => {
                        const sections = document.querySelectorAll('.opblock-' + method);
                        
                        sections.forEach(section => {
                            const partIdInput = section.querySelector('input[data-param="part_id"]');
                            
                            if (!partIdInput) return;
                            
                            // Убираем старые слушатели (клонированием)
                            const newInput = partIdInput.cloneNode(true);
                            partIdInput.parentNode.replaceChild(newInput, partIdInput);
                            
                            // Добавляем обработчик на потерю фокуса
                            newInput.addEventListener('blur', function() {
                                const partId = this.value;
                                loadAndFillPartData(partId, section, method.toUpperCase());
                            });
                            
                            // Добавляем обработчик на ввод (с задержкой)
                            let timeoutId;
                            newInput.addEventListener('input', function() {
                                clearTimeout(timeoutId);
                                const partId = this.value;
                                timeoutId = setTimeout(() => {
                                    loadAndFillPartData(partId, section, method.toUpperCase());
                                }, 800); // Ждём 800мс после последнего ввода
                            });
                        });
                    });
                }
                
                // Запускаем настройку
                setupPartIdListeners();
                
                // Пересоздаём обработчики при открытии/закрытии методов
                const observer = new MutationObserver(setupPartIdListeners);
                observer.observe(document.getElementById('swagger-ui'), { 
                    childList: true, 
                    subtree: true 
                });
                
                console.log('Auto-fill setup complete!');
            }
        });
    </script>
</body>
</html>
""")
