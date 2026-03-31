import axios from 'axios'
import type { FetchPostsParams, PageResponse, SocialPostCrawl } from '../types/post'

const api = axios.create({
  baseURL: '/api',
})

export const fetchPosts = (params: FetchPostsParams = {}): Promise<PageResponse<SocialPostCrawl>> =>
  api.get<PageResponse<SocialPostCrawl>>('/posts', { params }).then((r) => r.data)

export const fetchPost = (spcId: number): Promise<SocialPostCrawl> =>
  api.get<SocialPostCrawl>(`/posts/${spcId}`).then((r) => r.data)