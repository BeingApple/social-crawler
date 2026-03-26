export interface BrandAccount {
  managerName: string
  brandName: string
  socialMedia: string
  accountId: string
  accountType: string
  status: 'ON' | 'OFF'
}

export interface AccountFilters {
  managerName: string
  brandName: string
  socialMedia: string   // '' = ALL
  accountId: string
  accountType: string   // '' = ALL
  status: 'ALL' | 'ON' | 'OFF'
}
