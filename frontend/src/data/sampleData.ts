import type { BrandAccount } from '../types/brand'

export const SAMPLE_ACCOUNTS: BrandAccount[] = [
  { managerName: '박소운', brandName: '코치',    socialMedia: '인스타그램', accountId: 'coach',           accountType: 'KR', status: 'ON'  },
  { managerName: '김민지', brandName: '나이키',  socialMedia: '유튜브',     accountId: 'nike_kr',         accountType: 'KR', status: 'ON'  },
  { managerName: '박소운', brandName: '코치',    socialMedia: '인스타그램', accountId: 'coach_global',    accountType: 'HQ', status: 'OFF' },
  { managerName: '이재민', brandName: '아디다스', socialMedia: '페이스북',  accountId: 'adidas_official', accountType: 'HQ', status: 'ON'  },
  { managerName: '김민지', brandName: '나이키',  socialMedia: '유튜브',     accountId: 'nike_global',     accountType: 'HQ', status: 'OFF' },
  { managerName: '이재민', brandName: '아디다스', socialMedia: '인스타그램', accountId: 'adidas_kr',      accountType: 'KR', status: 'ON'  },
  { managerName: '한수진', brandName: '구찌',    socialMedia: '틱톡',       accountId: 'gucci_kr',        accountType: 'KR', status: 'ON'  },
  { managerName: '한수진', brandName: '구찌',    socialMedia: '인스타그램', accountId: 'gucci_official',  accountType: 'HQ', status: 'ON'  },
  { managerName: '박소운', brandName: '루이비통', socialMedia: '유튜브',    accountId: 'lv_official',     accountType: 'HQ', status: 'OFF' },
  { managerName: '한수진', brandName: '구찌',    socialMedia: '틱톡',       accountId: 'gucci_global',    accountType: 'HQ', status: 'OFF' },
  { managerName: '김민지', brandName: '나이키',  socialMedia: '틱톡',       accountId: 'nike_tiktok',     accountType: 'KR', status: 'ON'  },
  { managerName: '이재민', brandName: '뉴발란스', socialMedia: '인스타그램', accountId: 'nb_kr',          accountType: 'KR', status: 'ON'  },
]
