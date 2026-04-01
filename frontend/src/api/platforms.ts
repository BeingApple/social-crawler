import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export interface SocialPlatform {
  platformId: string
  platformName: string
}

export const fetchPlatforms = (): Promise<SocialPlatform[]> =>
  api.get<SocialPlatform[]>('/platforms').then((r) => r.data)
