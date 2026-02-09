'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getCurrentUser, signOut, User } from '@/lib/auth';
import {
    getTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    Task,
} from '@/lib/api';
import { ListTodo, PlusCircle, LogOut, Loader2, Edit, Trash2, CheckCircle, Clock, Calendar } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
// 1. IMPORT THE CHATBOT
import { ChatBot } from '@/components/chatbot';

export default function Dashboard() {
    const [user, setUser] = useState<User | null>(null);
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(true);
    const [newTaskTitle, setNewTaskTitle] = useState('');
    const [newTaskDescription, setNewTaskDescription] = useState('');
    const [editingTask, setEditingTask] = useState<Task | null>(null);
    const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
    const [showAddTask, setShowAddTask] = useState(false);
    const router = useRouter();

    useEffect(() => {
        const fetchUser = async () => {
            const currentUser = await getCurrentUser();
            if (!currentUser) {
                router.push('/');
                return;
            }
            setUser(currentUser);
            loadTasks(currentUser.id);
        };
        fetchUser();
    }, [router]);

    const loadTasks = async (userId: string) => {
        try {
            const data = await getTasks(userId);
            setTasks(data as Task[]);
        } catch (error) {
            console.error('Failed to load tasks:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateTask = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!user || !newTaskTitle.trim()) return;

        try {
            const task = await createTask(user.id, {
                title: newTaskTitle,
                description: newTaskDescription,
            });
            setTasks([task as Task, ...tasks]);
            setNewTaskTitle('');
            setNewTaskDescription('');
            setShowAddTask(false);
        } catch (error) {
            console.error('Failed to create task:', error);
        }
    };

    const handleToggleComplete = async (task: Task) => {
        if (!user) return;
        try {
            const updated = await toggleTaskCompletion(user.id, task.id, !task.completed);
            setTasks(tasks.map((t) => (t.id === task.id ? (updated as Task) : t)));
        } catch (error) {
            console.error('Failed to toggle task:', error);
        }
    };

    const handleDeleteTask = async (taskId: number) => {
        if (!user) return;
        try {
            await deleteTask(user.id, taskId);
            setTasks(tasks.filter((t) => t.id !== taskId));
        } catch (error) {
            console.error('Failed to delete task:', error);
        }
    };

    const handleUpdateTask = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!user || !editingTask) return;
        try {
            const updated = await updateTask(user.id, editingTask.id, {
                title: editingTask.title,
                description: editingTask.description,
            });
            setTasks(tasks.map((t) => (t.id === editingTask.id ? updated as Task : t)));
            setEditingTask(null);
        } catch (error) {
            console.error('Failed to update task:', error);
        }
    };

    const handleSignOut = () => {
        signOut();
        router.push('/');
    };

    const filteredTasks = tasks.filter(task => {
        if (filter === 'active') return !task.completed;
        if (filter === 'completed') return task.completed;
        return true;
    });

    const completedCount = tasks.filter(t => t.completed).length;
    const activeCount = tasks.length - completedCount;
    const completionPercentage = tasks.length > 0 ? Math.round((completedCount / tasks.length) * 100) : 0;

    if (loading) {
        return (
            <div className="min-h-screen bg-[#0a0a0c] flex items-center justify-center">
                <Loader2 className="w-10 h-10 text-violet-500 animate-spin" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0a0a0c] text-slate-200 px-4 py-12 relative">
            <div className="max-w-4xl mx-auto">
                
                {/* Header Section */}
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-10">
                    <div>
                        <h1 className="text-3xl font-bold text-white tracking-tight">
                            Hey, {user?.name || user?.email?.split('@')[0]}
                        </h1>
                        <p className="text-slate-500 text-sm">You've completed {completionPercentage}% of your tasks today.</p>
                    </div>
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={handleSignOut}
                        className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-xl hover:bg-red-500/10 hover:text-red-400 hover:border-red-500/20 transition-all text-sm font-medium text-slate-400"
                    >
                        <LogOut className="w-4 h-4" /> Sign Out
                    </motion.button>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
                    <StatBox icon={<ListTodo className="text-violet-400"/>} label="Total Tasks" value={tasks.length} color="violet" />
                    <StatBox icon={<Clock className="text-amber-400"/>} label="Pending" value={activeCount} color="amber" />
                    <StatBox icon={<CheckCircle className="text-emerald-400"/>} label="Done" value={completedCount} color="emerald" />
                </div>

                {/* Filter & Action Bar */}
                <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
                    <div className="flex bg-white/5 p-1 rounded-xl border border-white/10">
                        {(['all', 'active', 'completed'] as const).map((f) => (
                            <button
                                key={f}
                                onClick={() => setFilter(f)}
                                className={`px-5 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-all ${
                                    filter === f ? 'bg-violet-600 text-white shadow-lg' : 'text-slate-500 hover:text-slate-300'
                                }`}
                            >
                                {f}
                            </button>
                        ))}
                    </div>

                    {!showAddTask && (
                        <motion.button
                            whileHover={{ scale: 1.03 }}
                            whileTap={{ scale: 0.97 }}
                            onClick={() => setShowAddTask(true)}
                            className="px-6 py-2.5 bg-gradient-to-r from-violet-600 to-indigo-600 text-white rounded-xl font-bold text-sm shadow-xl shadow-violet-600/20 flex items-center gap-2"
                        >
                            <PlusCircle className="w-4 h-4" /> New Task
                        </motion.button>
                    )}
                </div>

                {/* Add Task Form */}
                <AnimatePresence>
                    {showAddTask && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="overflow-hidden mb-8"
                        >
                            <form onSubmit={handleCreateTask} className="bg-white/5 border border-white/10 rounded-2xl p-6 space-y-4">
                                <input
                                    type="text"
                                    value={newTaskTitle}
                                    onChange={(e) => setNewTaskTitle(e.target.value)}
                                    placeholder="Task title..."
                                    required
                                    className="w-full bg-[#0a0a0c] border border-white/10 rounded-xl px-4 py-3 text-white focus:border-violet-500 outline-none transition-all"
                                />
                                <textarea
                                    value={newTaskDescription}
                                    onChange={(e) => setNewTaskDescription(e.target.value)}
                                    placeholder="Add a description..."
                                    rows={2}
                                    className="w-full bg-[#0a0a0c] border border-white/10 rounded-xl px-4 py-3 text-white focus:border-violet-500 outline-none transition-all resize-none"
                                />
                                <div className="flex gap-3">
                                    <button type="submit" className="flex-1 bg-white text-black font-bold py-2 rounded-xl hover:bg-slate-200 transition-colors">Create</button>
                                    <button type="button" onClick={() => setShowAddTask(false)} className="px-6 bg-white/5 text-slate-400 py-2 rounded-xl hover:bg-white/10 transition-colors">Cancel</button>
                                </div>
                            </form>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Tasks Container */}
                <div className="space-y-3">
                    {filteredTasks.map((task, index) => (
                        <motion.div
                            layout
                            key={task.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                            className="group relative bg-white/5 border border-white/10 rounded-2xl p-5 hover:bg-white/[0.07] transition-all overflow-hidden"
                        >
                            <div className={`absolute left-0 top-0 bottom-0 w-1 transition-colors ${task.completed ? 'bg-emerald-500' : 'bg-violet-600'}`} />

                            {editingTask?.id === task.id ? (
                                <form onSubmit={handleUpdateTask} className="space-y-3">
                                    <input
                                        value={editingTask.title}
                                        onChange={(e) => setEditingTask({ ...editingTask, title: e.target.value })}
                                        className="w-full bg-[#0a0a0c] border border-white/10 rounded-lg px-3 py-2 text-white outline-none focus:border-violet-500"
                                    />
                                    <textarea
                                        value={editingTask.description}
                                        onChange={(e) => setEditingTask({ ...editingTask, description: e.target.value })}
                                        className="w-full bg-[#0a0a0c] border border-white/10 rounded-lg px-3 py-2 text-white outline-none focus:border-violet-500 text-sm"
                                    />
                                    <div className="flex gap-2">
                                        <button type="submit" className="px-4 py-1.5 bg-violet-600 text-white rounded-lg text-xs font-bold">Save</button>
                                        <button type="button" onClick={() => setEditingTask(null)} className="px-4 py-1.5 bg-white/5 text-slate-400 rounded-lg text-xs">Cancel</button>
                                    </div>
                                </form>
                            ) : (
                                <div className="flex items-start gap-4">
                                    <input
                                        type="checkbox"
                                        checked={task.completed}
                                        onChange={() => handleToggleComplete(task)}
                                        className="mt-1.5 w-5 h-5 rounded-md border-white/20 bg-transparent text-violet-600 focus:ring-violet-600 cursor-pointer transition-all"
                                    />
                                    <div className="flex-1">
                                        <h3 className={`font-semibold text-lg transition-all ${task.completed ? 'line-through text-slate-500' : 'text-white'}`}>
                                            {task.title}
                                        </h3>
                                        {task.description && (
                                            <p className="text-slate-500 text-sm mt-1 leading-relaxed">{task.description}</p>
                                        )}
                                        <div className="mt-3 flex items-center gap-3">
                                            <span className="flex items-center gap-1.5 text-[11px] font-bold text-slate-600 uppercase tracking-tighter">
                                                <Calendar className="w-3 h-3" />
                                                {new Date(task.created_at).toLocaleDateString()}
                                            </span>
                                            {task.completed && (
                                                <span className="bg-emerald-500/10 text-emerald-500 text-[10px] font-bold px-2 py-0.5 rounded-full border border-emerald-500/20">SUCCESS</span>
                                            )}
                                        </div>
                                    </div>
                                    
                                    <div className="flex opacity-0 group-hover:opacity-100 transition-opacity">
                                        <button onClick={() => setEditingTask(task)} className="p-2 hover:bg-white/10 rounded-lg text-slate-500 hover:text-white transition-colors">
                                            <Edit className="w-4 h-4" />
                                        </button>
                                        <button onClick={() => handleDeleteTask(task.id)} className="p-2 hover:bg-red-500/10 rounded-lg text-slate-500 hover:text-red-400 transition-colors">
                                            <Trash2 className="w-4 h-4" />
                                        </button>
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    ))}
                    {filteredTasks.length === 0 && (
                        <div className="text-center py-20 bg-white/5 border border-dashed border-white/10 rounded-3xl">
                            <p className="text-slate-500 font-medium">No tasks found in this view.</p>
                        </div>
                    )}
                </div>
            </div>

            {/* 2. RENDER THE CHATBOT HERE */}
            {user && <ChatBot userId={user.id} onTasksChanged={() => loadTasks(user.id)} />}
        </div>
    );
}

// Stats Helper Component
function StatBox({ icon, label, value, color }: { icon: any, label: string, value: number, color: string }) {
    const colors: any = {
        violet: 'border-violet-500/20',
        amber: 'border-amber-500/20',
        emerald: 'border-emerald-500/20'
    };
    return (
        <div className={`bg-white/5 border ${colors[color]} rounded-2xl p-5 flex items-center gap-4`}>
            <div className="p-3 bg-white/5 rounded-xl">{icon}</div>
            <div>
                <p className="text-[11px] font-bold text-slate-500 uppercase tracking-widest leading-none mb-1">{label}</p>
                <p className="text-2xl font-bold text-white leading-none">{value}</p>
            </div>
        </div>
    );
}