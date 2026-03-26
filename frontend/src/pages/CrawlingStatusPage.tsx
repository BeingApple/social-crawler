import { useState } from 'react'
import {
  Box, Typography, Paper, Grid, TextField,
  FormControl, InputLabel, Select, MenuItem, Card, CardContent, Link,
} from '@mui/material'
import type { SelectChangeEvent } from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import { SAMPLE_CRAWLING_POSTS } from '../data/crawlingSampleData'
import type { CrawlingFilters } from '../types/crawling'

const SOCIAL_MEDIA_OPTIONS = ['인스타그램 피드', '인스타그램 스토리', '인스타그램 릴스', '유튜브', '유튜브 쇼츠']
const ACCOUNT_TYPE_OPTIONS = ['KR', 'HQ']

const BRAND_OPTIONS = [...new Set(SAMPLE_CRAWLING_POSTS.map((p) => p.brandName))]

const INITIAL_FILTERS: CrawlingFilters = {
  dateFrom: '',
  dateTo: '',
  managerName: '',
  brandName: '',
  socialMedia: '',
  accountType: '',
}

const columns: GridColDef[] = [
  { field: 'managerName',   headerName: '담당자명',       width: 100 },
  { field: 'brandName',     headerName: '브랜드명',       width: 110 },
  { field: 'socialMedia',   headerName: '소셜 미디어',    width: 140 },
  { field: 'accountType',   headerName: '계정 구분',      width: 90  },
  { field: 'accountName',   headerName: '계정명',         width: 120 },
  { field: 'followers',     headerName: '팔로워수',       width: 100, type: 'number',
    valueFormatter: (value: number) => value.toLocaleString() },
  {
    field: 'postUrl',
    headerName: '게시글 바로가기',
    width: 130,
    renderCell: ({ value }) => (
      <Link href={value as string} target="_blank" rel="noopener" underline="hover" fontSize={13}>
        바로가기
      </Link>
    ),
  },
  { field: 'uploadedAt',    headerName: '업로드 날짜',    width: 120 },
  {
    field: 'imageUrl',
    headerName: '이미지',
    width: 80,
    renderCell: ({ value }) =>
      value ? (
        <Box component="img" src={value as string} alt="post" sx={{ width: 40, height: 40, objectFit: 'cover', borderRadius: 1 }} />
      ) : (
        <Box sx={{ width: 40, height: 40, bgcolor: '#e0e0e0', borderRadius: 1 }} />
      ),
  },
  { field: 'postTitle',     headerName: '게시글 제목',    width: 160 },
  { field: 'postContent',   headerName: '게시글 내용',    width: 220 },
  { field: 'peopleTags',    headerName: '인물태그',       width: 160,
    valueFormatter: (value: string[]) => value.join(', ') },
  { field: 'hashtags',      headerName: '해시태그',       width: 180,
    valueFormatter: (value: string[]) => value.join(' ') },
  {
    field: 'attachedLinks',
    headerName: '게시글 내 첨부 링크',
    width: 180,
    renderCell: ({ value }) => {
      const links = value as string[]
      if (!links.length) return '-'
      return (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
          {links.map((url, i) => (
            <Link key={i} href={url} target="_blank" rel="noopener" underline="hover" fontSize={12} noWrap>
              {url}
            </Link>
          ))}
        </Box>
      )
    },
  },
]

export default function CrawlingStatusPage() {
  const [filters, setFilters] = useState<CrawlingFilters>(INITIAL_FILTERS)

  const handleText =
    (field: keyof CrawlingFilters) => (e: React.ChangeEvent<HTMLInputElement>) =>
      setFilters((prev) => ({ ...prev, [field]: e.target.value }))

  const handleSelect =
    (field: keyof CrawlingFilters) => (e: SelectChangeEvent<string>) =>
      setFilters((prev) => ({ ...prev, [field]: e.target.value }))

  const rows = SAMPLE_CRAWLING_POSTS
    .filter((p) => {
      if (filters.dateFrom && p.uploadedAt < filters.dateFrom) return false
      if (filters.dateTo && p.uploadedAt > filters.dateTo) return false
      if (filters.managerName && !p.managerName.includes(filters.managerName)) return false
      if (filters.brandName && p.brandName !== filters.brandName) return false
      if (filters.socialMedia && p.socialMedia !== filters.socialMedia) return false
      if (filters.accountType && p.accountType !== filters.accountType) return false
      return true
    })
    .map((p, i) => ({ id: i, ...p }))

  return (
    <>
      <Typography variant="h5" fontWeight={700} mb={3}>
        크롤링 현황
      </Typography>

      {/* 필터 영역 */}
      <Paper elevation={1} sx={{ p: 2.5, mb: 3 }}>
        <Grid container spacing={2}>

          {/* 업로드 기간 */}
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
              <Typography variant="body2" sx={{ color: 'text.secondary', whiteSpace: 'nowrap', minWidth: 72 }}>
                업로드 기간
              </Typography>
              <TextField
                size="small"
                type="date"
                label="시작"
                value={filters.dateFrom}
                onChange={handleText('dateFrom')}
                InputLabelProps={{ shrink: true }}
                sx={{ width: 160 }}
              />
              <Typography variant="body2" color="text.secondary">~</Typography>
              <TextField
                size="small"
                type="date"
                label="끝"
                value={filters.dateTo}
                onChange={handleText('dateTo')}
                InputLabelProps={{ shrink: true }}
                sx={{ width: 160 }}
              />
            </Box>
          </Grid>

          {/* 담당자명 */}
          <Grid item xs={12} sm={3}>
            <TextField
              size="small" fullWidth
              label="담당자명"
              value={filters.managerName}
              onChange={handleText('managerName')}
            />
          </Grid>

          {/* 브랜드명 */}
          <Grid item xs={12} sm={3}>
            <FormControl size="small" fullWidth>
              <InputLabel>브랜드명</InputLabel>
              <Select value={filters.brandName} label="브랜드명" onChange={handleSelect('brandName')}>
                <MenuItem value="">전체</MenuItem>
                {BRAND_OPTIONS.map((v) => <MenuItem key={v} value={v}>{v}</MenuItem>)}
              </Select>
            </FormControl>
          </Grid>

          {/* 소셜 미디어 */}
          <Grid item xs={12} sm={3}>
            <FormControl size="small" fullWidth>
              <InputLabel>소셜 미디어</InputLabel>
              <Select value={filters.socialMedia} label="소셜 미디어" onChange={handleSelect('socialMedia')}>
                <MenuItem value="">전체</MenuItem>
                {SOCIAL_MEDIA_OPTIONS.map((v) => <MenuItem key={v} value={v}>{v}</MenuItem>)}
              </Select>
            </FormControl>
          </Grid>

          {/* 계정 구분 */}
          <Grid item xs={12} sm={3}>
            <FormControl size="small" fullWidth>
              <InputLabel>계정 구분</InputLabel>
              <Select value={filters.accountType} label="계정 구분" onChange={handleSelect('accountType')}>
                <MenuItem value="">전체</MenuItem>
                {ACCOUNT_TYPE_OPTIONS.map((v) => <MenuItem key={v} value={v}>{v}</MenuItem>)}
              </Select>
            </FormControl>
          </Grid>

        </Grid>
      </Paper>

      {/* 테이블 */}
      <Card elevation={2}>
        <CardContent>
          <DataGrid
            rows={rows}
            columns={columns}
            autoHeight
            checkboxSelection
            pageSizeOptions={[5, 10, 25]}
            initialState={{ pagination: { paginationModel: { pageSize: 10 } } }}
          />
        </CardContent>
      </Card>
    </>
  )
}
