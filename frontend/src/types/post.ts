export interface Post {
  postId: number
  brandId: number
  platform: string
  externalPostId: string
  content: string | null
  hashtags: string[] | null
  likes: number
  comments: number
  views: number
  postedAt: string | null
  crawledAt: string
}

export interface PageResponse<T> {
  content: T[]
  totalElements: number
  totalPages: number
  size: number
  number: number
}

export interface FetchPostsParams {
  platform?: string
  page?: number
  size?: number
}
