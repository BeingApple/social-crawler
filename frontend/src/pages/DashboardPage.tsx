import { useEffect, useState } from 'react'
import { Typography, Paper, Grid, TextField, FormControl, InputLabel, Select, MenuItem } from '@mui/material'
import type { SelectChangeEvent } from '@mui/material'
import DataTable from '../components/dashboard/DataTable'
import { fetchAssignees } from '../api/assignees'
import type { BrandAssignee, AssigneeFilters } from '../types/brand'
import { PLATFORM_OPTIONS } from '../constants/platform'

const INITIAL_FILTERS: AssigneeFilters = {
  assigneeName: '',
  brandName: '',
  platformId: '',
  accountId: '',
  accountType: '',
  active: 'ALL',
}

const ACCOUNT_TYPE_OPTIONS = ['KR', 'HQ']

export default function DashboardPage() {
  const [assignees, setAssignees] = useState<BrandAssignee[]>([])
  const [filters, setFilters]     = useState<AssigneeFilters>(INITIAL_FILTERS)
  const [error, setError]         = useState<string | null>(null)

  useEffect(() => {
    fetchAssignees()
      .then(setAssignees)
      .catch(() => setError('계정 목록을 불러오지 못했습니다.'))
  }, [])

  const handleText =
    (field: keyof AssigneeFilters) => (e: React.ChangeEvent<HTMLInputElement>) =>
      setFilters((prev) => ({ ...prev, [field]: e.target.value }))

  const handleSelect =
    (field: keyof AssigneeFilters) => (e: SelectChangeEvent<string>) =>
      setFilters((prev) => ({ ...prev, [field]: e.target.value }))

  return (
    <>
      <Typography variant="h5" fontWeight={700} mb={3}>
        계정 리스트
      </Typography>

      {error && <Typography color="error" mb={2}>{error}</Typography>}

      {/* 필터 영역 */}
      <Paper elevation={1} sx={{ p: 2.5, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, sm: 4 }}>
            <TextField size="small" fullWidth label="담당자명" value={filters.assigneeName} onChange={handleText('assigneeName')} />
          </Grid>
          <Grid size={{ xs: 12, sm: 4 }}>
            <TextField size="small" fullWidth label="브랜드명" value={filters.brandName} onChange={handleText('brandName')} />
          </Grid>
          <Grid size={{ xs: 12, sm: 4 }}>
            <FormControl size="small" fullWidth>
              <InputLabel>소셜 미디어</InputLabel>
              <Select value={filters.platformId} label="소셜 미디어" onChange={handleSelect('platformId')}>
                <MenuItem value="">전체</MenuItem>
                {PLATFORM_OPTIONS.map(({ value, label }) => (
                  <MenuItem key={value} value={value}>{label}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid size={{ xs: 12, sm: 4 }}>
            <TextField size="small" fullWidth label="계정 아이디" value={filters.accountId} onChange={handleText('accountId')} />
          </Grid>
          <Grid size={{ xs: 12, sm: 4 }}>
            <FormControl size="small" fullWidth>
              <InputLabel>계정 구분</InputLabel>
              <Select value={filters.accountType} label="계정 구분" onChange={handleSelect('accountType')}>
                <MenuItem value="">전체</MenuItem>
                {ACCOUNT_TYPE_OPTIONS.map((v) => <MenuItem key={v} value={v}>{v}</MenuItem>)}
              </Select>
            </FormControl>
          </Grid>
          <Grid size={{ xs: 12, sm: 4 }}>
            <FormControl size="small" fullWidth>
              <InputLabel>활성화 상태</InputLabel>
              <Select value={filters.active} label="활성화 상태" onChange={handleSelect('active')}>
                <MenuItem value="ALL">전체</MenuItem>
                <MenuItem value="ON">ON</MenuItem>
                <MenuItem value="OFF">OFF</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* 테이블 */}
      <DataTable assignees={assignees} filters={filters} />
    </>
  )
}