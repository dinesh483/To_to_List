const API = "http://localhost:8000";

// ── Helpers ──────────────────────────────────────────────────────────────────

function showStatus(msg, isError = false) {
  const el = document.getElementById("status-msg");
  el.textContent = msg;
  el.className = "status-msg" + (isError ? " error" : "");
  setTimeout(() => { el.textContent = ""; el.className = "status-msg"; }, 3000);
}

function getFormData() {
  const today = new Date().toISOString().split("T")[0];
  return {
    task_id: parseInt(document.getElementById("edit-id").value) || Date.now(),
    task_name: document.getElementById("task-name").value.trim(),
    task_description: document.getElementById("task-desc").value.trim(),
    is_completed: document.getElementById("is-completed").checked,
    priority: document.getElementById("priority").value,
    due_date: document.getElementById("due-date").value || today,
    created_at: today
  };
}

function clearForm() {
  document.getElementById("edit-id").value = "";
  document.getElementById("task-name").value = "";
  document.getElementById("task-desc").value = "";
  document.getElementById("is-completed").checked = false;
  document.getElementById("priority").value = "High";
  document.getElementById("due-date").value = "";
  document.getElementById("form-title").textContent = "Add New Task";
  document.getElementById("submit-btn").textContent = "Add Task";
  document.getElementById("cancel-btn").style.display = "none";
}

// ── Render ───────────────────────────────────────────────────────────────────

function renderTasks(tasks) {
  const container = document.getElementById("task-list");

  if (!tasks.length) {
    container.innerHTML = `<div class="empty">No tasks yet. Add one above!</div>`;
    return;
  }

  container.innerHTML = tasks.map(t => `
    <div class="task-card ${t.is_completed ? "done" : ""}">
      <div class="info">
        <h3>${escHtml(t.task_name)}</h3>
        <p>${escHtml(t.task_description)}</p>
        <div class="meta">
          <span class="badge badge-${t.priority}">${t.priority} priority</span>
          ${t.is_completed ? '<span class="badge badge-done">Completed</span>' : ""}
          <span class="badge badge-date">Due: ${t.due_date}</span>
        </div>
      </div>
      <div class="task-actions">
        <button class="btn-edit" onclick="startEdit(${t.task_id})">Edit</button>
        <button class="btn-del" onclick="deleteTask(${t.task_id})">Delete</button>
      </div>
    </div>
  `).join("");
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// ── API calls ────────────────────────────────────────────────────────────────

// GET /task — load all tasks
async function loadTasks() {
  try {
    const res = await fetch(`${API}/task`);
    const data = await res.json();
    renderTasks(data);
  } catch (err) {
    showStatus("Could not connect to backend. Is it running?", true);
  }
}

// POST /task — create a new task
async function createTask(task) {
  const res = await fetch(`${API}/task`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task)
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// PUT /task/{id} — update a task
async function updateTask(id, task) {
  const res = await fetch(`${API}/task/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task)
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// DELETE /task/{id} — delete a task
//
// NOTE: Your backend's delete route requires a request body (task: tasks).
// That's unusual for DELETE — most REST APIs don't send a body.
// We send a minimal placeholder body to satisfy your current backend.
// You may want to remove the `task` parameter from your delete route later.
async function deleteTask(id) {
  if (!confirm("Delete this task?")) return;
  try {
    const today = new Date().toISOString().split("T")[0];
    const res = await fetch(`${API}/task/${id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        task_id: id, task_name: "x", task_description: "x",
        is_completed: false, priority: "Low",
        due_date: today, created_at: today
      })
    });
    if (!res.ok) throw new Error(await res.text());
    showStatus("Task deleted.");
    loadTasks();
  } catch (err) {
    showStatus("Delete failed: " + err.message, true);
  }
}

// ── Form actions ──────────────────────────────────────────────────────────────

async function submitTask() {
  const task = getFormData();
  if (!task.task_name) { showStatus("Task name is required.", true); return; }

  const editId = document.getElementById("edit-id").value;

  try {
    if (editId) {
      await updateTask(parseInt(editId), task);
      showStatus("Task updated successfully.");
    } else {
      await createTask(task);
      showStatus("Task added successfully.");
    }
    clearForm();
    loadTasks();
  } catch (err) {
    showStatus("Error: " + err.message, true);
  }
}

// GET /task/{id} — pre-fill the form for editing
async function startEdit(id) {
  try {
    const res = await fetch(`${API}/task/${id}`);
    const t = await res.json();
    if (t.error) { showStatus(t.error, true); return; }

    document.getElementById("edit-id").value = t.task_id;
    document.getElementById("task-name").value = t.task_name;
    document.getElementById("task-desc").value = t.task_description;
    document.getElementById("is-completed").checked = t.is_completed;
    document.getElementById("priority").value = t.priority;
    document.getElementById("due-date").value = t.due_date;
    document.getElementById("form-title").textContent = "Edit Task";
    document.getElementById("submit-btn").textContent = "Update Task";
    document.getElementById("cancel-btn").style.display = "inline-block";
    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (err) {
    showStatus("Could not load task.", true);
  }
}

function cancelEdit() { clearForm(); loadTasks(); }

// ── Init ──────────────────────────────────────────────────────────────────────
loadTasks();