export interface BrandAssignee {
  assigneeId: number
  brandId: number
  brandName: string | null
  platformId: string
  assigneeName: string
  accountId: string
  accountType: string
  active: boolean
}

export interface AssigneeFilters {
  assigneeName: string
  brandName: string
  platformId: string   // '' = ALL
  accountId: string
  accountType: string  // '' = ALL
  active: 'ALL' | 'ON' | 'OFF'
}