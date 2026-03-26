import { Box, Card, CardContent } from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import type { BrandAccount, AccountFilters } from '../../types/brand'

interface Props {
  accounts: BrandAccount[]
  filters: AccountFilters
}

const STATUS_CHIP_COLOR: Record<string, string> = { ON: '#2e7d32', OFF: '#d32f2f' }

const columns: GridColDef[] = [
  { field: 'accountId',   headerName: '계정 아이디',  width: 160 },
  { field: 'brandName',   headerName: '브랜드명',      width: 120 },
  { field: 'socialMedia', headerName: '소셜 미디어',   width: 130 },
  { field: 'accountType', headerName: '계정 구분',     width: 100 },
  { field: 'managerName', headerName: '담당자명',      width: 110 },
  {
    field: 'status',
    headerName: '활성화 상태',
    width: 110,
    renderCell: ({ value }) => (
      <Box
        component="span"
        sx={{
          px: 1.5, py: 0.4, borderRadius: 2, fontSize: 12, fontWeight: 700,
          color: '#fff', bgcolor: STATUS_CHIP_COLOR[value as string] ?? '#757575',
        }}
      >
        {value}
      </Box>
    ),
  },
]

export default function DataTable({ accounts, filters }: Props) {
  const rows = accounts
    .filter((a) => {
      if (filters.managerName && !a.managerName.toLowerCase().includes(filters.managerName.toLowerCase())) return false
      if (filters.brandName && !a.brandName.toLowerCase().includes(filters.brandName.toLowerCase())) return false
      if (filters.socialMedia && a.socialMedia !== filters.socialMedia) return false
      if (filters.accountId && !a.accountId.toLowerCase().includes(filters.accountId.toLowerCase())) return false
      if (filters.accountType && a.accountType !== filters.accountType) return false
      if (filters.status !== 'ALL' && a.status !== filters.status) return false
      return true
    })
    .map((a, i) => ({ id: i, ...a }))

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
