package com.crawler.api.controller;

import com.crawler.api.dto.SocialCrawlAccountCredentialResponse;
import com.crawler.api.dto.SocialCrawlAccountRequest;
import com.crawler.api.dto.SocialCrawlAccountResponse;
import com.crawler.service.SocialCrawlAccountService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.NoSuchElementException;

@RestController
@RequestMapping("/api/crawl-accounts")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")   // 개발용. 운영 시 도메인 명시
public class SocialCrawlAccountController {

    private final SocialCrawlAccountService service;

    /** 전체 목록 (loginId 복호화, loginPw 미포함) */
    @GetMapping
    public ResponseEntity<List<SocialCrawlAccountResponse>> list() {
        return ResponseEntity.ok(service.findAll());
    }

    /** 단건 조회 (loginId 복호화, loginPw 미포함) */
    @GetMapping("/{id}")
    public ResponseEntity<SocialCrawlAccountResponse> get(@PathVariable Long id) {
        try {
            return ResponseEntity.ok(service.findById(id));
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    /** loginId + loginPw 원문 복호화 반환 */
    @GetMapping("/{id}/decrypt")
    public ResponseEntity<SocialCrawlAccountCredentialResponse> decrypt(@PathVariable Long id) {
        try {
            return ResponseEntity.ok(service.decrypt(id));
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    /** 생성 */
    @PostMapping
    public ResponseEntity<SocialCrawlAccountResponse> create(
            @Valid @RequestBody SocialCrawlAccountRequest req) {
        return ResponseEntity.status(201).body(service.create(req));
    }

    /** 수정 */
    @PutMapping("/{id}")
    public ResponseEntity<SocialCrawlAccountResponse> update(
            @PathVariable Long id,
            @Valid @RequestBody SocialCrawlAccountRequest req) {
        try {
            return ResponseEntity.ok(service.update(id, req));
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    /** 삭제 */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }
}
