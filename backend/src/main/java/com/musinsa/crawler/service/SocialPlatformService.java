package com.musinsa.crawler.service;

import com.musinsa.crawler.api.dto.SocialPlatformResponse;
import com.musinsa.crawler.domain.repository.SocialPlatformRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SocialPlatformService {

    private final SocialPlatformRepository platformRepository;

    public List<SocialPlatformResponse> findAllPlatforms() {
        return platformRepository.findAll()
                .stream()
                .map(SocialPlatformResponse::from)
                .toList();
    }
}
