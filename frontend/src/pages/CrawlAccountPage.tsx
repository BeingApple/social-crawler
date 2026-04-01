import { useEffect, useState } from 'react'
import {
  Typography, Paper, Card, CardContent, Button, Chip,
  Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, FormControl, InputLabel, Select, MenuItem,
  IconButton, Tooltip, Box,
} from '@mui/material'
import type { SelectChangeEvent } from '@mui/material'
import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import { DataGrid, GridColDef, GridRowSelectionModel } from '@mui/x-data-grid'
import {
  fetchAll, fetchDecrypt, create, update, remove,
} from '../api/crawlAccounts'
import type {
  SocialCrawlAccount,
  SocialCrawlAccountCredential,
  SocialCrawlAccountRequest,
  AccountStatus,
} from '../types/crawlAccount'
import { usePlatforms } from '../hooks/usePlatforms'
import type { SocialPlatform } from '../api/platforms'

// ─── 상수 ───────────────────────────────────────────────────────────────────

const STATUS_OPTIONS: AccountStatus[] = ['ACTIVE', 'BLOCKED', 'EXPIRED', 'PAUSED']

const STATUS_CHIP_COLOR: Record<AccountStatus, 'success' | 'error' | 'warning' | 'default'> = {
  ACTIVE:  'success',
  BLOCKED: 'error',
  EXPIRED: 'warning',
  PAUSED:  'default',
}

const EMPTY_FORM: SocialCrawlAccountRequest = {
  name:       '',
  platformId: '',
  loginId:    '',
  loginPw:    '',
  issue:      '',
  status:     'ACTIVE',
}

// ─── 타입 ────────────────────────────────────────────────────────────────────

type Row = SocialCrawlAccount & { id: number }

// ─── 컬럼 정의 ───────────────────────────────────────────────────────────────

const columns: GridColDef<Row>[] = [
  { field: 'accountId',  headerName: 'ID',       width: 70,  type: 'number' },
  { field: 'name',       headerName: '계정명',    width: 160 },
  { field: 'platformId', headerName: '플랫폼',    width: 110 },
  { field: 'loginId',    headerName: '로그인 ID', width: 180 },
  {
    field: 'status',
    headerName: '상태',
    width: 100,
    renderCell: ({ value }) => {
      const status = value as AccountStatus
      return <Chip label={status} color={STATUS_CHIP_COLOR[status]} size="small" />
    },
  },
  { field: 'issue',     headerName: '이슈',       width: 200, valueFormatter: (v: string | null) => v ?? '-' },
  {
    field: 'updatedAt',
    headerName: '수정일시',
    width: 160,
    valueFormatter: (v: string) => v ? new Date(v).toLocaleString('ko-KR') : '-',
  },
]

// ─── 폼 다이얼로그 ───────────────────────────────────────────────────────────

interface FormDialogProps {
  open:       boolean
  editTarget: SocialCrawlAccount | null
  platforms:  SocialPlatform[]
  onClose:    () => void
  onSaved:    () => void
}

