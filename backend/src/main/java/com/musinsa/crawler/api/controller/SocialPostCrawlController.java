package com.musinsa.crawler.api.controller;

import com.musinsa.crawler.api.dto.SocialPostCrawlResponse;
import com.musinsa.crawler.domain.repository.SocialPostCrawlRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/posts")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")   // 개발용. 운영 시 도메인 명시
public class SocialPostCrawlController {

    private final SocialPostCrawlRepository postRepository;

    /** 게시물 목록 (페이징 + 다중 필터) */
    @GetMapping
    public ResponseEntity<Page<SocialPostCrawlResponse>> list(
            @RequestParam(required = false) String platformId,
            @RequestParam(required = false) String brandName,
            @RequestParam(required = false) String crawlCase,
            @RequestParam(required = false) String accountType,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate postedFrom,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate postedTo,
            @PageableDefault(size = 20) Pageable pageable
    ) {
        LocalDateTime fromDt = postedFrom != null ? postedFrom.atStartOfDay()           : null;
        LocalDateTime toDt   = postedTo   != null ? postedTo.plusDays(1).atStartOfDay() : null;

        Page<SocialPostCrawlResponse> page = postRepository
                .findWithFilters(platformId, brandName, crawlCase, accountType, fromDt, toDt, pageable)
                .map(SocialPostCrawlResponse::from);

        return ResponseEntity.ok(page);
    }

    /** 게시물 단건 조회 */
    @GetMapping("/{spcId}")
    public ResponseEntity<SocialPostCrawlResponse> get(@PathVariable Long spcId) {
        return postRepository.findById(spcId)
                .map(SocialPostCrawlResponse::from)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}