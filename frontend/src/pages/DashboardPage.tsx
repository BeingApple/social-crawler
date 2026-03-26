import { useState } from 'react'
import { Typography, Paper, Grid, TextField, FormControl, InputLabel, Select, MenuItem } from '@mui/material'
import type { SelectChangeEvent } from '@mui/material'
import DataTable from '../components/dashboard/DataTable'
import { SAMPLE_ACCOUNTS } from '../data/sampleData'
import type { AccountFilters } from '../types/brand'

const INITIAL_FILTERS: AccountFilters = {
  managerName: '',
  brandName: '',
  socialMedia: '',
  accountId: '',
  accountType: '',
  status: 'ALL',
}

const SOCIAL_MEDIA_OPTIONS = ['인스타그램', '유튜브', '틱톡', '페이스북']
const ACCOUNT_TYPE_OPTIONS = ['KR', 'HQ']

export default function DashboardPage() {
  const accounts = SAMPLE_ACCOUNTS
  const [filters, setFilters] = useState<AccountFilters>(INITIAL_FILTERS)

  const handleText =
    (field: keyof AccountFilters) => (e: React.ChangeEvent<HTMLInputElement>) =>
      setFilters((prev) => ({ ...prev, [field]: e.target.value }))

  const handleSelect =
    (field: keyof AccountFilters) => (e: SelectChangeEvent<string>) =>
      setFilters((prev) => ({ ...prev, [field]: e.target.value }))

  return (
    <>
      <Typography variant="h5" fontWeight={700} mb={3}>
        계정 리스트
      </Typography>

      {/* 필터 영역 */}
      <Paper elevation={1} sx={{ p: 2.5, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <TextField size="small" fullWidth label="담당자명" value={filters.managerName} onChange={handleText('managerName')} />
          </Grid>
          <Grid item xs={12} sm={4}>
            <TextField size="small" fullWidth label="브랜드명" value={filters.brandName} onChange={handleText('brandName')} />
          </Grid>
          <Grid item xs={12} sm={4}>
            <FormControl size="small" fullWidth>
              <InputLabel>소셜 미디어</InputLabel>
              <Select value={filters.socialMedia} label="소셜 미디어" onChange={handleSelect('socialMedia')}>
                <MenuItem value="">전체</MenuItem>
                {SOCIAL_MEDIA_OPTIONS.map((v) => <MenuItem key={v} value={v}>{v}</MenuItem>)}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4}>
            <TextField size="small" fullWidth label="계정 아이디" value={filters.accountId} onChange={handleText('accountId')} />
          </Grid>
          <Grid item xs={12} sm={4}>
            <FormControl size="small" fullWidth>
              <InputLabel>계정 구분</InputLabel>
              <Select value={filters.accountType} label="계정 구분" onChange={handleSelect('accountType')}>
                <MenuItem value="">전체</MenuItem>
                {ACCOUNT_TYPE_OPTIONS.map((v) => <MenuItem key={v} value={v}>{v}</MenuItem>)}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4}>
            <FormControl size="small" fullWidth>
              <InputLabel>활성화 상태</InputLabel>
              <Select value={filters.status} label="활성화 상태" onChange={handleSelect('status')}>
                <MenuItem value="ALL">전체</MenuItem>
                <MenuItem value="ON">ON</MenuItem>
                <MenuItem value="OFF">OFF</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* 테이블 */}
      <DataTable accounts={accounts} filters={filters} />
    </>
  )
}
