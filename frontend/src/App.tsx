import { Routes, Route, NavLink, Navigate, useLocation } from 'react-router-dom'
import { Box, Typography, List, ListItemButton, ListItemText, Divider } from '@mui/material'
import DashboardPage from './pages/DashboardPage'
import CrawlingStatusPage from './pages/CrawlingStatusPage'
import CrawlAccountPage from './pages/CrawlAccountPage'

const LNB_WIDTH = 220

const NAV_GROUPS = [
  {
    group: '공식 계정 관리',
    items: [
      { label: '계정 리스트', path: '/accounts' },
      { label: '크롤링 현황', path: '/crawling' },
    ],
  },
  {
    group: '설정',
    items: [
      { label: '크롤 계정 관리', path: '/crawl-accounts' },
    ],
  },
]

function Lnb() {
  const location = useLocation()

  return (
    <Box
      component="nav"
      sx={{
        width: LNB_WIDTH,
        flexShrink: 0,
        bgcolor: '#1a1a2e',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        pt: 2,
      }}
    >
      <Box sx={{ px: 3, pb: 2 }}>
        <Typography
          variant="subtitle2"
          sx={{ color: '#8888aa', fontWeight: 600, letterSpacing: 1, fontSize: 11 }}
        >
          MUSINSA
        </Typography>
      </Box>

      <Divider sx={{ borderColor: '#2a2a4a' }} />

      {NAV_GROUPS.map(({ group, items }, gi) => (
        <Box key={gi}>
          {group && (
            <Typography
              sx={{
                px: 2,
                pt: 2.5,
                pb: 0.5,
                fontSize: 11,
                fontWeight: 600,
                letterSpacing: 0.8,
                color: '#6666aa',
                textTransform: 'uppercase',
              }}
            >
              {group}
            </Typography>
          )}

          <List dense sx={{ px: 1, mt: group ? 0 : 1 }}>
            {items.map(({ label, path }) => {
              const isActive =
                path === '/'
                  ? location.pathname === '/'
                  : location.pathname.startsWith(path)

              return (
                <ListItemButton
                  key={path}
                  component={NavLink}
                  to={path}
                  selected={isActive}
                  sx={{
                    borderRadius: 1.5,
                    mb: 0.5,
                    pl: group ? 3 : 2,
                    color: isActive ? '#fff' : '#9999bb',
                    '&.Mui-selected': {
                      bgcolor: '#2e2e5e',
                      color: '#fff',
                      '&:hover': { bgcolor: '#3a3a6e' },
                    },
                    '&:hover': { bgcolor: '#22224a', color: '#fff' },
                  }}
                >
                  <ListItemText
                    primary={label}
                    slotProps={{ primary: { fontSize: 13, fontWeight: isActive ? 600 : 400 } }}
                  />
                </ListItemButton>
              )
            })}
          </List>
        </Box>
      ))}
    </Box>
  )
}

function TitleHeader() {
  return (
    <Box
      component="header"
      sx={{
        height: 56,
        display: 'flex',
        alignItems: 'center',
        px: 3,
        bgcolor: '#fff',
        borderBottom: '1px solid #e8e8f0',
        flexShrink: 0,
      }}
    >
      <Typography variant="h6" fontWeight={700} sx={{ color: '#1a1a2e', letterSpacing: -0.3 }}>
        크롤링
      </Typography>
    </Box>
  )
}

export default function App() {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#f4f4f8' }}>
      <Lnb />

      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <TitleHeader />

        <Box component="main" sx={{ flex: 1, p: 3, overflow: 'auto' }}>
          <Routes>
            <Route path="/" element={<Navigate to="/accounts" replace />} />
            <Route path="/accounts" element={<DashboardPage />} />
            <Route path="/crawling" element={<CrawlingStatusPage />} />
            <Route path="/crawl-accounts" element={<CrawlAccountPage />} />
          </Routes>
        </Box>
      </Box>
    </Box>
  )
}