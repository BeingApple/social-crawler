import { Routes, Route, Link } from 'react-router-dom'
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material'
import PostListPage from './pages/PostListPage'

export default function App() {
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Brand Social Crawler — Admin
          </Typography>
          <Button color="inherit" component={Link} to="/">Posts</Button>
        </Toolbar>
      </AppBar>

      <Box sx={{ p: 3 }}>
        <Routes>
          <Route path="/" element={<PostListPage />} />
        </Routes>
      </Box>
    </>
  )
}
