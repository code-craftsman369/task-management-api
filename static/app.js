const API_BASE = 'http://localhost:5001';

// Load tasks on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    
    // Event listeners
    document.getElementById('addTaskForm').addEventListener('submit', addTask);
    document.getElementById('filterStatus').addEventListener('change', loadTasks);
    document.getElementById('filterPriority').addEventListener('change', loadTasks);
    document.getElementById('searchQuery').addEventListener('input', loadTasks);
});

async function loadTasks() {
    const status = document.getElementById('filterStatus').value;
    const priority = document.getElementById('filterPriority').value;
    const search = document.getElementById('searchQuery').value;
    
    let url = `${API_BASE}/tasks?`;
    
    if (status !== 'all') url += `status=${status}&`;
    if (priority !== 'all') url += `priority=${priority}&`;
    if (search) url += `search=${search}&`;
    
    try {
        const response = await fetch(url);
        const tasks = await response.json();
        displayTasks(tasks);
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

function displayTasks(tasks) {
    const tasksList = document.getElementById('tasksList');
    
    if (tasks.length === 0) {
        tasksList.innerHTML = `
            <div class="empty-state">
                <h3>No tasks found</h3>
                <p>Add a new task to get started!</p>
            </div>
        `;
        return;
    }
    
    tasksList.innerHTML = tasks.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''} ${task.priority}">
            <div class="task-header">
                <span class="task-title ${task.completed ? 'completed' : ''}">${task.title}</span>
                <span class="task-priority priority-${task.priority}">${task.priority.toUpperCase()}</span>
            </div>
            ${task.description ? `<div class="task-description">${task.description}</div>` : ''}
            <div class="task-meta">
                <span>📅 Created: ${new Date(task.created_at).toLocaleString()}</span>
                ${task.deadline ? `<span>⏰ Deadline: ${new Date(task.deadline).toLocaleString()}</span>` : ''}
            </div>
            <div class="task-actions">
                <button class="btn-small btn-success" onclick="toggleTask(${task.id})">
                    ${task.completed ? '↩️ Undo' : '✅ Complete'}
                </button>
                <button class="btn-small btn-danger" onclick="deleteTask(${task.id})">🗑️ Delete</button>
            </div>
        </div>
    `).join('');
}

async function addTask(e) {
    e.preventDefault();
    
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const priority = document.getElementById('priority').value;
    const deadline = document.getElementById('deadline').value;
    
    const taskData = {
        title,
        description,
        priority,
        deadline: deadline || null
    };
    
    try {
        const response = await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        });
        
        if (response.ok) {
            document.getElementById('addTaskForm').reset();
            loadTasks();
        }
    } catch (error) {
        console.error('Error adding task:', error);
    }
}

async function toggleTask(id) {
    try {
        await fetch(`${API_BASE}/tasks/${id}/toggle`, {
            method: 'PATCH'
        });
        loadTasks();
    } catch (error) {
        console.error('Error toggling task:', error);
    }
}

async function deleteTask(id) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        await fetch(`${API_BASE}/tasks/${id}`, {
            method: 'DELETE'
        });
        loadTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}