import axios from 'axios'
import type { BrandAssignee } from '../types/brand'

const api = axios.create({
  baseURL: '/api',
})

export const fetchAssignees = (): Promise<BrandAssignee[]> =>
  api.get<BrandAssignee[]>('/assignees').then((r) => r.data)