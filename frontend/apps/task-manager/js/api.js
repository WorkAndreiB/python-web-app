// const API_BASE_URL = "https://beyondmain.onrender.com";
const API_BASE_URL = "http://localhost:8000";

async function taskRequest(path, options) {
    const response = await fetch(`${API_BASE_URL}/tasks-manager/tasks${path}`, options);
    if (!response.ok) {
        throw new Error(`Request failed (HTTP ${response.status}).`);
    }
    return response.json();
}

export function getTasks() {
    return taskRequest("");
}

export function createTask(task) {
    return taskRequest("", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(task),
    });
}

export function updateTask(id, task) {
    return taskRequest(`/${encodeURIComponent(id)}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(task),
    });
}