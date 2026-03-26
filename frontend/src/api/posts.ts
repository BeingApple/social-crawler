import axios from 'axios'
import type { FetchPostsParams, PageResponse, Post } from '../types/post'

const api = axios.create({
  baseURL: '/api',
})

export const fetchPosts = (params: FetchPostsParams = {}): Promise<PageResponse<Post>> =>
  api.get<PageResponse<Post>>('/posts', { params }).then((r) => r.data)

export const fetchPost = (postId: number): Promise<Post> =>
  api.get<Post>(`/posts/${postId}`).then((r) => r.data)
