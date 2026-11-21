import { createTask, deleteTask, getTasks, updateTask } from "./api.js";

const form = document.getElementById("task-form");
const title = document.getElementById("title");
const description = document.getElementById("description");
const status = document.getElementById("status");
const priority = document.getElementById("priority");
const formTitle = document.getElementById("form-title");
const saveButton = document.getElementById("save-button");
const cancelButton = document.getElementById("cancel-button");
const refreshButton = document.getElementById("refresh-button");
const statusFilter = document.getElementById("filter-status");
const priorityFilter = document.getElementById("filter-priority");
const formMessage = document.getElementById("form-message");
const listMessage = document.getElementById("list-message");
const taskList = document.getElementById("task-list");

const priorities = ["URGENT", "HIGH", "MEDIUM", "LOW"];
const statusLabels = { TODO: "To do", IN_PROGRESS: "In progress", DONE: "Done" };
let editingId = null;
let busy = false;

function setBusy(value) {
    busy = value;
    form.querySelectorAll("input, textarea, select").forEach((field) => { field.disabled = value; });
    saveButton.disabled = value;
    cancelButton.disabled = value;
    refreshButton.disabled = value;
    statusFilter.disabled = value;
    priorityFilter.disabled = value;
    taskList.querySelectorAll("button").forEach((button) => { button.disabled = value; });
}

// Reset the form to its initial state
function resetForm() {
    form.reset();
    editingId = null;
    formTitle.textContent = "New task";
    saveButton.textContent = "Add task";
    cancelButton.hidden = true;
}

// Render the list of tasks in the UI
function renderTasks(tasks) {
    taskList.replaceChildren();
    for (const task of tasks) {
        const item = document.createElement("li");
        item.className = "task-item";
        const heading = document.createElement("h3");
        heading.textContent = task.title;
        const detail = document.createElement("p");
        detail.className = "task-description";
        detail.textContent = task.description;
        const meta = document.createElement("div");
        meta.className = "task-meta";
        const statusBadge = document.createElement("span");
        statusBadge.className = "badge";
        statusBadge.textContent = statusLabels[task.status] ?? task.status;
        const priorityBadge = document.createElement("span");
        priorityBadge.className = "badge priority";
        const priorityValue = typeof task.priority === "number" ? priorities[task.priority] : task.priority;
        priorityBadge.textContent = priorityValue ? `${priorityValue.toLowerCase()} priority` : "Unknown priority";
        meta.append(statusBadge, priorityBadge);
        const editButton = document.createElement("button");
        editButton.type = "button";
        editButton.className = "edit-button";
        editButton.textContent = "Edit";
        editButton.setAttribute("aria-label", `Edit ${task.title}`);
        editButton.disabled = busy;
        editButton.addEventListener("click", () => {
            editingId = task.id;
            title.value = task.title;
            description.value = task.description;
            status.value = task.status;
            priority.value = priorityValue;
            formTitle.textContent = "Edit task";
            saveButton.textContent = "Save changes";
            cancelButton.hidden = false;
            formMessage.textContent = "";
            title.focus();
        });
        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.className = "delete-button";
        deleteButton.textContent = "Delete";
        deleteButton.setAttribute("aria-label", `Delete ${task.title}`);
        deleteButton.disabled = busy;
        deleteButton.addEventListener("click", async () => {
            if (busy || !window.confirm(`Delete "${task.title}"?`)) return;

            setBusy(true);
            listMessage.textContent = "Deleting task...";
            try {
                await deleteTask(task.id);
                if (editingId === task.id) {
                    resetForm();
                }
                formMessage.textContent = "";
                await loadTasks();
            } catch (error) {
                listMessage.textContent = "Could not delete task. Please try again.";
                console.error("Failed to delete task.", error);
            } finally {
                setBusy(false);
            }
        });
        const actions = document.createElement("div");
        actions.className = "task-actions";
        actions.append(editButton, deleteButton);
        item.append(heading, detail, meta, actions);
        taskList.append(item);
    }
    if (!tasks.length && (statusFilter.value !== "ALL" || priorityFilter.value !== "ALL")) {
        listMessage.textContent = "No tasks match these filters.";
    } else if (!tasks.length) {
        listMessage.textContent = "No tasks yet. Add one to get started.";
    } else {
        listMessage.textContent = `${tasks.length} ${tasks.length === 1 ? "task" : "tasks"}`;
    }
}

// call loadTasks to initially populate the task list
async function loadTasks() {
    listMessage.textContent = "Loading tasks...";
    try {
        const tasks = await getTasks({
            status: statusFilter.value === "ALL" ? null : statusFilter.value,
            priority: priorityFilter.value === "ALL" ? null : priorityFilter.value,
        });
        renderTasks(tasks);
    } catch (error) {
        listMessage.textContent = "Could not load tasks. Please try refreshing.";
        console.error("Failed to load tasks.", error);
    }
}

async function reloadTasks() {
    setBusy(true);
    try {
        await loadTasks();
    } finally {
        setBusy(false);
    }
}

refreshButton.addEventListener("click", reloadTasks);

statusFilter.addEventListener("change", reloadTasks);
priorityFilter.addEventListener("change", reloadTasks);

cancelButton.addEventListener("click", () => {
    resetForm();
    formMessage.textContent = "";
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (busy) return;

    const task = {
        title: title.value,
        description: description.value,
        status: status.value,
        priority: priority.value,
    };
    if (!task.title.trim() || !task.description.trim()) {
        formMessage.textContent = "Title and description cannot be blank.";
        return;
    }

    const updating = editingId !== null;
    setBusy(true);
    formMessage.textContent = updating ? "Saving changes..." : "Adding task...";
    try {
        if (updating) {
            await updateTask(editingId, task);
        } else {
            await createTask(task);
        }
        resetForm();
        formMessage.textContent = updating ? "Task updated." : "Task added.";
        await loadTasks();
    } catch (error) {
        formMessage.textContent = `Could not ${updating ? "update" : "add"} task. Please try again.`;
        console.error("Failed to save task.", error);
    } finally {
        setBusy(false);
    }
});

setBusy(true);
loadTasks().finally(() => setBusy(false));
