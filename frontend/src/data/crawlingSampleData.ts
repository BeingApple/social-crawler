import type { CrawlingPost } from '../types/crawling'

/**
 * 소셜 미디어 타입별 수집 가능 범위
 *
 * 플랫폼           | 제목 | 내용 | 인물태그       | 해시태그    | 첨부링크
 * 인스타그램 피드  | X    | O    | 태그된 모든 계정 | 앞 5개    | X
 * 인스타그램 스토리| X    | O    | 태그된 모든 계정 | 앞 5개    | 랜딩 링크
 * 인스타그램 릴스  | X    | O    | 태그된 모든 계정 | 앞 5개    | X
 * 유튜브           | O    | O    | 태그된 모든 계정 | 앞 5개    | 랜딩 링크 앞 3개
 * 유튜브 쇼츠      | O    | O    | X              | 앞 5개    | 랜딩 링크 앞 3개
 */
export const SAMPLE_CRAWLING_POSTS: CrawlingPost[] = [
  // 인스타그램 피드 — 제목 X, 첨부링크 X
  {
    managerName: '박소운',
    brandName: '코치',
    socialMedia: '인스타그램 피드',
    accountType: 'KR',
    accountName: 'coach_kr',
    followers: 124000,
    postUrl: 'https://www.instagram.com/p/abc1234/',
    uploadedAt: '2026-03-25',
    imageUrl: 'https://picsum.photos/seed/coach1/80/80',
    postTitle: '',
    postContent: '새로운 시즌을 맞아 선보이는 코치의 봄 컬렉션을 소개합니다. 지금 만나보세요.',
    peopleTags: ['@stylist_jiyeon', '@fashionista_kim'],
    hashtags: ['#코치', '#COACH', '#2026SS', '#봄코디', '#가방'],
    attachedLinks: [],
  },
  // 인스타그램 스토리 — 제목 X, 첨부링크: 랜딩 링크
  {
    managerName: '박소운',
    brandName: '코치',
    socialMedia: '인스타그램 스토리',
    accountType: 'KR',
    accountName: 'coach_kr',
    followers: 124000,
    postUrl: 'https://www.instagram.com/stories/coach_kr/def5678/',
    uploadedAt: '2026-03-25',
    imageUrl: 'https://picsum.photos/seed/coach2/80/80',
    postTitle: '',
    postContent: '신상 백팩 지금 바로 확인하세요!',
    peopleTags: ['@coach_official'],
    hashtags: ['#코치', '#COACH', '#신상', '#백팩', '#스토리'],
    attachedLinks: ['https://coach.com/kr/collection/ss2026'],
  },
  // 인스타그램 릴스 — 제목 X, 첨부링크 X
  {
    managerName: '김민지',
    brandName: '나이키',
    socialMedia: '인스타그램 릴스',
    accountType: 'KR',
    accountName: 'nike_kr',
    followers: 980000,
    postUrl: 'https://www.instagram.com/reel/ghi9012/',
    uploadedAt: '2026-03-24',
    imageUrl: 'https://picsum.photos/seed/nike1/80/80',
    postTitle: '',
    postContent: 'Air Max의 역사를 기념하는 특별한 날, 지금 당신의 스타일을 찾아보세요.',
    peopleTags: ['@nikesportswear', '@athlete_junho'],
    hashtags: ['#AirMaxDay', '#Nike', '#나이키', '#에어맥스', '#운동화'],
    attachedLinks: [],
  },
  // 유튜브 — 제목 O, 첨부링크: 랜딩 링크 앞 3개
  {
    managerName: '박소운',
    brandName: '루이비통',
    socialMedia: '유튜브',
    accountType: 'HQ',
    accountName: 'louisvuitton',
    followers: 2100000,
    postUrl: 'https://www.youtube.com/watch?v=jkl3456',
    uploadedAt: '2026-03-22',
    imageUrl: 'https://picsum.photos/seed/lv1/80/80',
    postTitle: 'LV 2026 봄 컬렉션 패션위크 하이라이트',
    postContent: '파리 패션위크에서 선보인 루이비통의 2026 봄 컬렉션 풀영상입니다. 디렉터 니콜라 제스키에르가 직접 소개하는 이번 시즌의 테마와 핵심 아이템을 확인하세요.',
    peopleTags: ['@nicolasghesquiere', '@lvofficial', '@fashionweekparis'],
    hashtags: ['#LouisVuitton', '#루이비통', '#FashionWeek', '#2026SS', '#파리패션위크'],
    attachedLinks: [
      'https://louisvuitton.com/fashionweek2026',
      'https://louisvuitton.com/kr/collection',
      'https://louisvuitton.com/kr/store',
    ],
  },
  // 유튜브 쇼츠 — 제목 O, 인물태그 X, 첨부링크: 랜딩 링크 앞 3개
  {
    managerName: '한수진',
    brandName: '구찌',
    socialMedia: '유튜브 쇼츠',
    accountType: 'HQ',
    accountName: 'gucciofficial',
    followers: 3400000,
    postUrl: 'https://www.youtube.com/shorts/mno7890',
    uploadedAt: '2026-03-23',
    imageUrl: 'https://picsum.photos/seed/gucci1/80/80',
    postTitle: 'Gucci Spring 2026 — 15초 하이라이트',
    postContent: '구찌 2026 봄 시즌의 핵심 룩을 15초로 압축했습니다. 전체 컬렉션은 링크에서 확인하세요.',
    peopleTags: [],
    hashtags: ['#Gucci', '#구찌', '#Shorts', '#Fashion', '#2026'],
    attachedLinks: [
      'https://gucci.com/collection/spring2026',
      'https://gucci.com/kr',
      'https://gucci.com/kr/stores',
    ],
  },
]
