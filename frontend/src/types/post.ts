export interface SocialPostCrawl {
  spcId: number
  platformId: string
  crawlCase: string
  brandName: string
  accountId: string
  accountType: string
  postId: string
  postUrl: string
  postType: string | null
  postedAt: string
  postTitle: string | null
  textContent: string | null
  personTags: string | null
  hashtags: string | null
  mediaUrl: string | null
  thumbnailUrl: string | null
  viewCount: number | null
  likeCount: number | null
  commentCount: number | null
  shareCount: number | null
  authorName: string | null
  authorFollowers: number | null
  duplicate: boolean
  junk: boolean
  createdAt: string
}

export interface PageResponse<T> {
  content: T[]
  totalElements: number
  totalPages: number
  size: number
  number: number
}

export interface FetchPostsParams {
  platformId?: string
  brandName?: string
  crawlCase?: string
  postedFrom?: string   // ISO date (YYYY-MM-DD)
  postedTo?: string     // ISO date (YYYY-MM-DD)
  page?: number
  size?: number
}