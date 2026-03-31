export interface BrandAssignee {
  assigneeId: number
  brandId: number
  brandName: string | null
  platformId: string
  region: string | null
  assigneeName: string
  accountId: string
  active: boolean
}

export interface AssigneeFilters {
  assigneeName: string
  brandName: string
  platformId: string   // '' = ALL
  region: string       // '' = ALL
  accountId: string
  active: 'ALL' | 'ON' | 'OFF'
}