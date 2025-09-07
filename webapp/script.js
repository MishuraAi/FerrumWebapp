document.addEventListener('DOMContentLoaded', function () {
    const tg = window.Telegram.WebApp;
    tg.expand(); // Расширяем приложение на весь экран

    const mainButton = tg.MainButton;
    mainButton.setText('Отправить отчет');
    mainButton.enable();
    mainButton.show();

    // --- Логика добавления/удаления материалов ---
    const addMaterialBtn = document.getElementById('add-material-btn');
    const materialsContainer = document.getElementById('materials-container');
    let materialId = 0;

    addMaterialBtn.addEventListener('click', function () {
        materialId++;
        const newItem = document.createElement('div');
        newItem.classList.add('material-item');
        newItem.id = `material-${materialId}`;
        newItem.innerHTML = `
            <input type="text" class="material-name" placeholder="Наименование материала">
            <input type="number" class="material-length" placeholder="Длина (мм)">
            <button type="button" class="remove-material-btn">&times;</button>
        `;
        materialsContainer.appendChild(newItem);
    });

    materialsContainer.addEventListener('click', function (e) {
        if (e.target && e.target.classList.contains('remove-material-btn')) {
            e.target.closest('.material-item').remove();
        }
    });

    // --- Отправка данных боту ---
    mainButton.onClick(function () {
        const department = document.getElementById('department').value;
        const process = document.getElementById('process').value;
        const description = document.getElementById('description').value;
        const problems = document.getElementById('problems').value;
        
        const materials = [];
        document.querySelectorAll('.material-item').forEach(item => {
            const name = item.querySelector('.material-name').value;
            const length = item.querySelector('.material-length').value;
            if (name && length) { // Собираем только если оба поля заполнены
                materials.push({ name, length });
            }
        });

        // Проверка, что хотя бы одно основное поле заполнено
        if (!department && !process && !description) {
            tg.showAlert('Пожалуйста, заполните хотя бы одно из полей: Цех, Процесс или Описание работы.');
            return;
        }

        const data = {
            department,
            process,
            description,
            problems,
            materials,
        };

        // Отправляем данные в виде JSON-строки
        tg.sendData(JSON.stringify(data));
        // После отправки можно закрыть Web App
        tg.close();
    });
});