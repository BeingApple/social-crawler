package com.crawler.api.controller;

import com.crawler.api.dto.SocialPlatformResponse;
import com.crawler.service.SocialPlatformService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/platforms")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class SocialPlatformController {

    private final SocialPlatformService platformService;

    @GetMapping
    public ResponseEntity<List<SocialPlatformResponse>> list() {
        return ResponseEntity.ok(platformService.findAllPlatforms());
    }
}
