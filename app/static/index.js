    google.charts.load('current', {'packages':['gantt']});
    //google.charts.setOnLoadCallback(drawChart);

        function toMilliseconds(minutes) {
        return minutes * 24 * 60 * 60 * 1000;
      }

      function drawChart(activities) {
        var otherData = new google.visualization.DataTable();
        otherData.addColumn("string", "Task ID");
        otherData.addColumn("string", "Task Name");
        otherData.addColumn("string", "Resource");
        otherData.addColumn("date", "Start");
        otherData.addColumn("date", "End");
        otherData.addColumn("number", "Duration");
        otherData.addColumn("number", "Percent Complete");
        otherData.addColumn("string", "Dependencies");

        for (const act in activities)
        {
            console.log(activities[act].activity_number);
            otherData.addRows([
            [
                activities[act].activity_number,
               activities[act].activity_number,
                activities[act].activity_number,
                null,
                null,
                toMilliseconds(activities[act].duration),
                100,
                activities[act].predecessors.join(),
            ]]);
        }

//        otherData.addRows([
//          [
//            "1",
//            "1",
//            "1",
//            null,
//            null,
//            toMilliseconds(5),
//            100,
//            null,
//          ]]);
//
//                  otherData.addRows([
//          [
//            "2",
//            "2",
//            "2",
//            null,
//            null,
//            toMilliseconds(5),
//            100,
//            '1',
//          ]]);


//        otherData.addRows([
//          [
//            "toTrain",
//            "Walk to train stop",
//            "walk",
//            null,
//            null,
//            toMilliseconds(5),
//            100,
//            null,
//          ],
//          [
//            "music",
//            "Listen to music",
//            "music",
//            null,
//            null,
//            toMilliseconds(70),
//            100,
//            null,
//          ],
//          [
//            "wait",
//            "Wait for train",
//            "wait",
//            null,
//            null,
//            toMilliseconds(10),
//            100,
//            "toTrain",
//          ],
//          [
//            "train",
//            "Train ride",
//            "train",
//            null,
//            null,
//            toMilliseconds(45),
//            75,
//            "wait",
//          ],
//          [
//            "toWork",
//            "Walk to work",
//            "walk",
//            null,
//            null,
//            toMilliseconds(10),
//            0,
//            "train",
//          ],
//          [
//            "work",
//            "Sit down at desk",
//            null,
//            null,
//            null,
//            toMilliseconds(2),
//            0,
//            "toWork",
//          ],
//        ]);

        var options = {
          height: 275,
          gantt: {
            defaultStartDate: new Date(2015, 3, 28),
          },
        };

        var chart = new google.visualization.Gantt(
          document.getElementById("chart_div")
        );

        chart.draw(otherData, options);
      }











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
            alert('Результат расчета: ' + JSON.stringify(result["cp"])); // Выводим результат в виде alert

            cp_info_el = document.getElementById('cp_info');
            cp_info_el.innerHTML = '';
            act = (result["cp"]);
            for (const prop in act) {
                console.log(act[prop])
                div_el = document.createElement("div");
                div_el.className = "item"
                theSpanContents = document.createTextNode("Критический путь: " + act[prop]);

                div_el.appendChild(theSpanContents);

                cp_info_el.appendChild(div_el);
                cp_info_el.appendChild(document.createElement("br"));
            }


            div_el = document.createElement("div");
            div_el.className = "item"
            theSpanContents = document.createTextNode("Длительность: " + result["time"]);
            div_el.appendChild(theSpanContents);
            cp_info_el.appendChild(div_el);
            cp_info_el.appendChild(document.createElement("br"));
            drawChart(activities);

        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при расчете критического пути.');
        }
    });
    drawChart()