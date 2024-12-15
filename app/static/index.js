    document.getElementById('addRowButton').addEventListener('click', () => {
        const tableBody = document.getElementById('activityTable').getElementsByTagName('tbody')[0];
        const newRow = tableBody.insertRow();

        const cell1 = newRow.insertCell(0);
        const cell2 = newRow.insertCell(1);
        const cell3 = newRow.insertCell(2);

        cell1.innerHTML = '<input type="text" placeholder="Введите номер" required>';
        cell2.innerHTML = '<input type="number" placeholder="Введите длительность" required>';
        cell3.innerHTML = '<input type="text" placeholder="Введите предшественников">';
    });

    document.getElementById('calculateButton').addEventListener('click', async function() {
        const tableRows = document.querySelectorAll('#activityTable tbody tr');
        const activities = [];

        tableRows.forEach(row => {
            const activityNumber = row.cells[0].querySelector('input').value;
            const duration = row.cells[1].querySelector('input').value;
            const predecessors = row.cells[2].querySelector('input').value;

            if (activityNumber && duration) { // Проверяем, что номер и длительность заполнены
                activities.push({
                    activity_number: activityNumber,
                    duration: parseFloat(duration),
                    predecessors: predecessors.split(',').map(item => item.trim()) // Разделяем предшественников по запятой
                });
            }
        });

        try {
            const response = await fetch('http://localhost:5001/calculate_critical_path', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(activities),
            });

            const result = await response.json();
            console.log(result); // Здесь вы можете обработать результат
            alert('Результат расчета: ' + JSON.stringify(result)); // Выводим результат в виде alert
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при расчете критического пути.');
        }
    });