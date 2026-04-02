import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box, Typography, Paper, Grid, TextField,
  FormControl, InputLabel, Select, MenuItem, Card, CardContent, Link, Button,
} from '@mui/material'
import type { SelectChangeEvent } from '@mui/material'
import { DataGrid, GridColDef, GridPaginationModel, GridRenderCellParams } from '@mui/x-data-grid'
import { fetchPosts } from '../api/posts'
import type { SocialPostCrawl, FetchPostsParams } from '../types/post'
import { usePlatforms } from '../hooks/usePlatforms'

const CRAWL_CASE_OPTIONS = [
  { value: 'CASE1', label: 'CASE1 (공식계정)' },
  { value: 'CASE2', label: 'CASE2 (키워드검색)' },
]

type Row = SocialPostCrawl & { id: number }

interface Filters {
  dateFrom:   string
  dateTo:     string
  brandName:  string
  platformId: string
  crawlCase:  string
}

const INITIAL_FILTERS: Filters = {
  dateFrom:   '',
  dateTo:     '',
  brandName:  '',
  platformId: '',
  crawlCase:  '',
}

export default function CrawlingStatusPage() {
  const navigate = useNavigate()
  const [filters, setFilters]   = useState<Filters>(INITIAL_FILTERS)
  const [rows, setRows]         = useState<Row[]>([])
  const [total, setTotal]       = useState(0)
  const [page, setPage]         = useState(0)
  const [pageSize, setPageSize] = useState(20)
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState<string | null>(null)
  const { platforms, platformLabels } = usePlatforms()

  const columns = useMemo<GridColDef<Row>[]>(() => [
    {
      field: 'detail',
      headerName: '',
      width: 72,
      sortable: false,
      renderCell: ({ row }: GridRenderCellParams<Row>) => (
        <Button size="small" onClick={() => navigate(`/crawling/${row.spcId}`)}>
          상세
        </Button>
      ),
    },
    { field: 'brandName',  headerName: '브랜드명',    width: 110 },
    {
      field: 'platformId',
      headerName: '소셜 미디어',
      width: 120,
      valueFormatter: (value: string) => platformLabels[value] ?? value,
    },
    { field: 'crawlCase',  headerName: '수집 유형',    width: 110 },
    { field: 'accountId',  headerName: '계정명',       width: 130 },
    {
      field: 'authorFollowers',
      headerName: '팔로워수',
      width: 100,
      type: 'number',
      valueFormatter: (value: number | null) => value != null ? value.toLocaleString() : '-',
    },
    {
      field: 'postUrl',
      headerName: '게시글 바로가기',
      width: 130,
      renderCell: ({ value }: GridRenderCellParams<Row, string>) => (
        <Link href={value} target="_blank" rel="noopener" underline="hover" fontSize={13}>
          바로가기
        </Link>
      ),
    },
    {
      field: 'postedAt',
      headerName: '업로드 날짜',
      width: 120,
      valueFormatter: (value: string) => value ? new Date(value).toLocaleDateString('ko-KR') : '-',
    },
    {
      field: 'thumbnailUrl',
      headerName: '이미지',
      width: 80,
      renderCell: ({ value }: GridRenderCellParams<Row, string | null>) =>
        value ? (
          <Box component="img" src={value} alt="post" sx={{ width: 40, height: 40, objectFit: 'cover', borderRadius: 1 }} />
        ) : (
          <Box sx={{ width: 40, height: 40, bgcolor: '#e0e0e0', borderRadius: 1 }} />
        ),
    },
    { field: 'postTitle',   headerName: '게시글 제목', width: 160 },
    { field: 'textContent', headerName: '게시글 내용', width: 220 },
    {
      field: 'hashtags',
      headerName: '해시태그',
      width: 180,
      renderCell: ({ value }: GridRenderCellParams<Row, string | null>) => {
        if (!value) return '-'
        try {
          const tags: string[] = JSON.parse(value)
          return tags.join(' ')
        } catch {
          return value
        }
      },
    },
    {
      field: 'personTags',
      headerName: '인물태그',
      width: 160,
      renderCell: ({ value }: GridRenderCellParams<Row, string | null>) => {
        if (!value) return '-'
        try {
          const tags: string[] = JSON.parse(value)
          return tags.join(', ')
        } catch {
          return value
        }
      },
    },
    {
      field: 'likeCount',
      headerName: '좋아요',
      width: 80,
      type: 'number',
      valueFormatter: (value: number | null) => value != null ? value.toLocaleString() : '-',
    },
    {
      field: 'commentCount',
      headerName: '댓글',
      width: 80,
      type: 'number',
      valueFormatter: (value: number | null) => value != null ? value.toLocaleString() : '-',
    },
    {
      field: 'viewCount',
      headerName: '조회수',
      width: 90,
      type: 'number',
      valueFormatter: (value: number | null) => value != null ? value.toLocaleString() : '-',
    },
  ], [platformLabels])

  useEffect(() => {
    setLoading(true)
    setError(null)

    const params: FetchPostsParams = {
      platformId:  filters.platformId || undefined,
      brandName:   filters.brandName  || undefined,
      crawlCase:   filters.crawlCase  || undefined,
      postedFrom:  filters.dateFrom   || undefined,
      postedTo:    filters.dateTo     || undefined,
      page,
      size: pageSize,
    }

    fetchPosts(params)
      .then((data) => {
        setRows(data.content.map((p) => ({ id: p.spcId, ...p })))
        setTotal(data.totalElements)
      })
      .catch(() => setError('데이터를 불러오지 못했습니다.'))
      .finally(() => setLoading(false))
  }, [filters.platformId, filters.brandName, filters.crawlCase, filters.dateFrom, filters.dateTo, page, pageSize])

  const handleText =
    (field: keyof Filters) => (e: React.ChangeEvent<HTMLInputElement>) => {
      setFilters((prev) => ({ ...prev, [field]: e.target.value }))
      setPage(0)
    }

  const handleSelect =
    (field: keyof Filters) => (e: SelectChangeEvent<string>) => {
      setFilters((prev) => ({ ...prev, [field]: e.target.value }))
      setPage(0)
    }

  const handlePaginationChange = (model: GridPaginationModel) => {
    setPage(model.page)
    setPageSize(model.pageSize)
  }

  return (
    <>
      <Typography variant="h5" fontWeight={700} mb={3}>
        크롤링 현황
      </Typography>

      {/* 필터 영역 */}
      <Paper elevation={1} sx={{ p: 2.5, mb: 3 }}>
        <Grid container spacing={2}>

          {/* 업로드 기간 */}
          <Grid size={12}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
              <Typography variant="body2" sx={{ color: 'text.secondary', whiteSpace: 'nowrap', minWidth: 72 }}>
                업로드 기간
              </Typography>
              <TextField
                size="small" type="date" label="시작"
                value={filters.dateFrom} onChange={handleText('dateFrom')}
                slotProps={{ inputLabel: { shrink: true } }}
                sx={{ width: 160 }}
              />
              <Typography variant="body2" color="text.secondary">~</Typography>
              <TextField
                size="small" type="date" label="끝"
                value={filters.dateTo} onChange={handleText('dateTo')}
                slotProps={{ inputLabel: { shrink: true } }}
                sx={{ width: 160 }}
              />
            </Box>
          </Grid>

          {/* 브랜드명 */}
          <Grid size={{ xs: 12, sm: 3 }}>
            <TextField size="small" fullWidth label="브랜드명" value={filters.brandName} onChange={handleText('brandName')} />
          </Grid>

          {/* 소셜 미디어 */}
          <Grid size={{ xs: 12, sm: 3 }}>
            <FormControl size="small" fullWidth>
              <InputLabel>소셜 미디어</InputLabel>
              <Select value={filters.platformId} label="소셜 미디어" onChange={handleSelect('platformId')}>
                <MenuItem value="">전체</MenuItem>
                {platforms.map((p) => (
                  <MenuItem key={p.platformId} value={p.platformId}>{p.platformName}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          {/* 수집 유형 */}
          <Grid size={{ xs: 12, sm: 3 }}>
            <FormControl size="small" fullWidth>
              <InputLabel>수집 유형</InputLabel>
              <Select value={filters.crawlCase} label="수집 유형" onChange={handleSelect('crawlCase')}>
                <MenuItem value="">전체</MenuItem>
                {CRAWL_CASE_OPTIONS.map(({ value, label }) => (
                  <MenuItem key={value} value={value}>{label}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

        </Grid>
      </Paper>

      {error && <Typography color="error" mb={1}>{error}</Typography>}

      {/* 테이블 */}
      <Card elevation={2}>
        <CardContent>
          <DataGrid
            rows={rows}
            columns={columns}
            rowCount={total}
            loading={loading}
            paginationMode="server"
            paginationModel={{ page, pageSize }}
            onPaginationModelChange={handlePaginationChange}
            pageSizeOptions={[10, 20, 50]}
            sx={{ width: '100%' }}
            checkboxSelection
            disableRowSelectionOnClick
          />
        </CardContent>
      </Card>
    </>
  )
}
