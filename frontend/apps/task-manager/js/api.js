const API_BASE_URL = "https://beyondmain.onrender.com";

async function taskRequest(path, options) {
    const response = await fetch(`${API_BASE_URL}/tasks-manager/tasks${path}`, options);
    if (!response.ok) {
        throw new Error(`Request failed (HTTP ${response.status}).`);
    }
    if (response.status === 204) {
        return null;
    }
    return response.json();
}

export function getTasks({ priority = null, status = null } = {}) {
    const queryParams = new URLSearchParams();

    if (priority !== null) {
        queryParams.append("priority", priority);
    }

    if (status !== null) {
        queryParams.append("status", status);
    }

    const queryString = queryParams.toString();
    console.log(`Query string: ${queryString}`);

    return taskRequest(queryString ? `?${queryString}` : "");
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

export function deleteTask(id) {
    return taskRequest(`/${encodeURIComponent(id)}`, {
        method: "DELETE",
    });
}
