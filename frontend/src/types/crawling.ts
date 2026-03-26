export interface CrawlingPost {
  managerName: string
  brandName: string
  socialMedia: string
  accountType: 'KR' | 'HQ'
  accountName: string
  followers: number
  postUrl: string
  uploadedAt: string
  imageUrl: string
  postTitle: string
  postContent: string
  peopleTags: string[]
  hashtags: string[]
  attachedLinks: string[]
}

export interface CrawlingFilters {
  dateFrom: string
  dateTo: string
  managerName: string
  brandName: string
  socialMedia: string   // '' = ALL
  accountType: string   // '' = ALL
}
