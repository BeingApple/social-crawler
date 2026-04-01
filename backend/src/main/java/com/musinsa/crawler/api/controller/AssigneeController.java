package com.musinsa.crawler.api.controller;

import com.musinsa.crawler.api.dto.AssigneeResponse;
import com.musinsa.crawler.service.AssigneeService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/assignees")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")   // 개발용. 운영 시 도메인 명시
public class AssigneeController {

    private final AssigneeService assigneeService;

    /** 담당자(계정) 전체 목록 — 프론트에서 클라이언트 사이드 필터링 */
    @GetMapping
    public ResponseEntity<List<AssigneeResponse>> list() {
        return ResponseEntity.ok(assigneeService.findAllAssignees());
    }
}