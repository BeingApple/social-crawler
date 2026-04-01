import axios from 'axios'
import type {
  SocialCrawlAccount,
  SocialCrawlAccountCredential,
  SocialCrawlAccountRequest,
} from '../types/crawlAccount'

const api = axios.create({ baseURL: '/api' })

export const fetchAll = (): Promise<SocialCrawlAccount[]> =>
  api.get<SocialCrawlAccount[]>('/crawl-accounts').then((r) => r.data)

export const fetchById = (id: number): Promise<SocialCrawlAccount> =>
  api.get<SocialCrawlAccount>(`/crawl-accounts/${id}`).then((r) => r.data)

export const fetchDecrypt = (id: number): Promise<SocialCrawlAccountCredential> =>
  api.get<SocialCrawlAccountCredential>(`/crawl-accounts/${id}/decrypt`).then((r) => r.data)

export const create = (body: SocialCrawlAccountRequest): Promise<SocialCrawlAccount> =>
  api.post<SocialCrawlAccount>('/crawl-accounts', body).then((r) => r.data)

export const update = (id: number, body: SocialCrawlAccountRequest): Promise<SocialCrawlAccount> =>
  api.put<SocialCrawlAccount>(`/crawl-accounts/${id}`, body).then((r) => r.data)

export const remove = (id: number): Promise<void> =>
  api.delete(`/crawl-accounts/${id}`).then(() => undefined)
