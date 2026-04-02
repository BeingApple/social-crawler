import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box, Typography, Paper, Chip, Button, Link,
  Divider, CircularProgress,
} from '@mui/material'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import OpenInNewIcon from '@mui/icons-material/OpenInNew'
import { fetchPost } from '../api/posts'
import type { SocialPostCrawl } from '../types/post'
import { usePlatforms } from '../hooks/usePlatforms'

function StatCard({ label, value }: { label: string; value: number | null | undefined }) {
  return (
    <Paper elevation={1} sx={{ p: 2, textAlign: 'center', minWidth: 110 }}>
      <Typography variant="h6" fontWeight={700}>
        {value != null ? value.toLocaleString() : '-'}
      </Typography>
      <Typography variant="caption" color="text.secondary">{label}</Typography>
    </Paper>
  )
}

function MediaViewer({ post }: { post: SocialPostCrawl }) {
  const isVideo =
    ['reel', 'video', 'clip'].some((t) => post.postType?.toLowerCase().includes(t)) ||
    (post.mediaUrl ? /\.(mp4|mov|webm|m4v)(\?|$)/i.test(post.mediaUrl) : false)

  if (post.mediaUrl && isVideo) {
    return (
      <Box sx={{ borderRadius: 2, overflow: 'hidden', bgcolor: '#000', width: '100%' }}>
        <video
          controls
          poster={post.thumbnailUrl ?? undefined}
          style={{ width: '100%', maxHeight: 480, display: 'block' }}
        >
          <source src={post.mediaUrl} />
        </video>
      </Box>
    )
  }

  const displayUrl = post.mediaUrl ?? post.thumbnailUrl

  if (displayUrl) {
    return (
      <Box
        component="img"
        src={displayUrl}
        alt="media"
        sx={{ width: '100%', maxHeight: 480, objectFit: 'cover', borderRadius: 2, display: 'block' }}
      />
    )
  }

  return (
    <Box
      sx={{
        width: '100%', height: 280,
        bgcolor: '#e8e8f0', borderRadius: 2,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}
    >
      <Typography color="text.secondary" variant="body2">미디어 없음</Typography>
    </Box>
  )
}

function InfoRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <Box sx={{ display: 'flex', gap: 2, py: 0.75, alignItems: 'flex-start' }}>
      <Typography variant="body2" color="text.secondary" sx={{ minWidth: 90, flexShrink: 0 }}>
        {label}
      </Typography>
      <Box sx={{ flex: 1, wordBreak: 'break-word' }}>
        {typeof value === 'string' || value == null
          ? <Typography variant="body2">{value ?? '-'}</Typography>
          : value}
      </Box>
    </Box>
  )
}

