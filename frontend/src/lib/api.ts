// src/lib/api.ts
import axios from 'axios';
import { getToken } from './auth'; // Import getToken

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Task {
  id: number;
  user_id: string; // Added user_id to Task interface
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

// Helper to get authorization headers
const getAuthHeaders = () => {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const getTasks = async (userId: string) => {
  const response = await axios.get(`${API_URL}/api/${userId}/tasks`, { headers: getAuthHeaders() });
  return response.data;
};

export const createTask = async (userId: string, task: Partial<Task>) => {
  const response = await axios.post(`${API_URL}/api/${userId}/tasks`, task, { headers: getAuthHeaders() });
  return response.data;
};

export const updateTask = async (userId: string, taskId: number, task: Partial<Task>) => {
  const response = await axios.put(`${API_URL}/api/${userId}/tasks/${taskId}`, task, { headers: getAuthHeaders() });
  return response.data;
};

export const deleteTask = async (userId: string, taskId: number) => {
  const response = await axios.delete(`${API_URL}/api/${userId}/tasks/${taskId}`, { headers: getAuthHeaders() });
  return response.data;
};

export const toggleTaskCompletion = async (userId: string, taskId: number, completed: boolean) => {
  const response = await axios.patch(`${API_URL}/api/${userId}/tasks/${taskId}/complete`, { completed }, { headers: getAuthHeaders() });
  return response.data;
};

export interface ChatResponse {
  response: string;
  conversation_id: number;
  user_id: string;
}

export const chatWithAI = async (userId: string, message: string, conversationId: number | null = null): Promise<ChatResponse> => {
  const payload = {
    message: message,
    conversation_id: conversationId,
  };
  const response = await axios.post<ChatResponse>(`${API_URL}/api/${userId}/chat`, payload, { headers: getAuthHeaders() });
  return response.data;
};