function FormDialog({ open, editTarget, platforms, onClose, onSaved }: FormDialogProps) {
  const [form, setForm]     = useState<SocialCrawlAccountRequest>(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [error, setError]   = useState<string | null>(null)

  useEffect(() => {
    if (open) {
      setForm(
        editTarget
          ? { name: editTarget.name, platformId: editTarget.platformId, loginId: editTarget.loginId, loginPw: '', issue: editTarget.issue ?? '', status: editTarget.status }
          : EMPTY_FORM
      )
      setError(null)
    }
  }, [open, editTarget])

  const handleText = (field: keyof SocialCrawlAccountRequest) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
      setForm((prev) => ({ ...prev, [field]: e.target.value }))

  const handleSelect = (field: keyof SocialCrawlAccountRequest) =>
    (e: SelectChangeEvent<string>) =>
      setForm((prev) => ({ ...prev, [field]: e.target.value }))

  const handleSubmit = async () => {
    setSaving(true)
    setError(null)
    try {
      if (editTarget) {
        await update(editTarget.accountId, form)
      } else {
        await create(form)
      }
      onSaved()
      onClose()
    } catch {
      setError('저장에 실패했습니다.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{editTarget ? '계정 수정' : '계정 추가'}</DialogTitle>
      <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
        {error && <Typography color="error" variant="body2">{error}</Typography>}

        <TextField
          label="계정명" size="small" fullWidth required
          value={form.name} onChange={handleText('name')}
        />

        <FormControl size="small" fullWidth required>
          <InputLabel>플랫폼</InputLabel>
          <Select value={form.platformId} label="플랫폼" onChange={handleSelect('platformId')}>
            {platforms.map((p) => (
              <MenuItem key={p.platformId} value={p.platformId}>{p.platformName}</MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          label="로그인 ID" size="small" fullWidth required
          value={form.loginId} onChange={handleText('loginId')}
        />

        <TextField
          label="로그인 PW" size="small" fullWidth required type="password"
          value={form.loginPw} onChange={handleText('loginPw')}
        />

        <FormControl size="small" fullWidth required>
          <InputLabel>상태</InputLabel>
          <Select value={form.status} label="상태" onChange={handleSelect('status')}>
            {STATUS_OPTIONS.map((s) => (
              <MenuItem key={s} value={s}>{s}</MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          label="이슈 (선택)" size="small" fullWidth multiline minRows={2}
          value={form.issue ?? ''} onChange={handleText('issue')}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={saving}>취소</Button>
        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? '저장 중…' : '저장'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}

// ─── 비밀번호 확인 다이얼로그 ────────────────────────────────────────────────

interface DecryptDialogProps {
  open:      boolean
  credential: SocialCrawlAccountCredential | null
  onClose:   () => void
}

function DecryptDialog({ open, credential, onClose }: DecryptDialogProps) {
  const copy = (text: string) => navigator.clipboard.writeText(text)

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="xs">
      <DialogTitle>비밀번호 확인</DialogTitle>
      <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
        {credential ? (
          <>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <TextField
                label="로그인 ID" size="small" fullWidth
                value={credential.loginId} slotProps={{ input: { readOnly: true } }}
              />
              <Tooltip title="복사">
                <IconButton onClick={() => copy(credential.loginId)} size="small">
                  <ContentCopyIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <TextField
                label="로그인 PW" size="small" fullWidth
                value={credential.loginPw} slotProps={{ input: { readOnly: true } }}
              />
              <Tooltip title="복사">
                <IconButton onClick={() => copy(credential.loginPw)} size="small">
                  <ContentCopyIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </Box>
          </>
        ) : (
          <Typography variant="body2" color="text.secondary">불러오는 중…</Typography>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>닫기</Button>
      </DialogActions>
    </Dialog>
  )
}

// ─── 메인 페이지 ─────────────────────────────────────────────────────────────

export default function CrawlAccountPage() {
  const [rows, setRows]               = useState<Row[]>([])
  const [loading, setLoading]         = useState(false)
  const [error, setError]             = useState<string | null>(null)
  const [selection, setSelection]     = useState<GridRowSelectionModel>([])
  const { platforms }                 = usePlatforms()

  const [formOpen, setFormOpen]       = useState(false)
  const [editTarget, setEditTarget]   = useState<SocialCrawlAccount | null>(null)

  const [decryptOpen, setDecryptOpen]     = useState(false)
  const [credential, setCredential]       = useState<SocialCrawlAccountCredential | null>(null)

  const load = () => {
    setLoading(true)
    setError(null)
    fetchAll()
      .then((data) => setRows(data.map((a) => ({ id: a.accountId, ...a }))))
      .catch(() => setError('목록을 불러오지 못했습니다.'))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const selectedId = selection.length === 1 ? (selection[0] as number) : null
  const selectedRow = selectedId != null ? rows.find((r) => r.id === selectedId) ?? null : null

  const handleAdd = () => {
    setEditTarget(null)
    setFormOpen(true)
  }

  const handleEdit = () => {
    if (!selectedRow) return
    setEditTarget(selectedRow)
    setFormOpen(true)
  }

  const handleDecrypt = async () => {
    if (!selectedId) return
    setCredential(null)
    setDecryptOpen(true)
    try {
      const cred = await fetchDecrypt(selectedId)
      setCredential(cred)
    } catch {
      setCredential(null)
    }
  }

  const handleDelete = async () => {
    if (!selectedId) return
    if (!window.confirm('선택한 계정을 삭제하시겠습니까?')) return
    try {
      await remove(selectedId)
      setSelection([])
      load()
    } catch {
      setError('삭제에 실패했습니다.')
    }
  }

  return (
    <>
      <Typography variant="h5" fontWeight={700} mb={3}>
        크롤 계정 관리
      </Typography>

      {error && <Typography color="error" mb={1}>{error}</Typography>}

      {/* 액션 버튼 */}
      <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
        <Button variant="contained" size="small" onClick={handleAdd}>
          추가
        </Button>
        <Button variant="outlined" size="small" onClick={handleEdit} disabled={!selectedRow}>
          수정
        </Button>
        <Button variant="outlined" size="small" onClick={handleDecrypt} disabled={!selectedId}>
          비밀번호 확인
        </Button>
        <Button variant="outlined" size="small" color="error" onClick={handleDelete} disabled={!selectedId}>
          삭제
        </Button>
      </Box>

      {/* 테이블 */}
      <Card elevation={2}>
        <CardContent>
          <DataGrid
            rows={rows}
            columns={columns}
            loading={loading}
            autoHeight
            checkboxSelection
            disableMultipleRowSelection
            rowSelectionModel={selection}
            onRowSelectionModelChange={setSelection}
            pageSizeOptions={[10, 20, 50]}
            initialState={{ pagination: { paginationModel: { pageSize: 20 } } }}
          />
        </CardContent>
      </Card>

      {/* 생성/수정 폼 */}
      <FormDialog
        open={formOpen}
        editTarget={editTarget}
        platforms={platforms}
        onClose={() => setFormOpen(false)}
        onSaved={load}
      />

      {/* 비밀번호 확인 */}
      <DecryptDialog
        open={decryptOpen}
        credential={credential}
        onClose={() => setDecryptOpen(false)}
      />
    </>
  )
}
