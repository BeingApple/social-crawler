export const PLATFORM_LABELS: Record<string, string> = {
  instagram: '인스타그램',
  youtube: '유튜브',
  tiktok: '틱톡',
  x: 'X',
}

export const PLATFORM_OPTIONS = Object.entries(PLATFORM_LABELS).map(([value, label]) => ({ value, label }))