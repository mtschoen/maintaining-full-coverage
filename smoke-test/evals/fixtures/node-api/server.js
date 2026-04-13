import express from 'express';

const app = express();
app.use(express.json());

const tasks = [];
let nextId = 1;

app.get('/tasks', (request, response) => {
    response.json(tasks);
});

app.post('/tasks', (request, response) => {
    const task = {
        id: nextId++,
        title: request.body.title,
        done: false,
        createdAt: new Date().toISOString()
    };
    tasks.push(task);
    response.status(201).json(task);
});

app.patch('/tasks/:id', (request, response) => {
    const task = tasks.find(t => t.id === parseInt(request.params.id));
    if (!task) {
        return response.status(404).json({ error: 'Task not found' });
    }
    if (request.body.title !== undefined) task.title = request.body.title;
    if (request.body.done !== undefined) task.done = request.body.done;
    response.json(task);
});

const port = process.env.PORT || 3099;
app.listen(port, () => {
    console.log(`Task API running on port ${port}`);
});
