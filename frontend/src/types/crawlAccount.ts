export type AccountStatus = 'ACTIVE' | 'BLOCKED' | 'EXPIRED' | 'PAUSED'

export interface SocialCrawlAccount {
  accountId: number
  name: string
  platformId: string
  loginId: string
  issue: string | null
  status: AccountStatus
  createdAt: string
  updatedAt: string
}

export interface SocialCrawlAccountCredential {
  accountId: number
  loginId: string
  loginPw: string
}

export interface SocialCrawlAccountRequest {
  name: string
  platformId: string
  loginId: string
  loginPw: string
  issue?: string | null
  status: AccountStatus
}
