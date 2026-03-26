import { useEffect, useState } from 'react'
import {
  Box, Chip, FormControl, InputLabel, MenuItem,
  Select, Typography,
} from '@mui/material'
import { DataGrid, GridColDef, GridPaginationModel, GridRenderCellParams } from '@mui/x-data-grid'
import type { SelectChangeEvent } from '@mui/material'
import { fetchPosts } from '../api/posts'
import type { Post } from '../types/post'

type Platform = '' | 'instagram' | 'tiktok' | 'twitter'
const PLATFORMS: Platform[] = ['', 'instagram', 'tiktok', 'twitter']

type Row = Post & { id: number }

const columns: GridColDef<Row>[] = [
  { field: 'postId',    headerName: 'ID',         width: 80 },
  { field: 'platform',  headerName: 'Platform',   width: 110,
    renderCell: (p: GridRenderCellParams<Row, string>) => <Chip label={p.value} size="small" /> },
  { field: 'content',   headerName: 'Content',    flex: 1,
    renderCell: (p: GridRenderCellParams<Row, string | null>) => p.value?.slice(0, 80) ?? '—' },
  { field: 'likes',     headerName: 'Likes',      width: 90 },
  { field: 'comments',  headerName: 'Comments',   width: 100 },
  { field: 'views',     headerName: 'Views',      width: 100 },
  { field: 'postedAt',  headerName: 'Posted At',  width: 170,
    renderCell: (p: GridRenderCellParams<Row, string | null>) =>
      p.value ? new Date(p.value).toLocaleString('ko-KR') : '—' },
  { field: 'crawledAt', headerName: 'Crawled At', width: 170,
    renderCell: (p: GridRenderCellParams<Row, string>) => new Date(p.value ?? '').toLocaleString('ko-KR') },
]

export default function PostListPage() {
  const [platform, setPlatform] = useState<Platform>('')
  const [rows, setRows]         = useState<Row[]>([])
  const [total, setTotal]       = useState(0)
  const [page, setPage]         = useState(0)
  const [pageSize, setPageSize] = useState(20)
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetchPosts({ platform: platform || undefined, page, size: pageSize })
      .then((data) => {
        setRows(data.content.map((r) => ({ id: r.postId, ...r })))
        setTotal(data.totalElements)
      })
      .catch(() => setError('데이터를 불러오지 못했습니다.'))
      .finally(() => setLoading(false))
  }, [platform, page, pageSize])

  const handlePlatformChange = (e: SelectChangeEvent<Platform>) => {
    setPlatform(e.target.value as Platform)
    setPage(0)
  }

  const handlePaginationChange = (model: GridPaginationModel) => {
    setPage(model.page)
    setPageSize(model.pageSize)
  }

  return (
    <Box>
      <Typography variant="h5" mb={2}>게시물 목록</Typography>

      <FormControl size="small" sx={{ mb: 2, minWidth: 160 }}>
        <InputLabel>Platform</InputLabel>
        <Select<Platform> value={platform} label="Platform" onChange={handlePlatformChange}>
          {PLATFORMS.map((p) => (
            <MenuItem key={p} value={p}>{p || 'ALL'}</MenuItem>
          ))}
        </Select>
      </FormControl>

      {error && <Typography color="error" mb={1}>{error}</Typography>}

      <DataGrid
        rows={rows}
        columns={columns}
        rowCount={total}
        loading={loading}
        paginationMode="server"
        paginationModel={{ page, pageSize }}
        onPaginationModelChange={handlePaginationChange}
        pageSizeOptions={[10, 20, 50]}
        autoHeight
        disableRowSelectionOnClick
      />
    </Box>
  )
}
