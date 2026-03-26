package com.musinsa.crawler.api.controller;

import com.musinsa.crawler.api.dto.PostResponse;
import com.musinsa.crawler.domain.repository.PostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/posts")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")   // 개발용. 운영 시 도메인 명시
public class PostController {

    private final PostRepository postRepository;

    /** 전체 게시물 목록 (페이징) */
    @GetMapping
    public ResponseEntity<Page<PostResponse>> list(
            @RequestParam(required = false) String platform,
            @PageableDefault(size = 20, sort = "crawledAt", direction = Sort.Direction.DESC) Pageable pageable
    ) {
        Page<PostResponse> page = (platform != null)
                ? postRepository.findByPlatform(platform, pageable).map(PostResponse::from)
                : postRepository.findAll(pageable).map(PostResponse::from);

        return ResponseEntity.ok(page);
    }

    /** 게시물 단건 조회 */
    @GetMapping("/{postId}")
    public ResponseEntity<PostResponse> get(@PathVariable Long postId) {
        return postRepository.findById(postId)
                .map(PostResponse::from)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