export default function PostDetailPage() {
  const { spcId } = useParams<{ spcId: string }>()
  const navigate = useNavigate()
  const [post, setPost] = useState<SocialPostCrawl | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const { platformLabels } = usePlatforms()

  useEffect(() => {
    if (!spcId) return
    setLoading(true)
    fetchPost(Number(spcId))
      .then(setPost)
      .catch(() => setError('게시글 데이터를 불러오지 못했습니다.'))
      .finally(() => setLoading(false))
  }, [spcId])

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', pt: 8 }}>
        <CircularProgress />
      </Box>
    )
  }

  if (error || !post) {
    return (
      <Box sx={{ pt: 4 }}>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/crawling')} sx={{ mb: 2 }}>
          뒤로가기
        </Button>
        <Typography color="error">{error ?? '게시글을 찾을 수 없습니다.'}</Typography>
      </Box>
    )
  }

  const hashtags: string[] = (() => {
    try { return post.hashtags ? JSON.parse(post.hashtags) : [] } catch { return [] }
  })()

  const personTags: string[] = (() => {
    try { return post.personTags ? JSON.parse(post.personTags) : [] } catch { return [] }
  })()

  return (
    <>
      {/* 헤더 */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3, flexWrap: 'wrap' }}>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate(-1)} size="small">
          뒤로가기
        </Button>
        <Typography variant="h5" fontWeight={700}>게시글 상세</Typography>
        <Typography variant="body2" color="text.secondary">#{post.spcId}</Typography>
        {post.duplicate && <Chip label="중복" size="small" color="warning" />}
        {post.junk && <Chip label="정크" size="small" color="error" />}
      </Box>

      {/* 본문 */}
      <Box sx={{ display: 'flex', gap: 3, alignItems: 'flex-start', flexWrap: 'wrap' }}>

        {/* 미디어 */}
        <Box sx={{ flexShrink: 0, width: 320 }}>
          <MediaViewer post={post} />
          {post.postUrl && (
            <Button
              component={Link}
              href={post.postUrl}
              target="_blank"
              rel="noopener"
              variant="outlined"
              size="small"
              endIcon={<OpenInNewIcon />}
              sx={{ mt: 1.5, width: '100%' }}
            >
              원본 게시글 보기
            </Button>
          )}
        </Box>

        {/* 정보 패널 */}
        <Paper elevation={1} sx={{ flex: 1, minWidth: 300, p: 3 }}>

          <Typography variant="subtitle2" fontWeight={700} mb={1.5}>기본 정보</Typography>
          <InfoRow label="플랫폼" value={
            <Chip label={platformLabels[post.platformId] ?? post.platformId} size="small" />
          } />
          <InfoRow label="브랜드" value={post.brandName} />
          <InfoRow label="계정" value={post.accountId} />
          <InfoRow label="수집 유형" value={post.crawlCase} />
          <InfoRow label="게시 유형" value={post.postType} />
          <InfoRow
            label="업로드 일시"
            value={post.postedAt ? new Date(post.postedAt).toLocaleString('ko-KR') : '-'}
          />
          <InfoRow
            label="수집 일시"
            value={post.createdAt ? new Date(post.createdAt).toLocaleString('ko-KR') : '-'}
          />

          <Divider sx={{ my: 2 }} />

          <Typography variant="subtitle2" fontWeight={700} mb={1.5}>작성자</Typography>
          <InfoRow label="이름" value={post.authorName} />
          <InfoRow
            label="팔로워"
            value={post.authorFollowers != null ? post.authorFollowers.toLocaleString() : null}
          />

          <Divider sx={{ my: 2 }} />

          <Typography variant="subtitle2" fontWeight={700} mb={1.5}>게시글</Typography>
          {post.postTitle && <InfoRow label="제목" value={post.postTitle} />}

          {post.textContent ? (
            <Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>본문</Typography>
              <Typography
                variant="body2"
                sx={{
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                  bgcolor: '#f8f8fc',
                  borderRadius: 1,
                  p: 1.5,
                  maxHeight: 220,
                  overflowY: 'auto',
                  fontSize: 13,
                  lineHeight: 1.7,
                }}
              >
                {post.textContent}
              </Typography>
            </Box>
          ) : (
            <InfoRow label="본문" value="-" />
          )}

          {hashtags.length > 0 && (
            <Box sx={{ mt: 1.5 }}>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 0.75 }}>해시태그</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.75 }}>
                {hashtags.map((tag) => (
                  <Chip key={tag} label={tag} size="small" variant="outlined" color="primary" />
                ))}
              </Box>
            </Box>
          )}

          {personTags.length > 0 && (
            <Box sx={{ mt: 1.5 }}>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 0.75 }}>인물태그</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.75 }}>
                {personTags.map((tag) => (
                  <Chip key={tag} label={tag} size="small" variant="outlined" />
                ))}
              </Box>
            </Box>
          )}

        </Paper>
      </Box>

      {/* 지표 */}
      <Box sx={{ display: 'flex', gap: 2, mt: 3, flexWrap: 'wrap' }}>
        <StatCard label="좋아요" value={post.likeCount} />
        <StatCard label="댓글" value={post.commentCount} />
        <StatCard label="조회수" value={post.viewCount} />
        <StatCard label="공유" value={post.shareCount} />
        <StatCard label="팔로워" value={post.authorFollowers} />
      </Box>
    </>
  )
}
