package com.musinsa.crawler.api.controller;

import com.musinsa.crawler.api.dto.SocialPostCrawlResponse;
import com.musinsa.crawler.service.SocialPostCrawlService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;

@RestController
@RequestMapping("/api/posts")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")   // 개발용. 운영 시 도메인 명시
public class SocialPostCrawlController {

    private final SocialPostCrawlService postService;

    /** 게시물 목록 (페이징 + 다중 필터) */
    @GetMapping
    public ResponseEntity<Page<SocialPostCrawlResponse>> list(
            @RequestParam(required = false) String platformId,
            @RequestParam(required = false) String brandName,
            @RequestParam(required = false) String crawlCase,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate postedFrom,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate postedTo,
            @PageableDefault(size = 20) Pageable pageable
    ) {
        return ResponseEntity.ok(
                postService.findPosts(platformId, brandName, crawlCase, postedFrom, postedTo, pageable)
        );
    }

    /** 게시물 단건 조회 */
    @GetMapping("/{spcId}")
    public ResponseEntity<SocialPostCrawlResponse> get(@PathVariable Long spcId) {
        return postService.findPost(spcId)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}