import { Box, Card, CardContent } from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import type { BrandAssignee, AssigneeFilters } from '../../types/brand'
import { PLATFORM_LABELS } from '../../constants/platform'

interface Props {
  assignees: BrandAssignee[]
  filters: AssigneeFilters
}

const STATUS_CHIP_COLOR: Record<string, string> = { ON: '#2e7d32', OFF: '#d32f2f' }

const columns: GridColDef[] = [
  { field: 'accountId',    headerName: '계정 아이디',  width: 160 },
  { field: 'brandName',    headerName: '브랜드명',      width: 120 },
  {
    field: 'platformId',
    headerName: '소셜 미디어',
    width: 130,
    valueFormatter: (value: string) => PLATFORM_LABELS[value] ?? value,
  },
  { field: 'region',       headerName: '지역 구분',     width: 90  },
  { field: 'assigneeName', headerName: '담당자명',      width: 110 },
  {
    field: 'active',
    headerName: '활성화 상태',
    width: 110,
    renderCell: ({ value }) => {
      const label = value ? 'ON' : 'OFF'
      return (
        <Box
          component="span"
          sx={{
            px: 1.5, py: 0.4, borderRadius: 2, fontSize: 12, fontWeight: 700,
            color: '#fff', bgcolor: STATUS_CHIP_COLOR[label] ?? '#757575',
          }}
        >
          {label}
        </Box>
      )
    },
  },
]

export default function DataTable({ assignees, filters }: Props) {
  const rows = assignees
    .filter((a) => {
      if (filters.assigneeName && !a.assigneeName.toLowerCase().includes(filters.assigneeName.toLowerCase())) return false
      if (filters.brandName && !(a.brandName ?? '').toLowerCase().includes(filters.brandName.toLowerCase())) return false
      if (filters.platformId && a.platformId !== filters.platformId) return false
      if (filters.accountId && !a.accountId.toLowerCase().includes(filters.accountId.toLowerCase())) return false
      if (filters.region && a.region !== filters.region) return false
      if (filters.active !== 'ALL') {
        const isActive = filters.active === 'ON'
        if (a.active !== isActive) return false
      }
      return true
    })
    .map((a) => ({ id: a.assigneeId, ...a }))

  return (
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
  )
}