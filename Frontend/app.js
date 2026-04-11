const API = "http://127.0.0.1:8000/task";

// GET all tasks
async function getTasks() {
  const res = await fetch(API);
  const data = await res.json();

  let html = "";

  data.forEach(task => {
    html += `
      <div class="task">
        <h3>${task.task_name}</h3>
        <p>${task.task_description}</p>
        <button onclick="deleteTask(${task.task_id})">Delete</button>
      </div>
    `;
  });

  document.getElementById("task_list").innerHTML = html;
}

// ADD task
async function addTask() {
  const name = document.getElementById("task_name").value;
  const desc = document.getElementById("task_desc").value;

  await fetch(API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      task_id: Math.floor(Math.random() * 10000),
      task_name: name,
      task_description: desc,
      is_completed: false,
      created_at: "2026-04-11",
      priority: "High",
      due_date: "2026-04-11"
    })
  });

  getTasks();
}

// DELETE task
async function deleteTask(id) {
  await fetch(`${API}/${id}`, {
    method: "DELETE"
  });

  getTasks();
}

// load tasks when page opens
getTasks();